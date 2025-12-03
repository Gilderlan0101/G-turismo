import random


def secret_verificatio_code_for_emails() -> int:
    """secret_verificatio_code_for_emails: Gerador de codigo aleatorio no formato  inteiro"""
    code = random.randint(1000, 9999)
    return str(code)
