# Publicação dos carrosséis — GHL (Dara)

> Como os carrosséis saem da pasta e vão pro Instagram.
> Instância: `app.daracrm.ai`, location `VMB8GS9dWC42opXRMV6h` (Multiplic).

## Agendamento (Julio, 18/09/26)

**Um carrossel por dia, todos os dias, às 15h.**

Sem exceção de fim de semana. No CSV isso vira `postAtSpecificTime` no
formato `YYYY-MM-DD 15:00:00`, uma data por linha, avançando um dia a cada
post.

Não agendar tudo de uma vez logo de cara: subir as primeiras semanas, ler o
desempenho e só então encher a fila. Fila cheia é difícil de desmontar.

## Categorias

Criadas em `Configurações do Social Planner → Categorias sociais`:

- **Teste** (laranja) — carrosséis de CTA `INFLUENCER`
- **Produção** (escuro) — carrosséis de CTA `SONHO`

A categoria é só do GHL: colore e filtra o calendário dele e **não vai junto
pro Instagram**.

## Primeiro comentário

Campo `followUpComment` = **sempre a CTA curta**, nunca crédito de foto.
Ver `cta-tipos.md`.

## Carga em massa por CSV

`Planejador Social → Nova publicação → Carregar de CSV → Formato Avançado`.

Colunas que a Multiplic usa (o resto da planilha é GBP/TikTok/YouTube/
Pinterest e fica vazio):

| Coluna | Conteúdo |
|---|---|
| `postAtSpecificTime` | `YYYY-MM-DD 15:00:00` |
| `content` | legenda, já sem o cabeçalho de controle do `legenda.md` |
| `imageUrls` | os 9 slides, **URLs públicas**, separadas por vírgula, na ordem |
| `category` | `Teste` ou `Produção` |
| `tags` | livre |
| `followUpComment` | a CTA curta |
| `type` | `post` |

**`imageUrls` exige URL pública, não arquivo.** São 9 por carrossel. O plano é
hospedar os PNGs no site (`multiplic-consorcios`, Next.js, pasta `public/`) e
derivar a URL do caminho da pasta, o que permite gerar o CSV inteiro por
script.

## Limite do Instagram

A API de publicação da Meta permite **50 posts por conta em 24h**. Publicar em
lote grande falha; agendar em lote é seguro. Já há um post com status
"Falhou" no planejador — vale investigar antes de agendar em volume.

## Pendências

- [ ] URL base do site publicado, pra montar os `imageUrls`
- [ ] Decidir o crédito da capa 52 (`DcrNrtih1c5`), única em CC BY-SA 4.0,
      que exige atribuição por lei — linha na legenda ou trocar a foto
