#!/usr/bin/env python3
"""Régua de contato: junta as candidatas de vários carrosséis numa imagem só,
com rótulo por arquivo, pra dar pra escolher a capa olhando.

  python3 scripts/contato.py <pasta1> <pasta2> ... -o /tmp/folha.png
"""
import json, os, subprocess, sys

args=[a for a in sys.argv[1:] if a!='-o']
out=args[args.index([a for a in args if a.endswith('.png')][0])] if any(a.endswith('.png') for a in args) else '/tmp/folha.png'
pastas=[a for a in args if not a.endswith('.png')]
RAIZ=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))

blocos=[]
for p in pastas:
    p=os.path.abspath(p.rstrip('/'))
    c=json.load(open(os.path.join(p,'conteudo.json')))
    cand=os.path.join(p,'candidatas')
    cr=json.load(open(os.path.join(cand,'creditos.json')))
    thumbs=''.join(
      f'<figure><img src="file://{cand}/{x["arquivo"]}"/><figcaption>{x["arquivo"]}</figcaption></figure>'
      for x in cr)
    blocos.append(f'<section><h2>{os.path.basename(p)} — {" ".join(c["titulo"])}</h2>'
                  f'<p class=b>busca: {c["busca"]}</p><div class=g>{thumbs}</div></section>')

html=f'''<!doctype html><meta charset=utf-8><style>
body{{background:#fff;font:13px system-ui;margin:0;padding:18px;width:1500px}}
section{{margin-bottom:22px}} h2{{font-size:17px;margin:0 0 2px}}
p.b{{color:#888;margin:0 0 10px;font-size:12px}}
.g{{display:grid;grid-template-columns:repeat(6,1fr);gap:10px}}
figure{{margin:0}} img{{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:5px;background:#eee}}
figcaption{{font-size:11px;color:#555;margin-top:3px;text-align:center}}
</style>{''.join(blocos)}'''

tmp='/tmp/_contato.html'; open(tmp,'w').write(html)
js=f'''const {{chromium}}=require('playwright');(async()=>{{
 const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1500,height:900}}}});
 await p.goto('file://{tmp}');await p.waitForTimeout(1200);
 await p.screenshot({{path:'{out}',fullPage:true}});await b.close();}})();'''
open('/tmp/_contato.js','w').write(js)
subprocess.run(['node','/tmp/_contato.js'],check=True,
  env={**os.environ,'NODE_PATH':os.path.join(RAIZ,'marketing/conteudo/.render/node_modules')})
print(out)
