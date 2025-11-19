from fractions import Fraction
from enum import Enum
from abc import ABC
from .auxiliar import decimal_a_fraccion

allowed_commands: list[str] = [
    "frac",
    "left",
    "right",
    "pi"
]


class TokenType(Enum):
    COMMAND = 1,

    # Operators
    SUM = 3,
    SUB = 4,
    # MULT = 5, This is done with the \cdot command
    # DIV = 6, This already will be expressed as a fraction
    POW = 9

    # Special Characters
    OPEN_PARENTHESES = 7,
    CLOSE_PARENTHESES = 8,

    # Braces
    OPEN_BRACE = 11,
    CLOSE_BRACE = 12,

    # Other tokens
    DIGIT = 9,
    PERIOD = 0

    EOF = 5


class Token:
    def __init__(self, _type: TokenType, value: str | None = None):
        self.type = _type
        self.value: str = value if value is not None else ""

    def __repr__(self) -> str:
        return f"Token({self.type!r}, {self.value!r})"


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos: int = 0
        self.current_char: str | None = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.text and self.pos < len(
            self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def command(self) -> Token:
        # We are at a backslash, consume '\' then letters
        self.advance()  # skip '\'
        start = self.pos
        while self.current_char is not None and self.current_char.isalpha():
            self.advance()
        cmd = self.text[start:self.pos]
        if cmd not in allowed_commands:
            raise ValueError(f"Unsupported LaTeX command '\\{cmd}'")
        return Token(TokenType.COMMAND, cmd)

    def get_token(self) -> Token:
        while self.current_char is not None and self.current_char.isspace():
            self.skip_whitespace()

        if self.current_char is None:
            return Token(TokenType.EOF)

        if self.current_char.isdigit():
            return Token(TokenType.DIGIT, self.current_char)
        else:
            tok: TokenType | None = None

            match self.current_char:
                case '\\':
                    return self.command()
                case '{':
                    tok = TokenType.OPEN_BRACE
                case '}':
                    tok = TokenType.CLOSE_BRACE
                case '(':
                    tok = TokenType.OPEN_PARENTHESES
                case ')':
                    tok = TokenType.CLOSE_PARENTHESES
                case '+':
                    tok = TokenType.SUM
                case '-':
                    tok = TokenType.SUB
                case '^':
                    tok = TokenType.POW
                case '.':
                    tok = TokenType.PERIOD

            if tok is not None:
                return Token(tok)
            else:
                raise ValueError(f"Unrecognized token: {self.current_char}")

    def tokenize(self) -> list[Token]:
        token_list: list[Token] = []

        while self.current_char is not None:
            t = self.get_token()
            token_list.append(t)

        return token_list


# Clase abstracta
class AST(ABC):
    pass


class NumberAST(AST):
    def __init__(self, value: Fraction) -> None:
        self.value: Fraction = value

    def __str__(self) -> str:
        return self.value.__str__()

    def __repr__(self) -> str:
        return f"Number({self.value})"


class OperationTypes(Enum):
    SUM = 1,
    SUBTRACT = 2,
    MULTIPLY = 3,
    DIVIDE = 4,
    POWER = 5


allowed_unaries: list[OperationTypes] = [
    OperationTypes.SUBTRACT
]


class BinOpAST(AST):
    def __init__(self, lhs: AST, op: OperationTypes, rhs: AST) -> None:
        self.lhs: AST = lhs
        self.op: OperationTypes = op
        self.rhs: AST = rhs

    def __repr__(self) -> str:
        return f"BinOp({self.lhs}, {self.op}, {self.rhs})"


class UnaryOpAST(AST):
    def __init__(self, part: AST, op: OperationTypes) -> None:
        if op not in allowed_unaries:
            raise ValueError(f"Operator not allowed as unary: {op}")
        self.op: OperationTypes = op
        self.part: AST = part


class Parser:
    def __init__(self, text: str) -> None:
        lexer = Lexer(text)
        self.tokens: list[Token] = lexer.tokenize()
        self.current_pos: int = 0
        self.current_token: Token | None = self.tokens[self.current_pos] if self.tokens and self.current_pos < len(
            self.tokens) else None

    def advance(self):
        self.current_pos += 1
        self.current_token = self.tokens[self.current_pos] if self.tokens and self.current_pos < len(
            self.tokens) else None

    def eat_token(self, type: TokenType):
        if self.current_token is None or self.current_token.type != type:
            raise Exception(
                f"Was expecting token of type {type}")

        self.advance()

    # Long form argument groups and builds numbers transforming them into their full version
    # Short form operands let stuff like \frac45 consider 4 and 5 as different arguments,
    # long form will group them together to form 45
    def parse_operand(self, long_form: bool = True) -> AST:
        if self.current_token is None:
            raise Exception("Expected Operand")

        match self.current_token.type:
            case TokenType.DIGIT:
                if long_form:
                    return self.collapse_number()
                else:
                    return NumberAST(Fraction(int(self.current_token.value)))

    def collapse_number(self) -> AST:
        # Create number using a series of tokens
        saw_dot: bool = False

        while self.current_token is not None and \
                (self.current_token.type == TokenType.DIGIT or self.current_token.type == TokenType.PERIOD):

    def parse_expression(self) -> AST:
        pass

        # # ---------- AST Nodes ----------

        # class AST:
        #     pass

        # class Number(AST):
        #     def __init__(self, value: int):
        #         self.value = value

        #     def __repr__(self):
        #         return f"Number({self.value})"

        # class FractionNode(AST):
        #     def __init__(self, numerator: AST, denominator: AST):
        #         self.numerator = numerator
        #         self.denominator = denominator

        #     def __repr__(self):
        #         return f"FractionNode({self.numerator!r}, {self.denominator!r})"

        # class UnaryOp(AST):
        #     def __init__(self, op: str, operand: AST):
        #         self.op = op
        #         self.operand = operand

        #     def __repr__(self):
        #         return f"UnaryOp({self.op!r}, {self.operand!r})"

        # class BinaryOp(AST):
        #     def __init__(self, left: AST, op: str, right: AST):
        #         self.left = left
        #         self.op = op
        #         self.right = right

        #     def __repr__(self):
        #         return f"BinaryOp({self.left!r}, {self.op!r}, {self.right!r})"

        # # ---------- Parser (recursive descent) ----------

        # class Parser:
        #     def __init__(self, text: str):
        #         self.lexer = Lexer(text)
        #         self.current_token = self.lexer.get_next_token()

        #     def eat(self, token_type: str):
        #         if self.current_token.type == token_type:
        #             self.current_token = self.lexer.get_next_token()
        #         else:
        #             raise ValueError(
        #                 f"Expected token {token_type}, got {self.current_token.type}"
        #             )

        #     def parse(self) -> AST:
        #         node = self.expr()
        #         if self.current_token.type != "EOF":
        #             raise ValueError(f"Unexpected token at end: {self.current_token}")
        #         return node

        #     # expr : term (('PLUS' | 'MINUS') term)*
        #     def expr(self):
        #         node = self.term()
        #         while self.current_token.type in ("PLUS", "MINUS"):
        #             op = self.current_token
        #             self.eat(op.type)
        #             right = self.term()
        #             node = BinaryOp(node, op.value, right)
        #         return node

        #     # term : unary (('STAR' | 'SLASH') unary)*
        #     def term(self):
        #         node = self.unary()
        #         while self.current_token.type in ("STAR", "SLASH"):
        #             op = self.current_token
        #             self.eat(op.type)
        #             right = self.unary()
        #             node = BinaryOp(node, op.value, right)
        #         return node

        #     # unary : ('PLUS' | 'MINUS') unary | power
        #     def unary(self):
        #         if self.current_token.type in ("PLUS", "MINUS"):
        #             op = self.current_token
        #             self.eat(op.type)
        #             operand = self.unary()
        #             return UnaryOp(op.value, operand)
        #         return self.power()

        #     # power : primary ('CARET' unary)?
        #     def power(self):
        #         node = self.primary()
        #         if self.current_token.type == "CARET":
        #             self.eat("CARET")
        #             right = self.unary()
        #             node = BinaryOp(node, '^', right)
        #         return node

        #     # primary : NUMBER | FRAC-group | (LPAREN expr RPAREN) | (LBRACE expr RBRACE)
        #     def primary(self):
        #         tok = self.current_token

        #         if tok.type == "NUMBER":
        #             self.eat("NUMBER")
        #             return Number(tok.value)

        #         if tok.type == "FRAC":
        #             return self.frac()

        #         if tok.type == "LPAREN":
        #             self.eat("LPAREN")
        #             node = self.expr()
        #             self.eat("RPAREN")
        #             return node

        #         if tok.type == "LBRACE":
        #             # treat {...} like parentheses at top-level too
        #             return self.braced_expr()

        #         raise ValueError(f"Unexpected token in primary(): {tok}")

        #     # braced_expr : LBRACE expr RBRACE
        #     def braced_expr(self):
        #         self.eat("LBRACE")
        #         node = self.expr()
        #         self.eat("RBRACE")
        #         return node

        #     # frac : 'FRAC' group group
        #     # group : '{' expr '}' | primary (single token)
        #     def frac(self):
        #         self.eat("FRAC")
        #         num = self.frac_group()
        #         den = self.frac_group()
        #         return FractionNode(num, den)

        #     def frac_group(self):
        #         if self.current_token.type == "LBRACE":
        #             return self.braced_expr()
        #         # unbraced: LaTeX-style single token argument
        #         return self.primary()

        # # ---------- Evaluation to Fraction ----------

        # def eval_ast(node: AST) -> Fraction:
        #     if isinstance(node, Number):
        #         return Fraction(node.value, 1)

        #     if isinstance(node, FractionNode):
        #         num = eval_ast(node.numerator)
        #         den = eval_ast(node.denominator)
        #         if den == 0:
        #             raise ZeroDivisionError("Division by zero in \\frac")
        #         return num / den

        #     if isinstance(node, UnaryOp):
        #         val = eval_ast(node.operand)
        #         if node.op == '+':
        #             return val
        #         elif node.op == '-':
        #             return -val
        #         else:
        #             raise ValueError(f"Unknown unary op {node.op}")

        #     if isinstance(node, BinaryOp):
        #         left = eval_ast(node.left)
        #         right = eval_ast(node.right)
        #         if node.op == '+':
        #             return left + right
        #         elif node.op == '-':
        #             return left - right
        #         elif node.op == '*':
        #             return left * right
        #         elif node.op == '/':
        #             if right == 0:
        #                 raise ZeroDivisionError("Division by zero")
        #             return left / right
        #         elif node.op == '^':
        #             # exponent should be integer ideally
        #             if not (right.denominator == 1):
        #                 raise ValueError("Fractional exponents not supported")
        #             return left ** right.numerator
        #         else:
        #             raise ValueError(f"Unknown binary op {node.op}")

        #     raise ValueError(f"Unknown AST node type: {type(node)}")

        # # ---------- Convert AST back to Python 'Fraction(...)' expression ----------

        # def ast_to_python(node: AST) -> str:
        #     if isinstance(node, Number):
        #         return f"Fraction({node.value}, 1)"

        #     if isinstance(node, FractionNode):
        #         num = ast_to_python(node.numerator)
        #         den = ast_to_python(node.denominator)
        #         return f"({num} / {den})"

        #     if isinstance(node, UnaryOp):
        #         expr = ast_to_python(node.operand)
        #         if node.op == '-':
        #             return f"(-{expr})"
        #         return f"(+{expr})"

        #     if isinstance(node, BinaryOp):
        #         left = ast_to_python(node.left)
        #         right = ast_to_python(node.right)
        #         if node.op == '^':
        #             return f"({left} ** {right})"
        #         return f"({left} {node.op} {right})"

        #     raise ValueError(f"Unknown AST node type: {type(node)}")

        # # ---------- Convenience wrappers ----------

        # def parse_fraction_expr(text: str) -> Fraction:
        #     """
        #     Parse a LaTeX-ish math string and return a Python Fraction value.
        #     """
        #     ast = Parser(text).parse()
        #     return eval_ast(ast)

        # def to_python_fraction_expr(text: str) -> str:
        #     """
        #     Parse and return a string of Python code using Fraction(...).
        #     """
        #     ast = Parser(text).parse()
        #     return ast_to_python(ast)

        # # ---------- Demo ----------

        # if __name__ == "__main__":
        #     examples = [
        #         r"\frac43",
        #         r"\frac{4}{3}",
        #         r"5 + 6",
        #         r"\frac12 + \frac{3}{4}",
        #         r"3/4 + 1/2",
        #         r"-\frac{1}{2} * (3 + 5)",
        #         r"(\frac{2}{3})^2",
        #     ]

        #     for s in examples:
        #         value = parse_fraction_expr(s)
        #         code = to_python_fraction_expr(s)
        #         print(f"{s!r} => {value}   (Python: {code})")
