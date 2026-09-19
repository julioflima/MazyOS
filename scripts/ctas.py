"""
Blocos de CTA da Multiplic — fonte única da verdade.
Usado por montar-carrossel.py (slides) e produzir-carrossel.py (legenda).
Texto fechado e validado: ver identidade/referencias/.../cta-tipos.md
"""

CTAS = {
 'cta-sonho': {
   'rotulo': 'SONHO',
   'publico': 'cliente final, rede da Izabel',
   'convite': ['<p class="solo">Gostou? Fez sentido?</p>',
     '<p>Então imagina a chave na sua mão, sem um centavo de juro no caminho.</p>',
     '<p><b>O que trava a maioria não é falta de dinheiro. É não saber como funciona.</b></p>'],
   'fecho': ['<p>Se quiser entender, comente essa palavra abaixo:</p>',
     '<div class="palavra">SONHO</div>',
     '<p>Eu te mando o material que explica tudo, do começo ao fim, de graça.</p>',
     '<p>MUDE a história de endividamento da sua família.</p>'],
   'legenda': ('Gostou? Fez sentido?\n\n'
     'Então imagina a chave na sua mão, sem um centavo de juro no caminho. O que trava a '
     'maioria não é falta de dinheiro. É não saber como funciona.\n\n'
     'Se quiser entender, comente **SONHO** abaixo. Eu te mando o material que '
     'explica tudo, do começo ao fim, de graça.\n\n'
     'MUDE a história de endividamento da sua família.'),
   'cta_curto': 'Comente SONHO aqui e eu te mando o material que explica tudo, de graça.',
   'hashtags': ['#consorcio','#casapropria','#planejamentofinanceiro','#educacaofinanceira',
     '#consorcioimobiliario','#sairdoaluguel','#primeiroimovel','#organizacaofinanceira',
     '#patrimonio','#cartadecredito','#multiplic','#fortaleza'],
 },
 'cta-influencer': {
   'rotulo': 'INFLUENCER',
   'publico': 'criadores de conteúdo, distribuição',
   'convite': ['<p class="solo">Gostou? Fez sentido?</p>',
     '<p>Imagina ser parceiro de uma empresa que tira famílias do juro e as coloca dentro da própria casa.</p>',
     '<p><b>Você apresenta a possibilidade. Eu conduzo o resto.</b></p>'],
   'fecho': ['<p>Se te tocou, comente essa palavra abaixo:</p>',
     '<div class="palavra">INFLUENCER</div>',
     '<p>Vinte minutos comigo e você entende tudo. Entender de consórcio é comigo.</p>',
     '<p>MUDE a história de endividamento do seu país.</p>'],
   'legenda': ('Gostou? Fez sentido?\n\n'
     'Imagina ser parceiro de uma empresa que tira famílias do juro e as coloca dentro da '
     'própria casa. Você apresenta a possibilidade. Eu conduzo o resto.\n\n'
     'Se te tocou, comente **INFLUENCER** abaixo. Vinte minutos comigo e você '
     'entende tudo — entender de consórcio é comigo.\n\n'
     'MUDE a história de endividamento do seu país.'),
   'cta_curto': 'Comente INFLUENCER aqui e a gente marca vinte minutos pra conversar.',
   'hashtags': ['#consorcio','#parceria','#criadordeconteudo','#rendaextra','#monetizacao',
     '#influencerdigital','#educacaofinanceira','#creatoreconomy','#empreendedorismo',
     '#indicacao','#multiplic','#fortaleza'],
 },
}

# Variante enxuta do CTA do influencer, usada em ~25% dos carrosséis para dar
# ritmo ao feed (Julio, 18/09/26). Mesmo nome de pasta — o que muda é só o
# texto. Selecionada pelo campo "cta_curto": true no conteudo.json.
CTA_CURTO = {
 'cta-sonho': {
   'convite': ['<p class="solo">Gostou? Fez sentido?</p>',
     '<p><b>Então imagina começar hoje.</b></p>'],
   'fecho': ['<p>Comente essa palavra abaixo:</p>',
     '<div class="palavra">SONHO</div>',
     '<p>MUDE a história de endividamento da sua família.</p>'],
   'legenda': ('Gostou? Fez sentido?\n\n'
     'Então imagina começar hoje.\n\n'
     'Comente **SONHO** abaixo.\n\n'
     'MUDE a história de endividamento da sua família.'),
 },
 'cta-influencer': {
   'convite': ['<p class="solo">Gostou? Fez sentido?</p>',
     '<p><b>Então imagina fazer isso pela sua audiência.</b></p>'],
   'fecho': ['<p>Comente essa palavra abaixo:</p>',
     '<div class="palavra">INFLUENCER</div>',
     '<p>MUDE a história de endividamento do seu país.</p>'],
   'legenda': ('Gostou? Fez sentido?\n\n'
     'Então imagina fazer isso pela sua audiência.\n\n'
     'Comente **INFLUENCER** abaixo.\n\n'
     'MUDE a história de endividamento do seu país.'),
 },
}
