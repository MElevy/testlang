class TestlangInterpreter:
    def __init__(self, lexer, parser, vars: dict = {}) -> None:
        self.vars = vars
        self.lexer = lexer
        self.parser = parser

    def interpret(self, tree, is_expr: bool = False):
        for node in tree:
            if node[0] in ('INT', 'FLOAT'):
                return node[1]
            elif node[0] == 'STRING':
                return node[1][1:-1]
            elif node[0] == 'NAME':
                if node[1] in self.vars.keys():
                    return self.vars[node[1]]
                raise Exception(f'{node[1]} is not a variable')
            elif node[0] == 'INPUT':
                return input()
            elif node[0] == 'CODEBLOCK':
                return node[1][1:-1]

            if node[0] == 'ADD':
                return self.interpret(node[1], True) + self.interpret(node[2], True)
            elif node[0] == 'MUL':
                return self.interpret(node[1], True) * self.interpret(node[2], True)
            elif node[0] == 'DIV':
                return self.interpret(node[1], True) / self.interpret(node[2], True)
            elif node[0] == 'SUB':
                return self.interpret(node[1], True) - self.interpret(node[2], True)
            elif node[0] == 'EQUALS':
                return self.interpret(node[1], True) == self.interpret(node[2], True)

            if node[0] == 'ASSIGN':
                self.vars[node[1][0][1]] = self.interpret(node[2], True)
                if is_expr: return self.vars[node[1][0][1]]

            if node[0] == 'IF':
                if self.interpret(node[1], True):
                    self.interpret(self.parser.parse(self.lexer.lex(self.interpret(node[2]))))

            if node[0] == 'PRINT':
                print((
                    str(self.interpret(node[1], True))
                        .replace('\\n', '\n')
                        .replace('\\\n', '\\n')
                        .replace('\\t', '\t')
                        .replace('\\\t', '\\t')
                ), end = '')

if __name__ == '__main__':
    from testlang import lexer, parser
    from pprint import pprint
    import sys

    tlexer = lexer.TestlangLexer()
    tparser = parser.TestlangParser()
    tinterpreter = TestlangInterpreter(tlexer, tparser)
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            code = f.read()

        toks = tlexer.lex(code)
        tree = tparser.parse(toks)
        res = tinterpreter.interpret(tree)
