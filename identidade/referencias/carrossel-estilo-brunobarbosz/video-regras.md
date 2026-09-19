# Vídeo vertical — regras base

> Valem para **todos** os vídeos de carrossel. Definidas por Julio em 18/09/26
> durante a construção da primeira amostra.

## Ritmo e transição

- **A fala nunca atropela a transição.** Cada cena tem silêncio antes da
  narração (o slide termina de entrar) e depois dela (a fala acaba antes de o
  slide começar a sair). Hoje esse respiro é de **0,9s de cada lado**.
- **Transição de 0,9s**, deslizando para o lado (`slideleft`), imitando alguém
  arrastando um carrossel. 0,55s ficou apressado.
- Duração de cada cena = respiro + áudio + respiro. A sincronia entre fala e
  slide sai disso, sem alinhamento manual.

## Narração

- **Literal.** A narração lê exatamente o que está escrito no slide. Versão
  falada reduzida foi testada e reprovada: o que se lê tem que ser o que se
  ouve.
- Gerada direto de `conteudo.json` + `ctas.py`, sem roteiro intermediário.
- Voz: `lWq4KDY8znfkV0DrK8Vb` (ElevenLabs), escolhida entre quatro testadas.
  Modelo `eleven_multilingual_v2`.
- A capa é narrada com **título + subtítulo**.

## Movimento

- **Nada de zoom nos slides de texto.** Foi testado e reprovado: denuncia foto
  parada fingindo movimento e arrisca cortar as bordas do texto.
- **Zoom só na capa**, onde a foto sangra nos 9:16 e não há texto dentro dela.

## Capa (Remotion)

Única parte animada em Remotion; o resto são os PNGs do carrossel deslizando.

- Foto preenchendo 1080x1920 (resolve a tarja preta do 4:5 encaixado)
- Zoom lento e contínuo ao longo da cena
- Título subindo linha a linha, com mola e atraso entre elas
- Subtítulo entrando depois que o título assenta
- Logo fixo no topo

Projeto em `video-capa/`.

## Saída

- 1080x1920, 30fps, H.264 + AAC
- Salvo em `~/Documents/media/multiplic/consorcios/`
- Nome: `vd-<titulo-do-carrossel>-<sonho|influencer>.mp4`

## Ponto em aberto

Com narração literal o vídeo passa de **2 minutos**, o que é longo demais para
Reels e Shorts. Decidir entre aceitar o formato longo, encurtar o texto dos
slides, ou escrever um texto próprio para vídeo.

---

# Formato podcast (a partir de 19/09/26)

O carrossel deixou de ser o formato do vídeo. Agora cada cena é uma **imagem
cheia** referente ao que está sendo dito, com o texto entrando como legenda
sobre a foto. O **layout de carrossel aparece só na última cena**, onde a
Izabel assina.

Motivo: TikTok não aceita carrossel e Reels não tem teste para carrossel —
então todo o conteúdo de CTA `INFLUENCER` migra para vídeo.

## Legenda

- O texto **acumula** conforme é falado, até formar o bloco, como nas peças do
  Lord. Legenda palavra a palavra (karaokê) foi testada e reprovada.
- Quebra nos mesmos parágrafos do carrossel.
- 46px, peso 500, sobre gradiente escuro.

## Sobreposição de vozes

**A fala da cena seguinte começa antes de a anterior terminar** — cerca de 1
segundo. Dá urgência e prende a atenção, como alguém falando por cima de
outra pessoa. Julio: *"é uma característica importante ao fazer vídeos
virais"*.

Detalhe técnico: `acrossfade` não serve, porque abaixa a voz que sai e o
efeito desaparece. O áudio é posicionado com `adelay` e somado com `amix`, as
duas vozes em volume cheio.

> Isso substitui a regra anterior de "a fala nunca atropela a transição", que
> valia para o formato de carrossel.

## Ritmo e som

- Narração acelerada em **1,12×**
- Trilha de jazz ao fundo, bem baixa, gerada pelo ElevenLabs (`music_generation`)
- Efeito de digitação na cena final, onde o CTA pede para comentar
  (`sound_generation`)

**Não usar gravação comercial protegida** como "Polka Dots and Moonbeams" do
Tommy Dorsey com Sinatra: o Content ID do Instagram silencia o vídeo inteiro,
narração inclusive, além do risco de uso comercial não licenciado.

## Permissões necessárias no ElevenLabs

`text_to_speech`, `sound_generation`, `music_generation`, `models_read`.
