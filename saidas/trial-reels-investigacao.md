# Trial Reels automatizados — investigação

**Objetivo:** publicar 57 reels verticais como Trial Reel na @izabelmultiplic,
sem trabalho manual. Julio foi categórico: **manual não é opção.**

Atualizado por uma rotina de hora em hora. Cada rodada acrescenta; nada
aqui se reinvestiga.

---

## FECHADO — não reinvestigar

| O quê | Veredito | Evidência |
|---|---|---|
| instagram.com no desktop | **Não tem** controle de Trial | Confirmado 19/09/26 |
| Menu Criar da web | Só Publicação, Vídeo ao vivo, Anúncio — sem Reel | Visto na interface |
| App Edits | Só celular, sem versão desktop | Documentação |
| GHL | Sem trial e sem rascunho | As 40 colunas do CSV avançado não têm nenhum dos dois |
| Rascunho como contorno | Rascunho do Instagram é local do aparelho | Nada externo escreve lá |
| Rascunho na API | **Não existe** | A doc oficial de Content Publishing não contém a palavra "draft" |
| Converter reel publicado em trial | Impossível | Trial é definido na criação, não é estado que se liga depois |
| Arquivar e restaurar | Volta como reel normal | — |
| Duplicar e marcar como trial | Instagram não tem "duplicar"; e duplicata sofre penalidade de alcance | — |
| Automação de navegador | **Inaceitável** | É o padrão que o Meta de fato pune, ao contrário de publicar por API |
| Pilotar o celular daqui | Impossível | As ferramentas de simulador não controlam aparelho físico, e o Simulador não roda apps da App Store |

## Conhecido e disponível

- **Metricool** suporta `Instagram Post Type = TRIAL_REEL` em importação CSV,
  junto com `First Comment Text`, YouTube Shorts e TikTok. Resolve tudo, mas é pago.
- Trial reel exige **conta profissional com 1.000+ seguidores** e o Instagram
  ter liberado o recurso no perfil. **Ainda não verificado para a @izabelmultiplic
  — se não bater, nada disso funciona, em ferramenta nenhuma.**

## A pista principal

O Metricool publica trial reel **via API**. Logo a Instagram Graph API expõe o
recurso. Se for verdade, dá pra escrever um publicador próprio com um app Meta
do Julio: automatizado, sem mensalidade, pela rota sancionada.

Falta descobrir: qual o parâmetro exato na criação do container, quais
permissões, se exige App Review, e se é limitado a parceiros aprovados.

---

## Diário

### 19/09/26 — abertura
Mapeamento acima consolidado a partir da conversa. Investigação da API ainda
não começou; é o próximo passo.
