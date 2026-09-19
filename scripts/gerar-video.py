#!/usr/bin/env python3
"""
Transforma um carrossel em vídeo vertical 9:16 com narração do ElevenLabs.

  python3 scripts/gerar-video.py marketing/conteudo/videos/consorcio/<id> [--cta=cta-sonho]

Um áudio por cena: a duração da cena É a duração do áudio dela, então a
sincronia entre fala e slide não depende de alinhamento manual.
"""
import json, os, subprocess, sys, urllib.request, urllib.error

PASTA = os.path.abspath(sys.argv[1].rstrip('/'))
flag = lambda n, d: next((a.split('=',1)[1] for a in sys.argv if a.startswith(f'--{n}=')), d)
CTA  = flag('cta', 'cta-sonho')
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

cfg = json.load(open(os.path.join(RAIZ, 'identidade/referencias/carrossel-estilo-brunobarbosz/video-config.json')))
CHAVE = [l.split('=',1)[1].strip() for l in open(os.path.join(RAIZ, '.env')) if l.startswith('ELEVEN')][0]

conteudo = json.load(open(os.path.join(PASTA, 'conteudo.json')))
sys.path.insert(0, os.path.join(RAIZ, 'scripts'))
from ctas import CTAS
import re as _re

def limpo(t):
    return _re.sub(r'\s+', ' ', _re.sub(r'<[^>]+>', '', t)).strip()

def roteiro_literal():
    """A narração lê exatamente o que está no slide (Julio, 18/09/26).
    Antes eu usava uma versão falada reduzida, e o texto na tela não batia
    com o que se ouvia."""
    cenas = [{'slide': 'slide-01.png',
              'fala': f"{' '.join(conteudo['titulo'])}. "
                      f"{conteudo['subtitulo'].replace('→','').strip().rstrip('.')}."}]
    n = 1
    for bloco in conteudo['slides']:
        n += 1
        cenas.append({'slide': f'slide-{n:02d}.png', 'fala': ' '.join(limpo(x) for x in bloco)})
    for parte in ('convite', 'fecho'):
        n += 1
        linhas = [limpo(x) for x in CTAS[CTA][parte]]
        cenas.append({'slide': f'slide-{n:02d}.png', 'fala': ' '.join(x for x in linhas if x)})
    return {'cenas': cenas}

rot = os.path.join(PASTA, 'roteiro.json')
roteiro = json.load(open(rot)) if (os.path.exists(rot) and '--roteiro' in sys.argv) else roteiro_literal()

# silêncio antes e depois da fala em cada cena, para ela não disputar com a
# transição (regra de Julio, 18/09/26)
RESPIRO = 0.9

def texto(cena):
    """'@capa' lê o título e o subtítulo da capa, que antes não eram narrados."""
    if cena['fala'].strip() == '@capa':
        sub = conteudo['subtitulo'].replace('→', '').strip().rstrip('.')
        return f"{' '.join(conteudo['titulo'])}. {sub}."
    return cena['fala']
saida = os.path.join(PASTA, 'video')
os.makedirs(saida, exist_ok=True)

def narrar(texto, destino):
    if os.path.exists(destino) and os.path.getsize(destino) > 1000:
        return
    corpo = json.dumps({'text': texto, 'model_id': cfg['modelo'],
                        'voice_settings': {'stability': 0.5, 'similarity_boost': 0.75}}).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{cfg['voz_id']}",
        data=corpo, headers={'xi-api-key': CHAVE, 'Content-Type': 'application/json'}, method='POST')
    open(destino, 'wb').write(urllib.request.urlopen(req, timeout=90).read())

def duracao(f):
    return float(subprocess.run(['ffprobe','-v','quiet','-show_entries','format=duration',
                                 '-of','csv=p=0', f], capture_output=True, text=True).stdout.strip())

CAPA_REMOTION = os.path.join(RAIZ, 'video-capa')

def cena_capa(mp3, d, mp4):
    """A capa é a única parte animada em Remotion: a foto sangra nos 9:16 e
    faz zoom lento enquanto o título sobe linha a linha. Nos slides de texto
    o zoom foi reprovado, aqui ele é o ponto."""
    pub = os.path.join(CAPA_REMOTION, 'public')
    os.makedirs(pub, exist_ok=True)
    # áudio já com o respiro, pra a fala não atropelar a entrada do título
    padded = os.path.join(pub, 'fala-capa.mp3')
    subprocess.run(['ffmpeg','-y','-i',mp3,'-af',
        f'adelay={int(RESPIRO*1000)}|{int(RESPIRO*1000)},apad=whole_dur={d}',
        '-t',str(d), padded], check=True, capture_output=True)
    shutil.copy2(os.path.join(PASTA,'capa.jpg'), os.path.join(pub,'capa.jpg'))
    shutil.copy2(os.path.join(RAIZ,'identidade/logo-branco.png'), os.path.join(pub,'logo-branco.png'))
    props = {'titulo': conteudo['titulo'],
             'subtitulo': conteudo['subtitulo'].replace('→','').strip(),
             'capa':'capa.jpg','logo':'logo-branco.png',
             'audio':'fala-capa.mp3','duracao': round(d,2)}
    pj = os.path.join(pub, '_props.json'); json.dump(props, open(pj,'w'), ensure_ascii=False)
    subprocess.run(['npx','remotion','render','src/index.ts','Capa', mp4, f'--props={pj}'],
                   cwd=CAPA_REMOTION, check=True, capture_output=True)

import shutil
partes, total = [], 0.0
for i, cena in enumerate(roteiro['cenas'], 1):
    mp3 = os.path.join(saida, f'fala-{i:02d}.mp3')
    narrar(texto(cena), mp3)
    # Regra: a fala não atropela a transição. Cada cena ganha silêncio no
    # início (o slide termina de entrar) e no fim (a fala acaba antes de sair).
    d = RESPIRO + duracao(mp3) + RESPIRO
    img = os.path.join(PASTA, CTA, cena['slide'])
    mp4 = os.path.join(saida, f'cena-{i:02d}.mp4')
    if i == 1 and os.path.exists(os.path.join(PASTA, 'capa.jpg')):
        cena_capa(mp3, d, mp4)
        partes.append((mp4, d)); total += d
        print(f'  cena {i:02d}  {d:5.1f}s  [capa animada]  {texto(cena)[:34]}...')
        continue
    # 1080x1350 centrado num quadro 9:16; o fundo preto do slide emenda com a barra
    subprocess.run(['ffmpeg','-y','-loop','1','-i',img,'-i',mp3,
        '-filter_complex',
        '[0:v]scale=1080:-1,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,format=yuv420p[v]',
        '-map','[v]','-map','1:a','-c:v','libx264','-r','30','-t',str(d),
        '-af',f'adelay={int(RESPIRO*1000)}|{int(RESPIRO*1000)},apad',
        '-c:a','aac','-b:a','192k',mp4],
        check=True, capture_output=True)
    partes.append((mp4, d)); total += d
    print(f'  cena {i:02d}  {d:5.1f}s  {texto(cena)[:46]}...')

# Corte seco entre slides fica duro. T de crossfade suaviza a virada, e o
# áudio atravessa junto (acrossfade) pra não haver salto na narração.
T = 0.9        # transição mais lenta; 0,55s ficava apressado
entradas, filtros = [], []
for f, _ in partes: entradas += ['-i', f]
v, a, desloc = '[0:v]', '[0:a]', 0.0
for i in range(1, len(partes)):
    desloc += partes[i-1][1] - T
    filtros.append(f'{v}[{i}:v]xfade=transition=slideleft:duration={T}:offset={desloc:.3f}[v{i}]')
    filtros.append(f'{a}[{i}:a]acrossfade=d={T}[a{i}]')
    v, a = f'[v{i}]', f'[a{i}]'
total -= T * (len(partes) - 1)

# Os vídeos prontos ficam fora do repositório, na media do Julio.
import unicodedata, re as _re
def slug(t):
    t = unicodedata.normalize('NFD', t).encode('ascii','ignore').decode()
    return _re.sub(r'-+','-', _re.sub(r'[^a-z0-9]+','-', t.lower())).strip('-')

titulo = ' '.join(json.load(open(os.path.join(PASTA,'conteudo.json')))['titulo'])
MEDIA = flag('media', '/Users/juliolima/Documents/media/multiplic/consorcios')
os.makedirs(MEDIA, exist_ok=True)
final = os.path.join(MEDIA, f'vd-{slug(titulo)}-{CTA.replace("cta-","")}.mp4')
subprocess.run(['ffmpeg','-y'] + entradas + ['-filter_complex', ';'.join(filtros),
    '-map', v, '-map', a, '-c:v','libx264','-crf','20','-pix_fmt','yuv420p',
    '-c:a','aac','-b:a','192k', final], check=True, capture_output=True)
print(f'\n{final}\n{total:.1f}s no total')
