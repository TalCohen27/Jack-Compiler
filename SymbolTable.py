import constants


class SymbolTable:
    def __init__(self):
        self.curr_class_symbol_table = {}
        self.curr_subroutine_symbol_table = {}
        self.curr_var_count_table = {}
        self.init_var_count_table()

    def init_var_count_table(self):
        self.curr_var_count_table[constants.VAR] = 0
        self.curr_var_count_table[constants.FIELD] = 0
        self.curr_var_count_table[constants.STATIC] = 0
        self.curr_var_count_table[constants.ARG] = 0

    def startSubroutine(self):
            self.curr_subroutine_symbol_table = {}
            self.curr_var_count_table[constants.ARG] = 0
            self.curr_var_count_table[constants.VAR] = 0

    def define(self, name, sym_type, kind):
            ind = self.curr_var_count_table[kind]
            self.curr_var_count_table[kind] += 1
            if kind in [constants.STATIC, constants.FIELD]:
                scope = constants.CLASS_LEVEL
                self.curr_class_symbol_table[name] = \
                    {'name': name, 'type': sym_type, 'kind': kind, 'index': ind, 'scope': scope}
            else:
                scope = constants.SUBROUTINE_LEVEL
                self.curr_subroutine_symbol_table[name] = \
                    {'name': name, 'type': sym_type, 'kind': kind, 'index': ind, 'scope': scope}

    def var_count(self, var_kind):
        return self.curr_var_count_table[var_kind]

    def kind_of(self, ident):
        if ident in self.curr_subroutine_symbol_table:
            return self.curr_subroutine_symbol_table[ident]['kind']
        elif ident in self.curr_class_symbol_table:
            return self.curr_class_symbol_table[ident]['kind']
        else:
            return None

    def type_of(self, ident):
        if ident in self.curr_subroutine_symbol_table:
            return self.curr_subroutine_symbol_table[ident]['type']
        elif ident in self.curr_class_symbol_table:
            return self.curr_class_symbol_table[ident]['type']
        else:
            return None

    def index_of(self, ident):
        if ident in self.curr_subroutine_symbol_table:
            return self.curr_subroutine_symbol_table[ident]['index']
        elif ident in self.curr_class_symbol_table:
            return self.curr_class_symbol_table[ident]['index']
        else:
            return None

