from dataclasses import dataclass
import decode as d


class Expression:
    pass


@dataclass
class VariableExpression(Expression):
    variable: int


@dataclass
class ValueExpression(Expression):
    value: str | int | bool | VariableExpression


@dataclass
class UnaryExpression(Expression):
    operator: d.UnaryOperator
    operand: Expression


@dataclass
class BinaryExpression(Expression):
    operator: d.BinaryOperator
    left: Expression
    right: Expression


@dataclass
class LambdaExpression(Expression):
    variable: int
    body: Expression


@dataclass
class IfExpression(Expression):
    condition: Expression
    then_branch: Expression
    else_branch: Expression


def build_ast(tokens: list[d.Token]) -> Expression:
    if not tokens:
        raise ValueError("Empty token list")

    token = tokens.pop(0)

    if isinstance(token, d.ValueToken):
        return ValueExpression(value=token.value)

    if isinstance(token, d.VariableToken):
        return VariableExpression(variable=token.variable)

    if isinstance(token, d.UnaryOperatorToken):
        operand = build_ast(tokens)
        return UnaryExpression(operator=token.operator, operand=operand)

    if isinstance(token, d.BinaryOperatorToken):
        left = build_ast(tokens)
        right = build_ast(tokens)
        return BinaryExpression(operator=token.operator, left=left, right=right)

    if isinstance(token, d.LambdaToken):
        body = build_ast(tokens)
        return LambdaExpression(variable=token.variable, body=body)

    if isinstance(token, d.IfToken):
        condition = build_ast(tokens)
        then_branch = build_ast(tokens)
        else_branch = build_ast(tokens)
        return IfExpression(
            condition=condition, then_branch=then_branch, else_branch=else_branch
        )

    raise ValueError(f"Unknown token {token}")
