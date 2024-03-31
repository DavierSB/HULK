scripts = [
    '42;', #0
    'print((((1 + 2) ^ 3) * 4) / 5);', #1
    'print(sin(30));', #2
    '1 + tan(x);', #3
    'let msg = "Hello World" in print(msg);', #4
    'let a = 6, b = a * 7 in print(b);', #5
    """let a = 6 in
           let b = a * 7 in
              print(b);""", #6
    'let a = 42 in if (a % 2 == 0) print("Even") else print("Odd");', #7
    'let a = 42 in print(if (a % 2 == 0) "even" else "odd");', #8
    """ let a = 42 in let mod = a % 3 in
            print(
            if (mod == 0) "Magic"
            elif (mod %3 == 1) "Woke"
            else "Dumb"
            );
    """,#9
    """let iterable = range(0, 10) in
    while (iterable.next())
        let x = iterable.current() in
            print(x);
    """,#10
    'for (x in range(0, 10)) print(x);',#11
    """let pt = new Point() in
    print("x: " @ pt.getX() @ "; y: " @ pt.getY());""",#12
    """let pt = new Point(3,4) in
    print("x: " @ pt.getX() @ "; y: " @ pt.getY());""",#13
    """let pt = new PolarPoint(3,4) in
    print("rho: " @ pt.rho());
    """,#14
    """let a = 42 in
    if (a % 2 == 0) {
        print(a);
        print("Even");
    }
    else print("Odd");
    """,#15
    """let a = 10 in while (a >= 0) {
    print(a);
    a := a - 1;
}
""",#16
""" let a = 0 in
        let b = a := 1 in {
            print(a);
            print(b);
        }
    """,#17
    """{
    print("JAJAJA");
    let x = "boniato" in 
    while (true)
    if (x == "boniato")
    x := "rico"
    else
    {
    x := "Ohlaleliju";
    sin(cos(x));
    }
    }""",#18
    """function gcd(a, b) => while (a > 0)
    let m = a % b in {
        b := a;
        a := m;
    };42;
    """,#19
    """
    function tan(x) => sin(x)/cos(x);
    function alligator(){"Croac";}
    tan(alligator());
    """,#20
    """type Point {
    x = 0;
    y = 0;

    getX() => self.x;
    getY() => self.y;

    setX(x) => self.x := x;
    setY(y) => self.y := y;
    }42;""", #21
    """type Range(min:Number, max:Number) {
    min = min;
    max = max;
    current = min - 1;

    next(): Boolean => (self.current := self.current + 1) < max;
    current(): Number => self.current;
}
type Knight inherits Person {
    name() => "Sir" @@ base();
}
function fib(n) => if (n == 0 | n == 1) 1 else fib(n-1) + fib(n-2);
function fact(x) => let f = 1 in for (i in range(1, x+1)) f := f * i;
42;
""" #22
    ]