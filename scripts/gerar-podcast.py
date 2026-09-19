#!/usr/bin/env python3
"""
Versão "podcast" do carrossel: imagem cheia por cena, texto como legenda
queimada, narração acelerada. O layout de carrossel aparece só na última cena,
onde a Izabel assina.

  python3 scripts/gerar-podcast.py <pasta-do-carrossel> [--cta=cta-sonho] [--ritmo=1.12]
"""
import json, os, re, subprocess, sys, shutil, urllib.request

PASTA = os.path.abspath(sys.argv[1].rstrip('/'))
flag = lambda n,d: next((a.split('=',1)[1] for a in sys.argv if a.startswith(f'--{n}=')), d)
CTA   = flag('cta','cta-sonho')
RITMO = float(flag('ritmo','1.0'))   # 1.6x: testado por Julio, é onde ganha energia
SUFIXO = flag('sufixo','')
RAIZ  = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.insert(0, os.path.join(RAIZ,'scripts'))
from ctas import CTAS

cfg = json.load(open(os.path.join(RAIZ,'identidade/referencias/carrossel-estilo-brunobarbosz/video-config.json')))
cfg['voz_id'] = flag('voz', cfg['voz_id'])
CHAVE = [l.split('=',1)[1].strip() for l in open(os.path.join(RAIZ,'.env')) if l.startswith('ELEVEN')][0]
conteudo = json.load(open(os.path.join(PASTA,'conteudo.json')))
limpo = lambda t: re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',t)).strip()

saida = os.path.join(PASTA, 'podcast'+SUFIXO); os.makedirs(saida, exist_ok=True)

def narrar(texto, base):
    """Pede o áudio com alinhamento por caractere — é o que permite legenda
    sincronizada palavra a palavra."""
    mp3, js = f'{base}.mp3', f'{base}.json'
    if os.path.exists(mp3) and os.path.exists(js): return mp3, json.load(open(js))
    corpo = json.dumps({'text':texto,'model_id':cfg['modelo'],
                        'voice_settings':{'stability':0.5,'similarity_boost':0.75}}).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{cfg['voz_id']}/with-timestamps",
        data=corpo, headers={'xi-api-key':CHAVE,'Content-Type':'application/json'}, method='POST')
    d = json.load(urllib.request.urlopen(req, timeout=120))
    import base64; open(mp3,'wb').write(base64.b64decode(d['audio_base64']))
    json.dump(d['alignment'], open(js,'w'))
    return mp3, d['alignment']

def palavras(al, fator):
    """Junta os caracteres em palavras com início e fim, já no ritmo acelerado."""
    out, atual, ini = [], '', None
    for ch, s, e in zip(al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']):
        if ch.isspace():
            if atual: out.append({'t':atual,'ini':ini/fator,'fim':e/fator}); atual, ini = '', None
        else:
            if ini is None: ini = s
            atual += ch
            fim = e
    if atual: out.append({'t':atual,'ini':ini/fator,'fim':fim/fator})
    return out

# ------- monta as cenas
escolhidas = json.load(open(os.path.join(PASTA,'cenas/escolhidas.json')))
cenas = [{'n':1,'img':os.path.join(PASTA,'capa.jpg'),'capa':True,'paras':[],
          'fala':f"{' '.join(conteudo['titulo'])}. {conteudo['subtitulo'].replace('→','').strip().rstrip('.')}."}]
for i,bloco in enumerate(conteudo['slides'], 2):
    k = str(i)
    if k not in escolhidas: continue
    cenas.append({'n':i,'img':os.path.join(PASTA,'cenas',k,escolhidas[k]),
                  'paras':[limpo(x) for x in bloco],
                  'fala':' '.join(limpo(x) for x in bloco)})
# convite do CTA ainda é imagem
n_conv = len(cenas)+1
cenas.append({'n':n_conv,'img':os.path.join(PASTA,'cenas','7',escolhidas['7']),
              'paras':[limpo(x) for x in CTAS[CTA]['convite'] if limpo(x)],
              'fala':' '.join(limpo(x) for x in CTAS[CTA]['convite'] if limpo(x))})
# a última é o slide do carrossel, onde a Izabel assina
slides = sorted(f for f in os.listdir(os.path.join(PASTA,CTA)) if f.startswith('slide-'))
cenas.append({'n':n_conv+1,'img':os.path.join(PASTA,CTA,slides[-1]),'carrossel':True,'paras':[],
              'fala':' '.join(limpo(x) for x in CTAS[CTA]['fecho'] if limpo(x))})

plano = []
for c in cenas:
    base = os.path.join(saida, f"fala-{c['n']:02d}")
    mp3, al = narrar(c['fala'], base)
    # o ritmo entra no nome: senão uma troca de velocidade reaproveita o
    # arquivo antigo e a mudança não acontece (aconteceu em 19/09/26)
    rapido = f'{base}-r{RITMO:.2f}.mp3'
    if not os.path.exists(rapido):
        # meio segundo de silêncio no fim: é aí que a próxima voz entra, em
        # vez de entrar por cima da última frase (Julio, 19/09/26)
        subprocess.run(['ffmpeg','-y','-i',mp3,'-filter:a',
                        f'atempo={RITMO},apad=pad_dur=0.5',rapido],
                       check=True, capture_output=True)
    dur = float(subprocess.run(['ffprobe','-v','quiet','-show_entries','format=duration',
                                '-of','csv=p=0',rapido],capture_output=True,text=True).stdout)
    pal = palavras(al, RITMO)
    # marca a qual parágrafo cada palavra pertence, para a legenda quebrar
    # igual ao carrossel em vez de virar um bloco corrido
    limites, k = [], 0
    for par in c.get('paras', []):
        k += len(par.split()); limites.append(k)
    for idx, w in enumerate(pal):
        w['p'] = next((j for j,lim in enumerate(limites) if idx < lim), max(len(limites)-1, 0))
    plano.append({**{k2:v for k2,v in c.items() if k2!='fala'},
                  'audio':rapido, 'dur':round(dur,2), 'palavras':pal})
    print(f"  cena {c['n']:02d}  {dur:5.1f}s  {len(plano[-1]['palavras'])} palavras")

json.dump(plano, open(os.path.join(saida,'plano.json'),'w'), ensure_ascii=False, indent=2)
print(f"\ntotal: {sum(c['dur'] for c in plano):.1f}s  ->  {saida}/plano.json")
