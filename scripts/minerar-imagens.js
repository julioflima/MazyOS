#!/usr/bin/env node
/**
 * Minerador de imagens para capas de carrossel (estética Lord Journal).
 *
 *   node scripts/minerar-imagens.js "termo de busca" [--dry] [--out=pasta] [--n=12]
 *
 * --dry   só lista o que achou, não baixa nada
 * --out   pasta de destino. O padrão é um acervo avulso, mas ao minerar pra um
 *          carrossel use sempre a pasta do vídeo:
 *          --out=marketing/conteudo/videos/<tema>/<id>/candidatas
 * --n     quantas candidatas por fonte (padrão 8)
 *
 * Fontes sem chave: Wikimedia Commons, The Met (CC0), Openverse.
 * Dica: buscar em INGLÊS devolve muito mais acervo histórico que em português.
 * Fontes com chave (opcional, lidas de .env): UNSPLASH_ACCESS_KEY, PEXELS_API_KEY.
 * Sem a chave, a fonte é pulada com aviso — o script segue funcionando.
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const args = process.argv.slice(2);
const termo = args.find(a => !a.startsWith('--'));
const flag = n => args.find(a => a.startsWith(`--${n}=`))?.split('=').slice(1).join('=');
const DRY = args.includes('--dry');
const N = parseInt(flag('n') || '8', 10);

if (!termo) {
  console.error('uso: node scripts/minerar-imagens.js "termo de busca" [--dry] [--out=pasta] [--n=12]');
  process.exit(1);
}

const slug = termo.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')
  .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 50);
const OUT = path.resolve(ROOT, flag('out') || path.join('marketing/conteudo/_acervo', slug));

// .env opcional
const env = {};
try {
  for (const l of fs.readFileSync(path.join(ROOT, '.env'), 'utf8').split('\n')) {
    const m = l.match(/^\s*([A-Z_]+)\s*=\s*(.*)\s*$/);
    if (m) env[m[1]] = m[2].replace(/^["']|["']$/g, '');
  }
} catch {}

const espera = ms => new Promise(r => setTimeout(r, ms));

// 429/403 aparecem quando se minera muitos temas seguidos (limite por hora do
// Wikimedia e do Unsplash). Espera e tenta de novo antes de desistir da fonte.
const get = async (url, headers = {}, tentativa = 0) => {
  const r = await fetch(url, { headers: { 'User-Agent': 'MazyOS-Multiplic/1.0 (contato via instagram @izabelmultiplic)', ...headers } });
  if ((r.status === 429 || r.status === 403) && tentativa < 2) {
    await espera(2500 * (tentativa + 1));
    return get(url, headers, tentativa + 1);
  }
  if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
  return r.json();
};

// ---------------------------------------------------------------- fontes

async function wikimedia(q) {
  const u = 'https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search'
    + `&gsrsearch=${encodeURIComponent(q + ' filetype:bitmap')}&gsrnamespace=6&gsrlimit=${N * 3}`
    + '&prop=imageinfo&iiprop=url|extmetadata|size&iiurlwidth=2000';
  const j = await get(u);
  return Object.values(j.query?.pages || {}).map(p => {
    const i = p.imageinfo?.[0]; if (!i) return null;
    const meta = i.extmetadata || {};
    const limpa = s => s ? String(s).replace(/<[^>]*>/g, '').trim() : '';
    return {
      fonte: 'Wikimedia Commons',
      titulo: p.title.replace(/^File:/, ''),
      url: i.thumburl || i.url,
      pagina: i.descriptionurl,
      licenca: limpa(meta.LicenseShortName?.value) || 'ver página',
      autor: limpa(meta.Artist?.value) || 'desconhecido',
      ano: limpa(meta.DateTimeOriginal?.value).slice(0, 10),
      largura: i.width, altura: i.height,
    };
  }).filter(Boolean)
    .filter(x => /\.(jpe?g|png)$/i.test(x.titulo) && (x.largura || 0) >= 1000)
    .slice(0, N);
}

async function met(q) {
  const s = await get(`https://collectionapi.metmuseum.org/public/collection/v1/search`
    + `?q=${encodeURIComponent(q)}&hasImages=true`);
  const ids = (s.objectIDs || []).slice(0, N * 2);
  const out = [];
  for (const id of ids) {
    if (out.length >= N) break;
    try {
      const o = await get(`https://collectionapi.metmuseum.org/public/collection/v1/objects/${id}`);
      if (!o.isPublicDomain || !o.primaryImage) continue;
      out.push({
        fonte: 'The Met',
        titulo: o.title,
        url: o.primaryImage,
        pagina: o.objectURL,
        licenca: 'CC0 / domínio público',
        autor: o.artistDisplayName || o.culture || 'desconhecido',
        ano: o.objectDate || '',
      });
    } catch {}
  }
  return out;
}

async function openverse(q) {
  // license_type=commercial,modification → só o que pode ser usado em peça
  // comercial e recortado/tratado. Sem isso volta muito NC/ND, que a Multiplic
  // não pode usar.
  const u = `https://api.openverse.org/v1/images/?q=${encodeURIComponent(q)}`
    + `&page_size=${N}&license_type=commercial,modification&size=large`;
  const j = await get(u);
  return (j.results || []).map(r => ({
    fonte: `Openverse · ${r.source}`,
    titulo: r.title,
    url: r.url,
    pagina: r.foreign_landing_url,
    licenca: `${r.license} ${r.license_version || ''}`.trim().toUpperCase(),
    autor: r.creator || 'desconhecido',
    largura: r.width, altura: r.height,
  })).filter(x => x.url);
}

async function unsplash(q) {
  if (!env.UNSPLASH_ACCESS_KEY) return { pulou: 'UNSPLASH_ACCESS_KEY não está no .env' };
  const u = `https://api.unsplash.com/search/photos?query=${encodeURIComponent(q)}&per_page=${N}&orientation=portrait`;
  const j = await get(u, { Authorization: `Client-ID ${env.UNSPLASH_ACCESS_KEY}` });
  return (j.results || []).map(r => ({
    fonte: 'Unsplash',
    titulo: r.description || r.alt_description || r.id,
    url: r.urls.full,
    pagina: r.links.html,
    licenca: 'Unsplash License (uso comercial liberado, crédito recomendado)',
    autor: r.user?.name || 'desconhecido',
    largura: r.width, altura: r.height,
  }));
}

async function pexels(q) {
  if (!env.PEXELS_API_KEY) return { pulou: 'PEXELS_API_KEY não está no .env' };
  const u = `https://api.pexels.com/v1/search?query=${encodeURIComponent(q)}&per_page=${N}&orientation=portrait`;
  const j = await get(u, { Authorization: env.PEXELS_API_KEY });
  return (j.photos || []).map(r => ({
    fonte: 'Pexels',
    titulo: r.alt || String(r.id),
    url: r.src.original,
    pagina: r.url,
    licenca: 'Pexels License (uso comercial liberado, crédito recomendado)',
    autor: r.photographer || 'desconhecido',
    largura: r.width, altura: r.height,
  }));
}

// ---------------------------------------------------------------- main

(async () => {
  let fontes = [['wikimedia', wikimedia], ['met', met], ['openverse', openverse],
                ['unsplash', unsplash], ['pexels', pexels]];
  // --sem-met: o acervo do Met é arte (quadro, escultura). Bom pra luxo e
  // arquitetura, ruído pra cena cotidiana. Produção em lote roda sem ele.
  if (args.includes('--sem-met')) fontes = fontes.filter(([n]) => n !== 'met');
  // --arquivo: só acervo documental/histórico. O Pexels é banco comercial —
  // modelo posado, sorriso de catálogo — e destrói o tom editorial (Julio,
  // 18/09/26: "são só peças de marketing em stock").
  if (args.includes('--arquivo')) fontes = fontes.filter(([n]) => n !== 'pexels' && n !== 'met');
  let todas = [];

  for (const [nome, fn] of fontes) {
    await espera(400);   // respiro entre fontes
    try {
      const r = await fn(termo);
      if (r && r.pulou) { console.log(`  ~ ${nome.padEnd(10)} pulada — ${r.pulou}`); continue; }
      console.log(`  ✓ ${nome.padEnd(10)} ${r.length} candidatas`);
      todas = todas.concat(r);
    } catch (e) {
      console.log(`  ✗ ${nome.padEnd(10)} falhou — ${e.message}`);
    }
  }

  console.log(`\n${todas.length} imagens encontradas para "${termo}"\n`);
  todas.forEach((x, i) => {
    const dim = x.largura ? `${x.largura}x${x.altura}` : '?';
    console.log(`${String(i + 1).padStart(2)}. [${x.fonte}] ${(x.titulo || '').slice(0, 60)}`);
    console.log(`    ${dim} · ${x.licenca} · ${x.autor}`);
  });

  if (DRY) { console.log('\n--dry: nada foi baixado.'); return; }

  fs.mkdirSync(OUT, { recursive: true });
  const creditos = [];
  for (let i = 0; i < todas.length; i++) {
    const x = todas[i];
    const nome = `${String(i + 1).padStart(2, '0')}-${x.fonte.split(' ')[0].toLowerCase()}.jpg`;
    try {
      const r = await fetch(x.url, { headers: { 'User-Agent': 'MazyOS-Multiplic/1.0' } });
      if (!r.ok) throw new Error(r.status);
      const buf = Buffer.from(await r.arrayBuffer());
      fs.writeFileSync(path.join(OUT, nome), buf);
      creditos.push({ arquivo: nome, ...x, bytes: buf.length });
      console.log(`  baixou ${nome} (${(buf.length / 1024).toFixed(0)} KB)`);
    } catch (e) { console.log(`  falhou ${nome} — ${e.message}`); }
  }
  fs.writeFileSync(path.join(OUT, 'creditos.json'), JSON.stringify(creditos, null, 2));

  // régua de contato pra escolher a capa
  const cards = creditos.map(c => `<figure><img src="${c.arquivo}"/><figcaption>
    <b>${c.arquivo}</b><br/>${c.fonte}<br/>${c.licenca}<br/>${c.autor}</figcaption></figure>`).join('');
  fs.writeFileSync(path.join(OUT, 'index.html'), `<!doctype html><meta charset="utf-8">
<style>body{background:#111;color:#eee;font:14px/1.4 system-ui;padding:24px}
h1{font-size:18px;margin:0 0 20px}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}
figure{margin:0}img{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:8px;background:#222}
figcaption{font-size:12px;color:#aaa;margin-top:8px}</style>
<h1>${termo} — ${creditos.length} candidatas</h1><main>${cards}</main>`);

  console.log(`\npronto: ${OUT}`);
  console.log(`abra ${path.join(OUT, 'index.html')} pra escolher a capa`);
})();
