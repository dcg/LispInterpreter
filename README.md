

LispInterpreter
===============


## Quick Start

* Das Projekt ben�tigt Python 2.7 http://www.python.org/download/releases/2.7.3/

* Das Projekt ben�tigt Tkinter http://tkinter.unpythonic.net/wiki/FrontPage?action=show&redirect=StartSeite

* Der Interpreter muss aus dem Ordner `src` per `python start.py` gestartet werden

* Dr�cke den Button `Load greater GUI` und `Eval`




## Projektaufbau

* Alle Quellcodes des Interpreters befinden sich im Verzeichnis `src`
	* Der Code des Interpreters ist unter `src/LISP` zu finden
	* W�hrend Code, der einzig zur Anwendung des Interpreters ben�tigt wird (z.B. Dateien laden und lesen), unter `src/IDE` zu finden ist

* Alle Testf�lle (PyUnit) befinden sich im Verzeichnis `test/LISP`

* Performance-Tests sind unter `test/OTHER` zu finden

## Der Interpreter

Zuerst sei angemerkt, dass dieser keiner Sprachdefinition folgt und wohl mit keinem vorhandenen LISP-System kompatibel ist. Die Motivation hinter diesem Interpreter ist einzig und allein autodidaktischer Natur.

Nichtsdestotrotz ist er an Lisp angelehnt und besitzt dessen typische Features wie Closures und Lambdas.

### Build-in-Functions
Da die meisten Funktionen direkt an Scheme angelehnt sind, wird nicht mehr genau auf sie eingegangen und nur anhand eines kurzen Beispiels ihre Funktion gezeigt. Funktionen, die so nicht in Scheme vorkommen, werden im folgenden Abschnitt genauer erl�utert.

+

	(+ 3 4) -> 9

-

	(- 3 4) -> -1

define

	(define foo 5) -> 5

if

	(if TRUE 5 6) -> 5
	(if FALSE 5 6) -> 6

eq?

	(eq? 5 5) -> TRUE

\>?

	(>? 4 3) -> TRUE

&lt;?

	(<? 4 3) -> FALSE

lambda

	(lambda (x) (+ 3 x)) -> (lambda (x) (+ 3 x))

begin

	(begin
		(+ 3 4)
		(+ 2 1))  -> 3

set!

	(set! foo 3) -> ()

quote

	('foo) -> foo
	(quote (3 4)) -> (3 4)

write

	(write (+ 3 4)) -> prints `7` to console
	(write "foobar") -> prints `foobar` to console

print

	(print (+ 3 4)) -> prints `7` to console
	(print "foobar") -> prints `"foobar"` to console

getParam

	(getParam N) returns N'th parameter inside a function 
	
	does not work in bytecode!

getLocal

	(getLocal N) returns N'th local variable 
	does not work in bytecode!

getSuperParam

	(getSuperParam N M) returns N'th parameter from M'th super-environment
	does not work in bytecode!

getSuperLocal

	(getSuperLocal N M) returns N'th local variable from M'th super-environment
	does not work in bytecode!

getGlobal

	(getGlobal N) returns N'th global variable
	does not work in bytecode!

eval

	(eval "(+ 3 4)") -> 7

str_concat

	(str_concat "foo" "bar") -> "foobar"

load

	(load "some_file.txt") -> content of some_file.txt

save

	(save "some_file.txt" "foobar") -> writes foobar to some_file.txt

type

	(type 5) -> LispInteger
	(type "foo") -> LispString
	(type 'lambda) -> LispSymbol

	(type +) -> Plus
	(type lambda) -> lambda
	(type (lambda x x)) -> UserFunction

call

	(call func 5) -> executes (func 5)
	works only in bytecode and is a quirk for `compile on define`. See bytecode section for more information

label$

	Tkinter LabelWidget

tk$

	TKinter RootPanel

	
text$

	Tkinter TextWidget

button$

	Tkinter ButtonWidget

frame$

	Tkinter FrameWidget

toplevel$

	Tkinter TopLevel Dialog

scrollbar$

	Tkinter Scrollbars
  

### First level of optimization (Opt-Code)

Im Zuge einer ersten Performanceoptimierung wurde der geparste Lisp-Code in eine optimalere Darstellung �berf�hrt. Diese wird im Folgenden als "Opt-Code" bezeichnet. So wurden die Methoden getParamm, getLocal, getSuperParam, getSuperLocal, getGlobal eingef�hrt, um jeden Zugriff auf ein Symbol zu ersetzen. Damit muss die Suche nach dem Symbol im Environment nicht mehr zur Ausf�hrungszeit get�tigt werden, sondern kann bereits bei der Definition einer Funktion erfolgen. Da es sich hierbei eigentlich um eine interne Optimierung des Interpreters handelt, wurden aus Gr�nden der Performance einige weitere Annahmen getroffen, die man bedenken muss, wenn man diese Funktionen direkt benutzen m�chte. 

So werden die Argumente der Funktion nicht evaluiert. Und Eval �berpr�ft gezielt, ob es sich bei einem LispCons um einen der oben erw�hnten Funktionsaufrufe handelt und gibt dann den Wert des entsprechenden Environments zur�ck. Da dadurch einige Iterationen durch Eval gespart werden, f�hrte dies ebenfalls zu einem sp�rbaren Performance-Plus, hat aber nat�rlich den Nachteil der Flexibilit�t, wenn man diese Funktionen direkt im Lisp-Code verwenden m�chte:

	###perfomance shortcuts####
    if lisp.first is getLocalSym:
        return getLocal.execute(env,lisp.rest.first)
    if lisp.first is getParamSym:
        return getParam.execute(env,lisp.rest.first)
    if lisp.first is getGlobalSym:
        return getGlobal.execute(env,lisp.rest.first)
    if lisp.first is GetSuperParam:
        return getSuperParam.execute(env,lisp.rest.first,lisp.rest.rest.first)
    if lisp.first is GetSuperLocal:
        return getSuperLocal.execute(env,lisp.rest.first,lisp.rest.rest.first)
    ### end of perfomance shortcuts###

M�chte man den Opt-Code einer Funktion sehen, kann man dieser das Symbol '++op++ senden

	 eval_input		      -> (lambda (x) (tf_output (quote setText) (eval (tf_input (quote getText)))))
	(eval_input '++op++)  -> ((getGlobal 32) ((getGlobal 10) setText) ((getGlobal 25) ((getGlobal 31) ((getGlobal 10) getText))))



### Bytecode

Als zweite Optimierungsstufe werden Funktionen zum Definitionszeitpunkt in ByteCode �bersetzt. Aus Verst�ndlichkeitsgr�nden wurde der Bytecode dabei in seiner textuellen Darstellung gelassen und nicht mehr weiter in Bytes �bersetzt.

Der Befehlssatz des Bytecodes wurde dabei bewusst auf dem absoluten Minimum gehalten:

	PUSH-CONSTANT
	PUSH-GLOBAL
	PUSH-LOCAL
	PUSH-PARAM
	PUSH-SUPER-PARAM
	PUSH-SUPER-LOCAL
	PUSH-INT
	DROP
	JUMP_IF_FALSE
	JUMP
	LABEL
	CALL

Jede weitere Funktion wird �ber einen der PUSH-Befehle auf den Stack gelegt und dann �ber `CALL` ausgef�hrt.

M�chte man den Bytecode einer Funktion sehen, kann man dieser das Symbol '++bc++ senden
	(eval_input '++bc++)  ->  	PUSH-CONSTANT 1
								PUSH-GLOBAL 10
								CALL 1
								PUSH-GLOBAL 31
								CALL 1
								PUSH-GLOBAL 25
								CALL 1
								PUSH-CONSTANT 0
								PUSH-GLOBAL 10
								CALL 1
								PUSH-GLOBAL 32
								CALL 2

Dadurch, dass Funktionen bereits zu ihren Definitionszeitpunkten zu Bytecode kompiliert werden und nicht 'lazy' zum ersten Aufruf, hat man einige Besonderheiten zu beachten. Der Bytecode-Compiler geht davon aus, dass jedes Symbol bereits durch den Opt-Coder in ein der indexbasierten Push-Funktionen �berf�hrt wurde, um dann den entsprechenden Stack Push Befehl daraus zu generieren. Ist nun aber eine Variable zum Definitionszeitpunkt der Funktion noch nicht bekannt, schl�gt die Bytecode-Kompilierung fehl. Zus�tzlich wertet der Bytecode-Compiler das Objekt auf welches die Variable zeigt aus. Handelt es sich um eine Funktion, muss er, nachdem er diese auf den Stack gepusht hat, ein `CALL` generieren.

Die L�sung daf�r ist, dass man �hnlich einer Variablen-Deklaration im Vorhinaus ein Binding mit dem richtigen Typ anlegen muss. Ein Beispiel dazu findet sich in `startGui.lsp`
	
	(define tf_input +)
	(define tf_output +)

	(define eval_input (lambda (x) (tf_output 'setText (eval (tf_input 'getText)))))
	(define load_file (lambda (x) (tf_input 'setText (load "IDE/moreGui.lsp"))))
	
	[...]
	#Richtige Zuweisung:
	(set! tf_input (text$ p_input))
	(set! tf_output (text$ root))

Ein weiteres Problem ist wenn lokale Variablen ben�tigt werden. Der Opt-Coder legt zwar f�r jede lokale Variable bereits ein Binding im Environment an, so dass diese �ber Index referenziert werden k�nnen. Da allerdings kein Typ f�r dieses Binding vorhanden ist, nimmt der ByteCode-Compiler immer an, dass es sich um kein Funktionsobjekt handeln wird und er somit kein `CALL` generieren muss. Soll trotzdem innerhalb einer Funktion ein lokales Binding als Funktion genutzt werden, muss diese im Lisp-Code explizit mit `(call ...)` angegeben werden. Ein Beispiel hierf�r findet sich in `moreGui.lsp`
 
	(define (eval_show_bc x) (begin 
  		(define result (eval (wrap_input_in_begin (tf_input 'getText))))
  		(if (eq? (type result) "UserFunction") (t_bytecode 'setText (call result '++bc++)) (t_bytecode 'setText "NO BYTECODE!!!"))
  		(if (eq? (type result) "UserFunction") (t_optcode 'setText (call result '++op++)) (t_optcode 'setText "NO OPTCODE!!!"))
  		(tf_output 'setText result)
  		)
	)
	
## CLI

Der Interpreter verf�gt �ber ein einfaches Command Line Interface, welches es erlaubt, beliebige Dateien zu laden und danach in eine konsolenbasierte REPL zu gehen. 

	python start.py -h
	Usage: start.py [options]

	Options:
	  -h, --help            show this help message and exit
	  -f FILE, --file=FILE  The Lisp file
	  
Zu beachten ist, dass aus Gr�nden der Einfachheit der Interpreter, falls kein File angegeben wird, die Datei GUI/startGui.lsp l�dt. Dies ist ebenfalls der Grund, warum das Script aus dem Ordner `src` gestartet werden muss.

## GUI

Das Projekt besitzt eine rudiment�re Entwicklungsumgebung, die vollst�ndig in Lisp implementiert ist. Aus Demonstrationsgr�nden besteht die GUI aus zwei Skripten, die in einer Art Bootstrapping nacheinander evaluiert werden k�nnen.

In `startGui.lsp` befindet sich der Code f�r eine rudiment�re GUI, die einzig einzelne LISP-Befehle evaluieren kann und deren Ausgabe anzeigen kann.

	(define eval_input (lambda (x) (tf_output 'setText (eval (tf_input 'getText)))))

![SimpleGui](/screenshots/Gui1.png "Simple Gui")

Da die Gui im Kontext des Interpreters definiert wurde, kann sie auch �ber diesen manipuliert werden.  
Eine umfangreichere Gui-Manipulation kann z.B. �ber die Datei 'IDE/moreGui.lsp' erreicht werden.

Dazu bet�tigt man entweder den Button `load greater Gui` oder aber l�dt die Datei h�ndisch in das Eingabefeld:
So w�rde `(load "IDE/moreGui.lsp")` die Datei einlesen und in den Ausgabebereich schreiben. Da die Gui aber vollst�ndig in Lisp implementiert ist, kann das Ergebnis dieser Funktion einfach an die n�chste Funktion weitergereicht werden. Somit f�hrt ein `(tf_input 'setText (load "IDE/moreGui.lsp"))` dazu, dass der Inhalt der Datei in das entsprechende Textfeld geschrieben wird.

Die daraufhin geladene Gui ist etwas komplexer und besitzt mehr Features.
So wird jeweils ein Fenster f�r die Optcode- als auch f�r die Bytecode-Anzeige geladen, sowie ein gr�ner Button `Eval-with-Begin` angezeigt. Dieser Button f�hrt dazu, dass der Code im Eingabefeld in ein `(begin ...)` gewrappt wird und das das Ergebnis (im Falle einer user definied function) in den beiden Fenstern angezeigt wird. 

Weiter besitzt die erweiterte GUI, �ber einen Scrollbalken und einen Clear-Button, der das Eingabefeld l�scht.

![ComplexGui](/screenshots/Gui2.png "Komplexe Gui")

M�chte man den erstellen Code speichern, empfiehlt es sich noch einen Speicher-Button zur Gui hinzuzuf�gen. Dazu wurde w�hrend der Entwicklung immer ein Fenster erzeugt, in den man den Code zwischenspeichern kann, um ihn dann in eine Datei zu schreiben.

	(define tmp_window (toplevel$ "tmp"))
	(define txt (text$ tmp_window))
	(txt 'pack)
	(define btn_save (button$ btn_panel "save" (lambda (x) (txt 'setText (tf_input 'getText)))))
	(btn_save 'pack)
	
Mit einem Klick auf `save` kann der Inhalt in das neue Fenster kopiert werden und daraufhin mit `(save "foo.lsp" txt 'getText)` gespeichert werden.



# Bekante Bugs und Quirks

* Defines ohne explizites Begin funktioniert nur mit 2 Bl�cken.

* Dinge m�ssen defined sein bevor sie genutzt werden! Und zwar mit ihrem richtigen "Typ" z.B. (define tf_output +).

* Funktionen im ByteCode per `define` zuzuweisen und dann aufzurufen geht nicht. Darum wird `call` eingef�hrt.



