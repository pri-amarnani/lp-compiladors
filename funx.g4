grammar funx;
root : bloc EOF;
bloc : instru*;

instru: func
    |funcCall
    |ifClause
    |cond
    |whileLoop
    |assignacio
    |writeClause
    |expr
    ;

blocFunc: instru*;
func: NOMF assignacioVars '{' blocFunc '}';
assignacioVars: (VAR)*;

funcCall: NOMF crearParams;
crearParams: (expr)*;

expr: '('expr')'
    |<assoc=right>  expr POT expr
    |expr MOD expr
    |expr (DIV|MULT) expr
    |expr (MES|MENYS) expr
    |funcCall
    |'-' NUM
    |(NUM|VAR)
    ;

cond: expr (IGUAL|MGRANQ|MPETITQ|MGRANIGUAL|MPETITIGUAL|DIFERENT) expr;

assignacio: VAR '<-' (expr|cond);
writeClause: 'print' (expr|cond);
ifClause: 'if' cond '{' blocFunc '}' (elseClause)?;
elseClause: 'else' '{' blocFunc '}';
whileLoop: 'while' cond '{' bloc '}';


VAR: [a-z][A-Za-z]*;
NOMF: [A-Z][a-zA-Z0-9]*;
NUM: [0-9]+ ;
MES: '+';
MENYS: '-';
MULT: '*';
DIV: '/';
POT: '^';
MOD: '%';
IGUAL: '=';
MGRANQ: '<';
MPETITQ: '>';
MGRANIGUAL: '>=';
MPETITIGUAL: '<=';
DIFERENT: '!=';
COMMENT : '#' ~[\r\n]* -> skip ;
WS : [ \n]+ -> skip;
