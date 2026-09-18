# Capa com foto histórica — referência Lord Journal

> Referência trazida por Julio (18/09/26): @lordjournalbr. Todos os carrosséis
> deles abrem com uma fotografia marcante — geralmente de arquivo, editorial,
> com serif branca por cima e o logo pequeno no topo.

## Todo carrossel tem capa com foto (Julio, 18/09/26)

Regra atual: **100% dos carrosséis abrem com capa de foto**, minerada pro tema
daquele carrossel. Não existe mais carrossel que comece direto no slide de
texto preto.

- **Todos** → capa com foto + slides de conteúdo no estilo thread preto
- **~10%** → carrossel inteiro em estilo editorial (foto em todos os slides,
  serif, sem header de tweet) — template ainda **não construído**

> Substitui a divisão anterior de 50/10/40, que previa carrossel sem capa.
> Julio mudou de ideia depois de ver a primeira amostra renderizada.

## De onde vêm as fotos

Nunca das mesmas fontes do Lord (Getty, Magnum, acervo de estúdio): são
imagens licenciadas e a Multiplic é peça comercial, não jornalismo. Risco real
de cobrança.

As fotos vêm do minerador `scripts/minerar-imagens.js`, que consulta só acervo
com uso comercial liberado:

| Fonte | Licença | Chave |
|---|---|---|
| Wikimedia Commons | PD / CC BY / CC BY-SA | não |
| The Met | CC0 | não |
| Openverse | filtrado em `commercial,modification` | não |
| Unsplash | Unsplash License | `UNSPLASH_ACCESS_KEY` |
| Pexels | Pexels License | `PEXELS_API_KEY` |

**Buscar em inglês.** O acervo histórico indexado em português é pequeno —
"1950s family new house front porch" devolve o acervo FSA (Russell Lee,
Dorothea Lange); a mesma busca em português devolve PDF de artigo acadêmico.

O script salva `creditos.json` com licença e autor de cada imagem. Toda foto
usada em publicação precisa ter a linha de crédito guardada ali — CC BY e
CC BY-SA **exigem** atribuição.

## Tratamento da capa

- Foto sangrando nos 1080x1350, `background-size: cover`
- Gradiente de baixo pra cima fechando em preto (~86% da altura) pro texto ler
- Título por cima, alinhado embaixo
- **Sem header de Instagram na capa** (regra de Julio, 18/09/26): nada de
  avatar, nome, @ ou selo de verificado. Isso descaracteriza a peça como
  propaganda da empresa — a capa tem que parecer matéria, não anúncio. O
  header de tweet entra só a partir do slide 02.
- **A palavra "consórcio" não aparece na capa** (regra de Julio, 18/09/26).
  Nem no título nem no subtítulo. Citar o produto na capa entrega a peça como
  propaganda antes de a pessoa ler qualquer coisa. O produto entra a partir do
  slide 02, depois que o assunto já se sustentou sozinho.
- **Logo Multiplic alterna entre topo e rodapé** de um carrossel pro outro.
  O Lord usa sempre no topo; aqui varia pra não virar template óbvio.
  No HTML é uma classe: `<div class="slide capa logo-topo">` põe no topo,
  sem a classe vai pro rodapé.

## A capa tem que inspirar, não entristecer (Julio, 18/09/26)

Feedback recorrente na revisão das 57 primeiras capas: **"fúnebre demais"**,
"não inspira riqueza". Acervo histórico em domínio público puxa muito para o
austero — foto de gente pobre, preto e branco duro, cena de despedida. Fica
bonito e vende o contrário do que a Multiplic promete.

Regra: a capa tem que soar **aspiracional**. Prosperidade, conquista,
tranquilidade, casa boa, família bem. O tratamento continua editorial e
escuro; o que muda é o assunto da foto.

Consequência prática: para temas de patrimônio, aposentadoria e herança,
preferir foto moderna bem produzida (Unsplash/Pexels) em vez de acervo
histórico. O histórico funciona bem para tema de grupo, tempo e trabalho —
não para tema de riqueza.

### Vocabulário de imagem que o Julio já pediu

- disciplina → **esporte** (treino, atleta, rotina)
- dois caminhos → **bifurcação de estrada**, não duas portas
- juro escondido → **mão entregando dinheiro** para outra
- herança / aposentadoria → riqueza tranquila, nunca velhice triste

## A foto tem que falar do título (regra dura)

Julio, 18/09/26, depois de reprovar 15 das 22 primeiras capas: **a imagem
precisa ter relação direta com o título.** Se o título cita um objeto
concreto, esse objeto aparece na foto — "Do carro à alavancagem" sem carro
na imagem não passa.

Por isso o `produzir-carrossel.py` **não escolhe mais capa sozinho**. O campo
`capa` no `conteudo.json` é obrigatório, e só se preenche depois de olhar as
candidatas em `candidatas/index.html`. O script também recusa uma foto que já
seja capa de outro carrossel — três capas tinham saído com a mesma imagem.

Ordem correta do trabalho:
1. escrever o texto
2. decidir **que imagem esse texto pede**
3. montar o termo de busca a partir dessa decisão
4. minerar, **olhar** as candidatas
5. escolher e só então gerar

## Foto de arquivo, não foto de banco (Julio, 18/09/26)

Dois feedbacks que se somam e definem a busca:

- **"muito comercial, saindo do tom chic da Lord"** — foto de banco com modelo
  posado, sorriso de catálogo e terno de figurino está proibida.
- **"gosto do nível de antigo; está realista demais, parece IA"** — foto
  moderna, nítida e limpa demais lê como imagem gerada. A textura analógica
  (grão, luz de época, cor desbotada) é parte do que faz parecer editorial.

Ordem de preferência das fontes, então, inverte o que estava valendo:

1. **Wikimedia Commons** e coleções de arquivo no Unsplash (NYPL, Royal Danish
   Library) — foto histórica real
2. **Openverse** filtrado em uso comercial
3. **Pexels** só quando o tema não existir em acervo (celular, app, carro novo)

O desafio é casar isso com a regra de não ser fúnebre: arquivo **aspiracional**
— festa, viagem, carro de época, casa boa, gente bem vestida, esporte — e não
arquivo de pobreza e despedida.

## O tratamento varia de peça pra peça (Julio, 18/09/26)

"O filtro vintage não pode estar em tudo, senão fica óbvio programado."

O feed do Lord alterna P&B de arquivo, cor quente de cinema, foto moderna crua
e card de citação em fundo creme. Nenhum filtro único aplicado a tudo.

No `conteudo.json` o campo `tratamento` aceita:

| valor | quando usar |
|---|---|
| `nenhum` | foto já tem cor boa e textura própria |
| `leve` | padrão; tira o excesso de nitidez sem descaracterizar |
| `forte` | foto moderna demais que precisa de época |
| `pb` | retrato, cena documental, qualquer imagem que ganhe em preto e branco |

Regra de grade: **não repetir o mesmo tratamento em peças vizinhas** no
calendário de publicação.
