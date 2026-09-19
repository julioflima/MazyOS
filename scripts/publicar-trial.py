#!/usr/bin/env python3
"""Publica os vídeos como Trial Reel no Instagram, via Graph API.

Trial reel só existe na API — não há toggle no instagram.com, e o GHL não
tem o campo. O parâmetro é `trial_params`, que a documentação oficial da
Meta não lista mas três implementações independentes usam (Ayrshare, o nó
de n8n do MookieLian, o servidor MCP do William-Gao). Confirmar no
primeiro vídeo antes de soltar o resto.

  graduation_strategy=MANUAL  -> fica trial pra sempre, a menos que alguém
                                 gradue no app. É o que o Julio quer:
                                 "sempre tem q ficar no trial".

O vídeo precisa estar num endereço público: a Meta baixa o arquivo pela
URL. O ngrok resolve — o GHL já provou que a mídia é copiada no upload,
então o túnel só precisa estar de pé durante a publicação.

  python3 scripts/publicar-trial.py --base=https://SEU.ngrok-free.app --limite=1
  python3 scripts/publicar-trial.py --base=... --limite=1 --pra-valer

Sem --pra-valer ele só mostra o que faria. Publicar é irreversível e
alcança o público, então o padrão é não publicar.
"""
import json, os, re, sys, time, unicodedata, urllib.parse, urllib.request

RAIZ  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VID   = os.path.join(RAIZ, 'marketing/conteudo/videos/consorcio')
MEDIA = '/Users/juliolima/Documents/media/multiplic/consorcios'
API   = 'https://graph.facebook.com/v23.0'
sys.path.insert(0, os.path.join(RAIZ, 'scripts'))
from ctas import CTAS

flag = lambda n, d=None: next((a.split('=',1)[1] for a in sys.argv if a.startswith(f'--{n}=')), d)
BASE     = (flag('base') or '').rstrip('/')
LIMITE   = int(flag('limite', '1'))
PRA_VALER = '--pra-valer' in sys.argv

TOKEN = os.environ.get('META_PAGE_ACCESS_TOKEN')
IG_ID = os.environ.get('META_IG_USER_ID')
if not TOKEN or not IG_ID:
    sys.exit('ERRO: faltam META_PAGE_ACCESS_TOKEN e META_IG_USER_ID no ambiente.\n'
             'Rode com: node --env-file=.env  ou  export a partir do .env')
if not BASE:
    sys.exit('ERRO: passe --base=https://... (o endereço público que serve os mp4)')

def chamar(caminho, dados=None):
    url = f'{API}/{caminho}'
    if dados is None:
        url += ('&' if '?' in url else '?') + urllib.parse.urlencode({'access_token': TOKEN})
        req = urllib.request.Request(url)
    else:
        dados = {**dados, 'access_token': TOKEN}
        req = urllib.request.Request(url, data=urllib.parse.urlencode(dados).encode())
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        corpo = e.read().decode()
        raise SystemExit(f'ERRO da Meta em {caminho}:\n{corpo}')

def slugify(t):
    t = unicodedata.normalize('NFD', t).encode('ascii','ignore').decode()
    return re.sub(r'-+','-', re.sub(r'[^a-z0-9]+','-', t.lower())).strip('-')

def legenda(pasta):
    """O legenda.md separa blocos por '---': 0 controle, 1 corpo, 2 hashtags."""
    p = os.path.join(pasta, 'legenda.md')
    if not os.path.exists(p): return ''
    partes = re.split(r'(?m)^---\s*$', open(p).read())
    corpo = partes[1].strip() if len(partes) > 1 else partes[0].strip()
    tags  = partes[2].strip() if len(partes) > 2 else ''
    return re.sub(r'\*\*(.+?)\*\*', r'\1', f'{corpo}\n\n{tags}'.strip())

# ---- reúne os vídeos prontos ----------------------------------------------
fila = []
for d in sorted(os.listdir(VID)):
    pasta = os.path.join(VID, d)
    conteudo = os.path.join(pasta, 'conteudo.json')
    if not os.path.exists(conteudo): continue
    titulo = ' '.join(json.load(open(conteudo))['titulo'])
    arq = f'vd-{slugify(titulo)}-influencer-podcast-inf.mp4'
    if os.path.exists(os.path.join(MEDIA, arq)):
        fila.append((d, titulo, arq, os.path.join(pasta, 'cta-influencer')))
fila = fila[:LIMITE]

if not fila:
    sys.exit('Nenhum vídeo montado encontrado.')

print(f'{len(fila)} vídeo(s){"" if PRA_VALER else "  [SIMULAÇÃO — nada será publicado]"}\n')
for d, titulo, arq, pasta_cta in fila:
    url = f'{BASE}/{arq}'
    print(f'{d}  {titulo}\n  {url}')
    if not PRA_VALER:
        print('  (simulação)\n'); continue

    # 1. container. trial_params é o que torna o reel um teste.
    c = chamar(f'{IG_ID}/media', {
        'media_type':  'REELS',
        'video_url':   url,
        'caption':     legenda(pasta_cta),
        'share_to_feed': 'false',
        'trial_params': json.dumps({'graduation_strategy': 'MANUAL'}),
    })
    cid = c['id']

    # 2. a Meta baixa e transcodifica o vídeo; isso leva tempo.
    for _ in range(60):
        st = chamar(f'{cid}?fields=status_code,status')
        if st.get('status_code') == 'FINISHED': break
        if st.get('status_code') == 'ERROR':
            raise SystemExit(f"  ERRO no processamento: {st.get('status')}")
        time.sleep(5)
    else:
        raise SystemExit('  o container não ficou pronto em 5 minutos')

    # 3. publica
    pub = chamar(f'{IG_ID}/media_publish', {'creation_id': cid})
    mid = pub['id']
    print(f'  publicado: {mid}')

    # 4. CTA curta no primeiro comentário — regra fixa do projeto
    chamar(f'{mid}/comments', {'message': CTAS['cta-influencer']['cta_curto']})
    print('  CTA no primeiro comentário\n')
    time.sleep(3)
