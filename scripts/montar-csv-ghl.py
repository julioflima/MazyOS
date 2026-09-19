#!/usr/bin/env python3
"""
Gera o CSV de carga em massa do GHL (Social Planner, Formato Avançado)
para um dos dois CTAs, e copia os slides para a pasta pública do site.

  python3 scripts/montar-csv-ghl.py cta-sonho --inicio=2026-09-19 --base=https://SEU-DOMINIO

Um carrossel por dia, 15h (fuso da location: America/Sao_Paulo).
"""
import json, os, re, sys, shutil, datetime, filecmp

RAIZ = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(RAIZ, 'scripts'))
from ctas import CTAS

CTA = sys.argv[1] if len(sys.argv) > 1 else 'cta-sonho'
flag = lambda n, d: next((a.split('=',1)[1] for a in sys.argv if a.startswith(f'--{n}=')), d)
INICIO = datetime.date.fromisoformat(flag('inicio', '2026-09-19'))
BASE   = flag('base', 'https://BASE-URL-PENDENTE').rstrip('/')
HORA   = flag('hora', '15:00:00')
# --intervalo=N: em vez de um post por dia, joga a leva inteira no mesmo dia,
# espaçada de N minutos a partir de HORA. Usado pra subir os carrosséis de
# teste de uma vez só, sem ocupar dois meses de calendário.
INTERVALO = int(flag('intervalo', '0'))
SITE   = flag('site', '/Users/juliolima/projects/multiplic-consorcios/public/carrosseis')
# As colunas do Formato Avançado são escopadas por plataforma na primeira
# linha do cabeçalho, então um CSV só atende as três redes: cada uma lê o
# grupo dela e ignora o resto.
#   modo=completo -> Instagram + Facebook + LinkedIn (padrão)
#   modo=imagens  -> só Instagram e Facebook
#   modo=pdf      -> só LinkedIn
#   modo=video    -> Instagram/Facebook Reels + YouTube Shorts + TikTok
MODO   = flag('modo', 'completo')
# O site guarda cada carrossel em três pastas: conteudo/ com o miolo educativo,
# que é byte a byte o mesmo em todos os CTAs, e uma pasta por CTA com só os
# slides da chamada. Assim nenhum arquivo é publicado duas vezes e nenhum CTA
# depende da pasta do outro.
# --limite=N: gera só os N primeiros. Serve pra subir um post de teste antes
# de soltar a leva inteira.
LIMITE = int(flag('limite', '0'))

VID = os.path.join(RAIZ, 'marketing/conteudo/videos/consorcio')
cta = CTAS[CTA]
slug = CTA.replace('cta-', '')

def legenda(p):
    """O legenda.md é dividido por linhas '---' em quatro blocos:
    0 cabeçalho de controle, 1 corpo, 2 hashtags, 3 crédito da foto.
    Pro Instagram vão só o corpo e as hashtags."""
    partes = re.split(r'(?m)^---\s*$', open(p).read())
    corpo = partes[1].strip() if len(partes) > 1 else partes[0].strip()
    tags  = partes[2].strip() if len(partes) > 2 else ''
    texto = f'{corpo}\n\n{tags}'.strip()
    return re.sub(r'\*\*(.+?)\*\*', r'\1', texto)   # Instagram não renderiza negrito

# O Formato Avançado tem DUAS linhas de cabeçalho: a primeira agrupa por
# plataforma (All Social, Facebook, Instagram, ...), a segunda nomeia as
# colunas. São 40 no total. Mandar só uma linha faz o GHL ler como básico e
# reclamar de colunas faltando. Por isso o cabeçalho vem do modelo oficial.
import csv
MODELO = os.path.join(RAIZ, 'templates/ghl-social-planner-avancado-modelo.csv')
with open(MODELO) as fh:
    GRUPOS, COLS = list(csv.reader(fh))[:2]

# índices dentro das 40 colunas
I_DATA, I_TEXTO, I_IMGS = 0, 1, 3
I_OTIM, I_MARCA, I_TAGS, I_CATEG, I_COMENT = 7, 8, 9, 10, 11
I_TIPO_FB, I_TIPO_IG = 12, 13
I_PDF_TITULO, I_POST_PDF = 14, 15   # LinkedIn: carrossel folheável só como PDF
I_VIDEOS = 5
# YouTube e TikTok só existem no modo vídeo — carrossel eles não aceitam.
I_YT_TITULO, I_YT_PRIVACIDADE, I_YT_TIPO = 26, 27, 28
I_TT_PRIVACIDADE, I_TT_COMENTARIO = 29, 31
I_TT_OUTRA_MARCA, I_TT_DUETO, I_TT_COSTURA = 30, 32, 33
I_TT_DIVULGACAO, I_TT_MARCA_PROPRIA = 34, 35
# O modelo oficial do GHL preenche as SETE colunas do TikTok. Deixar em
# branco é apostar num padrão que ninguém documentou (Julio, 19/09/26).
# --divulgacao=nao desliga a etiqueta de conteúdo promocional.
DIVULGAR = flag('divulgacao', 'sim') == 'sim'
MEDIA = '/Users/juliolima/Documents/media/multiplic/consorcios'

def titulo_de(vid):
    return ' '.join(json.load(open(os.path.join(VID, vid, 'conteudo.json')))['titulo'])

def slugify(t):
    import unicodedata
    t = unicodedata.normalize('NFD', t).encode('ascii', 'ignore').decode()
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', t.lower())).strip('-')
dirs = sorted(d for d in os.listdir(VID) if os.path.isdir(os.path.join(VID, d)))
# --pular=N: ignora os N primeiros carrosséis. Usado quando os primeiros já
# foram agendados numa carga anterior (ex.: o post de teste).
PULAR = int(flag('pular', '0'))
if PULAR:  dirs = dirs[PULAR:]
if LIMITE: dirs = dirs[:LIMITE]
linhas, copiados = [], 0
for i, vid in enumerate(dirs):
    pasta = os.path.join(VID, vid, CTA)
    slides = sorted(f for f in os.listdir(pasta) if f.startswith('slide-') and f.endswith('.png'))
    outros = [c for c in os.listdir(os.path.join(VID, vid))
              if c.startswith('cta-') and c != CTA]
    caminhos = []
    for f in slides:
        origem = os.path.join(pasta, f)
        # Compartilhado = idêntico em TODOS os CTAs. A comparação é por conteúdo,
        # nunca pela posição do slide: há carrosséis em que o miolo também muda,
        # e a regra "os seis primeiros são iguais" publicaria a imagem errada.
        gemeos = [os.path.join(VID, vid, c, f) for c in outros]
        comum = bool(gemeos) and all(os.path.exists(g) and filecmp.cmp(origem, g, shallow=False)
                                     for g in gemeos)
        sub = 'conteudo' if comum else slug
        destino = os.path.join(SITE, vid, sub)
        os.makedirs(destino, exist_ok=True)
        alvo = os.path.join(destino, f)
        if not (os.path.exists(alvo) and filecmp.cmp(origem, alvo, shallow=False)):
            shutil.copy2(origem, alvo); copiados += 1
        caminhos.append(f'{sub}/{f}')
    urls = ', '.join(f'{BASE}/carrosseis/{vid}/{c}' for c in caminhos)
    hora0 = datetime.datetime.combine(INICIO, datetime.time.fromisoformat(HORA))
    quando = hora0 + datetime.timedelta(minutes=i * INTERVALO) if INTERVALO \
             else hora0 + datetime.timedelta(days=i)
    linha = [''] * len(COLS)
    linha[I_DATA]   = quando.strftime('%Y-%m-%d %H:%M:%S')
    linha[I_TEXTO]  = legenda(os.path.join(pasta, 'legenda.md'))
    linha[I_IMGS]   = urls
    linha[I_OTIM]   = 'TRUE'
    linha[I_MARCA]  = 'FALSE'
    linha[I_TAGS]   = 'consorcio'
    linha[I_CATEG]  = 'Produção' if CTA == 'cta-sonho' else 'Teste'
    linha[I_COMENT] = cta['cta_curto']
    if MODO in ('completo', 'pdf'):
        # LinkedIn: sem isso o post vira mosaico e perde a ordem de leitura
        linha[I_PDF_TITULO] = ' '.join(json.load(open(os.path.join(VID, vid, 'conteudo.json')))['titulo'])
        linha[I_POST_PDF]   = 'TRUE'
    if MODO in ('completo', 'imagens'):
        linha[I_TIPO_FB] = 'post'
        linha[I_TIPO_IG] = 'post'
    if MODO == 'video':
        # No modo vídeo não vai imagem nenhuma: o post é o mp4 vertical.
        titulo = titulo_de(vid)
        arq = f"vd-{slugify(titulo)}-{slug}-podcast-inf.mp4"
        cam = os.path.join(MEDIA, arq)
        if not os.path.exists(cam):
            raise SystemExit(f'ERRO: vídeo não encontrado para {vid}:\n  {cam}')
        linha[I_IMGS]    = ''
        linha[I_VIDEOS]  = f'{BASE}/{arq}'
        linha[I_TIPO_FB] = 'reel'
        linha[I_TIPO_IG] = 'reel'
        # YouTube: sem título o post é recusado, e sem type=short o vídeo
        # vertical entra como vídeo comum e não cai no feed de Shorts.
        # O campo aceita 100 caracteres (Julio, 19/09/26).
        linha[I_YT_TITULO]      = titulo[:100]
        linha[I_YT_PRIVACIDADE] = 'public'
        linha[I_YT_TIPO]        = 'short'
        linha[I_TT_PRIVACIDADE]   = 'everyone'
        linha[I_TT_COMENTARIO]    = 'TRUE'
        # Dueto e costura ligados: é alcance de graça, e o conteúdo é
        # educativo — não há nada aqui que a gente não queira que reusem.
        linha[I_TT_DUETO]         = 'TRUE'
        linha[I_TT_COSTURA]       = 'TRUE'
        # Não divulgamos marca de terceiro; o vídeo promove a própria
        # Multiplic. Por isso a divulgação de conteúdo comercial vai
        # ligada e apontando para "marca própria": é o que a política do
        # TikTok pede de quem promove o próprio negócio, e declarar
        # errado é risco de derrubada do vídeo.
        linha[I_TT_OUTRA_MARCA]   = 'FALSE'
        linha[I_TT_DIVULGACAO]    = 'TRUE' if DIVULGAR else 'FALSE'
        linha[I_TT_MARCA_PROPRIA] = 'TRUE' if DIVULGAR else 'FALSE'
    linhas.append(linha)

# Vão existir muitos CSVs ao longo do tempo. O nome carrega tudo o que
# identifica a carga: quando foi gerado, qual CTA, para que mídia, quantos
# posts e o período que ele agenda.
pasta_csv = os.path.join(RAIZ, 'marketing/conteudo/ghl-csv')
os.makedirs(pasta_csv, exist_ok=True)
hoje = datetime.date.today().isoformat()
fim  = INICIO if INTERVALO else (INICIO + datetime.timedelta(days=len(linhas) - 1))
mes  = lambda d: f'{d.day:02d}{["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"][d.month-1]}'
saida = os.path.join(pasta_csv,
    f'{hoje}_{slug}_{MODO}_{len(linhas)}posts_{mes(INICIO)}-{mes(fim)}.csv')
with open(saida, 'w', newline='') as fh:
    w = csv.writer(fh)
    w.writerow(GRUPOS); w.writerow(COLS)
    w.writerows(linhas)

if len(linhas) > 90:
    print(f'ATENÇÃO: {len(linhas)} posts — o GHL importa no máximo 90 por CSV.')

ja_no_ar = sum(len(l[I_IMGS].split(',')) for l in linhas) - copiados
print(f'{len(linhas)} posts  |  {copiados} imagens novas  |  {ja_no_ar} já publicadas')
print(f'de {linhas[0][I_DATA]}  ate {linhas[-1][I_DATA]}')
print(saida)
