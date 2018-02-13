# CFG2CNF
### Python tool able to convert a Context Free Grammar in Chomsky Normal Form

## 1 Goals
The main purpose of this project is to provide a strategy for converting a Context Free Grammar in his Chomsky Normal Form

## 2 How to use
The Grammar G=(V, T, P, S) is read by a `.txt` file, so need a certain formattation, that follow:
```
Terminals:
+ - ( ) ^ number variable
Variables:
Expr Term AddOp MulOp Factor Primary
Productions:
Expr->Term | Expr AddOp Term | AddOp Term;
Term->Factor | Term MulOp Factor;
Factor->Primary | Factor ^ Primary;
Primary->number | variable;
Primary->( Expr );
AddOp->+ | -;
MulOp->* | /
```
Where is obvious how T, V and P are loaded (text after *Terminals/Variables/Productions:*), maybe less obviously is selected S as the first Variable from the left.

The script must be called in a form like ``CFG2CNF.py model.txt``, and it produces an ``out.txt`` file. The output corresponding to the above example is:
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