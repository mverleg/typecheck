
# Typechecker

## Done

* Numbers, texts
* Nulls
* Function declarations
* Function calls

## Todo

* Overloads (?)
* Variables
* Function references
* Flex nr literals
* Recursion
* Structs
* Tuples
* Arrays
* Union types
* Interfaces/traits
* Closures (capture)
* Generics
* Scopes


Propagate type info backwards more, i.e.
    f(a, b):
        a + b
    c = 0
    c = f(x, y)
  In this case we should infer
  - c is an int
  - so f returns int
  - so (a + b) is int
  - so a and b are ints
    - (if that's the only addition that returns ints)
    - more generally types where A: Add<B, out=int>
  - so f takes two ints
  - so x and y are ints

