from fractions import Fraction
from enum import Enum
from abc import ABC, abstractmethod
from .auxiliar import decimal_a_fraccion, array_top


class AllowedCommands(Enum):
    frac = 1
    left = 2
    right = 3
    pi = 4
    cdot = 5


command_map: dict[str, AllowedCommands] = {
    "frac": AllowedCommands.frac,
    "left": AllowedCommands.left,
    "right": AllowedCommands.right,
    "pi": AllowedCommands.pi,
    "cdot": AllowedCommands.cdot
}


class TokenType(Enum):
    COMMAND = 1

    # Operators
    SUM = 2
    MINUS = 3
    POW = 4
    SUBSCRIPT = 5

    # Special Characters
    LPARENTHESES = 6
    RPARENTHESES = 7

    # Braces
    LBRACE = 8
    RBRACE = 9

    # Other tokens
    DIGIT = 10
    PERIOD = 11

    CHAR = 12

    EOF = 13


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
        if cmd not in command_map:
            raise ValueError(f"Unsupported LaTeX command '\\{cmd}'")
        return Token(TokenType.COMMAND, cmd)

    def get_token(self) -> Token:
        while self.current_char is not None and self.current_char.isspace():
            self.skip_whitespace()

        if self.current_char is None:
            return Token(TokenType.EOF)

        if self.current_char.isdigit():
            ch = self.current_char
            self.advance()
            return Token(TokenType.DIGIT, ch)

        if self.current_char.isalpha():
            ch = self.current_char
            self.advance()
            return Token(TokenType.CHAR, ch)

        tok: TokenType | None = None
        match self.current_char:
            case '\\':
                return self.command()
            case '{':
                tok = TokenType.LBRACE
            case '}':
                tok = TokenType.RBRACE
            case '(':
                tok = TokenType.LPARENTHESES
            case ')':
                tok = TokenType.RPARENTHESES
            case '+':
                tok = TokenType.SUM
            case '-':
                tok = TokenType.MINUS
            case '^':
                tok = TokenType.POW
            case '.':
                tok = TokenType.PERIOD
            case '_':
                tok = TokenType.SUBSCRIPT

        if tok is not None:
            ch = self.current_char
            self.advance()
            # important: store the character itself as `value` (esp. for '.')
            return Token(tok, ch)

        raise ValueError(f"Unrecognized token: {self.current_char}")

    def tokenize(self) -> list[Token]:
        token_list: list[Token] = []

        while self.current_char is not None:
            t = self.get_token()
            if t.type == TokenType.EOF:
                break
            token_list.append(t)

        return token_list


# Clase abstracta
class AST(ABC):
    pass


class ICommandParser(ABC):
    @abstractmethod
    def parsefrac(self) -> AST:
        pass

    @abstractmethod
    def parseleft(self) -> AST:
        pass

    @abstractmethod
    def parseright(self) -> AST:
        pass

    @abstractmethod
    def parsepi(self) -> AST:
        pass


class NumberAST(AST):
    def __init__(self, value: Fraction) -> None:
        self.value: Fraction = value

    def __str__(self) -> str:
        return self.value.__str__()

    def __repr__(self) -> str:
        return f"Number({self.value})"


class VariableAST(AST):
    def __init__(self, id: str) -> None:
        self.id = id

    def __str__(self) -> str:
        return self.id.__str__()

    def __repr__(self) -> str:
        return f"Variable({self.id})"


class OperationTypes(Enum):
    SUM = 1
    SUBTRACT = 2
    MULTIPLY = 3
    DIVIDE = 4
    POWER = 5


allowed_unaries: list[OperationTypes] = [
    OperationTypes.SUBTRACT
]

operation_precedences: dict[OperationTypes, int] = {
    OperationTypes.SUM: 13,
    OperationTypes.SUBTRACT: 13,
    OperationTypes.MULTIPLY: 14,
    OperationTypes.DIVIDE: 14,
    OperationTypes.POWER: 15
}


def precedence(op: OperationTypes):
    return operation_precedences[op]


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

    def __repr__(self) -> str:
        return f"UnaryOp({self.op}, {self.part})"


class Parser(ICommandParser):
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

    def eat_token(self, type: TokenType) -> str:
        if self.current_token is None or self.current_token.type != type:
            raise Exception(
                f"Was expecting token of type {type}")
        value = self.current_token.value
        self.advance()

        return value

    def eat_command(self) -> AllowedCommands:
        return command_map[self.eat_token(TokenType.COMMAND)]

    # Operator precedence (checks if an operator exists even)
    def parse_operator(self) -> OperationTypes | None:
        tok = self.current_token
        if tok is None:
            return None

        match tok.type:
            case TokenType.COMMAND:
                cmd = command_map[tok.value]
                if cmd == AllowedCommands.cdot:
                    self.eat_token(TokenType.COMMAND)
                    return OperationTypes.MULTIPLY
            case TokenType.POW:
                self.eat_token(TokenType.POW)
                return OperationTypes.POWER
            case TokenType.SUM:
                self.eat_token(TokenType.SUM)
                return OperationTypes.SUM
            case TokenType.MINUS:
                self.eat_token(TokenType.MINUS)
                return OperationTypes.SUBTRACT
        return None

    # Long form argument groups and builds numbers transforming them into their full version
    # Short form operands let stuff like \frac45 consider 4 and 5 as different arguments,
    # long form will group them together to form 45
    def get_token_as_operand(self, long_form: bool = True) -> AST | None:
        tok = self.current_token
        if tok is None:
            return None

        # Check if we're on an operator (Unary parsing)
        op = self.parse_operator()
        if op is not None:
            dest: AST | None = self.parse_operand()
            if dest is None:
                raise Exception("Expected operand after unary operator")
            return UnaryOpAST(dest, op)

        # Commands that behave like operands: \frac, \pi, \left...
        if tok.type == TokenType.COMMAND:
            cmd: AllowedCommands = command_map[tok.value]
            match cmd:
                case AllowedCommands.frac:
                    self.eat_token(TokenType.COMMAND)
                    return self.parsefrac()
                case AllowedCommands.left:
                    self.eat_token(TokenType.COMMAND)
                    return self.parseleft()
                case AllowedCommands.pi:
                    self.eat_token(TokenType.COMMAND)
                    return self.parsepi()
            return None

        match tok.type:
            case TokenType.DIGIT:
                if long_form:
                    return self.collapse_number()
                else:
                    d = self.eat_token(TokenType.DIGIT)
                    return NumberAST(Fraction(int(d)))

            case TokenType.CHAR:
                c = self.eat_token(TokenType.CHAR)
                return VariableAST(c)

            case TokenType.LPARENTHESES:
                self.eat_token(TokenType.LPARENTHESES)
                expr = self.parse_expression()
                self.eat_token(TokenType.RPARENTHESES)
                return expr

            case TokenType.LBRACE:
                self.eat_token(TokenType.LBRACE)
                expr = self.parse_expression()
                self.eat_token(TokenType.RBRACE)
                return expr
        return None

    def parse_operand(self, long_form=True) -> AST:
        r: AST | None = self.get_token_as_operand(long_form)
        if r is None:
            raise Exception("Expected Operand")
        return r

    def collapse_number(self) -> AST:
        chars: list[str] = []

        while (
            self.current_token is not None
            and self.current_token.type in (TokenType.DIGIT, TokenType.PERIOD)
        ):
            chars.append(self.current_token.value)
            self.advance()

        num_str = "".join(chars)      # e.g. "12.5"
        frac = decimal_a_fraccion(num_str)
        return NumberAST(frac)

    def parsefrac(self) -> AST:
        """
        Assumes '\\frac' has already been consumed.

        Supports:
            - \\frac12  (short form: single-digit operands)
            - \\frac{1}{2}  (long form: full expressions)
        """

        numerator = self.parse_operand(long_form=False)
        denominator = self.parse_operand(long_form=False)

        return BinOpAST(numerator, OperationTypes.DIVIDE, denominator)

    def parsepi(self) -> AST:
        raise NotImplementedError("parsepi not implemented yet")

    def parseleft(self) -> AST:
        """
        Parse \\left( expr \\right) style groups.
        Assumes 'left' command has already been consumed.
        """
        if self.current_token is None or self.current_token.type != TokenType.LPARENTHESES:
            raise Exception("Expected '(' after \\left")

        self.eat_token(TokenType.LPARENTHESES)
        expr = self.parse_expression()

        # Right command
        m = self.eat_command()
        if m != AllowedCommands.right:
            raise Exception("Expected \\right directive")

        self.eat_token(TokenType.RPARENTHESES)
        return expr

    def parseright(self) -> AST:
        # Bare \right shouldn't really appear as an operand: treat as no-op.
        raise Exception("\\right without \\left directive")

    def expr_to_postfix(self) -> list[AST | OperationTypes]:
        opstack: list[OperationTypes] = []
        totalstack: list[AST | OperationTypes] = []

        # Obligatory first operand
        totalstack.append(self.parse_operand())

        m: OperationTypes | None = self.parse_operator()
        while m is not None:
            while len(opstack) != 0 and precedence(m) <= precedence(array_top(opstack)):
                last = opstack.pop()
                totalstack.append(last)
            opstack.append(m)

            totalstack.append(self.parse_operand())
            m = self.parse_operator()

        while len(opstack) != 0:
            totalstack.append(opstack.pop())

        return totalstack

    def postfix_parse(self, postfix: list[AST | OperationTypes]) -> AST:
        stack: list[AST] = []
        for item in postfix:
            if isinstance(item, AST):
                stack.append(item)
            else:
                # binary op: pop right then left
                if len(stack) < 2:
                    raise Exception("Invalid postfix expression")
                rhs = stack.pop()
                lhs = stack.pop()
                stack.append(BinOpAST(lhs, item, rhs))

        if len(stack) != 1:
            raise Exception("Invalid postfix expression")

        return stack[0]

    def parse_expression(self) -> AST:
        return self.postfix_parse(self.expr_to_postfix())

# ===== Evaluator =====


def eval_ast(node: AST, env: dict[str, Fraction] | None = None) -> Fraction:
    """
    Evaluate an AST into a Python Fraction.

    env: optional mapping from variable name -> Fraction
    """
    if env is None:
        env = {}

    # Numbers
    if isinstance(node, NumberAST):
        return node.value

    # Variables
    if isinstance(node, VariableAST):
        if node.id in env:
            return env[node.id]
        raise ValueError(f"Unknown variable '{node.id}' in expression")

    # Unary ops (only SUBTRACT is allowed by your AST)
    if isinstance(node, UnaryOpAST):
        val = eval_ast(node.part, env)
        if node.op == OperationTypes.SUBTRACT:
            return -val
        raise ValueError(f"Unsupported unary operation {node.op}")

    # Binary ops
    if isinstance(node, BinOpAST):
        left = eval_ast(node.lhs, env)
        right = eval_ast(node.rhs, env)

        if node.op == OperationTypes.SUM:
            return left + right
        if node.op == OperationTypes.SUBTRACT:
            return left - right
        if node.op == OperationTypes.MULTIPLY:
            return left * right
        if node.op == OperationTypes.DIVIDE:
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right
        if node.op == OperationTypes.POWER:
            # Require integer exponent
            if right.denominator != 1:
                raise ValueError(
                    "Non-integer exponent not supported for Fraction")
            exp = right.numerator
            return left ** exp

        raise ValueError(f"Unsupported binary operation {node.op}")

    raise TypeError(f"Unknown AST node type: {type(node)}")


def eval_latex(expr: str, env: dict[str, Fraction] | None = None) -> Fraction:
    """
    Convenience: parse a LaTeX-ish expression and evaluate to a Fraction.
    """
    parser = Parser(expr)
    ast = parser.parse_expression()
    return eval_ast(ast, env)
