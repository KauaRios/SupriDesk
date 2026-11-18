import sqlite3
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
from regras import cadastrar_pedido, alterar_status
import csv
from tkinter import filedialog
class Interface:
    def __init__(self,banco) -> None:
        self.banco=banco
        self.raiz=tk.Tk()
        self.raiz.title("SupriDesk")
        self.raiz.geometry("1000x550")
        self.raiz.minsize(850, 450)
        self.raiz.columnconfigure(1, weight=1)
        self.raiz.rowconfigure(1, weight=1)
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
            pedidos=[]
            for item in self.tabela.get_children():
                valores=self.tabela.item(item,"values")
                pedidos.append(valores)
            
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
            cadastrar_pedido(self.banco, setor, material, quantidade, prioridade)
        except ValueError as erro:
            messagebox.showwarning("Atenção", str(erro))
            return
        except sqlite3.Error as erro:
                messagebox.showerror("Erro",f"Nao foi possivel inserir na tabela{erro}")
                return
        self.campo_setor.delete(0, "end")
        self.campo_material.delete(0, "end")
        self.campo_quantidade.delete(0, "end")
        self.prioridade.set("Normal")
        self.pesquisar()
        messagebox.showinfo("Sucesso","Pedido cadastrado com sucesso")
    def criar_tabela(self):
        quadro_tabela = ttk.Frame(self.raiz, padding=(12, 0))
        quadro_tabela.grid(row=1, column=1, sticky="nsew")
        quadro_tabela.columnconfigure(0, weight=1)
        quadro_tabela.rowconfigure(0, weight=1)
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
        self.tabela.grid(row=0, column=0, sticky="nsew")
        rolagem_vertical = ttk.Scrollbar(quadro_tabela, orient="vertical", command=self.tabela.yview)
        rolagem_vertical.grid(row=0, column=1, sticky="ns")
        rolagem_horizontal = ttk.Scrollbar(quadro_tabela, orient="horizontal", command=self.tabela.xview)
        rolagem_horizontal.grid(row=1, column=0, sticky="ew")
        self.tabela.configure(yscrollcommand=rolagem_vertical.set, xscrollcommand=rolagem_horizontal.set)
        acoes = ttk.Frame(self.raiz, padding=12)
        acoes.grid(row=2, column=1, sticky="ew")

        self.botao_iniciar=ttk.Button(acoes,text="Iniciar atendimento",command=self.iniciar_atendimento)
        self.botao_iniciar.pack(side="left", padx=(0, 8))


        self.botao_concluir=ttk.Button(acoes,text="Concluir atendimento",command=self.concluir_atendimento)
        self.botao_concluir.pack(side="left")
        self.botao_exportar=ttk.Button(acoes,text="Exportar CSV",command=self.exportar_csv)
        self.botao_exportar.pack(side="right")
    def iniciar_atendimento(self):
        id_pedido=self.obter_id_selecionado()
        
        if id_pedido is  None:
            return
        atualizado=alterar_status(self.banco,"Pendente",id_pedido,"Em atendimento")
        if atualizado:
            self.pesquisar()
            messagebox.showinfo("Sucesso","Atendimento iniciado")
        else:
            messagebox.showwarning("Atencão","O pedido precisa estar pendente para iniciar atendimento")
    def concluir_atendimento(self):
        id_pedido=self.obter_id_selecionado()

        if id_pedido is None:
            return
        atualizado=alterar_status(self.banco,"Em atendimento",id_pedido,"Atendida")
        if atualizado:
            self.pesquisar()
            messagebox.showinfo("Sucesso","Pedido Concluido")
        else:
            messagebox.showwarning("Atencão","O pedido precisa estar em atendimento para ser concluido")
    def carregar_pedidos(self):
        self.tabela.delete(*self.tabela.get_children())
        pedido=self.banco.listar_pedidos()
        for pd in pedido:
            self.tabela.insert("","end",values=pd)
    def criar_filtros(self):
        filtros = ttk.Frame(self.raiz)
        filtros.grid(row=0, column=1, sticky="ew", padx=12, pady=12)
        ttk.Label(filtros, text="Setor ou material:").grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.campo_pesquisa = ttk.Entry(filtros)
        self.campo_pesquisa.grid(row=0, column=1, sticky="ew", padx=(0, 12))
        ttk.Label(filtros, text="Status:").grid(row=0, column=2, padx=(0, 8))
        self.filtro_status = ttk.Combobox(filtros, values=("Todos", "Pendente", "Em atendimento", "Atendida"), state="readonly")
        self.filtro_status.set("Todos")
        self.filtro_status.grid(row=0, column=3, sticky="ew")
        filtros.columnconfigure(1, weight=1)
        
        self.botao_pesquisar=ttk.Button(filtros,text="Pesquisar",command=self.pesquisar)
        self.botao_pesquisar.grid(row=1, column=1, sticky="w", pady=(6, 0))
        self.botao_limpar=ttk.Button(filtros,text="Limpar filtros",command=self.limpar_filtros)
        self.botao_limpar.grid(row=1, column=3, sticky="w", pady=(6, 0))
    def limpar_filtros(self):
        self.campo_pesquisa.delete(0, "end")
        self.filtro_status.set("Todos")
        self.carregar_pedidos()
    def pesquisar(self):
        texto=self.campo_pesquisa.get()
        status=self.filtro_status.get()
        try:
            pedidos=self.banco.busca(texto,status) 
        except sqlite3.Error as erro:
            messagebox.showerror("Erro",f"Nao foi possivel pesquisar pedidos:{erro}")
            return
        self.tabela.delete(*self.tabela.get_children())
        for pedido in pedidos:
            self.tabela.insert("","end",values=pedido)

    def criar_formulario(self):
        formulario = ttk.Frame(self.raiz, padding=12)
        formulario.grid(row=0, column=0, rowspan=3, sticky="ns")
        ttk.Label(formulario, text="Cadastrar pedido").grid(row=0, column=0, sticky="w", pady=(0, 16))
        self.label_setor = ttk.Label(formulario, text="Setor")
        self.label_setor.grid(row=1, column=0, sticky="w")
        self.campo_setor = ttk.Entry(formulario, width=22)
        self.campo_setor.grid(row=2, column=0, sticky="ew", pady=(3, 12))
        self.label_material = ttk.Label(formulario, text="Material")
        self.label_material.grid(row=3, column=0, sticky="w")
        self.campo_material = ttk.Entry(formulario, width=22)
        self.campo_material.grid(row=4, column=0, sticky="ew", pady=(3, 12))
        self.label_quantidade = ttk.Label(formulario, text="Quantidade")
        self.label_quantidade.grid(row=5, column=0, sticky="w")
        self.campo_quantidade = ttk.Entry(formulario, width=22)
        self.campo_quantidade.grid(row=6, column=0, sticky="ew", pady=(3, 12))
        self.label_prioridade = ttk.Label(formulario, text="Prioridade")
        self.label_prioridade.grid(row=7, column=0, sticky="w")
        self.prioridade = ttk.Combobox(formulario, values=("Normal", "Alta"), state="readonly", width=20)
        self.prioridade.set("Normal")
        self.prioridade.grid(row=8, column=0, sticky="ew", pady=(3, 16))
        self.botao_cadastrar = ttk.Button(formulario, text="Cadastrar", command=self.cadastrar)
        self.botao_cadastrar.grid(row=9, column=0, sticky="ew")

    def iniciar(self):
        self.raiz.mainloop()
 

