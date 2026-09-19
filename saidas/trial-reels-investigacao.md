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

## RESOLVIDO — a rota existe

**O parâmetro é `trial_params`**, enviado na criação do container de mídia
(`POST /<IG_USER_ID>/media`), junto com `media_type=REELS` e `video_url`.

Campo interno: `graduation_strategy`, com dois valores possíveis:

| Valor | O que faz |
|---|---|
| `MANUAL` | fica trial até alguém graduar no app |
| `SS_PERFORMANCE` | o Instagram gradua sozinho se performar bem |

**Usar `SS_PERFORMANCE`**: sobe como trial, e o que for bem chega aos
seguidores automaticamente. Zero trabalho manual, que é o requisito do Julio.

Ressalva registrada: a página oficial `IG User Media` **não lista** esse
parâmetro (a lista alfabética pula de `share_to_feed` para `thumb_offset`).
Mas três implementações independentes o documentam e usam. Existe; a
documentação da Meta é que está incompleta. Confirmar no primeiro teste real.

Graduar um trial já publicado **não** é exposto pela API — só no app. Por isso
`SS_PERFORMANCE` importa: é a única graduação que acontece sem ninguém.

---

## Diário

### 19/09/26 — abertura
Mapeamento acima consolidado a partir da conversa. Investigação da API ainda
não começou; é o próximo passo.

### 19/09/26 — a rota encontrada

`trial_params` confirmado por três fontes independentes. A automação é
possível, sem ferramenta paga.

**O que falta, e não é técnico:** acesso. Gerar o token exige autenticar numa
conta com cargo na Página do Facebook e no Instagram da Multiplic.

O Julio **não precisa** do código de verificação da dona da conta — isso seria
entrar como ela. O certo é a Izabel adicioná-lo como administrador em
`business.facebook.com` → Configurações → Pessoas, uma vez. Depois ele
autentica com o próprio login e nunca mais depende do celular dela.

Nota: isso já foi feito uma vez — o GHL publica no Instagram da Multiplic hoje,
então alguém já completou esse OAuth.

**Pendência que pode derrubar tudo:** trial reel exige 1.000+ seguidores na
conta. Ainda não verificado para a @izabelmultiplic. Sem isso, nem
`trial_params` nem ferramenta nenhuma funciona.

**Próximo passo:** com o cargo concedido, escrever `scripts/publicar-trial.py`
— cria o container com `trial_params`, aponta para o mp4 servido pelo ngrok,
publica. Não executar nada sem o Julio autorizar.
