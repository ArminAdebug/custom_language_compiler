# Custom Language Compiler

A small, personal compiler experiment written in Python. I built it to
explore how a programming language can be processed and translated into
x86-64 assembly, from parsing expressions to generating low-level
instructions.

This is an experimental learning project, not a complete or
production-ready compiler.

## What I explored

-   **Lexer / tokenization** --- breaking source text into meaningful
    pieces.
-   **Parser** --- processing declarations, assignments, and
    expressions.
-   **AST and expression structure** --- representing nested expressions
    so their grouping and operator precedence can be handled.
-   **Intermediate representation (IR)** --- experimenting with a
    lower-level form between source expressions and generated
    instructions.
-   **Assembly generation** --- translating supported operations into
    x86-64 assembly instructions.
-   **Register allocation** --- managing a small pool of general-purpose
    registers while evaluating expressions.
-   **Low-level details** --- working with registers, memory operands,
    arithmetic instructions, and division instructions such as `idiv`.

The implementation is intentionally limited and experimental. The code
shows my own exploration of the compiler pipeline rather than an attempt
to implement every feature of a real-world language.

## Example input

One of the kinds of nested expressions I used to test the
implementation:

``` c
int a = 0;
int b;

b = (5 * a) + (((50 + 4) * 2 - 3 / 9 / 5) - 6);

int c;

c = (b + 4) * 2 - 3 / a;
```

This example is useful for testing nested parentheses, operator
precedence, variable declarations, assignments, and code generation for
arithmetic expressions.

**Runtime note:** `a` is initialized to `0`, so the final expression
contains division by zero. It can be used to inspect parsing/code
generation, but change `a` to a non-zero value before expecting the
generated program to execute successfully.

## Made from scratch

I wrote this project myself as a personal experiment, without internet
access or AI assistance. In particular, I worked out the
AST/expression-handling logic from scratch on paper before implementing
it in code. Building the expression handling for deeply nested
arithmetic was one of the main challenges and the most educational part
of the project.

## Project status

-   Personal and experimental
-   Limited language features
-   Not intended for production use
-   No guarantee that every valid-looking input is supported

The repository is kept as a record of my experiments with compiler
construction, parsing, expression trees, register handling, and assembly
generation.
