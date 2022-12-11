INTENGER, PLUS, MINUS, MULT, DIV, EOF, LPRN, RPRN = (
    'INTENGER',
    'PLUS',
    'MINUS',
    'MULT',
    'DIV',
    'EOF',
    'LPRN',
    'RPRN'
)

class Token(object):

    def __init__(self,type,value) -> None:
        self.type = type
        self.value = value
    
    def __str__(self) -> str:
        return 'Token({type},{value})'.format(
            type = self.type,
            value = repr(self.value)
        )

    def __repr__(self) -> str:
        return self.__str__

class Lexer(object):

    def __init__(self,text) -> None:
        self.text = text
        self.pos = 0
        self.current_token = None
        self.char = self.text[self.pos]

    def error(self):
        raise Exception("ERROR!!!")

    def skip_space(self):
        while self.char is not None and self.char ==' ':
            self.advance()

    def advance(self):
        self.pos += 1

        if self.pos > len(self.text) - 1:
            self.char = None
        else:
            self.char = self.text[self.pos]
    
    def intenger(self):

        result = ''

        while self.char is not None and '0'<=self.char<='9':
            result += self.char
            self.advance()
        
        return int(result)

    def get_next_token(self):
        while self.char is not None:
            if self.char ==' ':
                self.skip_space()
                continue
            
            if ord('0')<= ord(self.char) <= ord('9'):
                return Token(INTENGER,self.intenger())
        
            if self.char == '+':
                self.advance()
                return Token(PLUS,'+')

            if self.char == '-':
                self.advance()
                return Token(MINUS,'-')

            if self.char == '*':
                self.advance()
                return Token(MULT,'*')
            
            if self.char == '/':
                self.advance()
                return Token(DIV,'/')
            
            if self.char == '(':
                self.advance()
                return Token(LPRN,'(')
            
            if self.char == ')':
                self.advance()
                return Token(RPRN,')')

            self.error()

        return Token(EOF, None)
    
class Interpreter(object):

    def __init__(self,lexer) -> None:
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error():
        raise Exception('Interperter Error!')

    def eat(self,token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token

        if token.type == INTENGER:
            self.eat(INTENGER)
            return token.value
        elif token.type == LPRN:
            self.eat(LPRN)
            result = self.expr()
            self.eat(RPRN)
            return result
    
    def term(self):

        result = self.factor()

        while self.current_token.type in (MULT, DIV):
            token = self.current_token
            if token.type == MULT:
                self.eat(MULT)
                result = result * self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                result = result / self.factor()

        return result

    def expr(self):

        result = self.term()
    
        while self.current_token.type in (PLUS,MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()

        return result

def main(): 

    while True:
        try:
            text = input('calc>>>')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        inter = Interpreter(lexer)

        result = inter.expr()
        print(result)

if __name__ == '__main__':
    main()