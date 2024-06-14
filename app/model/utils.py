import re


def is_valid_cpf(cpf):
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais (caso inválido)
    if cpf == cpf[0] * 11:
        return False
    
    # Calcula os dígitos verificadores
    digitos = cpf[:-2]
    verificador1 = _calcula_digito_verificador(digitos)
    verificador2 = _calcula_digito_verificador(digitos + verificador1)
    
    # Verifica se os dígitos verificadores estão corretos
    return cpf[-2:] == verificador1 + verificador2

def _calcula_digito_verificador(digitos):
    soma = 0
    peso = len(digitos) + 1
    for digito in digitos:
        soma += int(digito) * peso
        peso -= 1
    resto = soma % 11
    if resto < 2:
        return '0'
    else:
        return str(11 - resto)

def is_valid_cep(cep):
    # Verifica se tem 8 dígitos
    if len(cep) != 8:
        return False
    
    return True

def is_valid_email(email: str):
    # Regex pattern for validating an email address
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):    
    # Verifica se tem 10 ou 11 dígitos
    if len(phone) == 10 or len(phone) == 11:
        return True
    
    return False