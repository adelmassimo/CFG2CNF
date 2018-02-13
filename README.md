# CFG2CNF
### Python tool able to convert a Context Free Grammar in Chomsky Normal Form

## 1 Goals
The main purpose of this project is to provide a strategy for converting a Context Free Grammar in his Chomsky Normal Form

## 2 How to use
The Grammar G=(V, T, P, S) is read by file, that need a certain formattation, like below:
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

