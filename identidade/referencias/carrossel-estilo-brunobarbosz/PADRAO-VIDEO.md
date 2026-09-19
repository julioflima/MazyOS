# Padrão de vídeo — Multiplic

> Tudo o que foi decidido durante a construção do protótipo (18–19/09/26).
> Este arquivo é a fonte da verdade. Antes de mudar qualquer coisa aqui,
> confira se não foi algo já testado e reprovado — a lista está no fim.

## Formato

Cada carrossel vira um vídeo vertical **1080x1920, 30fps, H.264 + AAC**,
no formato "podcast": imagem cheia por cena, texto entrando como legenda
sobre a foto, narração por cima.

O **layout de carrossel aparece só na última cena**, onde a Izabel assina.

Motivo da migração: TikTok não aceita carrossel e Reels não tem teste para
carrossel. Todo o conteúdo passa a ser vídeo.

## Estrutura das cenas

| Cena | Conteúdo | Composição |
|---|---|---|
| 1 | Capa: foto sangrando, título subindo linha a linha, subtítulo depois | `Capa` (Remotion) |
| 2..N | Uma imagem por bloco do ensaio, legenda acumulando | `Cena` (Remotion) |
| N+1 | Convite do CTA, sobre imagem | `Cena` |
| N+2 | Fecho do CTA, elementos entrando um a um | `Fecho` (Remotion) |

## Narração

- **Literal**: lê exatamente o que está no slide. Versão falada reduzida foi
  testada e reprovada.
- Gerada de `conteudo.json` + `ctas.py`, sem roteiro intermediário.
- Voz: **`5p4THmLc2S6kXKO1pOM5`** (voz B), modelo `eleven_multilingual_v2`.
- Velocidade: **1,2×**
- A capa é narrada com título + subtítulo.
- Consumo medido: **~1.537 caracteres por vídeo**; os 57 dão ~88 mil.
  Conta no plano **Creator** (136 mil/mês), que comporta a leva inteira.

## Áudio

- **Trilha de fundo a 15%**, constante, sem ducking.
- Metade dos vídeos com **Death of a Bluebird**, metade com **Documentary**,
  alternando por índice.
- **Sobreposição de vozes: 1,0s.** A fala da cena seguinte começa antes de a
  anterior terminar — dá urgência e prende. Cai no silêncio final de cada
  narração (meio segundo acrescentado), nunca em cima das últimas palavras.
- Sem fade de entrada na voz que chega; fade de 0,3s só na que morre.
- **Efeito de teclado de 0,8s** no instante em que a palavra-chave é FALADA
  (tempo vindo do alinhamento do ElevenLabs, não fixo).
  Arquivo: `identidade/audio/digitar.mp3`.

## Movimento

- **Zoom forte** nas imagens: 1 → 1,28 nas cenas, 1 → 1,3 na capa.
- Transição entre cenas: crossfade de 1,0s (mesmo valor da sobreposição, para
  áudio e vídeo não desalinharem).
- **Nada de zoom em slide de texto** — reprovado.

## Legenda

- O texto **acumula** conforme é falado, até formar o bloco, como nas peças do
  Lord. Karaokê palavra a palavra foi reprovado.
- Quebra nos mesmos parágrafos do carrossel. 46px, peso 500.

## CTA

- **Todos os vídeos usam o CTA `INFLUENCER`.**
- No vídeo entra o CTA completo (dois blocos: convite e fecho).
- Na legenda do post, o primeiro comentário leva a **CTA curta**
  (`cta_curto` em `ctas.py`).

## Imagens

- Uma por cena, minerada para o que aquele trecho diz.
- Só acervo documental (`--arquivo`): Wikimedia, Openverse, Unsplash.
  **Pexels é último recurso** — é banco comercial e destrói o tom.
- Enquadramento fechado, sem excesso de céu, assunto legível em meio segundo.
- **Gente nas imagens, sempre que possível** (Julio, 19/09/26): rosto, mãos,
  família, alguém fazendo algo. O espectador precisa se reconhecer na cena.
  Objeto isolado e paisagem vazia não geram identificação — usar só quando o
  trecho falar de uma coisa, não de uma pessoa.
  Na prática, os termos de busca devem nomear **pessoas em situação**:
  "família na porta de casa", "mãos contando dinheiro", "casal olhando
  planta da casa" — não "casa", "dinheiro", "planta".

## Saída

`~/Documents/media/multiplic/consorcios/vd-<titulo>-<cta>-<trilha>.mp4`

## Permissões necessárias no ElevenLabs

`text_to_speech`, `sound_generation`, `music_generation`, `models_read`,
`user_read` (para ler a cota).

## Testado e REPROVADO — não repetir

| O quê | Por quê |
|---|---|
| Zoom em slide de texto | denuncia foto parada, corta bordas |
| Narração reduzida (diferente da tela) | o que se lê tem que ser o que se ouve |
| Legenda karaokê palavra a palavra | não é o registro do Lord |
| Transição de 0,55s | apressada |
| Sobreposição de 1s em cima das palavras | soterra a última frase |
| Ducking da trilha no efeito sonoro | ficou pior que constante |
| Efeito de teclado de 2,8s | continua teclando depois da fala |
| Logo da empresa nas cenas | poluía |
| Gravação comercial protegida (Sinatra) | Content ID silencia o vídeo inteiro |
| Fecho como PNG estático | os elementos têm que entrar um a um |

## Armadilhas técnicas já enfrentadas

- **Cache de áudio deve incluir a velocidade no nome do arquivo.** Sem isso,
  trocar o ritmo reaproveita o arquivo antigo e nada muda.
- **Cada versão precisa de pasta própria** (`podcast<sufixo>`) para plano e
  cenas. Compartilhar pasta fez três versões saírem idênticas.
- **Áudio e vídeo em passes separados.** Montar tudo num comando só truncava
  o áudio em 4,6s de forma intermitente. O script confere a duração do áudio
  antes de juntar e aborta se estiver curto.
- **Contar inputs do ffmpeg com contador explícito**, não por pares: a trilha
  entra com `-stream_loop -1 -i`, que são quatro argumentos.
- **Trilha menor que o vídeo** é repetida num arquivo próprio antes da
  montagem; `-stream_loop` direto truncou o áudio.

## Distribuição e hospedagem

- Publicação: **1 vídeo por dia, 15h**, fuso `America/Sao_Paulo` (o GHL usa o
  fuso da location, então a hora vai literal no CSV).
- Os vídeos são servidos por **ngrok** a partir da máquina do Julio no momento
  da importação; o CSV aponta para a URL do túnel na coluna `videoUrls`.
  Tipo `reel` para Facebook e Instagram.
- **Cuidado**: essa arquitetura só é segura se o GHL copiar a mídia na
  importação. Se ele apenas referenciar, quem baixa é a Meta na hora de
  publicar, e o túnel precisaria estar de pé todo dia às 15h. Confirmar com um
  post de teste antes de subir a leva.
- Peso medido: **~44 MB por vídeo** (84s, CRF 20). Os 57 dão ~2,5 GB pelo
  túnel — conferir o limite de banda da conta ngrok.

## Produção escalonada

`scripts/lote-videos.py`, em duas fases porque a escolha de imagem exige olho:

```bash
python3 scripts/lote-videos.py preparar --de=1 --ate=10   # minera
python3 scripts/lote-videos.py produzir --de=1 --ate=10   # narra e monta
```

A trilha alterna por índice: metade **Bluebird**, metade **Documentary**.

Cada carrossel precisa de um `cenas/buscas.json` com um termo de busca por
bloco do ensaio — sem ele a imagem vira ilustração genérica. É o único passo
que não se automatiza.

## Tempos medidos (19/09/26)

| Etapa | Medido |
|---|---|
| Minerar um termo | 17s |
| Narrar uma cena | 2s |
| Renderizar uma cena no Remotion | 8s |
| Montagem final (3 passes ffmpeg) | 26s |

Máquina: **~4 min por vídeo**. Com a escrita dos termos e a escolha das
imagens: **7 a 9 min por vídeo**. Os 57 dão 7 a 8 horas, em lotes de 10
(~1h15 cada).

## Verificação obrigatória — nenhum vídeo sai sem isso

Regra do Julio (19/09/26): *"tenha certeza que para cada vídeo gerado ele
será verificado todas as imagens se faz sentido com o texto e se no fim o
áudio fora montado correto, ou seja há fala e fundo musical e todo ele."*

`scripts/verificar-video.py <pasta> --sufixo=-inf` roda sozinho no fim de
`lote-videos.py produzir`, e reprova o vídeo em vez de dá-lo por pronto.

**Áudio (automático).** Quatro medidas no arquivo final:

1. o mp4 tem faixa de áudio;
2. a duração bate com o plano (soma das cenas menos a sobreposição);
3. nenhum silêncio de meio segundo em ponto nenhum;
4. **a trilha corre do início ao fim**, por cancelamento: remonta a
   narração sozinha a partir do plano, inverte a fase e soma ao `_mix.wav`.
   A fala se cancela e sobra a música. Onde ela está, o resíduo fica em
   **-23 dB**; onde morreu, **-91 dB**. Margem de 69 dB, sem ambiguidade.

O vídeo é localizado pelo título do próprio carrossel, nunca pelo mp4 mais
recente da pasta — senão o verificador aprova o áudio de outro vídeo.

**Imagem x texto (olho humano).** Renderiza `_conferencia.png`: cada cena
ao lado da frase falada nela. Isso não se automatiza — é olhar e dizer se
a imagem tem a ver com o texto. Se a folha não renderizar, o vídeo é
REPROVADO: sem ela ninguém conferiu nada.

### Métodos que testei e NÃO servem para provar a trilha

| Método | Por que falha |
|---|---|
| `silencedetect` no mp4 | a fala cobre a ausência de música; aprova vídeo mudo |
| volume médio nas pausas entre falas | com sobreposição de 1,0s não existe pausa |
| energia de grave (lowpass 60 Hz) contra a mediana | a música tem passagens quietas: 5 falsos positivos num vídeo bom |
| grave contra a mediana das janelas | se a trilha morre cedo, a maioria quebrada vira a referência |

Os dois primeiros **aprovaram um vídeo quebrado de propósito**. Todo
detector novo tem que ser testado contra um vídeo com a trilha morta aos
6s antes de entrar aqui.

## CSV: modo vídeo (YouTube Shorts e TikTok)

`montar-csv-ghl.py --modo=video` preenche, além do comum:

| Coluna | Valor | Por quê |
|---|---|---|
| 6 `videoUrls` | mp4 no ngrok | no modo vídeo não vai imagem nenhuma |
| 13/14 `type` | `reel` | Facebook e Instagram |
| 27 YouTube `title` | título do carrossel, até 100 caracteres | **sem título o post é recusado** |
| 28 YouTube `privacyLevel` | `public` | |
| 29 YouTube `type` | `short` | **sempre curto**: sem isso o vertical entra como vídeo comum e não cai no feed de Shorts |
| 30 TikTok `privacyLevel` | `everyone` | |
| 31 TikTok `promoteOtherBrand` | `FALSE` | não promovemos marca de terceiro |
| 32 TikTok `enableComment` | `TRUE` | o CTA pede comentário; sem isso ele não funciona |
| 33 TikTok `enableDuet` | `TRUE` | alcance de graça; o conteúdo é educativo |
| 34 TikTok `enableStitch` | `TRUE` | idem |
| 35 TikTok `videoDisclosure` | `TRUE` | ver abaixo |
| 36 TikTok `promoteYourBrand` | `TRUE` | ver abaixo |

**Divulgação no TikTok** (decidido por Julio, 19/09/26): os vídeos saem
declarados como conteúdo promocional da própria Multiplic. O TikTok exibe
a etiqueta "Conteúdo promocional". É o que a política pede de quem promove
o próprio negócio — e é isso que os vídeos fazem, inclusive recrutando
parceiros. Declarar errado é risco de derrubada do vídeo.
`--divulgacao=nao` desliga, se um dia for o caso.

As sete colunas do TikTok vão **sempre preenchidas**. O modelo oficial do
GHL preenche as sete; deixar em branco é apostar num padrão que ninguém
documentou.

Os CSVs de vídeo gerados antes de 19/09/26 saíram com as colunas 27-29
vazias. Conferir antes de importar.

## Paralelismo: o teto é a API, não o processador

Regra do Julio (19/09/26): *"minere as paginas em serie para n expire, o
limite dela não é o core é o limite que as paginas aguentam via API."*

**Mineração é sempre em série**, mesmo com vários processos rodando. Há uma
trava de arquivo (`.mineracao.lock`, `flock` exclusivo) em `lote-videos.py`:
se dois processos tentarem minerar, o segundo espera a vez. Combinado
quebra; trava não.

Medido em 19/09/26 com 3 termos:

| | tempo | resultado |
|---|---|---|
| série | 21,0s | 6, 5 e 6 imagens |
| paralelo | 4,4s | **429 do Openverse**, uma cena com 3 imagens |

5x mais rápido e com menos imagem. Velocidade que custa imagem não é ganho.

**O que pode correr junto**, porque não toca as fontes de imagem:

| Etapa | Paralelizável? | Por quê |
|---|---|---|
| Minerar | **NÃO** | cota horária do Wikimedia/Unsplash/Openverse |
| Narrar (ElevenLabs) | com cuidado | cota é de caracteres, mas há teto de concorrência no plano Creator |
| Render Remotion | pouco | já usa vários núcleos sozinho |
| Montagem ffmpeg | pouco | idem |
| Verificação | sim | é só ffmpeg medindo |

A máquina tem 10 núcleos, e uma rodada sozinha já deixa a carga em 4. Abrir
três esteiras não triplica nada: só faz as etapas de CPU brigarem entre si
enquanto a mineração, que é o gargalo real, continua em fila.
