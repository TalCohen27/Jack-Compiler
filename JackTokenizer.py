from constants import Keyword, TokenType, Symbol, Operator

class JackTokenizer:
    def __init__(self, _filepath):
        self.file_path = _filepath
        self.tokens = []
        self.all_keywords = [keyword.value for keyword in Keyword]
        self.all_symbols = [symbol.value for symbol in Symbol]
        self.curr_line = ""
        self.curr_line_index = 0
        self.sepcialChars = {'&': Operator.AMPERSAND.value,
                             '<': Operator.LEFT_ARROW.value, '>': Operator.RIGHT_ARROW.value}

    def Tokenize(self):
        with open(self.file_path, 'r') as jack_file:
            self.curr_line = jack_file.readline()
            while self.curr_line:
                self.curr_line = (self.curr_line.split(r'//', 1)[0]).strip()
                self.curr_line = (self.curr_line.split(r'/**', 1)[0]).strip()
                self.curr_line = (self.curr_line.split(r'*/', 1)[0]).strip()
                self.curr_line_index = 0
                if self.curr_line and self.curr_line[0] != '*':
                    while self.curr_line_index in range(len(self.curr_line)):
                        chara = self.curr_line[self.curr_line_index]
                        if chara == ' ':
                            self.skipWhiteSpaces()
                        elif chara in self.all_symbols:
                            if chara in [Symbol.AMPERSAND.value, Symbol.LEFT_ARROW.value, Symbol.RIGHT_ARROW.value]:
                                self.tokens.append(Token(TokenType.SYMBOL.value, self.sepcialChars[chara]))
                            else:
                                self.tokens.append(Token(TokenType.SYMBOL.value, chara))
                            self.curr_line_index += 1
                        elif JackTokenizer.RepresentsInt(chara):
                            self.tokens.append(Token(TokenType.INT_CONST.value, self.tokenize_Int_Const()))
                        elif chara == '"':
                            self.curr_line_index += 1
                            self.tokens.append(Token(TokenType.STRING_CONST.value, self.tokenize_string_const()))
                        else:
                            word = self.tokenizeKeywordOrIdent()
                            if word in self.all_keywords:
                                self.tokens.append(Token(TokenType.KEYWORD.value, word))
                            else:
                                self.tokens.append((Token(TokenType.IDENTIFIER.value, word)))
                self.curr_line = jack_file.readline()
        return self.tokens

    def skipWhiteSpaces(self):
        while self.curr_line[self.curr_line_index] == ' ':
            self.curr_line_index += 1

    def tokenizeKeywordOrIdent(self):
        res = ''
        while self.curr_line_index < len(self.curr_line) and \
                JackTokenizer.LegalChar(self.curr_line[self.curr_line_index]):
            res += self.curr_line[self.curr_line_index]
            self.curr_line_index += 1
        return res

    def tokenize_string_const(self):
        string_const = ''
        while self.curr_line_index < len(self.curr_line) and \
                self.curr_line[self.curr_line_index] != '"':
            string_const += self.curr_line[self.curr_line_index]
            self.curr_line_index += 1
        self.curr_line_index += 1
        return string_const

    def tokenize_Int_Const(self):
        number = self.curr_line[self.curr_line_index]
        self.curr_line_index += 1
        while self.curr_line_index < len(self.curr_line) and \
                JackTokenizer.RepresentsInt(self.curr_line[self.curr_line_index]):
            number += self.curr_line[self.curr_line_index]
            self.curr_line_index += 1
        return int(number)

    @staticmethod
    def RepresentsInt(c):
        try:
            int(c)
            return True
        except ValueError:
            return False

    @staticmethod
    def LegalChar(c):
        if not (c.isalnum() or c == '_'):
            return False
        return True


class Token:
    def __init__(self, _type, _token):
        self.type = _type
        self.token = _token

