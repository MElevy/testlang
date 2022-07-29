import re

class Token:
    def __init__(self, value, name, span):
        self.value = value
        self.span = span
        self.name = name

    def list(self):
        return [self.name, self.value]

    def __repr__(self):
        return 'Token(value = %s, name = \"%s\", span = %s)' % (self.value, self.name, self.span)

class Lexer:
    def __init__(self, definitions, token_unrecognized):
        self.definitions = definitions
        self.token_unrecognized = token_unrecognized
        self.lineno = 0

    def lex(self, text):
        i = 0
        tokens = []
        while i < len(text):
            for definition in self.definitions:
                if (match := re.match(definition[1], text[i:])):
                    span = match.span()
                    res = definition[2](Token(text[i:i + span[1]], definition[0], (i, i + span[1])))
                    i += span[1]
                    if res != None: tokens.append(res)
                    break
            else:
                self.token_unrecognized(Token(text[i], 'UNRECOGNIZED', (i, i + 1)))
                i += 1

        return tokens

if __name__ == '__main__':
    from pprint import pprint
    def HANDLE_expr(t):
        t.value = eval(t.value)
        return t
    def HANDLE_t(t): return t
    def IGNORE_t(t): pass
    def HANDLE_TOKNOTFOUND(t_val): raise Exception('Could not handle, ' + t_val)
    new_lexer = Lexer([
        ('EXPR', r'(\d+\.\d*|\d+)(( *)((\+|\*|/|-|==)( *)(\d+\.\d*|\d+)))*', HANDLE_expr),
        ('COMMENT', r'#\.*', IGNORE_t),
        ('WHITESPACE', r'( |\t)+', IGNORE_t)
    ], HANDLE_TOKNOTFOUND)
    pprint(new_lexer.lex(input('> ')))
