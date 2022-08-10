class TestlangParser:
    def __init__(self):
        self._pos = 0
        self._tokens = []

    @property
    def tok(self):
        return self._line[self._pos]

    @property
    def last_tok(self):
        if self._pos > 0:
            return self._line[self._pos - 1]
        raise Exception(f'Expected token before {self.tok}')

    @property
    def next_tok(self):
        if self._pos < len(self._line) - 1:
            return self._line[self._pos + 1]
        return None

    @property
    def next_toks(self):
        return self._line[self._pos + 1:]

    def accept(self, criteria = lambda tok: True):
        if criteria(self.next_tok):
            return True
        return False

    def expect(self, criteria = lambda tok: True):
        if self.accept(criteria):
            return True
        raise TypeError('Expected different token')

    def next(self):
        self._pos += 1

    def expr(self):
        tree = []
        if self.tok.name in ('ADD', 'SUB', 'MUL', 'DIV', 'ASSIGN', 'EQUALS'):
            op = self.tok.name
            expr1 = [self.last_tok.list()]
            self.next()
            expr2 = self.expr()
            tree = [op, expr1, expr2]
        else:
            if self.accept(lambda tok: (tok is not None) and tok.name not in ('CODEBLOCK', 'IF')):
                self.next()
                tree.append(self.expr())
            else:
                tree.append(self.tok.list())

        return tree

    def remove_whitespace(self):
        self._tokens = [tok for tok in self._tokens if tok.name not in ('TAB', 'SPACE')]

    def split_on_newline(self):
        new_toks = [[]]
        for tok in self._tokens:
            if tok.name == 'NEWLINE':
                new_toks.append([])
            else:
                new_toks[-1].append(tok)
        self._tokens = new_toks

    def parse(self, tokens):
        self._tokens = tokens
        tree = []

        self.remove_whitespace()
        self.split_on_newline()

        for line in self._tokens:
            self._line = line
            self._pos = 0
            while self._pos < len(line):
                if self.tok.name in ('ADD', 'MUL', 'DIV', 'SUB', 'ASSIGN', 'EQUALS'):
                    tree.append(self.expr())
                elif self.tok.name == 'PRINT':
                    name = self.tok.name
                    self.next()
                    expr = self.expr()
                    tree.append([name, expr])
                    self.next()
                elif self.tok.name == 'IF':
                    name = self.tok.name
                    self.next()
                    condition = self.expr()
                    self.next()
                    execution = [self.tok.list()]
                    tree.append([name, condition, execution])
                    self.next()
                else:
                    self.next()

        return tree

if __name__ == '__main__':
    from testlang import lexer
    from pprint import pprint

    tlexer = lexer.TestlangLexer()
    tparser = TestlangParser()

    toks = tlexer.lex(input('$'))
    pprint(toks)

    tree = tparser.parse(toks)
    pprint(tree)
