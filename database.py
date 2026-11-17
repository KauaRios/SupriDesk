import sqlite3
from pathlib import Path
from regras import transicao_permitida

bancodir = Path(__file__).resolve().parent / "data"
bancodir.mkdir(exist_ok=True)


class Banco:
    def __init__(self) -> None:
        self.conexao = sqlite3.connect(bancodir / "solicitacoes.db")
        self.cursor = self.conexao.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos(id INTEGER PRIMARY KEY,
        setor TEXT NOT NULL,
        material TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        prioridade TEXT NOT NULL,
        status TEXT NOT NULL,
        data_hora TEXT NOT NULL)""")
        self.conexao.commit()

    def inserir_tabela(
        self, setor, material, quantidade, prioridade, status, data_hora
    ):

        self.cursor.execute(
            """INSERT INTO pedidos(setor,material,quantidade,prioridade,status,data_hora) VALUES(?,?,?,?,?,?)""",
            (setor, material, quantidade, prioridade, status, data_hora),
        )
        self.conexao.commit()

    def busca(self, texto, status):
        pesquisa = f"%{texto}%"
        if status == "Todos":
            self.cursor.execute(
                """SELECT * FROM pedidos WHERE setor LIKE ? OR material LIKE ?""",
                (pesquisa, pesquisa),
            )
        else:
            self.cursor.execute(
                """SELECT * FROM pedidos WHERE (setor LIKE ? OR material LIKE ?) AND status = ?""",
                (pesquisa, pesquisa, status),
            )
        return self.cursor.fetchall()

    def atualizar(self, status, id, novo_status):
        if not transicao_permitida(status, novo_status):
            return False
        self.cursor.execute(
            """UPDATE pedidos set STATUS=? WHERE id=? AND status=?""",
            (novo_status, id, status),
        )

        if self.cursor.rowcount == 0:
            return False
        self.conexao.commit()
        return True

    def listar_pedidos(self):

        self.cursor.execute("""SELECT * FROM pedidos""")
        return self.cursor.fetchall()
