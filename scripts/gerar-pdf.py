#!/usr/bin/env python3
"""
Junta os slides de cada carrossel num PDF de página por slide — o formato de
"documento" do LinkedIn, que é o único que vira carrossel folheável lá.
Post com várias imagens no LinkedIn vira mosaico e quebra a leitura em ordem.

  python3 scripts/gerar-pdf.py cta-sonho [--site=<pasta public/carrosseis>]
"""
import json, os, sys
from PIL import Image

RAIZ = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
CTA  = sys.argv[1] if len(sys.argv) > 1 else 'cta-sonho'
flag = lambda n, d: next((a.split('=',1)[1] for a in sys.argv if a.startswith(f'--{n}=')), d)
SITE = flag('site', '/Users/juliolima/projects/multiplic-consorcios/public/carrosseis')
slug = CTA.replace('cta-', '')
VID  = os.path.join(RAIZ, 'marketing/conteudo/videos/consorcio')

feitos = 0
for vid in sorted(d for d in os.listdir(VID) if os.path.isdir(os.path.join(VID, d))):
    pasta = os.path.join(VID, vid, CTA)
    slides = sorted(f for f in os.listdir(pasta) if f.startswith('slide-') and f.endswith('.png'))
    if not slides: continue
    # RGBA não é aceito em PDF; converte mantendo o fundo preto da peça
    paginas = [Image.open(os.path.join(pasta, f)).convert('RGB') for f in slides]
    titulo = ' '.join(json.load(open(os.path.join(VID, vid, 'conteudo.json')))['titulo'])
    saida = os.path.join(pasta, 'carrossel.pdf')
    paginas[0].save(saida, save_all=True, append_images=paginas[1:],
                    format='PDF', resolution=144.0, title=titulo)
    destino = os.path.join(SITE, vid, slug)
    os.makedirs(destino, exist_ok=True)
    os.replace(saida, os.path.join(pasta, 'carrossel.pdf')) if False else None
    import shutil; shutil.copy2(saida, os.path.join(destino, 'carrossel.pdf'))
    feitos += 1

print(f'{feitos} PDFs gerados ({slug}) — um por carrossel, uma página por slide')
