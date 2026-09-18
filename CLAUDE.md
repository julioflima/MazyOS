# MazyOS — Sistema operacional do negócio

Sua empresa roda em cima desse arquivo. Aqui ficam as regras de operação
do MazyOS — como o Claude lê o contexto, aprende com correções, mantém
tudo atualizado e cria skills novas conforme a operação evolui.

Esse arquivo é editável. Quando o `/instalar` rodar, ele complementa o
final dessa página com as regras específicas do seu negócio.

---

## Contexto do negócio

No início de toda conversa, ler os seguintes arquivos (quando existirem
e estiverem preenchidos):

1. `_memoria/empresa.md` — quem é o usuário, o que faz, como funciona o negócio
2. `_memoria/preferencias.md` — tom de voz, estilo de escrita, o que evitar
3. `_memoria/estrategia.md` — foco atual, prioridades, prazos

Usar essas informações como base pra qualquer resposta ou decisão. Ao
sugerir prioridades, formatos ou abordagens, considerar o foco atual
descrito em `estrategia.md`.

Pra qualquer tarefa visual (carrossel, post, landing page), consultar
`identidade/design-guide.md` como referência de estilo.

Não é necessário listar o que foi lido nem confirmar a leitura. Apenas
usar o contexto naturalmente.

---

## Fluxo de trabalho

Antes de executar qualquer tarefa, verificar se existe skill relevante
em `.claude/skills/`. Se encontrar, seguir as instruções da skill. Se
não encontrar, executar a tarefa normalmente.

Ao concluir uma tarefa que não tinha skill mas parece repetível (o
usuário provavelmente vai pedir de novo no futuro), perguntar:

> "Isso pode virar uma skill pra próxima vez. Quer que eu crie?"

Não perguntar pra tarefas pontuais ou perguntas simples. Só quando o
padrão de repetição for claro.

---

## Aprender com correções

Quando o usuário corrigir algo, melhorar uma resposta ou dar uma
instrução que parece permanente (frases como "na verdade é assim", "não
faça mais isso", "prefiro assim", "sempre que...", "evita...", "da
próxima vez..."), perguntar:

> "Quer que eu salve isso pra não precisar repetir?"

Se sim, identificar onde faz mais sentido salvar:

- **Sobre o negócio** (clientes, serviços, mercado) → `_memoria/empresa.md`
- **Sobre preferências e estilo** (tom de voz, formato, o que evitar) → `_memoria/preferencias.md`
- **Sobre prioridades e foco** (projetos, metas, prazos) → `_memoria/estrategia.md`
- **Regra de comportamento nessa pasta** → próprio `CLAUDE.md`

Salvar com uma linha nova clara, sem reformatar o arquivo inteiro.
Confirmar mostrando a linha adicionada.

Não perguntar se a correção for óbvia de contexto imediato (ex: "na
verdade o arquivo se chama X"). Só perguntar quando a informação tiver
valor duradouro.

---

## Manter contexto atualizado

Ao terminar uma tarefa que mudou algo relevante (cliente novo, skill
nova, mudança de foco, processo novo, ferramenta instalada, estrutura
alterada), perguntar:

> "Isso mudou algo no teu contexto. Quer que eu atualize a memória?"

Se sim, identificar o que atualizar:

- **Cliente, serviço, ferramenta, equipe** → `_memoria/empresa.md`
- **Mudança de prioridade ou foco** → `_memoria/estrategia.md`
- **Tom ou estilo** → `_memoria/preferencias.md`
- **Pasta, regra de organização, skill criada** → `CLAUDE.md`
- **Visual (cores, fontes, logo)** → `identidade/design-guide.md`

Mostrar o que vai mudar antes de salvar. Não reformatar o arquivo
inteiro, só adicionar ou editar a linha relevante.

**Quando NÃO perguntar:**
- Tarefas pontuais sem impacto no contexto (escrever um email avulso, criar um post)
- Perguntas simples ou conversas sem ação
- Mudanças já salvas pelo bloco "Aprender com correções"

**Dica:** rode `/atualizar` pra uma varredura completa quando houver dúvida.

---

## Criação de skills

Quando o usuário pedir skill nova:

1. Verificar se existe template relevante em `templates/skills/`. Se
   existir, usar como base e adaptar pro contexto
2. Perguntar se é específica desse projeto ou útil em qualquer:
   - Específica → `.claude/skills/nome-da-skill/SKILL.md` (local)
   - Universal → `~/.claude/skills/nome-da-skill/SKILL.md` (global)
3. Ler `_memoria/empresa.md` e `_memoria/preferencias.md` pra calibrar
   o conteúdo da skill ao contexto do negócio
4. Se a skill precisar de arquivos de apoio (templates, exemplos),
   criar dentro da pasta da skill
5. Seguir o fluxo da skill-creator nativa do Claude Code

---

# Multiplic — MazyOS

> Perfil: criador solo / negócio pequeno. A operação gira em torno de
> conteúdo pra atrair influenciadores parceiros e gerar leads de
> consórcio.

## O que é esse workspace

Operação de conteúdo e negócio da Multiplic — corretora de seguros
focada em consórcios. Aqui se produz o conteúdo que atrai clientes
diretos e, principalmente, influenciadores parceiros pro modelo de
indicação via cupom.

**Estrutura de pastas:**
- `_memoria/` — quem é a Multiplic, como fala, o que tá em foco
- `identidade/` — cores, fontes, logo, pattern da marca
- `marketing/` — conteúdo, SEO, campanhas (saída das skills)
- `saidas/` — análises, emails, documentos pontuais
- `tarefas.md` — o que tá em jogo agora

## Quem é

Multiplic — corretora de seguros focada na venda de consórcios de todos
os tipos (imóvel, veículo, sala comercial, etc.). Equipe: Izabel (CEO),
Isadora (Backoffice), Julio (Engenheiro), + 3 parceiros indiretos.

## O que produz

- Carrosséis educativos sobre consórcio pro Instagram
- Conteúdo em formato stories pra academia de formação de influencers
- Atendimento e fechamento direto de consórcio com clientes finais

## Modelo de negócio em construção

A Multiplic quer virar uma plataforma: influenciadores indicam clientes
via cupom e ganham por indicação. Em troca, recebem formação (academia
em formato de stories) sobre como vender consórcio. A Multiplic dá o
treinamento e fecha o negócio com o cliente por trás.

## Tom de voz

Direto, próximo, didático — fala como quem explica pro vizinho. Usa
pergunta retórica pra abrir ("E se eu te disser que..."), reforça a
ideia central de formas diferentes, sempre fecha com CTA claro (marcar
reunião, comentar, chamar no direct). Ver `_memoria/preferencias.md`
pra detalhes e exemplo real.

Evitar: "caro cliente", jargão de guru, formalidade de corporação.

## Posicionamento

Consórcio não é sobre ter o dinheiro todo — é sobre começar a se
organizar agora pro objetivo (imóvel, casa, sala comercial). A Multiplic
existe pra mostrar esse caminho e, cada vez mais, pra dar a
influenciadores parceiros uma forma real de monetizar indicando.

## Regras do sistema

- Conteúdo novo (carrossel, post) salvar em `marketing/conteudo/<tipo>-<tema>-<data>/`
- Toda peça visual usa a paleta e o logo de `identidade/design-guide.md`
- Prioridade atual: carrossel educativo com foco em atrair influenciadores (ver `_memoria/estrategia.md`)

## Ferramentas conectadas

- [ ] Instagram / Meta Ads
- [ ] Google Ads
- [ ] Projeto `multiplic-consorcios` (Next.js) — `/Users/juliolima/projects/multiplic-consorcios`

*(Marcar conforme for instalando os MCPs)*
