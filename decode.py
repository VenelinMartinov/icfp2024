from __future__ import annotations

from enum import Enum, auto
from dataclasses import dataclass

import ascii_helpers


class TranslateException(Exception):
    pass


class WrongIndicatorException(TranslateException):
    pass


class UnhandledIndicatorException(TranslateException):
    pass


class Indicator(Enum):
    WRONG_INDICATOR = auto()
    BOOLEAN_TRUE = "T"
    BOOLEAN_FALSE = "F"
    INTEGER = "I"
    STRING = "S"
    UNARY = "U"
    BINARY = "B"
    IF = "?"
    LAMBDA = "L"
    VARIABLE = "v"


@dataclass
class Message:
    indicator: Indicator
    token_body: str

    @classmethod
    def from_string(cls, token: str) -> Message:
        return Message(indicator=Indicator(token[0]), token_body=token[1:])


@dataclass
class Token:
    pass


@dataclass
class ValueToken(Token):
    value: str | int | bool


class UnaryOperator(Enum):
    NEGATE = "-"
    NOT = "!"
    STRING_TO_INT = "#"
    INT_TO_STRING = "$"


@dataclass
class UnaryOperatorToken(Token):
    operator: UnaryOperator


class BinaryOperator(Enum):
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULO = "%"
    EQUAL = "="
    LESS_THAN = "<"
    GREATER_THAN = ">"
    AND = "&"
    OR = "|"
    STRING_CONCAT = "."
    TAKE_FIRST = "T"
    DROP_FIRST = "D"
    APPLY = "$"


@dataclass
class BinaryOperatorToken(Token):
    operator: BinaryOperator


@dataclass
class IfToken(Token):
    pass


@dataclass
class LambdaToken(Token):
    variable: int


@dataclass
class VariableToken(Token):
    variable: int


def parse_integer(msg: Message) -> ValueToken:
    if msg.indicator != Indicator.INTEGER:
        raise WrongIndicatorException(f"Wrong indicator {msg}")

    return ValueToken(value=ascii_helpers.decode_integer(msg.token_body))


def parse_string(msg: Message) -> ValueToken:
    if msg.indicator != Indicator.STRING:
        raise WrongIndicatorException(f"Wrong indicator {msg}")

    return ValueToken(value=ascii_helpers.decode_string(msg.token_body))


def parse_unary(msg: Message) -> UnaryOperatorToken:
    if msg.indicator != Indicator.UNARY:
        raise WrongIndicatorException(f"Wrong indicator {msg}")

    operator = UnaryOperator(msg.token_body[0])

    return UnaryOperatorToken(operator=operator)


def parse_binary(msg: Message) -> BinaryOperatorToken:
    if msg.indicator != Indicator.BINARY:
        raise WrongIndicatorException(f"Wrong indicator {msg}")

    operator = BinaryOperator(msg.token_body[0])

    return BinaryOperatorToken(operator=operator)


def parse_lambda(msg: Message) -> LambdaToken:
    if msg.indicator != Indicator.LAMBDA:
        raise WrongIndicatorException(f"Wrong indicator {msg}")

    return LambdaToken(variable=ascii_helpers.decode_integer(msg.token_body))


def parse_variable(msg: Message) -> VariableToken:
    if msg.indicator != Indicator.VARIABLE:
        raise WrongIndicatorException(f"Wrong indicator {msg}")

    return VariableToken(variable=ascii_helpers.decode_integer(msg.token_body))


def parse_token(token: str) -> Token:
    msg = Message.from_string(token)

    match msg.indicator:
        case Indicator.UNARY:
            return parse_unary(msg)
        case Indicator.BINARY:
            return parse_binary(msg)
        case Indicator.BOOLEAN_FALSE:
            return ValueToken(value=False)
        case Indicator.BOOLEAN_TRUE:
            return ValueToken(value=True)
        case Indicator.INTEGER:
            return parse_integer(msg)
        case Indicator.STRING:
            return parse_string(msg)
        case Indicator.IF:
            return IfToken()
        case Indicator.LAMBDA:
            return parse_lambda(msg)
        case Indicator.VARIABLE:
            return parse_variable(msg)
        case _:
            raise UnhandledIndicatorException(f"{msg}")


def main():
    pass


if __name__ == "__main__":
    main()
