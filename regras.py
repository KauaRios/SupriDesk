from datetime import datetime


def cadastrar_pedido(banco, setor, material, quantidade, prioridade):
    setor, material, quantidade = validar_pedido(setor, material, quantidade)
    if prioridade not in ("Normal", "Alta"):
        raise ValueError("Selecione uma prioridade válida: Normal ou Alta.")
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    banco.inserir_tabela(setor, material, quantidade, prioridade, "Pendente", data_hora)


def alterar_status(banco, status, id_pedido, novo_status):
    if not transicao_permitida(status, novo_status):
        return False
    return banco.atualizar(status, id_pedido, novo_status)


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

