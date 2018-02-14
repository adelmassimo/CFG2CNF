# CFG2CNF
### Python tool able to convert a Context Free Grammar in Chomsky Normal Form

## 1 Goals
The main purpose of this project is to provide a strategy for converting a Context Free Grammar in his Chomsky Normal Form

## 2 How to use
The script must be called in a form like ``CFG2CNF.py model.txt``, and it produces an ``out.txt`` file.
The Grammar G=(V, T, P, S) is read by a `.txt` file, so need a certain formattation, that follow:
```
Terminals:
+ - ( ) ^ number variable
Variables:
Expr Term AddOp MulOp Factor Primary
Productions:
Expr -> Term | Expr AddOp Term | AddOp Term;
Term -> Factor | Term MulOp Factor;
Factor -> Primary | Factor ^ Primary;
Primary -> number | variable;
Primary -> ( Expr );
AddOp -> + | -;
MulOp -> * | /
```
Is important to:
* Use spaces between symbols, one space, not more
* use te ';' character to separate rows in productions: don't use for the last.

Where is obvious how T, V and P are loaded (text after *Terminals/Variables/Productions:*), maybe less obviously is selected S as the first Variable from the left.
**N.B.** the ε-rule symbol is fixed and it's simplly ``e``
The output corresponding to the above example is:
```
AddOp -> + | -
Term -> Term B1 | Primary | Factor C1
MulOp -> * | /
Expr -> Expr A1 | AddOp Term | Term B1 | Primary | Factor C1
S0 -> Expr A1 | AddOp Term | Term B1 | Primary | Factor C1
Primary -> Y | variable | X D1
A1 -> AddOp Term
B1 -> MulOp Factor
W -> )
Factor -> Primary | Factor C1
Y -> number
X -> (
C1 -> Z Primary
Z -> ^
D1 -> Expr W
```

## 3 The Routine
The routine follows [Wikipedia](https://en.wikipedia.org/wiki/Chomsky_normal_form) formulation of this algorthm, in particular:
1. **START**: add ``S0->S`` production
2. **TERM**: replace terminal symbols with variables in production containing boht on the right
3. **BIN**: make rules binaries, in other words break in more parts rules which right side is longer than 2
4. **DEL**: eliminate ε-rules and eventually rearrange other productions
5. **UNIT**: remove all production which the right side is only a variable


## 4 Known Bugs
* New variables (like `C1` and `Z` in `C1 -> Z Primary`) are introduced using a fixed and coded set:
```
variablesJar = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "W", "X", "Y", "Z"]
```
This strategy could result a limit in vision of a big computation, but it's easily avoidable adding symbols