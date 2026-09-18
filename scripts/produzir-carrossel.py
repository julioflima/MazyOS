#!/usr/bin/env python3
"""
Esteira completa de um carrossel, da mineração da capa ao PNG e à legenda.

  python3 scripts/produzir-carrossel.py marketing/conteudo/videos/consorcio/<id>

Espera um conteudo.json na pasta, com um campo "busca" (termo EM INGLÊS pra
minerar a capa). Faz, em ordem:
  1. minera candidatas/ (pula se já existir)
  2. escolhe a capa e grava capa.jpg + credito-capa.json
  3. monta o HTML das duas versões de CTA
  4. renderiza os PNGs
  5. escreve a legenda.md de cada versão
"""
import json, os, re, subprocess, sys

PASTA = os.path.abspath(sys.argv[1].rstrip('/'))
RAIZ  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ctas import CTAS, CTA_CURTO

NODE_PATH = os.path.join(RAIZ, 'marketing/conteudo/.render/node_modules')
c = json.load(open(os.path.join(PASTA, 'conteudo.json')))
cand = os.path.join(PASTA, 'candidatas')

# ---------------------------------------------------------------- 1. minerar
if not os.path.isdir(cand):
    subprocess.run(['node', os.path.join(RAIZ,'scripts/minerar-imagens.js'),
                    c['busca'], f'--out={cand}', '--n=3', '--sem-met'],
                   cwd=RAIZ, check=True, stdout=subprocess.DEVNULL)

creditos = json.load(open(os.path.join(cand,'creditos.json')))

# ---------------------------------------------------------------- 2. capa
# A capa NUNCA é escolhida automaticamente (regra de Julio, 18/09/26).
# O auto-pick pegava a primeira candidata da fonte preferida sem ninguém olhar
# a foto, e produziu dezenas de capas sem relação com o título — além de
# repetir a mesma imagem em cinco carrosséis diferentes. Agora é obrigatório
# declarar "capa" no conteudo.json, depois de ver as candidatas.
escolha = c.get('capa')
if not escolha:
    raise SystemExit(
        f'\n  FALTA ESCOLHER A CAPA de {os.path.basename(PASTA)}.\n'
        f'  Abra {cand}/index.html, veja as candidatas, e ponha o nome do\n'
        f'  arquivo no campo "capa" do conteudo.json.\n')
foto = next(x for x in creditos if x['arquivo'] == escolha)

# trava anti-repetição: a mesma foto não pode servir de capa em dois carrosséis
import hashlib
meu = hashlib.md5(open(os.path.join(cand, foto['arquivo']),'rb').read()).hexdigest()
raiz_videos = os.path.dirname(os.path.dirname(PASTA))
for tema in os.listdir(raiz_videos):
    td = os.path.join(raiz_videos, tema)
    if not os.path.isdir(td): continue
    for outro in os.listdir(td):
        alvo = os.path.join(td, outro, 'capa.jpg')
        if os.path.abspath(os.path.join(td,outro)) == PASTA: continue
        if os.path.exists(alvo) and hashlib.md5(open(alvo,'rb').read()).hexdigest() == meu:
            raise SystemExit(f'\n  CAPA REPETIDA: essa foto já é a capa de {outro}.\n'
                             f'  Escolha outra candidata.\n')

subprocess.run(['sips','-Z','1600', os.path.join(cand, foto['arquivo']),
                '--out', os.path.join(PASTA,'capa.jpg')],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
json.dump({**foto, 'arquivo':'capa.jpg', 'origem': foto['arquivo']},
          open(os.path.join(PASTA,'credito-capa.json'),'w'), ensure_ascii=False, indent=2)

# ---------------------------------------------------------------- 3 e 4
subprocess.run(['python3', os.path.join(RAIZ,'scripts/montar-carrossel.py'), PASTA],
               check=True, stdout=subprocess.DEVNULL)
for nome in CTAS:
    subprocess.run(['node','render.js'], cwd=os.path.join(PASTA,nome), check=True,
                   env={**os.environ,'NODE_PATH':NODE_PATH}, stdout=subprocess.DEVNULL)

# ---------------------------------------------------------------- 5. legenda
def limpo(t):
    return re.sub(r'<b>(.*?)</b>', r'**\1**', re.sub(r'<[^>]+>','',t))

corpo = '\n\n'.join(limpo(p) for slide in c['slides'] for p in slide)
titulo = ' '.join(c['titulo'])
vid = os.path.basename(PASTA)

for nome, cta_padrao in CTAS.items():
    cta = {**cta_padrao, **CTA_CURTO.get(nome, {})} if c.get('cta_curto') else cta_padrao
    tags = ' '.join(cta['hashtags'] + ['#' + t for t in c.get('tags',[])])
    txt = f"""# Legenda — CTA {cta['rotulo']}

**Post:** {titulo}
**Origem:** reel `{vid}`
**Público:** {cta['publico']}

---

{corpo}

{cta['legenda']}

---

{tags}

---

*Foto de capa: {foto['autor']}, via {foto['fonte']} ({foto['licenca']}).*
"""
    open(os.path.join(PASTA, nome, 'legenda.md'),'w').write(txt)

print(f"{vid:<14} capa={foto['fonte'][:18]:<18} {titulo[:45]}")
