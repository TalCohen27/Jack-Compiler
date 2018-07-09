from constants import nonTerminals, TokenType, Keyword, Symbol, Operator, UnaryOperator, segment_map
import itertools
from VMWriter import VMWriter
from SymbolTable import SymbolTable
import constants
from os.path import split


class CompilationEngine:
    def __init__(self, _tokens, _in_path, _out_file):
        self.tokens = iter(_tokens)
        self.file_name = str(split(_in_path)[1].split('.')[0])
        self.out_file = _out_file
        self.writer = VMWriter(_out_file)
        self.sym_table = SymbolTable()
        self.class_name = ''
        self.curr_subroutine_name = ''
        self.curr_cond_index = 0

    def CompileClass(self):
            self.tokens.__next__()
            self.class_name = self.tokens.__next__().token
            self.tokens.__next__()  # {
            self.CompileClassVarDec()
            curr_token = self.tokens.__next__()
            while curr_token.token in [Keyword.FUNCTION.value, Keyword.METHOD.value,
                                       Keyword.CONSTRUCTOR.value]:
                self.CompileSubroutineDEC(curr_token.token)
                curr_token = self.tokens.__next__()

    def CompileClassVarDec(self):
        sym_kind = self.tokens.__next__()
        while sym_kind.token == Keyword.FIELD.value or sym_kind.token == Keyword.STATIC.value:
            sym_type = self.tokens.__next__()
            moreVars = True
            while moreVars:
                sym_name = self.tokens.__next__()
                moreVars = self.tokens.__next__().token == Symbol.COMMA.value
                self.sym_table.define(sym_name.token, sym_type.token, sym_kind.token)
            sym_kind = self.tokens.__next__()
        self.tokens = itertools.chain([sym_kind], self.tokens)

    def CompileSubroutineDEC(self, sub_type):
        self.sym_table.startSubroutine()
        return_type = self.tokens.__next__() # return type
        self.curr_subroutine_name = self.file_name + '.' + self.tokens.__next__().token
        self.tokens.__next__() # (
        if sub_type == constants.METHOD:
            self.sym_table.define('this', self.class_name, constants.ARG)
        self.CompileParameterList()
        self.tokens.__next__()   # )
        self.CompileSubroutineBody(sub_type)

    def CompileParameterList(self):
        arg_type = self.tokens.__next__()
        if arg_type.token == Symbol.PAREN_CLOSE.value:
            self.tokens = itertools.chain([arg_type], self.tokens)
        else:
            moreVars = True
            while moreVars:
                arg_name = self.tokens.__next__()
                curr_token = self.tokens.__next__()                     # , or  )
                moreVars = curr_token.token == Symbol.COMMA.value
                self.sym_table.define(arg_name.token, arg_type.token, constants.ARG)
                if moreVars:
                    arg_type = self.tokens.__next__()
                else:
                    self.tokens = itertools.chain([curr_token], self.tokens)

    def CompileSubroutineBody(self, sub_type):
        self.tokens.__next__()          # {
        self.CompileVarDec()
        self.writer.write_function(self.curr_subroutine_name, self.sym_table.var_count(constants.VAR))
        if sub_type == constants.METHOD:
            self.writer.write_push(constants.ARG, 0)
            self.writer.write_pop(constants.POINTER, 0)
        if sub_type == Keyword.CONSTRUCTOR.value:
            self.CompileCtorAlloc()
        self.CompileStatements()
        self.tokens.__next__()          # }

    def CompileCtorAlloc(self):
        self.writer.write_push(constants.CONST, self.sym_table.var_count(constants.FIELD))
        self.writer.write_call('Memory.alloc', 1)
        self.writer.write_pop(constants.POINTER, 0)

    def CompileVarDec(self):
        curr_token = self.tokens.__next__()
        hasVars = curr_token.token == Keyword.VAR.value
        while hasVars:
            var_type = self.tokens.__next__()  # type
            self.CompileInlineVars(var_type.token)
            curr_token = self.tokens.__next__()
            hasVars = curr_token.token == Keyword.VAR.value
        self.tokens = itertools.chain([curr_token], self.tokens)

    def CompileInlineVars(self, var_type):
        hasVarsInline = True
        while hasVarsInline:
            var_name = self.tokens.__next__()                        #ident
            curr_token = self.tokens.__next__()                         # , or ;
            hasVarsInline = (curr_token.token == Symbol.COMMA.value)
            self.sym_table.define(var_name.token, var_type, constants.VAR)

    def CompileStatements(self):
        state = self.tokens.__next__()
        while state.token in [Keyword.LET.value,
                              Keyword.DO.value, Keyword.RETURN.value, Keyword.WHILE.value, Keyword.IF.value]:
            if state.token == Keyword.LET.value:
                self.CompileLet()
            elif state.token == Keyword.WHILE.value:
                self.CompileWhile()
            elif state.token == Keyword.RETURN.value:
                self.CompileReturn()
            elif state.token == Keyword.IF.value:
                self.CompileIf()
            elif state.token == Keyword.DO.value:
                self.CompileDo()
            state = self.tokens.__next__()
        self.tokens = itertools.chain([state], self.tokens)

    def CompileLet(self):
        left_value = self.tokens.__next__()  #var name
        segment = segment_map[self.sym_table.kind_of(left_value.token)]
        index = self.sym_table.index_of(left_value.token)
        curr_token = self.tokens.__next__()
        if curr_token.token == Symbol.BRACKET_OPEN.value:
            self.CompileArrayAccess(segment, index, True)
        else:
            self.CompileExpression()
            self.writer.write_pop(segment, index)
        self.tokens.__next__()                                              # ;

    def CompileWhile(self):
        L1 = 'L' + str(self.curr_cond_index)
        self.curr_cond_index += 1
        L2 = 'L' + str(self.curr_cond_index)
        self.curr_cond_index += 1
        self.tokens.__next__() # (
        self.writer.write_label(L1)
        self.CompileExpression()
        self.tokens.__next__()  # )
        self.writer.write_arithmetic(constants.NOT)
        self.writer.write_if(L2)
        self.tokens.__next__()  # {
        self.CompileStatements()
        self.writer.write_goto(L1)
        self.tokens.__next__()  # }
        self.writer.write_label(L2)

    def CompileIf(self):
        L1 = 'L' + str(self.curr_cond_index)
        self.curr_cond_index += 1
        L2 = 'L' + str(self.curr_cond_index)
        self.curr_cond_index += 1
        self.tokens.__next__() # (
        self.CompileExpression()
        self.writer.write_arithmetic(constants.NOT)
        self.writer.write_if(L1)
        self.tokens.__next__()  # )
        self.tokens.__next__()  # {
        self.CompileStatements()
        self.writer.write_goto(L2)
        self.writer.write_label(L1)
        self.tokens.__next__()  # }
        curr_token = self.tokens.__next__()
        if curr_token.token == Keyword.ELSE.value:
            self.tokens.__next__() # {
            self.CompileStatements()
            self.tokens.__next__()  # }
        else:
            self.tokens = itertools.chain([curr_token], self.tokens)
        self.writer.write_label(L2)

    def CompileReturn(self):
        curr_token = self.tokens.__next__()
        if curr_token.token != Symbol.SEMI_COLON.value:
            self.tokens = itertools.chain([curr_token], self.tokens)
            self.CompileExpression()
            self.tokens.__next__()    # ;
        else:
            self.writer.write_push(constants.CONST, 0)
        self.writer.write_return()

    def CompileDo(self):
        self.compileSubroutineCall(True)
        self.tokens.__next__()  # ;

    def CompileExpression(self):
        self.CompileTerm()
        curr_token = self.tokens.__next__()
        if curr_token.token in [operator.value for operator in Operator]:
            self.CompileTerm()
            self.writer.write_arithmetic(curr_token.token)
        else:
            self.tokens = itertools.chain([curr_token], self.tokens)

    def CompileTerm(self):
        curr_token = self.tokens.__next__()
        if curr_token.type == TokenType.IDENTIFIER.value:
            next_token = self.tokens.__next__()
            if next_token.token == Symbol.BRACKET_OPEN.value:
                curr_token_kind = segment_map[self.sym_table.kind_of(curr_token.token)]
                curr_token_index = self.sym_table.index_of(curr_token.token)
                self.CompileArrayAccess(curr_token_kind, curr_token_index, False)
            elif next_token.token == Symbol.PERIOD.value or next_token.token == Symbol.PAREN_OPEN.value:
                self.tokens = itertools.chain([next_token], self.tokens)
                self.tokens = itertools.chain([curr_token], self.tokens)
                self.compileSubroutineCall(False)
            else:
                self.tokens = itertools.chain([next_token], self.tokens)
                self.writer.write_push(segment_map[self.sym_table.kind_of(curr_token.token)],
                                       self.sym_table.index_of(curr_token.token))
        elif curr_token.type == constants.TokenType.INT_CONST.value:
            self.writer.write_push(constants.CONST, str(curr_token.token))
        elif curr_token.type == constants.TokenType.STRING_CONST.value:
           self.CompileStringConstant(curr_token.token)
        elif curr_token.token == constants.Keyword.THIS.value:
            self.writer.write_push(constants.POINTER, 0)
        elif curr_token.type == constants.TokenType.KEYWORD.value:
            if curr_token.token == 'null' or curr_token.token == 'false':
                self.writer.write_push(constants.CONST, 0)
            elif curr_token.token == 'true':
                self.writer.write_push(constants.CONST, 1)
                self.writer.write_arithmetic('neg')
        else:
            if curr_token.token in [unary.value for unary in UnaryOperator]:
                self.CompileTerm()
                self.writer.write_arithmetic(constants.unary_operators_map[curr_token.token])
            elif curr_token.token == Symbol.PAREN_OPEN.value:
                self.CompileExpression()
                self.tokens.__next__()  # )

    def CompileStringConstant(self, str_const):
        self.writer.write_push(constants.CONST, len(str_const))
        self.writer.write_call('String.new', 1)
        for i in range(len(str_const)):
            self.writer.write_push(constants.CONST, ord(str_const[i]))
            self.writer.write_call('String.appendChar', 2)

    def CompileArrayAccess(self, arr_kind, arr_index, is_let):
        self.writer.write_push(arr_kind, arr_index)  # arr
        self.CompileExpression()  # arr[expres 1]
        self.writer.write_arithmetic('add')
        self.tokens.__next__()  # ]
        if is_let:
            self.tokens.__next__()    # =
            self.CompileExpression()
            self.writer.write_pop(constants.TEMP, 0)
            self.writer.write_pop(constants.POINTER, 1)
            self.writer.write_push(constants.TEMP, 0)
            self.writer.write_pop(constants.THAT, 0)
        else:
            self.writer.write_pop(constants.POINTER, 1)
            self.writer.write_push(constants.THAT, 0)

    def CompileExpressionList(self):
        num_exprss = 0
        curr_token = self.tokens.__next__()
        if curr_token.token != Symbol.PAREN_CLOSE.value:
            moreExpr = True
            self.tokens = itertools.chain([curr_token], self.tokens)
            while moreExpr:
                num_exprss += 1
                self.CompileExpression()
                curr_token = self.tokens.__next__()
                moreExpr = curr_token.token == Symbol.COMMA.value
                if not moreExpr:
                    self.tokens = itertools.chain([curr_token], self.tokens)
        else:
            self.tokens = itertools.chain([curr_token], self.tokens)
        return num_exprss

    def compileSubroutineCall(self, is_void):
        num_express = 0
        prefix = self.tokens.__next__().token
        next_token = self.tokens.__next__()    # ( or .
        if next_token.token == Symbol.PERIOD.value and \
                self.sym_table.type_of(prefix) is not None:
            function_name = self.sym_table.type_of(prefix) + '.' + self.tokens.__next__().token
            self.tokens.__next__()  # (
            self.writer.write_push(segment_map[self.sym_table.kind_of(prefix)],
                                   self.sym_table.index_of(prefix))
            num_express = 1
        elif next_token.token == Symbol.PERIOD.value:
            function_name = prefix + '.' + self.tokens.__next__().token
            self.tokens.__next__() # (
        else:
            function_name = self.class_name + '.' + prefix
            self.writer.write_push(constants.POINTER, 0)
            num_express = 1

        num_express += self.CompileExpressionList()
        self.writer.write_call(function_name, num_express)
        if is_void:
            self.writer.write_pop(constants.TEMP, 0)
        self.tokens.__next__()           # )



