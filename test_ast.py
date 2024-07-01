import ast_builder
import decode as d


def test_value_expression():
    token = d.ValueToken(value=5)
    expression = ast_builder.ValueExpression(value=5)
    assert ast_builder.build_ast([token]) == expression


def test_variable_expression():
    token = d.VariableToken(variable=3)
    expression = ast_builder.VariableExpression(variable=3)
    assert ast_builder.build_ast([token]) == expression


def test_unary_expression():
    token = d.UnaryOperatorToken(operator=d.UnaryOperator.NOT)
    operand = d.ValueToken(value=True)
    expression = ast_builder.UnaryExpression(
        operator=d.UnaryOperator.NOT, operand=ast_builder.ValueExpression(value=True)
    )
    assert ast_builder.build_ast([token, operand]) == expression


def test_binary_expression():
    token = d.BinaryOperatorToken(operator=d.BinaryOperator.ADD)
    left = d.ValueToken(value=3)
    right = d.ValueToken(value=5)
    expression = ast_builder.BinaryExpression(
        operator=d.BinaryOperator.ADD,
        left=ast_builder.ValueExpression(value=3),
        right=ast_builder.ValueExpression(value=5),
    )
    assert ast_builder.build_ast([token, left, right]) == expression


def test_lambda_expression():
    token = d.LambdaToken(variable=3)
    body = d.ValueToken(value=5)
    expression = ast_builder.LambdaExpression(
        variable=3, body=ast_builder.ValueExpression(value=5)
    )
    assert ast_builder.build_ast([token, body]) == expression


def test_if_expression():
    token = d.IfToken()
    condition = d.ValueToken(value=True)
    then_branch = d.ValueToken(value=3)
    else_branch = d.ValueToken(value=5)
    expression = ast_builder.IfExpression(
        condition=ast_builder.ValueExpression(value=True),
        then_branch=ast_builder.ValueExpression(value=3),
        else_branch=ast_builder.ValueExpression(value=5),
    )
    assert (
        ast_builder.build_ast([token, condition, then_branch, else_branch])
        == expression
    )


def test_nested_lambda_expression():
    tokens: list[d.Token] = [
        d.BinaryOperatorToken(operator=d.BinaryOperator.APPLY),
        d.BinaryOperatorToken(operator=d.BinaryOperator.APPLY),
        d.LambdaToken(variable=1),
        d.LambdaToken(variable=2),
        d.BinaryOperatorToken(operator=d.BinaryOperator.ADD),
        d.VariableToken(variable=1),
        d.VariableToken(variable=2),
        d.ValueToken(value=3),
        d.ValueToken(value=4),
    ]

    expression = ast_builder.BinaryExpression(
        operator=d.BinaryOperator.APPLY,
        left=ast_builder.BinaryExpression(
            operator=d.BinaryOperator.APPLY,
            left=ast_builder.LambdaExpression(
                variable=1,
                body=ast_builder.LambdaExpression(
                    variable=2,
                    body=ast_builder.BinaryExpression(
                        operator=d.BinaryOperator.ADD,
                        left=ast_builder.VariableExpression(variable=1),
                        right=ast_builder.VariableExpression(variable=2),
                    ),
                ),
            ),
            right=ast_builder.ValueExpression(value=3),
        ),
        right=ast_builder.ValueExpression(value=4),
    )

    assert ast_builder.build_ast(tokens) == expression
