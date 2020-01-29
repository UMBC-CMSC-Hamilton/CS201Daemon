class TestCase:
    def __init__(self):
        pass


def print_redirect(*args, ):
    pass


def input_redirect(prompt):
    return input(prompt)


def run_code(code_block, test_case):
    exec(code_block)
    return code_block
