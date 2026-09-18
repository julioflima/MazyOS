# Referência de estilo de carrossel — formato "thread/tweet screenshot"

> Referência trazida pelo usuário: carrossel do @brunobarbosz sobre o "Fio B".
> Nota: as imagens originais não puderam ser salvas em disco (chegaram coladas
> no chat, sem arquivo acessível) — este arquivo documenta a especificação
> visual e de copy pra reproduzir o mesmo estilo com a identidade da Multiplic.
> Adaptar sempre usando a paleta azul + dourado da Multiplic (nunca copiar a
> paleta azul/roxo do Twitter do exemplo — usar o AZUL PETRÓLEO da Multiplic
> como cor de destaque no lugar do azul do "verificado").

## Estrutura (layout tipo "print de tweet/thread")

- **Slide de capa**: imagem de fundo grande (foto real, tema do assunto),
  overlay escuro na parte inferior com gradiente. Avatar redondo pequeno +
  @handle com selo de verificado no canto inferior esquerdo da foto. Abaixo,
  título em caixa alta, fonte bold condensada, 3 linhas curtas. Subtítulo em
  peso regular menor, terminando com seta "→".
- **Slides de conteúdo**: fundo preto sólido. Header fixo no topo: avatar
  redondo + nome + @handle + selo de verificado. Corpo em texto branco,
  parágrafos curtos (1–3 linhas), bastante espaço em branco entre blocos.
  Pontuação de efeito: frases isoladas em linha própria pra dar ritmo
  ("Eu assisti tudo.", "É a minha.").
- **Negrito seletivo**: 1–2 frases-chave em bold por slide pra guiar o olho
  (números, conclusões, virada de argumento).
- **Imagens de apoio**: fotos/prints/memes inseridos no meio do texto quando
  ilustram o ponto (gráfico, meme, foto de contexto) — sempre com cantos
  levemente arredondados.
- **Setas "→"** usadas como bullet informal pra listas curtas.
- **Slide final**: CTA de "Seguir" em formato de botão (pill azul), com frase
  de fechamento forte antes do botão.

## Tom de copy

- Frases curtas, uma ideia por linha.
- Constrói tensão: contexto → dado → contra-argumento → virada → conclusão
  prática.
- Numerado/factual quando reforça autoridade (%, R$, prazos).
- Fecha sempre com aplicação prática ("o que fazer agora") + CTA de ação.
- Emoji pontual no fim de frase pra dar tom (😬 🙇‍♂️ 💡), nunca em excesso.

## Adaptação pra Multiplic

- Trocar avatar/@handle pelo perfil da Multiplic ou de Izabel
  (`identidade/equipe/izabel-perfil.png`).
- Selo de verificado pode ser mantido como elemento gráfico se a conta tiver,
  senão remover.
- Cor de destaque nos **negritos do corpo de texto**: azul claro `#6FB4E8`.
  Histórico: o navy do logo (`#003854`) é escuro demais no preto; o
  `#2D699C` que veio depois também não segurou (Julio, 18/09/26) — fica
  abafado, parece link desbotado. O `#6FB4E8` mantém a família azul da marca
  com contraste real sobre preto (~7:1).
- Cor de destaque no **botão/pill de CTA**: dourado `#BB842E`.
- Selo de verificado: usar o azul oficial do Instagram (`#3897F0` + check
  branco), não a cor da marca — é um elemento reconhecível de plataforma.
- Fundo: **preto puro**, igual à referência — não usar azul petróleo aqui
  (feedback do usuário, 28/08/26). O azul petróleo entra só nos negritos/ícones
  se fizer sentido, mas o fundo do bloco fica sempre preto.
- Última slide da série (CTA) segue o roteiro fixo — ver
  `identidade/referencias/carrossel-estilo-brunobarbosz/cta-influencer.md`.

## Quebra de parágrafo (Julio, 18/09/26)

Parágrafo longo em bloco único cansa e o leitor pula o slide. **Todo slide de
conteúdo tem no mínimo dois parágrafos**, separados por espaço em branco —
nunca um bloco corrido de cinco ou seis linhas.

Isso não contradiz a estrutura de ensaio do Lord: lá o parágrafo também tem
subordinada e fôlego, mas vem sempre em dois ou três blocos curtos por tela,
com respiro entre eles. O ensaio está na sintaxe, não no tamanho do bloco.

No `conteudo.json` cada slide é uma **lista** de parágrafos, e o
`scripts/montar-carrossel.py` renderiza um `<p>` por item.
