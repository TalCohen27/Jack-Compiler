from enum import Enum

CLASS_LEVEL = 1
SUBROUTINE_LEVEL = 2
VAR = 'var'
FIELD = 'field'
STATIC = 'static'
ARG = 'argument'
CLASS_NAME = 5
SUBROUTINE_NAME = 6
CONST = 'constant'
LOCAL = 'local'
THIS = 'this'
THAT = 'that'
POINTER = 'pointer'
TEMP = 'temp'
PUSH = 13
POP = 'pop'
ARITH = 14
LABEL = 15
GOTO = 16
IF = 17
CALL = 18
FUNCTION = 19
RETURN = 20
METHOD = 'method'
NOT = 'not'


segment_map = {
    'field': THIS,
    'static': STATIC,
    'var': LOCAL,
    'argument': ARG,
}


operators_map = {

    '+': 'add',
    '-': 'sub',
    '&amp;': 'and',
    '|': 'or',
    '&lt;': 'lt',
    '&gt;': 'gt',
    '=': 'eq',
    '~': 'not'
}

unary_operators_map = {

    '-': 'neg',
    '~': 'not'

}


class Keyword(Enum):
    CLASS = 'class'
    METHOD = 'method'
    FUNCTION = 'function'
    CONSTRUCTOR = 'constructor'
    INT = 'int'
    BOOLEAN = 'boolean'
    CHAR = 'char'
    VOID = 'void'
    VAR = 'var'
    STATIC = 'static'
    FIELD = 'field'
    LET = 'let'
    DO = 'do'
    IF = 'if'
    ELSE = 'else'
    WHILE = 'while'
    RETURN = 'return'
    TRUE = 'true'
    FALSE = 'false'
    NULL = 'null'
    THIS = 'this'


class TokenType(Enum):
    KEYWORD = 'keyword'
    SYMBOL = 'symbol'
    IDENTIFIER = 'identifier'
    INT_CONST = 'integerConstant'
    STRING_CONST = 'stringConstant'


class Symbol(Enum):
    BRACKET_CLOSE = ']'
    BRACKET_OPEN = '['
    CURLY_OPEN = '{'
    CURLY_CLOSE = '}'
    PAREN_OPEN = '('
    PAREN_CLOSE = ')'
    PERIOD = '.'
    COMMA = ','
    SEMI_COLON = ';'
    PLUS = '+'
    MINUS = '-'
    STAR = '*'
    DIV = '/'
    AMPERSAND = '&'
    VERTICAL = '|'
    LEFT_ARROW = '<'
    RIGHT_ARROW = '>'
    EQUAL = '='
    TILDA = '~'


class nonTerminals(Enum):
    CLASS = 'class'
    CLASS_VAR_DEC = "classVarDec"
    SUBROUTINE_DEC = "subroutineDec"
    PARAM_LIST = 'parameterList'
    SUBROUTINE_BODY = 'subroutineBody'
    VAR_DEC = 'varDec'
    STATEMENTS = 'statements'
    LET_STATEMENT = 'letStatement'
    IF_STATEMENT = 'ifStatement'
    WHILE_STATEMENT = 'whileStatement'
    DO_STATEMENT = 'doStatement'
    RETURN_STATEMENT = 'returnStatement'
    EXPRESSION = 'expression'
    TERM = 'term'
    EXPRESSION_LIST = 'expressionList'


class Operator(Enum):
    PLUS = '+'
    MINUS = '-'
    STAR = '*'
    DIV = '/'
    AMPERSAND = '&amp;'
    VERTICAL = '|'
    LEFT_ARROW = '&lt;'
    RIGHT_ARROW = '&gt;'
    EQUAL = '='


class UnaryOperator(Enum):
    MINUS = '-'
    TILDA = '~'
