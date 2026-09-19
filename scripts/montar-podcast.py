#!/usr/bin/env python3
"""Renderiza cada cena do plano no Remotion e emenda tudo com crossfade."""
import json, os, shutil, subprocess, sys

PASTA = os.path.abspath(sys.argv[1].rstrip('/'))
flag = lambda n,d: next((a.split('=',1)[1] for a in sys.argv if a.startswith(f'--{n}=')), d)
CTA  = flag('cta','cta-sonho')
SUFIXO = flag('sufixo','')
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
REM  = os.path.join(RAIZ,'video-capa'); PUB = os.path.join(REM,'public')
plano = json.load(open(os.path.join(PASTA,'podcast'+SUFIXO,'plano.json')))
os.makedirs(PUB, exist_ok=True)
shutil.copy2(os.path.join(RAIZ,'identidade/logo-branco.png'), os.path.join(PUB,'logo-branco.png'))

partes = []
for c in plano:
    img = f"cena-{c['n']:02d}.jpg" if not c.get('carrossel') else f"cena-{c['n']:02d}.png"
    shutil.copy2(c['img'], os.path.join(PUB, img))
    aud = f"aud-{c['n']:02d}.mp3"; shutil.copy2(c['audio'], os.path.join(PUB, aud))
    props = {'img':img,'audio':aud,'palavras':c['palavras'],'logo':'logo-branco.png',
             'carrossel':bool(c.get('carrossel')),'duracao':c['dur']}
    pj = os.path.join(PUB, f"_p{c['n']}.json"); json.dump(props, open(pj,'w'), ensure_ascii=False)
    mp4 = os.path.join(PASTA,'podcast'+SUFIXO,f"cena-{c['n']:02d}.mp4")
    if c.get('capa'):
        cont = json.load(open(os.path.join(PASTA,'conteudo.json')))
        props = {'titulo':cont['titulo'],'subtitulo':cont['subtitulo'].replace('→','').strip(),
                 'capa':img,'logo':'logo-branco.png','audio':aud,'duracao':c['dur']}
        json.dump(props, open(pj,'w'), ensure_ascii=False)
    if '--reusar' in sys.argv and os.path.exists(mp4):
        partes.append((mp4, c['dur'])); print(f"  cena {c['n']:02d} reaproveitada"); continue
    comp = 'Capa' if c.get('capa') else ('Fecho' if c.get('carrossel') else 'Cena')
    if c.get('carrossel'):
        sys.path.insert(0, os.path.join(RAIZ,'scripts'))
        from ctas import CTAS
        import re as _re
        shutil.copy2(os.path.join(RAIZ,'identidade/equipe/izabel-avatar.png'),
                     os.path.join(PUB,'izabel.png'))
        linhas = []
        for bruto in CTAS[CTA]['fecho']:
            txt = _re.sub(r'\s+',' ',_re.sub(r'<[^>]+>','',bruto)).strip()
            if not txt: continue
            tipo = 'palavra' if 'class="palavra"' in bruto else ('solo' if 'class="solo"' in bruto else 'p')
            linhas.append({'tipo':tipo,'texto':txt})
        props = {'avatar':'izabel.png','linhas':linhas,'audio':aud,'duracao':c['dur']}
        json.dump(props, open(pj,'w'), ensure_ascii=False)
    subprocess.run(['npx','remotion','render','src/index.ts',comp,mp4,f'--props={pj}'],
                   cwd=REM, check=True, capture_output=True)
    partes.append((mp4, c['dur'])); print(f"  cena {c['n']:02d} renderizada  {c['dur']:.1f}s")

# Sobreposição de vozes: a fala da cena seguinte começa antes de a anterior
# terminar. Dá sensação de urgência e prende — característica de vídeo viral
# (regra de Julio, 19/09/26). Com acrossfade a voz que sai perde volume e o
# efeito some, então o áudio é posicionado com adelay e somado com amix, as
# duas em volume cheio.
T = float(flag('sobrepor', '0.6'))   # cai no silêncio do fim, não nas últimas palavras

inicios, acc = [], 0.0
for k, (_, d) in enumerate(partes):
    inicios.append(acc)
    acc += d - (T if k < len(partes) - 1 else 0)
total = acc

entradas, filtros = [], []
for f, _ in partes: entradas += ['-i', f]
n_inputs = len(partes)

v = '[0:v]'
for i in range(1, len(partes)):
    filtros.append(f'{v}[{i}:v]xfade=transition=fade:duration={T}:offset={inicios[i]:.3f}[v{i}]')
    v = f'[v{i}]'

# Sem fade de entrada: a voz que chega já entra cheia. Quem morre é que
# desaparece, durante a sobreposição (Julio, 19/09/26).
for i, (_, d) in enumerate(partes):
    # o fade é curto e só no finalzinho, pra não apagar a frase que ainda
    # está sendo dita durante a sobreposição
    fade = '' if i == len(partes)-1 else f'afade=t=out:st={max(d-0.3,0):.3f}:d=0.3,'
    filtros.append(f'[{i}:a]{fade}adelay={int(inicios[i]*1000)}|{int(inicios[i]*1000)}[a{i}d]')
filtros.append(''.join(f'[a{i}d]' for i in range(len(partes))) +
               f'amix=inputs={len(partes)}:normalize=0:duration=longest[amix]')
a = '[amix]'

from ctas import CTAS
import unicodedata, re
def slug(t):
    t=unicodedata.normalize('NFD',t).encode('ascii','ignore').decode()
    return re.sub(r'-+','-',re.sub(r'[^a-z0-9]+','-',t.lower())).strip('-')
titulo = ' '.join(json.load(open(os.path.join(PASTA,'conteudo.json')))['titulo'])
MEDIA = '/Users/juliolima/Documents/media/multiplic/consorcios'
os.makedirs(MEDIA, exist_ok=True)
final = os.path.join(MEDIA, f"vd-{slug(titulo)}-{CTA.replace('cta-','')}-podcast{SUFIXO}.mp4")
# Efeito de digitação na cena final, no momento em que a palavra-chave
# aparece — o CTA pede para comentar, o som reforça o gesto.
quando_sfx = None
# Áudio mora em media/, não no repositório (regra do Julio, 19/09/26).
SFX = '/Users/juliolima/Documents/media/multiplic/audio/digitar.mp3'
if os.path.exists(SFX):
    # O som entra quando a palavra é FALADA, não quando aparece na tela.
    # O tempo vem do alinhamento do ElevenLabs, que já está no plano.
    idx_fecho = len(partes)-1
    rotulo = CTAS[CTA]['rotulo'].lower()
    pal = next((w for w in plano[idx_fecho].get('palavras',[])
                if rotulo in w['t'].lower().strip('.,:!?')), None)
    quando = inicios[idx_fecho] + (pal['ini'] if pal else 1.0)
    quando_sfx = quando
    entradas += ['-i', SFX]
    i_sfx = n_inputs; n_inputs += 1
    filtros.append(f'[{i_sfx}:a]volume=0.9,adelay={int(quando*1000)}|{int(quando*1000)}[sfx]')
    filtros.append(f'{a}[sfx]amix=inputs=2:normalize=0:duration=longest[comsfx]')
    a = '[comsfx]'

TRILHA = flag('trilha', '')
VOL    = flag('volume', '0.07')
if TRILHA and os.path.exists(TRILHA):
    # Trilha menor que o vídeo precisa repetir. O -stream_loop truncou o áudio
    # em alguns casos (bluebird, 60s num vídeo de 84s), então a repetição é
    # feita antes, num arquivo do tamanho exato.
    dur_t = float(subprocess.run(['ffprobe','-v','quiet','-show_entries','format=duration',
                                  '-of','csv=p=0',TRILHA],capture_output=True,text=True).stdout)
    loop = os.path.join(PASTA,'podcast'+SUFIXO,'_trilha-loop.mp3')
    voltas = max(int(total // dur_t) + 1, 1)
    subprocess.run(['ffmpeg','-y','-stream_loop',str(voltas),'-i',TRILHA,
                    '-t',str(round(total+1,2)),'-c:a','libmp3lame','-q:a','2',loop],
                   check=True, capture_output=True)
    entradas += ['-i', loop]
    idx = n_inputs; n_inputs += 1
    duck = ''   # sem ducking: Julio preferiu a trilha constante
    filtros.append(f'[{idx}:a]volume={VOL}{duck},afade=t=in:d=2,atrim=0:{total:.2f},'
                   f'afade=t=out:st={max(total-3,0):.2f}:d=3[bg]')
    filtros.append(f'{a}[bg]amix=inputs=2:normalize=0:duration=longest[mix]')
    a = '[mix]'
# Áudio e vídeo em passes separados: fazer tudo num comando só estava
# produzindo, de forma intermitente, uma faixa de áudio truncada em 4,6s.
# Assim dá para conferir a duração do áudio antes de juntar.
aud_mix = os.path.join(PASTA,'podcast'+SUFIXO,'_mix.wav')
subprocess.run(['ffmpeg','-y']+[x for x in entradas]+
    ['-filter_complex',';'.join(f for f in filtros if not f.startswith('[0:v]') and 'xfade' not in f),
     '-map',a,'-t',str(round(total,2)),'-c:a','pcm_s16le',aud_mix],
    check=True, capture_output=True)
d_aud = float(subprocess.run(['ffprobe','-v','quiet','-show_entries','format=duration','-of','csv=p=0',aud_mix],
                             capture_output=True,text=True).stdout)
if d_aud < total - 1:
    raise SystemExit(f'ERRO: áudio saiu com {d_aud:.1f}s para um vídeo de {total:.1f}s')

vid_mudo = os.path.join(PASTA,'podcast'+SUFIXO,'_video.mp4')
subprocess.run(['ffmpeg','-y']+[x for f,_ in partes for x in ('-i',f)]+
    ['-filter_complex',';'.join(f for f in filtros if 'xfade' in f),
     '-map',v,'-an','-c:v','libx264','-crf','20','-pix_fmt','yuv420p',
     '-t',str(round(total,2)),vid_mudo], check=True, capture_output=True)

subprocess.run(['ffmpeg','-y','-i',vid_mudo,'-i',aud_mix,'-map','0:v','-map','1:a',
    '-c:v','copy','-c:a','aac','-b:a','192k','-shortest',final], check=True, capture_output=True)
print(f'  áudio conferido: {d_aud:.1f}s')
print(f"\ntotal calculado: {total:.1f}s\n{final}")
