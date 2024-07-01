import pathlib
import decode as d
import ascii_helpers
from ast_eval import Evaluator


def test_ascii():
    assert ascii_helpers.ascii_to_index("!") == [0]
    assert ascii_helpers.ascii_to_index("/") == [14]


# pylint: disable=singleton-comparison
def test_bool():
    tok = d.parse_token("T")
    assert isinstance(tok, d.ValueToken)
    assert tok.value == True  # noqa
    tok = d.parse_token("F")
    assert isinstance(tok, d.ValueToken)
    assert tok.value == False  # noqa


def test_int():
    tok = d.parse_token("I/6")
    assert isinstance(tok, d.ValueToken)
    assert tok.value == 1337


def test_string():
    tok = d.parse_token("SB%,,/}Q/2,$_")
    assert isinstance(tok, d.ValueToken)
    assert tok.value == "Hello World!"


def test_unary():
    for op in d.UnaryOperator:
        tok = d.parse_token(f"U{op.value}")
        assert isinstance(tok, d.UnaryOperatorToken)
        assert tok.operator == op


def test_binary():
    for op in d.BinaryOperator:
        tok = d.parse_token(f"B{op.value}")
        assert isinstance(tok, d.BinaryOperatorToken)
        assert tok.operator == op


def test_lambda():
    tok = d.parse_token("L/6")
    assert isinstance(tok, d.LambdaToken)
    assert tok.variable == 1337


def test_variable():
    tok = d.parse_token("v/6")
    assert isinstance(tok, d.VariableToken)
    assert tok.variable == 1337


def test_intro_msg():
    msg_str = r"""SB%,,/}!.$}7%,#/-%}4/}4(%}M#(//,}/&}4(%}</5.$}P!2)!",%_~~<%&/2%}4!+).'}!}#/523%j}7%}35''%34}4(!4}9/5}(!6%}!},//+}!2/5.$l}S/5e2%}./7},//+).'}!4}4(%}u).$%8wl}N/}02!#4)#%}9/52}#/--5.)#!4)/.}3+),,3j}9/5}#!.}53%}/52}u%#(/w}3%26)#%l}@524(%2-/2%j}4/}+./7}(/7}9/5}!.$}/4(%2}345$%.43}!2%}$/).'j}9/5}#!.},//+}!4}4(%}u3#/2%"/!2$wl~~;&4%2},//+).'}!2/5.$j}9/5}-!9}"%}!$-)44%$}4/}9/52}&)234}#/523%3j}3/}-!+%}352%}4/}#(%#+}4()3}0!'%}&2/-}4)-%}4/}4)-%l}C.}4(%}-%!.4)-%j})&}9/5}7!.4}4/}02!#4)#%}-/2%}!$6!.#%$}#/--5.)#!4)/.}3+),,3j}9/5}-!9}!,3/}4!+%}/52}u,!.'5!'%y4%34wl~"""

    tok = d.parse_token(msg_str)

    assert isinstance(tok, d.ValueToken)

    assert (
        tok.value
        == "Hello and welcome to the School of the Bound Variable!\n\nBefore taking a course, we suggest that you have a look around. You're now looking at the [index]. To practice your communication skills, you can use our [echo] service. Furthermore, to know how you and other students are doing, you can look at the [scoreboard].\n\nAfter looking around, you may be admitted to your first courses, so make sure to check this page from time to time. In the meantime, if you want to practice more advanced communication skills, you may also take our [language_test].\n"  # noqa
    )


def test_encode_decode():
    msg = "Hello and welcome to the School of the Bound Variable!\n\nBefore taking a course, we suggest that you have a look around. You're now looking at the [index]. To practice your communication skills, you can use our [echo] service. Furthermore, to know how you and other students are doing, you can look at the [scoreboard].\n\nAfter looking around, you may be admitted to your first courses, so make sure to check this page from time to time. In the meantime, if you want to practice more advanced communication skills, you may also take our [language_test].\n"
    encoded = "S" + ascii_helpers.encode_string(msg)
    tok = d.parse_token(encoded)
    assert isinstance(tok, d.ValueToken)
    assert tok.value == msg


def test_eval():
    assert Evaluator().eval_tokens([d.ValueToken(value=42)]) == 42
    assert Evaluator().eval_tokens([d.ValueToken(value="Hello")]) == "Hello"

    assert not Evaluator().eval_tokens(
        [
            d.UnaryOperatorToken(operator=d.UnaryOperator.NOT),
            d.ValueToken(value=True),
        ]
    )

    assert (
        Evaluator().eval_tokens(
            [
                d.UnaryOperatorToken(operator=d.UnaryOperator.NEGATE),
                d.ValueToken(value=42),
            ]
        )
        == -42
    )


def test_eval_binary():
    assert (
        Evaluator().eval_tokens(
            [
                d.BinaryOperatorToken(operator=d.BinaryOperator.ADD),
                d.ValueToken(value=1),
                d.ValueToken(value=2),
            ]
        )
        == 3
    )

    assert (
        Evaluator().eval_tokens(
            [
                d.BinaryOperatorToken(operator=d.BinaryOperator.SUBTRACT),
                d.ValueToken(value=1),
                d.ValueToken(value=2),
            ]
        )
        == -1
    )

    assert (
        Evaluator().eval_tokens(
            [
                d.BinaryOperatorToken(operator=d.BinaryOperator.MULTIPLY),
                d.ValueToken(value=2),
                d.ValueToken(value=3),
            ]
        )
        == 6
    )

    assert (
        Evaluator().eval_tokens(
            [
                d.BinaryOperatorToken(operator=d.BinaryOperator.DIVIDE),
                d.ValueToken(value=6),
                d.ValueToken(value=2),
            ]
        )
        == 3
    )

    assert (
        Evaluator().eval_tokens(
            [
                d.BinaryOperatorToken(operator=d.BinaryOperator.MODULO),
                d.ValueToken(value=5),
                d.ValueToken(value=2),
            ]
        )
        == 1
    )

    assert Evaluator().eval_tokens(
        [
            d.BinaryOperatorToken(operator=d.BinaryOperator.EQUAL),
            d.ValueToken(value=5),
            d.ValueToken(value=5),
        ]
    )

    assert Evaluator().eval_tokens(
        [
            d.BinaryOperatorToken(operator=d.BinaryOperator.LESS_THAN),
            d.ValueToken(value=5),
            d.ValueToken(value=6),
        ]
    )

    assert Evaluator().eval_tokens(
        [
            d.BinaryOperatorToken(operator=d.BinaryOperator.GREATER_THAN),
            d.ValueToken(value=6),
            d.ValueToken(value=5),
        ]
    )

    assert Evaluator().eval_tokens(
        [
            d.BinaryOperatorToken(operator=d.BinaryOperator.AND),
            d.ValueToken(value=True),
            d.ValueToken(value=True),
        ]
    )


def test_eval_int_to_string():
    assert (
        Evaluator().eval_tokens(
            [
                d.UnaryOperatorToken(operator=d.UnaryOperator.STRING_TO_INT),
                d.parse_token("S/6"),
            ]
        )
        == 1337
    )


def test_eval_string_to_int():
    assert (
        Evaluator().eval_tokens(
            [
                d.UnaryOperatorToken(operator=d.UnaryOperator.INT_TO_STRING),
                d.parse_token("IB%,,/}Q/2,$_"),
            ]
        )
        == "Hello World!"
    )


def test_if():
    assert (
        Evaluator().eval_tokens(
            [
                d.IfToken(),
                d.ValueToken(value=True),
                d.ValueToken(value=42),
                d.ValueToken(value=1337),
            ]
        )
        == 42
    )

    assert (
        Evaluator().eval_tokens(
            [
                d.IfToken(),
                d.ValueToken(value=False),
                d.ValueToken(value=42),
                d.ValueToken(value=1337),
            ]
        )
        == 1337
    )


def test_if_with_eval():
    assert (
        Evaluator().eval_tokens(
            [
                d.IfToken(),
                d.ValueToken(value=True),
                d.BinaryOperatorToken(operator=d.BinaryOperator.ADD),
                d.ValueToken(value=1),
                d.ValueToken(value=2),
                d.BinaryOperatorToken(operator=d.BinaryOperator.SUBTRACT),
                d.ValueToken(value=1),
                d.ValueToken(value=2),
            ]
        )
        == 3
    )


def test_if_with_variables():
    assert (
        Evaluator(
            context={
                1: 1,
                2: 2,
            }
        ).eval_tokens(
            [
                d.IfToken(),
                d.ValueToken(value=True),
                d.VariableToken(variable=1),
                d.VariableToken(variable=2),
            ]
        )
        == 1
    )

    assert (
        Evaluator(
            context={
                1: 1,
                2: 2,
            }
        ).eval_tokens(
            [
                d.IfToken(),
                d.ValueToken(value=False),
                d.VariableToken(variable=1),
                d.VariableToken(variable=2),
            ]
        )
        == 2
    )


def test_eval_lambda():
    assert (
        Evaluator().eval_tokens(
            [
                d.BinaryOperatorToken(operator=d.BinaryOperator.APPLY),
                d.LambdaToken(variable=1),
                d.BinaryOperatorToken(operator=d.BinaryOperator.ADD),
                d.VariableToken(variable=1),
                d.ValueToken(value=2),
                d.ValueToken(value=3),
            ]
        )
        == 5
    )


def test_eval_nested_lambda():
    assert (
        Evaluator().eval_tokens(
            [
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
        )
        == 7
    )


def test_comst_lambda():
    assert (
        Evaluator().eval_tokens(
            [
                d.BinaryOperatorToken(operator=d.BinaryOperator.APPLY),
                d.LambdaToken(variable=1),
                d.ValueToken(value=1),
                d.ValueToken(value=1337),
            ]
        )
        == 1
    )


def test_higher_order():
    assert (
        Evaluator().eval_tokens(
            [
                d.BinaryOperatorToken(operator=d.BinaryOperator.APPLY),
                d.LambdaToken(variable=2),
                d.BinaryOperatorToken(operator=d.BinaryOperator.APPLY),
                d.VariableToken(variable=2),
                d.ValueToken(value=1337),
                d.LambdaToken(variable=1),
                d.ValueToken(value=1),
                d.ValueToken(value=1337),
            ]
        )
        == 1
    )

    assert (
        Evaluator().eval_tokens(
            [
                d.BinaryOperatorToken(operator=d.BinaryOperator.APPLY),
                d.LambdaToken(variable=2),
                d.BinaryOperatorToken(operator=d.BinaryOperator.APPLY),
                d.VariableToken(variable=2),
                d.ValueToken(value=1337),
                d.LambdaToken(variable=1),
                d.ValueToken(value=1),
                d.ValueToken(value=1337),
            ]
        )
        == 1
    )


def test_variable_shadowing():
    assert (
        Evaluator().eval_tokens(
            [
                d.BinaryOperatorToken(operator=d.BinaryOperator.APPLY),
                d.LambdaToken(variable=1),
                d.BinaryOperatorToken(operator=d.BinaryOperator.ADD),
                d.VariableToken(variable=1),
                d.BinaryOperatorToken(operator=d.BinaryOperator.APPLY),
                d.LambdaToken(variable=1),
                d.BinaryOperatorToken(operator=d.BinaryOperator.ADD),
                d.VariableToken(variable=1),
                d.ValueToken(value=1337),
                d.ValueToken(value=1),
                d.ValueToken(value=7),
            ]
        )
        == 1345
    )


def test_eval_example():
    tokens = 'B$ L# B$ L" B+ v" v" B* I$ I# v8'.split()
    tokens = [d.parse_token(tok) for tok in tokens]

    expect = d.parse_token("I-")

    assert isinstance(expect, d.ValueToken)

    assert Evaluator().eval_tokens(tokens) == expect.value


def test_eval_lambda_example():
    tokens = "B$ B$ B$ B$ L$ L$ L$ L# v$ I\" I# I$ I%".split()
    tokens = [d.parse_token(tok) for tok in tokens]

    assert Evaluator().eval_tokens(tokens) == 3


def test_language_test():
    content = pathlib.Path("language_test.txt").read_text(encoding="utf-8")
    tokens = [d.parse_token(tok) for tok in content.split()]
    res = Evaluator().eval_tokens(tokens)
    assert res == "Self-check OK, send `solve language_test 4w3s0m3` to claim points for it"
