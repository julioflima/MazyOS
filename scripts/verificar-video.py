#!/usr/bin/env python3
"""Verifica um vídeo pronto antes de ele sair pra publicação.

Duas coisas, porque foram as duas que já quebraram calado:

  1. ÁUDIO (automático, falha alto) — a trilha parou aos 6s uma vez e o
     vídeo saiu assim. Aqui o script mede o arquivo final de verdade:
     duração, silêncio em qualquer ponto, e energia nos intervalos SEM
     fala (que é onde a música tem que estar sozinha e audível).

  2. IMAGEM x TEXTO (folha de contato, julgamento humano) — monta uma
     folha com cada cena ao lado da frase que é falada nela. Isso não dá
     pra automatizar: é olhar e dizer se a imagem tem a ver com o que
     está sendo dito. Já foi reprovado duas vezes por não ter esse passo.

uso: verificar-video.py <pasta-do-video> [--sufixo -inf] [--video caminho.mp4]
"""
import json, os, re, subprocess, sys

args = sys.argv[1:]
def flag(nome, padrao=None):
    # aceita as duas formas: --sufixo -inf  e  --sufixo=-inf
    for a in args:
        if a.startswith(f'--{nome}='):
            return a.split('=', 1)[1]
    return args[args.index('--'+nome)+1] if '--'+nome in args else padrao

PASTA  = os.path.abspath(args[0])
SUFIXO = flag('sufixo', '')
POD    = os.path.join(PASTA, 'podcast'+SUFIXO)
plano  = json.load(open(os.path.join(POD, 'plano.json')))

def ffprobe(campo, arq):
    r = subprocess.run(['ffprobe','-v','quiet','-show_entries',campo,
                        '-of','csv=p=0',arq], capture_output=True, text=True)
    return r.stdout.strip()

# ---- localizar o mp4 final -------------------------------------------------
# O vídeo é achado pelo título deste carrossel, nunca pelo "mais recente"
# da pasta — senão o verificador aprova o áudio de outro vídeo.
vid = flag('video')
if not vid:
    import unicodedata
    MEDIA = '/Users/juliolima/Documents/media/multiplic/consorcios'
    CTA = flag('cta', 'influencer').replace('cta-', '')
    t = ' '.join(json.load(open(os.path.join(PASTA,'conteudo.json')))['titulo'])
    t = unicodedata.normalize('NFD', t).encode('ascii','ignore').decode()
    sl = re.sub(r'-+','-', re.sub(r'[^a-z0-9]+','-', t.lower())).strip('-')
    vid = os.path.join(MEDIA, f'vd-{sl}-{CTA}-podcast{SUFIXO}.mp4')
if not os.path.exists(vid):
    sys.exit(f'ERRO: vídeo final não existe:\n  {vid}\npasse --video se o nome for outro')

falhas, avisos = [], []
dur = float(ffprobe('format=duration', vid))
print(f'vídeo: {vid}\nduração: {dur:.1f}s\n')

# ---- 1. tem faixa de áudio? -----------------------------------------------
if not ffprobe('stream=codec_type', vid).count('audio'):
    falhas.append('o mp4 não tem faixa de áudio nenhuma')

# ---- 2. a duração bate com o plano? ---------------------------------------
T = float(flag('sobrepor', '1.0'))          # padrão do PADRAO-VIDEO.md
esperado = sum(c['dur'] for c in plano) - T * (len(plano) - 1)
if abs(dur - esperado) > 2.0:
    falhas.append(f'duração {dur:.1f}s foge do plano ({esperado:.1f}s) — '
                  'áudio truncado ou vídeo cortado')

# ---- 3. silêncio em qualquer ponto -----------------------------------------
# A trilha é contínua do primeiro ao último segundo. Silêncio de meio
# segundo já significa que a música morreu no meio.
r = subprocess.run(['ffmpeg','-i',vid,'-af','silencedetect=n=-50dB:d=0.5',
                    '-f','null','-'], capture_output=True, text=True)
mudos = [(float(a), float(b)) for a, b in
         re.findall(r'silence_start: ([\d.]+).*?silence_end: ([\d.]+)',
                    r.stderr, re.S)]
mudos = [(a, b) for a, b in mudos if b - a >= 0.5 and a < dur - 1.0]
if mudos:
    for a, b in mudos:
        falhas.append(f'SILÊNCIO de {a:.1f}s a {b:.1f}s — a trilha morreu ali')

# ---- 4. a trilha corre do início ao fim? (cancelamento da fala) ----------
# Remonto a narração sozinha a partir do próprio plano, inverto a fase e
# somo ao mix. A fala se cancela e sobra a trilha. Onde ela está, o resíduo
# fica em torno de -23 dB; onde ela morreu, despenca pra -91 dB. Medido em
# 19/09/26 num vídeo bom e num quebrado de propósito: 69 dB de margem.
# Antes disso tentei medir grave e medir silêncio — os dois davam falso
# aprovado, que foi como a trilha muda aos 6s chegou a sair.
T = float(flag('sobrepor', '1.0'))
mix = os.path.join(POD, '_mix.wav')
verificou_trilha = False
if not os.path.exists(mix):
    falhas.append(f'_mix.wav não existe ({mix}) — sem ele não dá pra provar '
                  'que a trilha está lá; rode a montagem de novo')
else:
    import tempfile
    tmp = tempfile.mkdtemp()
    ref = os.path.join(tmp, 'fala.wav')
    ins, filt, acc = [], [], 0.0
    for k, c in enumerate(plano):
        ins += ['-i', c['audio']]
        filt.append(f"[{k}:a]adelay={int(acc*1000)}|{int(acc*1000)}[a{k}]")
        acc += c['dur'] - (T if k < len(plano) - 1 else 0)
    filt.append(''.join(f'[a{k}]' for k in range(len(plano))) +
                f'amix=inputs={len(plano)}:normalize=0:duration=longest[out]')
    subprocess.run(['ffmpeg','-y',*ins,'-filter_complex',';'.join(filt),
                    '-map','[out]','-c:a','pcm_s16le',ref], capture_output=True)
    resid = os.path.join(tmp, 'resid.wav')
    subprocess.run(['ffmpeg','-y','-i',mix,'-i',ref,'-filter_complex',
                    '[1:a]volume=-1[inv];[0:a][inv]amix=inputs=2:normalize=0[r]',
                    '-map','[r]','-c:a','pcm_s16le',resid], capture_output=True)
    if os.path.exists(resid):
        verificou_trilha = True
        JAN, t, mortas, niveis = 5.0, 0.0, [], []
        while t < dur - 1.0:
            out = subprocess.run(['ffmpeg','-ss',f'{t:.2f}','-t',f'{min(JAN,dur-t):.2f}',
                                  '-i',resid,'-af','volumedetect','-f','null','-'],
                                 capture_output=True, text=True).stderr
            m = re.search(r'mean_volume: (-?[\d.]+) dB', out)
            v = float(m.group(1)) if m else -99.0
            niveis.append(v)
            if v < -50.0:
                mortas.append((t, v))
            t += JAN
        for t, v in mortas:
            falhas.append(f'SEM TRILHA a partir de ~{t:.0f}s (resíduo {v:.0f} dB, '
                          'o normal é -23)')
        if not mortas:
            print(f'trilha contínua do 0s ao {dur:.0f}s — {len(niveis)} janelas, '
                  f'resíduo entre {max(niveis):.0f} e {min(niveis):.0f} dB ✓')
    else:
        falhas.append('não consegui isolar a trilha para conferir')

# ---- 5. folha de conferência: a imagem tem a ver com o que é dito? -------
# Isto não se automatiza. Monta uma folha com cada cena ao lado da frase
# falada nela, pra alguém olhar e dizer se a imagem faz sentido com o texto.
# Duas levas de capas já foram reprovadas por faltar exatamente este passo.
folha = os.path.join(POD, '_conferencia.png')
linhas = []
for c in plano:
    txt = ' '.join(w['t'] for w in c.get('palavras', []))
    if not c.get('img') or not os.path.exists(c['img']):
        avisos.append(f"cena {c['n']}: imagem ausente ({c.get('img')})")
    linhas.append((c['n'], c.get('img') or '', txt))

def esc(t):
    return (t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'))

cards = ''.join(f'''<div class="l">
  <div class="n">{n}</div>
  <img src="file://{img}">
  <div class="t">{esc(txt) or "<i>sem fala</i>"}</div>
</div>''' for n, img, txt in linhas)

html = f'''<!doctype html><meta charset="utf-8"><style>
 body{{margin:0;background:#12161a;font:16px/1.5 -apple-system,Inter,sans-serif;
   color:#e8eaed;width:1240px}}
 h1{{font-size:19px;margin:26px 30px 6px;font-weight:600}}
 .sub{{margin:0 30px 20px;color:#8b949e;font-size:14px}}
 .l{{display:flex;gap:20px;align-items:center;padding:14px 30px;
   border-top:1px solid #222a31}}
 .n{{width:26px;font-size:22px;color:#7d8590;font-weight:700;flex:none}}
 img{{width:330px;height:250px;object-fit:cover;border-radius:6px;flex:none;
   background:#000}}
 .t{{font-size:17px;line-height:1.55}}
</style>
<h1>Conferência de imagem x texto</h1>
<div class="sub">{os.path.basename(vid)} — cada imagem precisa ter a ver com a
frase ao lado. Se não tiver, trocar o termo de busca daquela cena.</div>
{cards}'''

htm = os.path.join(POD, '_conferencia.html')
open(htm, 'w').write(html)
js = os.path.join(POD, '_conf.js')
open(js, 'w').write('''const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1240, height: 900 } });
  await p.goto('file://' + process.argv[2]);
  await p.waitForTimeout(500);
  await p.screenshot({ path: process.argv[3], fullPage: true });
  await b.close();
})();''')
# O playwright mora numa pasta própria de render, não na raiz do projeto.
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
amb = dict(os.environ,
           NODE_PATH=os.path.join(RAIZ, 'marketing/conteudo/.render/node_modules'))
r = subprocess.run(['node', js, htm, folha], capture_output=True, text=True, env=amb)
if r.returncode != 0 or not os.path.exists(folha):
    falhas.append('folha de conferência não renderizou, então ninguém pode '
                  'conferir as imagens: ' + r.stderr.strip()[:180])
else:
    for f in (js, htm):
        os.path.exists(f) and os.remove(f)

# ---- veredicto -------------------------------------------------------------
print()
for a in avisos: print('aviso:', a)
if falhas:
    print('\nREPROVADO:')
    for f in falhas: print('  -', f)
    sys.exit(1)
if not verificou_trilha:
    print('REPROVADO: não consegui medir a trilha — não trate como aprovado')
    sys.exit(1)
print('áudio APROVADO — fala e trilha íntegras do começo ao fim')
print(f'\nFALTA O OLHO — nenhum vídeo sai sem isto:\n  {folha}')
print('  confira se cada imagem tem a ver com a frase dita naquela cena.')
