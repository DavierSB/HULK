## PLY is Awesome

Bueno aqui hay un lexer que reconoce y tokeniza correctamente (o eso creo) todos los pedazos de codigo que aparecen en la orientacion del proyecto, de manera que esta listo para servir como lexer al menos en las etapas iniciales de nuestro trabajo.

Para probarlo corran el archivo prueba.py.

La prueba es tokenizar el codigo que aparezca en el archivo prueba_short.txt
En el archivo prueba_long.txt aparecen todos y cada uno de los fragmentos de codigo que aparecian en la orden del proyecto. Para elevar la complejidad de las pruebas que le realicen a este lexer y asi debuggearlo bien, copien desde prueba_long.py a prueba_short.py los pedazos de codigo con los que quieran armar la prueba.

En esencia PLY crea un compilador basandose en los parametros que le pasemos, tales parametros los defino en el archivo ply_lexer_specification.py

En tal archivo aparecen varios diccionarios con nombre de clases de tokens como llave y las expresiones regulares que matchean como valor.


## Why?
Se que quedamos en no usar PLY. Hice este lexer porque asi podemos continuar a las siguientes etapas del proyecto, sin estancarnos, y con la seguridad de que si pasa lo peor tenemos un lexer que hace todo lo que tiene q hacer


## El lexer manual como seria
La idea, es crear algo similar a PLY.lex .  PLY.lex es una clase que, al ser provista de los parametros correctos, crea el lexer que usted quiera, o sea, es un lexer generico.

La idea para nuestro lexer debe ser esa, crear un lexer generico.

Para ello, hay que trabajar duro con Automatas como se puede ver en el libro en ingles que subio Chave; pero es hacible (supongo), ya valoraremos si vale la pena el esfuerzo o no.

Por lo pronto, tenemos Lexer.