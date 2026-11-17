# SupriDesk

## Descrição

O sistema serve para gestão de solicitações de materiais, com histórico persistente e regras de atendimento.

## Tecnologias

O projeto foi desenvolvido com Python 3.14.10 e usa bibliotecas da biblioteca padrão: Tkinter/ttk, SQLite e CSV. É necessário ter uma instalação do Python com Tkinter disponível.

## Como executar
Clone o Projeto com
```bash
git clone <URL>
```


Na pasta do projeto, execute:

```bash
python main.py
```

O banco de dados é criado automaticamente na pasta `data` caso ela nao exista é criada também .

## Funcionalidades

- Cadastro de solicitações com setor, material, quantidade e prioridade.
- Exportação dos pedidos exibidos na tabela para arquivo CSV.
- Pesquisa por setor ou material e filtro por status do pedido, usando ambos ou somente um.
- Botões para iniciar e concluir o atendimento, seguindo as regras de negócio.
- Limpeza dos filtros para exibir todos os pedidos.

## Estrutura do projeto

- `main.py`: inicia o banco e a interface.
- `data/`: local onde o banco de dados é criado.
- `database.py`: módulo onde estão a classe `Banco` e seus métodos.
- `interface.py`: arquivo onde estão a classe `Interface` e seus métodos.
- `regras.py`: arquivo onde estão as regras de transição entre Pendente, Em atendimento e Atendida, além da validação dos campos e da quantidade inteira positiva.

## Testes realizados

- Após cadastrar **TI / Mouse USB / 5 / Alta**, o status inicia como **Pendente**.
- Ao tentar cadastrar **Administrativo / Papel A4 / 0 / Normal**, a operação é recusada e o usuário é avisado.
- Ao tentar burlar a regra de atendimento, o programa recusa concluir um pedido que já foi concluído ou que ainda não passou por **Em atendimento**.
- Ao fechar e reabrir o programa, os dados persistem no banco.
- Ao pesquisar **Mouse** ou **TI**, filtrar por **Atendida** e exportar, o CSV contém os itens exibidos na tabela Treeview, pois a função usa os dados da tabela em vez de buscar o banco inteiro.

## Uso de inteligência artificial

Utilizei o ChatGPT para auxiliar no posicionamento da interface e me ajudar a entender erros e auxiliar em testes
