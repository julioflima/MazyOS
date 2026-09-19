#!/usr/bin/env python3
"""Onde cada um dos 57 vídeos está na esteira.

Serve pra duas coisas: dar um panorama e dizer à próxima rodada da
rotina horária exatamente o que fazer em seguida. O estado sai do disco,
não de um registro paralelo — assim nada desanda se uma rodada morrer no
meio.

  python3 scripts/estado-producao.py            panorama
  python3 scripts/estado-producao.py --proximos=3   o que fazer agora
"""
import json, os, re, sys, unicodedata

RAIZ  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VID   = os.path.join(RAIZ, 'marketing/conteudo/videos/consorcio')
MEDIA = '/Users/juliolima/Documents/media/multiplic/consorcios'
flag  = lambda n, d: next((a.split('=',1)[1] for a in sys.argv if a.startswith(f'--{n}=')), d)

def slugify(t):
    t = unicodedata.normalize('NFD', t).encode('ascii','ignore').decode()
    return re.sub(r'-+','-', re.sub(r'[^a-z0-9]+','-', t.lower())).strip('-')

def estagio(d):
    """Primeiro estágio que ainda falta. É a ordem da esteira."""
    p = os.path.join(VID, d)
    cen = os.path.join(p, 'cenas')
    try:
        titulo = ' '.join(json.load(open(os.path.join(p,'conteudo.json')))['titulo'])
    except Exception:
        return 'sem-conteudo', '(conteudo.json ilegível)'
    mp4 = os.path.join(MEDIA, f'vd-{slugify(titulo)}-influencer-podcast-inf.mp4')
    if not os.path.exists(os.path.join(cen, 'buscas.json')):
        return 'termos', titulo
    if not os.path.isdir(cen) or not any(x.isdigit() for x in os.listdir(cen)):
        return 'minerar', titulo
    if not os.path.exists(os.path.join(cen, 'escolhidas.json')):
        return 'escolher', titulo
    if not os.path.exists(mp4):
        return 'produzir', titulo
    return 'pronto', titulo

dirs = sorted(d for d in os.listdir(VID) if os.path.isdir(os.path.join(VID, d)))
tudo = [(d, *estagio(d)) for d in dirs]

ORDEM = ['termos','minerar','escolher','produzir','pronto','sem-conteudo']
N = int(flag('proximos', '0'))

if not N:
    print(f'{len(dirs)} carrosséis\n')
    for e in ORDEM:
        q = [d for d, est, _ in tudo if est == e]
        if q: print(f'  {e:<12} {len(q):>3}')
    falta = [d for d, est, _ in tudo if est != 'pronto']
    print(f'\nprontos {len(dirs)-len(falta)} de {len(dirs)}  |  faltam {len(falta)}')
else:
    # Com rodadas de 30 em 30 minutos, duas podem se sobrepor se uma
    # estourar o tempo. Sem marcação elas pegariam os MESMOS vídeos e
    # gastariam a cota das fontes de imagem duas vezes pela mesma coisa.
    # Quem recebe um vídeo o marca; a marca vale 45 minutos.
    import time
    VALIDADE = 45 * 60
    marca = lambda d: os.path.join(VID, d, '.emandamento')

    def tomado(d):
        m = marca(d)
        if not os.path.exists(m):
            return False
        if time.time() - os.path.getmtime(m) > VALIDADE:
            os.remove(m)          # rodada anterior morreu; libera
            return False
        return True

    fila = []
    for d, est, t in tudo:
        if est in ('pronto', 'sem-conteudo') or tomado(d):
            continue
        fila.append((d, est, t))
        if len(fila) == N:
            break

    if not fila:
        restantes = [d for d, est, _ in tudo if est not in ('pronto','sem-conteudo')]
        if restantes:
            print(f'NADA A FAZER AGORA: os {len(restantes)} restantes estão '
                  'com outra rodada. Encerre sem fazer nada.')
        else:
            print('NADA A FAZER: todos os vídeos estão prontos.')
        sys.exit(0)

    for d, _, _ in fila:
        open(marca(d), 'w').write(str(int(time.time())))
    print(f'próximos {len(fila)} (marcados para esta rodada):')
    for d, est, t in fila:
        print(f'  {d}  [{est}]  {t}')
