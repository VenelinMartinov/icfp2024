from dataclasses import dataclass, field

import ast_builder
import ascii_helpers
import decode as d


class EvaluationException(Exception):
    pass


@dataclass
class Evaluator:
    context: dict[int, int | bool | str | ast_builder.Expression] = field(
        default_factory=dict
    )
    value_stack: list[int | bool | str | ast_builder.Expression] = field(
        default_factory=list
    )

    def eval_tokens(
        self, tokens: list[d.Token]
    ) -> int | bool | str | ast_builder.Expression:
        ast = ast_builder.build_ast(tokens)
        eval_res = self.eval_ast(ast)

        return eval_res

    def eval_ast(
        self, exp: ast_builder.Expression
    ) -> int | bool | str | ast_builder.Expression:
        if isinstance(exp, ast_builder.ValueExpression):
            if isinstance(exp.value, ast_builder.VariableExpression):
                return self.context[exp.value.variable]
            return exp.value

        if isinstance(exp, ast_builder.UnaryExpression):
            operand = self.eval_ast(exp.operand)
            if exp.operator == ast_builder.d.UnaryOperator.NOT:
                if not isinstance(operand, bool):
                    raise EvaluationException("Expected boolean operand")
                return not operand
            if exp.operator == ast_builder.d.UnaryOperator.NEGATE:
                if not isinstance(operand, int):
                    raise EvaluationException("Expected integer operand")
                return -operand
            if exp.operator == ast_builder.d.UnaryOperator.STRING_TO_INT:
                if not isinstance(operand, str):
                    raise EvaluationException("Expected string operand")
                enc_str = ascii_helpers.encode_string(operand)
                return ascii_helpers.decode_integer(enc_str)

            if exp.operator == ast_builder.d.UnaryOperator.INT_TO_STRING:
                if not isinstance(operand, int):
                    raise EvaluationException("Expected integer operand")
                enc_int = ascii_helpers.encode_integer(operand)
                enc_int = enc_int[::-1]
                return ascii_helpers.decode_string(enc_int)

        if isinstance(exp, ast_builder.BinaryExpression):
            if exp.operator == ast_builder.d.BinaryOperator.APPLY:
                self.value_stack.append(exp.right)
                return self.eval_ast(exp.left)

            left = self.eval_ast(exp.left)
            if isinstance(left, ast_builder.Expression):
                left = self.eval_ast(left)
            right = self.eval_ast(exp.right)
            if isinstance(right, ast_builder.Expression):
                right = self.eval_ast(right)
            if exp.operator == ast_builder.d.BinaryOperator.ADD:
                if not isinstance(left, int) or not isinstance(right, int):
                    raise EvaluationException("Expected integer operands")
                return left + right
            if exp.operator == ast_builder.d.BinaryOperator.SUBTRACT:
                if not isinstance(left, int) or not isinstance(right, int):
                    raise EvaluationException("Expected integer operands")
                return left - right
            if exp.operator == ast_builder.d.BinaryOperator.MULTIPLY:
                if not isinstance(left, int) or not isinstance(right, int):
                    raise EvaluationException("Expected integer operands")
                return left * right
            if exp.operator == ast_builder.d.BinaryOperator.DIVIDE:
                if not isinstance(left, int) or not isinstance(right, int):
                    raise EvaluationException("Expected integer operands")
                return int(left / right)

            if exp.operator == ast_builder.d.BinaryOperator.MODULO:
                if not isinstance(left, int) or not isinstance(right, int):
                    raise EvaluationException("Expected integer operands")
                return left - int(left / right) * right

            if exp.operator == ast_builder.d.BinaryOperator.EQUAL:
                return left == right

            if exp.operator == ast_builder.d.BinaryOperator.LESS_THAN:
                if not isinstance(left, int) or not isinstance(right, int):
                    raise EvaluationException("Expected integer operands")
                return left < right

            if exp.operator == ast_builder.d.BinaryOperator.GREATER_THAN:
                if not isinstance(left, int) or not isinstance(right, int):
                    raise EvaluationException("Expected integer operands")
                return left > right

            if exp.operator == ast_builder.d.BinaryOperator.AND:
                if not isinstance(left, bool) or not isinstance(right, bool):
                    raise EvaluationException("Expected boolean operands")
                return left and right

            if exp.operator == ast_builder.d.BinaryOperator.OR:
                if not isinstance(left, bool) or not isinstance(right, bool):
                    raise EvaluationException("Expected boolean operands")
                return left or right

            if exp.operator == ast_builder.d.BinaryOperator.STRING_CONCAT:
                if not isinstance(left, str) or not isinstance(right, str):
                    raise EvaluationException("Expected string operands")
                return left + right

            if exp.operator == ast_builder.d.BinaryOperator.TAKE_FIRST:
                if not isinstance(left, int) or not isinstance(right, str):
                    raise EvaluationException("Expected integer and string operands")
                return right[:left]

            if exp.operator == ast_builder.d.BinaryOperator.DROP_FIRST:
                if not isinstance(left, int) or not isinstance(right, str):
                    raise EvaluationException("Expected integer and string operands")
                return right[left:]

        if isinstance(exp, ast_builder.LambdaExpression):
            lambda_eval = Evaluator(
                context=self.context.copy(), value_stack=self.value_stack.copy()
            )
            val = lambda_eval.value_stack.pop(-1)
            lambda_eval.context[exp.variable] = val
            return lambda_eval.eval_ast(exp.body)

        if isinstance(exp, ast_builder.IfExpression):
            condition = self.eval_ast(exp.condition)
            if condition:
                return self.eval_ast(exp.then_branch)
            return self.eval_ast(exp.else_branch)

        if isinstance(exp, ast_builder.VariableExpression):
            if exp.variable not in self.context:
                raise EvaluationException(
                    f"Variable {exp.variable} not found in {self.context}"
                )
            val = self.context[exp.variable]
            if isinstance(val, ast_builder.LambdaExpression):
                return self.eval_ast(val)
            return val

        raise ValueError(f"Unknown expression type {exp}")
