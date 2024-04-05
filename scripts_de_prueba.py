scripts = [
    '42;', #0
    'print((((1 + 2) ^ 3) * 4) / 5);', #1
    'print(sin(30));', #2
    '1 + tan(x);', #3
    'let msg = "Hello World" in print(msg);', #4
    'let a = 6, b = a * 7 in print(b);', #5
    """let a = 6 in\n
           let b = a * 7 in\n
              print(b);""", #6
    'let a = 42 in if (a % 2 == 0) print("Even") else print("Odd");', #7
    'let a = 42 in print(if (a % 2 == 0) "even" else "odd");', #8
    """ let a = 42 in let mod = a % 3 in\n
            print(\n
            if (mod == 0) "Magic"\n
            elif (mod %3 == 1) "Woke"\n
            else "Dumb"\n
            );
    """,#9
    """let iterable = range(0, 10) in\n
    while (iterable.next())\n
        let x = iterable.current() in\n
            print(x);\n
    """,#10
    'for (x in range(0, 10)) print(x);',#11
    """let pt = new Point() in\n
    print("x: " @ pt.getX() @ "; y: " @ pt.getY());""",#12
    """let pt = new Point(3,4) in\n
    print("x: " @ pt.getX() @ "; y: " @ pt.getY());""",#13
    """let pt = new PolarPoint(3,4) in\n
    print("rho: " @ pt.rho());\n
    """,#14
    """let a = 42 in\n
    if (a % 2 == 0) {\n
        print(a);\n
        print("Even");\n
    }\n
    else print("Odd");\n
    """,#15
    """let a = 10 in while (a >= 0) {\n
    print(a);\n
    a := a - 1;\n
}
""",#16
""" let a = 0 in\n
        let b = a := 1 in {\n
            print(a);\n
            print(b);\n
        }
    """,#17
    """{\n
    print("JAJAJA");\n
    let x = "boniato" in\n 
    while (true)\n
    if (x == "boniato")\n
    x := "rico"\n
    else\n
    {\n
    x := "Ohlaleliju";\n
    sin(cos(x));\n
    }\n
    }""",#18
    """function gcd(a, b) => while (a > 0)\n
    let m = a % b in {\n
        b := a;\n
        a := m;\n
    };42;
    """,#19
    """
    function tan(x) => sin(x)/cos(x);\n
    function alligator(){"Croac";}\n
    tan(alligator());\n
    """,#20
    """type Point {\n
    x = 0;\n
    y = 0;\n
\n
    getX() => self.x;\n
    getY() => self.y;\n
\n
    setX(x) => self.x := x;\n
    setY(y) => self.y := y;\n
    }42;""", #21
    """type Range(min:Number, max:Number) {\n
    min = min;\n
    max = max;\n
    current = min - 1;\n
\n
    next(): Boolean => (self.current := self.current + 1) < max;\n
    current(): Number => self.current;\n
}\n
type Knight inherits Person {\n
    name() => "Sir" @@ base();\n
}\n
function fib(n) => if (n == 0 | n == 1) 1 else fib(n-1) + fib(n-2);\n
function fact(x) => let f = 1 in for (i in range(1, x+1)) f := f * i;\n
42;\n
""",#22
"""type A{\n
a : Number = 1;\n
}\n
type B inherits A{\n
\n
}\n
{\n
let z = new B() in print(z.a);\n
let z = new B() in print(z.c);\n
}\n
""",#23
"""type A{\n
a : Literal = "boniato";\n
}\n
type B{\n
a : Literal = a @ "casa";\n
}\n
42;
""",#24
"""
type A{\n
f() => 5;\n
}\n
type B inherits A{\n
g() => 6;\n
}\n
type C inherits B{\n
\n
}\n
let c = new C() in (c.f() + c.g()) as Literal;
""",#25
"""
type A{\n
f() => 5;\n
}\n
type B inherits A{\n
g() => 6;\n
}\n
type C inherits B{\n
f() => base() * 2;\n
g() => base() /2;\n
}\n
let c = new C() in (c.f() + c.g()) as Literal;\n
""",#26
"""type Point(x : Number, y : Number){\n
x = x;\n
y = y;\n
getX() => self.x;\n
getY() => self.y;\n
}\n
type TriDimensionalPoint(z : Number) inherits Point(0, "Viva Cuba"){\n
z = z;\n
getZ() => self.z;\n
}\n
type WeirdPoint inherits TriDimensionalPoint(1 + 2)\n
{\n
\n
}\n
let w = new WeirdPoint() in\n
print(w.getX() + w.getZ());\n
""",#27
"""
(while (5) let x = 3 in x) as Number;\n
"""
]