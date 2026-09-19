#!/usr/bin/env python3
"""
Produção escalonada dos vídeos. Duas fases, porque a escolha da imagem exige
olho humano e o resto não.

  preparar : minera as imagens das cenas e monta a régua de contato
  produzir : narra, renderiza, monta o vídeo e VERIFICA antes de dar por pronto
  conferir : só roda a verificação nos vídeos já montados

  python3 scripts/lote-videos.py preparar --de=1 --ate=10
  python3 scripts/lote-videos.py produzir --de=1 --ate=10
  python3 scripts/lote-videos.py conferir --de=1 --ate=10

Nenhum vídeo é dado como pronto sem passar pelo verificador: ele mede o
áudio do arquivo final (fala e trilha, do primeiro ao último segundo) e
monta a folha de conferência de imagem x texto, que ainda precisa de olho.

Padrão em identidade/referencias/carrossel-estilo-brunobarbosz/PADRAO-VIDEO.md
"""
import fcntl, json, os, re, subprocess, sys

RAIZ = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
VID  = os.path.join(RAIZ,'marketing/conteudo/videos/consorcio')
FASE = sys.argv[1] if len(sys.argv) > 1 else 'preparar'
flag = lambda n,d: next((a.split('=',1)[1] for a in sys.argv if a.startswith(f'--{n}=')), d)
DE, ATE = int(flag('de','1')), int(flag('ate','10'))

# A mineração é SEMPRE em série, mesmo que existam vários processos.
# O teto não é o processador — é o que as fontes aguentam por hora. Medido
# em 19/09/26: 3 termos em paralelo ficam 5x mais rápidos (4,4s contra 21s)
# e o Openverse devolve 429 em metade dos downloads. Velocidade que custa
# imagem não é ganho. A trava garante isso mesmo com a esteira paralela.
TRAVA = os.path.join(RAIZ, '.mineracao.lock')

class EmSerie:
    def __enter__(self):
        self.f = open(TRAVA, 'w')
        fcntl.flock(self.f, fcntl.LOCK_EX)     # espera a vez
        return self
    def __exit__(self, *e):
        fcntl.flock(self.f, fcntl.LOCK_UN); self.f.close()

# Áudio mora em media/, não no repositório: as trilhas somavam 9,6 MB e
# mídia não vai pro git (regra do Julio). MEDIA_AUDIO centraliza o caminho
# pra não haver dois lugares dizendo onde o arquivo está.
MEDIA_AUDIO = '/Users/juliolima/Documents/media/multiplic/audio'
TRILHAS = {'bluebird':    os.path.join(MEDIA_AUDIO, 'trilha-bluebird.mp3'),
           'documentary': os.path.join(MEDIA_AUDIO, 'trilha-documentary.mp3')}
for _nome, _p in TRILHAS.items():
    if not os.path.exists(_p):
        raise SystemExit(f'ERRO: trilha {_nome} não está em {_p}')
PARAMS = ['--cta=cta-influencer','--voz=5p4THmLc2S6kXKO1pOM5','--ritmo=1.2']

dirs = sorted(d for d in os.listdir(VID) if os.path.isdir(os.path.join(VID,d)))
alvo = dirs[DE-1:ATE]

def termos(pasta):
    """Cada bloco do ensaio pede uma imagem do que ele diz. Sem um termo
    escrito à mão, o resultado vira ilustração genérica — então o arquivo
    fica na pasta e pode ser revisto."""
    p = os.path.join(pasta,'cenas','buscas.json')
    return json.load(open(p)) if os.path.exists(p) else None

if FASE == 'preparar':
    faltando = []
    for i, vid in enumerate(alvo, DE):
        pasta = os.path.join(VID, vid)
        t = termos(pasta)
        if not t:
            faltando.append(vid); continue
        for n, termo in t.items():
            destino = os.path.join(pasta,'cenas',n)
            if os.path.isdir(destino): continue
            with EmSerie():
                subprocess.run(['node',os.path.join(RAIZ,'scripts/minerar-imagens.js'),
                                termo,f'--out={destino}','--n=5','--arquivo'],
                               check=True, stdout=subprocess.DEVNULL)
        print(f'{i:>3}. {vid} minerado')
    if faltando:
        print(f'\nSem termos de busca ({len(faltando)}): ' + ', '.join(faltando))
        print('Criar cenas/buscas.json em cada um antes de preparar.')

elif FASE in ('produzir', 'conferir'):
    reprovados, folhas = [], []
    for i, vid in enumerate(alvo, DE):
        if FASE == 'conferir':
            pasta = os.path.join(VID, vid)
            v = subprocess.run(['python3',os.path.join(RAIZ,'scripts/verificar-video.py'),
                                pasta,'--sufixo=-inf'], capture_output=True, text=True)
            marca = 'ok' if v.returncode == 0 else 'REPROVADO'
            print(f'{i:>3}. {vid}  {marca}')
            if v.returncode != 0:
                print('     ' + (v.stdout + v.stderr).strip().replace(chr(10), chr(10)+'     '))
                reprovados.append(vid)
            else:
                folhas.append((vid, os.path.join(pasta,'podcast-inf','_conferencia.png')))
            continue
        pasta = os.path.join(VID, vid)
        if not os.path.exists(os.path.join(pasta,'cenas','escolhidas.json')):
            print(f'{i:>3}. {vid}  PULADO: imagens não escolhidas'); continue
        # metade com cada trilha, alternando por índice
        nome = 'bluebird' if i % 2 else 'documentary'
        suf = '-inf'
        subprocess.run(['python3',os.path.join(RAIZ,'scripts/gerar-podcast.py'),pasta,
                        *PARAMS,f'--sufixo={suf}'], check=True, stdout=subprocess.DEVNULL)
        subprocess.run(['python3',os.path.join(RAIZ,'scripts/montar-podcast.py'),pasta,
                        '--cta=cta-influencer',f'--sufixo={suf}',
                        f'--trilha={TRILHAS[nome]}','--volume=0.15','--sobrepor=1.0',
                        '--reusar'], check=True, stdout=subprocess.DEVNULL)
        # Verificação obrigatória. O vídeo só é "pronto" depois que o
        # áudio foi medido — já saiu vídeo mudo aos 6s por falta disso.
        v = subprocess.run(['python3',os.path.join(RAIZ,'scripts/verificar-video.py'),
                            pasta,f'--sufixo={suf}'], capture_output=True, text=True)
        if v.returncode != 0:
            print(f'{i:>3}. {vid}  REPROVADO ({nome})')
            print('     ' + (v.stdout + v.stderr).strip().replace(chr(10), chr(10)+'     '))
            reprovados.append(vid); continue
        folhas.append((vid, os.path.join(pasta,'podcast'+suf,'_conferencia.png')))
        print(f'{i:>3}. {vid}  áudio ok  ({nome})')

    if reprovados:
        print(f'\nREPROVADOS ({len(reprovados)}): ' + ', '.join(reprovados))
    if folhas:
        print(f'\nFalta conferir imagem x texto em {len(folhas)} vídeos:')
        for vid, f in folhas: print(f'  {vid}  {f}')
