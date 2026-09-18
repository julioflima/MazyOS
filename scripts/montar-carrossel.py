#!/usr/bin/env python3
"""
Monta as duas versões de um carrossel (CTA SONHO e CTA INFLUENCER) a partir de
um conteudo.json na pasta do vídeo.

  python3 scripts/montar-carrossel.py marketing/conteudo/videos/consorcio/<id>

conteudo.json:
  { "titulo": ["linha 1","linha 2"], "subtitulo": "...", "logo": "topo"|"rodape",
    "slides": [ ["parágrafo 1 do slide", "parágrafo 2 do slide"], ... ] }

Cada slide é uma LISTA de parágrafos. Bloco único longo não é permitido —
quebrar sempre em dois ou mais.

A capa usa capa.jpg da mesma pasta (ou o placeholder, se não existir).
"""
import json, os, sys, html

PASTA = sys.argv[1].rstrip('/')
RAIZ  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
c = json.load(open(os.path.join(PASTA, 'conteudo.json')))

# ../../../../.. → da pasta do CTA até a raiz do projeto
REL = os.path.relpath(RAIZ, os.path.join(PASTA, 'cta-x'))
AVATAR = f'{REL}/identidade/equipe/izabel-avatar.png'
LOGO   = f'{REL}/identidade/logo-branco.png'
TEM_CAPA = os.path.exists(os.path.join(PASTA, 'capa.jpg'))

BADGE = ('<span class="badge"><svg aria-label="Verified" fill="rgb(0, 149, 246)" viewBox="0 0 40 40" '
 'role="img"><path d="M19.998 3.094 14.638 0l-2.972 5.15H5.432v6.354L0 14.64 3.094 20 0 25.359l5.432 '
 '3.137v5.905h5.975L14.638 40l5.36-3.094L25.358 40l3.232-5.6h6.162v-6.01L40 25.359 36.905 20 40 '
 '14.641l-5.248-3.03v-6.46h-6.419L25.358 0l-5.36 3.094Zm7.415 11.225 2.254 2.287-11.43 11.5-6.835-6.93 '
 '2.244-2.258 4.587 4.581 9.18-9.18Z" fill-rule="evenodd"></path></svg></span>')

def head():
    return f'''  <div class="head">
    <img class="avatar" src="{AVATAR}" />
    <div class="who">
      <div class="name">Izabel · Multiplic {BADGE}</div>
      <div class="handle">@izabelmultiplic</div>
    </div>
  </div>'''

def foot(n):
    return f'  <div class="foot"><img src="{LOGO}" /><div class="counter">{n:02d}</div></div>'

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ctas import CTAS

CSS = '''  :root{--azul-accent:#6FB4E8;--dourado:#BB842E;--off:#FAFAF7;
    --muted:rgba(250,250,247,.55);--border:rgba(255,255,255,.12)}
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:#111;font-family:'Inter',sans-serif;display:flex;flex-direction:column;
    align-items:center;gap:40px;padding:40px}
  .slide{width:1080px;height:1350px;background:#000;color:var(--off);position:relative;
    overflow:hidden;display:flex;flex-direction:column;padding:72px}
  .head{display:flex;align-items:center;gap:20px;padding-bottom:40px}
  .avatar{width:84px;height:84px;border-radius:50%;object-fit:cover;flex:none;background:#222}
  .who{display:flex;flex-direction:column;gap:4px}
  .name{display:flex;align-items:center;gap:10px;font-size:30px;font-weight:700;letter-spacing:-.01em}
  .badge{display:flex;align-items:center;flex:none}
  .badge svg{width:32px;height:32px}
  .handle{font-size:26px;font-weight:400;color:var(--muted)}
  .body{flex:1;display:flex;flex-direction:column;justify-content:center;gap:34px}
  p{font-size:39px;line-height:1.5;font-weight:400;letter-spacing:-.011em}
  b{font-weight:700;color:var(--azul-accent)}
  .solo{font-size:52px;font-weight:700;line-height:1.25;letter-spacing:-.02em}
  .palavra{align-self:flex-start;color:var(--dourado);font-size:92px;font-weight:900;
    letter-spacing:-.03em;line-height:1;padding-bottom:18px;border-bottom:5px solid var(--dourado)}
  .foot{display:flex;align-items:center;justify-content:space-between;padding-top:40px;
    border-top:1px solid var(--border)}
  .foot img{height:52px}
  .counter{font-size:24px;font-weight:500;letter-spacing:.18em;color:var(--muted)}
  .capa{padding:0;justify-content:flex-end}
  /* Tratamento da foto — escolhido POR CARROSSEL no conteudo.json, campo
     "tratamento". Filtro igual nas 57 vira template e se entrega como
     programado (Julio, 18/09/26); o feed do Lord varia de peça pra peça. */
  .capa .foto{position:absolute;inset:0;background-size:cover;background-position:center top}
  .t-leve  .foto{filter:sepia(.20) saturate(.88) contrast(1.04) brightness(.98)}
  .t-forte .foto{filter:sepia(.42) saturate(.72) contrast(1.10) brightness(.95) hue-rotate(-8deg)}
  .t-pb    .foto{filter:grayscale(1) contrast(1.12) brightness(.96)}
  .t-nenhum .grao,.t-nenhum .vinheta{opacity:0}
  .t-leve  .grao{opacity:.35} .t-leve  .vinheta{opacity:.5}
  .t-forte .grao{opacity:.55} .t-forte .vinheta{opacity:.75}
  .t-pb    .grao{opacity:.55} .t-pb    .vinheta{opacity:.7}
  .capa .grao{position:absolute;inset:0;opacity:0;mix-blend-mode:overlay;z-index:1;
    background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3'/></filter><rect width='100%25' height='100%25' filter='url(%23n)' opacity='0.55'/></svg>")}
  .capa .vinheta{position:absolute;inset:0;z-index:1;opacity:0;
    background:radial-gradient(ellipse at center,transparent 45%,rgba(0,0,0,.55) 100%)}
  .capa .capa-inner{position:relative;padding:72px;display:flex;flex-direction:column;gap:34px}
  /* Tipografia editorial: serifada em caixa baixa, como o Lord. Caixa alta e
     peso 900 liam como propaganda. */
  .capa h1{font-family:'Lora',serif;font-size:66px;font-weight:400;line-height:1.26;letter-spacing:-.005em}
  .capa h1 i{font-style:italic}
  .capa .sub{font-size:28px;font-weight:400;color:rgba(255,255,255,.72);letter-spacing:-.005em;line-height:1.4}
  .capa .foot{border-top:none;padding-top:8px}
  .logo-top{position:absolute;top:64px;left:72px;height:52px;z-index:2}
  .capa.logo-topo .foot img{visibility:hidden}
  .capa:not(.logo-topo) .logo-top{display:none}'''

RENDER = '''const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('file://' + path.join(__dirname, 'carrossel.html'));
  await p.waitForTimeout(600);
  const s = await p.$$('.slide');
  for (let i = 0; i < s.length; i++) {
    const n = String(i + 1).padStart(2, '0');
    await s[i].screenshot({ path: path.join(__dirname, `slide-${n}.png`) });
    console.log(`slide-${n}.png`);
  }
  await b.close();
})();
'''

for nome, cta in CTAS.items():
    dest = os.path.join(PASTA, nome)
    os.makedirs(dest, exist_ok=True)
    capa_bg = (f"linear-gradient(to bottom,transparent 42%,rgba(0,0,0,.55) 70%,rgba(0,0,0,.93) 100%),"
               f"url('../capa.jpg')" if TEM_CAPA else
               "linear-gradient(to bottom,rgba(0,0,0,.25),rgba(0,0,0,.9)),"
               "repeating-linear-gradient(135deg,#242a30 0 26px,#1d2227 26px 52px)")
    topo = c.get('logo','topo') == 'topo'
    trat = c.get('tratamento', 'leve')   # nenhum | leve | forte | pb
    slides = [f'''<div class="slide capa t-{trat}{' logo-topo' if topo else ''}">
  <div class="foto" style="background-image:{capa_bg}"></div>
  <div class="grao"></div>
  <div class="vinheta"></div>
  <img class="logo-top" src="{LOGO}" />
  <div class="capa-inner">
    <h1>{c.get('titulo_html') or html.escape(' '.join(c['titulo']))}</h1>
    <div class="sub">{html.escape(c['subtitulo']).replace(' →','&nbsp;→')}</div>
{foot(1)}
  </div>
</div>''']
    n = 1
    for txt in c['slides']:
        n += 1
        # cada slide é uma lista de parágrafos (ou uma string com \n\n).
        # Regra do Julio (18/09/26): parágrafo longo cansa — sempre quebrar em
        # dois ou mais blocos, nunca um bloco único de 5+ linhas.
        paras = txt if isinstance(txt, list) else txt.split('\n\n')
        corpo = '\n    '.join(f'<p>{t}</p>' for t in paras)
        slides.append(f'<div class="slide">\n{head()}\n  <div class="body">\n'
                      f'    {corpo}\n  </div>\n{foot(n)}\n</div>')
    for bloco in ('convite','fecho'):
        n += 1
        corpo = '\n    '.join(cta[bloco])
        gap = ' style="gap:28px"' if bloco == 'convite' else ' style="gap:32px"'
        slides.append(f'<div class="slide">\n{head()}\n  <div class="body"{gap}>\n'
                      f'    {corpo}\n  </div>\n{foot(n)}\n</div>')

    doc = f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800;900&family=Lora:ital,wght@0,400;0,500;1,400;1,500&display=swap" rel="stylesheet"/>
<style>
{CSS}
</style></head>
<body>

{chr(10).join(chr(10) + s for s in slides)}

</body></html>'''
    open(os.path.join(dest,'carrossel.html'),'w').write(doc)
    open(os.path.join(dest,'render.js'),'w').write(RENDER)
    print(f'{nome}: {len(slides)} slides')
