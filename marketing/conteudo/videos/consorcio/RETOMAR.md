# Onde paramos — revisão das capas (18/09/26)

## Estado

57 temas de consórcio, 114 carrosséis (2 CTAs cada), 914 PNGs, 114 legendas.
Tudo gerado e renderizado. O que está em aberto é **só a escolha das fotos de capa**.

Placar da revisão: ver `revisao-capas.json` (cada id tem o veredito e o motivo).

## O que já está decidido e implementado

- **Tipografia da capa:** Lora serifada, caixa baixa, frase corrida. Caixa alta
  em peso 900 lia como propaganda — trocada.
- **Gradiente:** começa aos 42% da altura, a foto respira.
- **Filtro:** campo `tratamento` no `conteudo.json` (`nenhum` / `leve` / `forte`
  / `pb`), escolhido **por carrossel**. Filtro igual em tudo se entrega como
  template.
- **Capa não cita "consórcio"** e não leva header de Instagram.
- **Logo alterna** topo e rodapé.
- **Script não escolhe capa sozinho** e recusa foto repetida.

## O problema que sobrou

O acervo disponível é fraco pro que a gente quer. Pexels é banco comercial
(modelo posado, "parece IA"); Wikimedia e Unsplash têm arquivo bom mas
respondem pouco a termo moderno, e bloqueiam por limite quando se minera muito
seguido.

Direção do Julio, acumulada: foto de **arquivo**, aspiracional (nunca fúnebre),
com relação direta com o título, e o objeto do título presente na imagem.

## Próximo passo sugerido

1. Terminar de julgar as capas (faltam ~36)
2. Reminerar as reprovadas com fonte de arquivo na frente
3. Distribuir os `tratamento` pelas 57 com critério, sem repetir vizinhos
4. Decidir se entra itálico nos títulos (sotaque editorial do Lord)

## Pendências antigas

- O que é o "material" gratuito prometido no CTA SONHO
- Anel de story no avatar: sim ou não
- Nada foi commitado ainda
