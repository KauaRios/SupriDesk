import sqlite3
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
from datetime import datetime
from regras import validar_pedido
import csv
from tkinter import filedialog
class Interface:
    def __init__(self,banco) -> None:
        self.banco=banco
        self.raiz=tk.Tk()
        self.raiz.title("SupriDesk")
        self.raiz.geometry("850x550")
        self.raiz.minsize(700, 450)
        self.criar_formulario()
        self.criar_filtros()
        self.criar_tabela()
        self.carregar_pedidos()
    def exportar_csv(self):
        caminho = filedialog.asksaveasfilename(
            title="Salvar histórico",
            defaultextension=".csv",
            filetypes=[("Arquivo CSV", "*.csv")],
        )
        if not caminho:
            return
        try:
            pedidos=self.banco.listar_pedidos()
            
            with open(caminho,"w",newline="",encoding="utf-8") as arquivo:
                escritor=csv.writer(arquivo)
                escritor.writerow(["ID","Setor","Material","Quantidade","Prioridade","Status","Data e Hora"])
                escritor.writerows(pedidos)
            messagebox.showinfo("Sucesso","Arquivo exportado com sucesso")
        except (OSError,sqlite3.Error) as e:
            messagebox.showerror("Erro",f"Erro ao exportar arquivo{e}")
                
 
    def obter_id_selecionado(self):
        selecao=self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Atenção", "Selecione um pedido na tabela.")
            return None
        item=self.tabela.item(selecao[0])
        return item["values"][0]
    def cadastrar(self):
        setor=self.campo_setor.get()
        material=self.campo_material.get()
        quantidade=self.campo_quantidade.get()
        prioridade=self.prioridade.get()
        
        #print(setor,material,quantidade,prioridade)
        try:
            setor, material, quantidade = validar_pedido(setor, material, quantidade)
        except ValueError as erro:
            messagebox.showwarning("Atenção", str(erro))
            return
        status = "Pendente"
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        try:
            self.banco.inserir_tabela(setor,material,quantidade,prioridade,status,data_hora)
        except sqlite3.Error as erro:
                messagebox.showerror("Erro",f"Nao foi possivel inserir na tabela{erro}")
                return
        self.campo_setor.delete(0, "end")
        self.campo_material.delete(0, "end")
        self.campo_quantidade.delete(0, "end")
        self.prioridade.set("Normal")
        self.carregar_pedidos()
        messagebox.showinfo("Sucesso","Pedido cadastrado com sucesso")
    def criar_tabela(self):
        quadro_tabela = ttk.Frame(self.raiz, padding=(12, 0))
        quadro_tabela.pack(fill="both", expand=True)
        self.tabela=ttk.Treeview(quadro_tabela,columns=("id","setor","material","quantidade","prioridade","status","data_hora"),show="headings")
        self.tabela.heading("id",text="ID")
        self.tabela.heading("setor",text="Setor")

        self.tabela.heading("material",text="Material")

        self.tabela.heading("quantidade",text="Quantidade")

        self.tabela.heading("prioridade",text="Prioridade")

        self.tabela.heading("status",text="Status")

        self.tabela.heading("data_hora",text="Data")
        for coluna, largura in (("id", 40), ("setor", 90), ("material", 130), ("quantidade", 75), ("prioridade", 75), ("status", 110), ("data_hora", 150)):
            self.tabela.column(coluna, width=largura, minwidth=40)
        self.tabela.pack(fill="both", expand=True)
        acoes = ttk.Frame(self.raiz, padding=12)
        acoes.pack(fill="x")

        self.botao_iniciar=ttk.Button(acoes,text="Iniciar atendimento",command=self.iniciar_atendimento)
        self.botao_iniciar.pack(side="left", padx=(0, 8))


        self.botao_concluir=ttk.Button(acoes,text="Concluir atendimento",command=self.concluir_atendimento)
        self.botao_concluir.pack(side="left")
        self.botao_exportar=ttk.Button(acoes,text="Exportar CSV",command=self.exportar_csv)
        self.botao_exportar.pack(side="left", padx=(8, 0))
    def iniciar_atendimento(self):
        id_pedido=self.obter_id_selecionado()
        
        if id_pedido is  None:
            return
        atualizado=self.banco.atualizar("Pendente",id_pedido,"Em atendimento")
        if atualizado:
            self.carregar_pedidos()
            messagebox.showinfo("Sucesso","Atendimento iniciado")
        else:
            messagebox.showwarning("Atencão","O pedido precisa estar pendente para iniciar atendimento")
    def concluir_atendimento(self):
        id_pedido=self.obter_id_selecionado()

        if id_pedido is None:
            return
        atualizado=self.banco.atualizar("Em atendimento",id_pedido,"Atendida")
        if atualizado:
            self.carregar_pedidos()
            messagebox.showinfo("Sucesso","Pedido Concluido")
        else:
            messagebox.showwarning("Atencão","O pedido precisa estar em atendimento para ser concluido")
    def carregar_pedidos(self):
        self.tabela.delete(*self.tabela.get_children())
        pedido=self.banco.listar_pedidos()
        for pd in pedido:
            self.tabela.insert("","end",values=pd)
    def criar_filtros(self):
        filtros = ttk.LabelFrame(self.raiz, text="Pesquisa", padding=10)
        filtros.pack(fill="x", padx=12, pady=(0, 10))
        ttk.Label(filtros, text="Setor ou material:").grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.campo_pesquisa = ttk.Entry(filtros)
        self.campo_pesquisa.grid(row=0, column=1, sticky="ew", padx=(0, 12))
        ttk.Label(filtros, text="Status:").grid(row=0, column=2, padx=(0, 8))
        self.filtro_status = ttk.Combobox(filtros, values=("Todos", "Pendente", "Em atendimento", "Atendida"), state="readonly")
        self.filtro_status.set("Todos")
        self.filtro_status.grid(row=0, column=3, sticky="ew")
        filtros.columnconfigure(1, weight=1)
        
        self.botao_pesquisar=ttk.Button(filtros,text="Pesquisar",command=self.pesquisar)
        self.botao_pesquisar.grid(row=0, column=4, padx=(8, 0))
        self.botao_limpar=ttk.Button(filtros,text="Limpar filtros",command=self.limpar_filtros)
        self.botao_limpar.grid(row=0, column=5, padx=(8, 0))
    def limpar_filtros(self):
        self.campo_pesquisa.delete(0, "end")
        self.filtro_status.set("Todos")
        self.carregar_pedidos()
    def pesquisar(self):
        texto=self.campo_pesquisa.get()
        status=self.filtro_status.get()
        
        pedidos=self.banco.busca(texto,status) 
        self.tabela.delete(*self.tabela.get_children())
        for pedido in pedidos:
            self.tabela.insert("","end",values=pedido)

    def criar_formulario(self):
        formulario = ttk.LabelFrame(self.raiz, text="Novo pedido", padding=10)
        formulario.pack(fill="x", padx=12, pady=12)
        self.label_setor = ttk.Label(formulario, text="Setor")
        self.label_setor.grid(row=0, column=0, sticky="w")
        self.campo_setor = ttk.Entry(formulario)
        self.campo_setor.grid(row=1, column=0, sticky="ew", padx=(0, 8))
        self.label_material = ttk.Label(formulario, text="Material")
        self.label_material.grid(row=0, column=1, sticky="w")
        self.campo_material = ttk.Entry(formulario)
        self.campo_material.grid(row=1, column=1, sticky="ew", padx=(0, 8))
        self.label_quantidade = ttk.Label(formulario, text="Quantidade")
        self.label_quantidade.grid(row=0, column=2, sticky="w")
        self.campo_quantidade = ttk.Entry(formulario, width=12)
        self.campo_quantidade.grid(row=1, column=2, sticky="ew", padx=(0, 8))
        self.label_prioridade = ttk.Label(formulario, text="Prioridade")
        self.label_prioridade.grid(row=0, column=3, sticky="w")
        self.prioridade = ttk.Combobox(formulario, values=("Normal", "Alta"), state="readonly", width=12)
        self.prioridade.set("Normal")
        self.prioridade.grid(row=1, column=3, sticky="ew", padx=(0, 8))
        self.botao_cadastrar = ttk.Button(formulario, text="Cadastrar", command=self.cadastrar)
        self.botao_cadastrar.grid(row=1, column=4, sticky="ew")
        formulario.columnconfigure(0, weight=1)
        formulario.columnconfigure(1, weight=2)

    def iniciar(self):
        self.raiz.mainloop()
 

