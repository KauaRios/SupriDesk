def validar_pedido(setor, material, quantidade):
    setor = setor.strip()
    material = material.strip()
    if not setor or not material or not quantidade:
        raise ValueError("Preencha todos os campos!")
    try:
        quantidade = int(quantidade)
    except ValueError:
        raise ValueError("A quantidade deve ser um número inteiro!")
    if quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero!")
    elif quantidade > 9223372036854775807:
        raise ValueError("A quantidade informada é muito grande")
    return setor, material, quantidade


def transicao_permitida(status, novo_status):
    return (status, novo_status) in (
        ("Pendente", "Em atendimento"),
        ("Em atendimento", "Atendida"),
    )

