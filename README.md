
# Typechecker

## Done

* Numbers, texts
* Nulls
* Function declarations
* Function calls

## Todo

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

## Functions

I'd like to have types for things like whether functions can do IO, can throw/panic, are async, 
yield, allocate, access globals, etc, but I'd like to infer them in most cases. For concrete 
functions, a function becomes Throws if it calls any function that throws. For type constraints,
this needs to be a little fancy: calling a generic function without explicit types makes the 
parent inherit the Throws if and only if the concrete type has it. This requires bounds to be 
explicit, so won't work behind dynamic dispatch - in such cases it must be explicit instead of
inferred whether it, e.g., Throws.

## Minor

* Should variable names be allowed to be the same as type names in scope?

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

