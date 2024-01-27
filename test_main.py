from unbabel_cli import main

# content of test_sample.py
def func(x):
    return x + 1


def test_answer():
    assert main() == 5