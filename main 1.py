import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
#PROGRAMADORES VITOR YUKI E JOÃO PAULO
ARQUIVO_ESTOQUE = "estoque.txt"

def carregar_estoque():
    estoque = {}
    try:
        with open(ARQUIVO_ESTOQUE, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    id_, nome, categoria, qtd, preco = linha.split(";")
                    estoque[id_] = {
                        "nome": nome,
                        "categoria": categoria,
                        "quantidade": int(qtd),
                        "preco": float(preco)
                    }
    except FileNotFoundError:
        with open(ARQUIVO_ESTOQUE, "w", encoding="utf-8") as f:
            pass
    return estoque

def salvar_estoque(estoque):
    with open(ARQUIVO_ESTOQUE, "w", encoding="utf-8") as f:
        for id_, dados in estoque.items():
            linha = f"{id_};{dados['nome']};{dados['categoria']};{dados['quantidade']};{dados['preco']}\n"
            f.write(linha)

def perguntar_continuar(janela_atual):
    janela_atual.destroy()
    if messagebox.askyesno("Continuar?", "Deseja continuar usando o programa?"):
        pass
    else:
        root.quit()

def adicionar_produto():
    janela = tk.Toplevel(root)
    janela.title("Adicionar Produto")
    janela.geometry("350x300")

    tk.Label(janela, text="ID:").pack()
    entry_id = tk.Entry(janela)
    entry_id.pack()

    tk.Label(janela, text="Nome:").pack()
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    tk.Label(janela, text="Categoria:").pack()
    entry_categoria = tk.Entry(janela)
    entry_categoria.pack()

    tk.Label(janela, text="Quantidade:").pack()
    entry_qtd = tk.Entry(janela)
    entry_qtd.pack()

    tk.Label(janela, text="Preço:").pack()
    entry_preco = tk.Entry(janela)
    entry_preco.pack()

    def salvar():
        id_ = entry_id.get().strip()
        nome = entry_nome.get().strip()
        categoria = entry_categoria.get().strip()
        qtd = entry_qtd.get().strip()
        preco = entry_preco.get().strip()

        if not id_ or not nome or not categoria or not qtd or not preco:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return

        estoque = carregar_estoque()
        if id_ in estoque:
            messagebox.showerror("Erro", "ID já existe no estoque.")
            return

        try:
            qtd = int(qtd)
            preco = float(preco)
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser inteiro e preço deve ser número.")
            return

        estoque[id_] = {"nome": nome, "categoria": categoria, "quantidade": qtd, "preco": preco}
        salvar_estoque(estoque)
        messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
        perguntar_continuar(janela)

    tk.Button(janela, text="Adicionar", command=salvar).pack(pady=10)

def atualizar_produto():
    janela = tk.Toplevel(root)
    janela.title("Atualizar Produto")
    janela.geometry("350x350")

    tk.Label(janela, text="Digite o ID do produto para atualizar:").pack()
    entry_id = tk.Entry(janela)
    entry_id.pack()

    def buscar():
        id_ = entry_id.get().strip()
        estoque = carregar_estoque()

        if id_ not in estoque:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return

        dados = estoque[id_]

        for widget in janela.winfo_children():
            widget.destroy()

        tk.Label(janela, text=f"Atualizando produto ID: {id_}").pack()

        tk.Label(janela, text="Nome:").pack()
        entry_nome = tk.Entry(janela)
        entry_nome.insert(0, dados["nome"])
        entry_nome.pack()

        tk.Label(janela, text="Categoria:").pack()
        entry_categoria = tk.Entry(janela)
        entry_categoria.insert(0, dados["categoria"])
        entry_categoria.pack()

        tk.Label(janela, text="Quantidade:").pack()
        entry_qtd = tk.Entry(janela)
        entry_qtd.insert(0, str(dados["quantidade"]))
        entry_qtd.pack()

        tk.Label(janela, text="Preço:").pack()
        entry_preco = tk.Entry(janela)
        entry_preco.insert(0, str(dados["preco"]))
        entry_preco.pack()

        def salvar():
            nome = entry_nome.get().strip()
            categoria = entry_categoria.get().strip()
            qtd = entry_qtd.get().strip()
            preco = entry_preco.get().strip()

            if not nome or not categoria or not qtd or not preco:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
                return
            try:
                qtd = int(qtd)
                preco = float(preco)
            except ValueError:
                messagebox.showerror("Erro", "Quantidade deve ser inteiro e preço deve ser número.")
                return

            estoque[id_] = {"nome": nome, "categoria": categoria, "quantidade": qtd, "preco": preco}
            salvar_estoque(estoque)
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            perguntar_continuar(janela)

        tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)

    tk.Button(janela, text="Buscar", command=buscar).pack(pady=10)

def remover_produto():
    janela = tk.Toplevel(root)
    janela.title("Remover Produto")
    janela.geometry("300x150")

    tk.Label(janela, text="Digite o ID do produto para remover:").pack()
    entry_id = tk.Entry(janela)
    entry_id.pack()

    def remover():
        id_ = entry_id.get().strip()
        estoque = carregar_estoque()

        if id_ not in estoque:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return

        if messagebox.askyesno("Confirmação", f"Tem certeza que deseja remover o produto ID {id_}?"):
            del estoque[id_]
            salvar_estoque(estoque)
            messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
            perguntar_continuar(janela)

    tk.Button(janela, text="Remover", command=remover).pack(pady=10)

def relatorio_estoque():
    janela = tk.Toplevel(root)
    janela.title("Relatório de Estoque")
    janela.geometry("600x400")

    estoque = carregar_estoque()  # <- LINHA CORRIGIDA AQUI

    cols = ("ID", "Nome", "Categoria", "Quantidade", "Preço")
    tree = ttk.Treeview(janela, columns=cols, show="headings")

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    for id_, dados in estoque.items():
        tree.insert("", "end", values=(
            id_,
            dados["nome"],
            dados["categoria"],
            dados["quantidade"],
            f"R$ {dados['preco']:.2f}"
        ))

    tree.pack(expand=True, fill="both")

    def fechar():
        janela.destroy()
        if not messagebox.askyesno("Continuar?", "Deseja continuar usando o programa?"):
            root.quit()

    tk.Button(janela, text="Fechar Relatório", command=fechar).pack(pady=10)

def sair():
    if messagebox.askyesno("Sair", "Tem certeza que deseja sair?"):
        root.quit()

# Janela principal
root = tk.Tk()
root.title("Controle de Estoque")
root.geometry("300x350")

tk.Label(root, text="Controle de Estoque do Mercado", font=("Arial", 14)).pack(pady=10)

tk.Button(root, text="Adicionar Produto", width=25, command=adicionar_produto).pack(pady=5)
tk.Button(root, text="Atualizar Produto", width=25, command=atualizar_produto).pack(pady=5)
tk.Button(root, text="Remover Produto", width=25, command=remover_produto).pack(pady=5)
tk.Button(root, text="Relatório de Estoque", width=25, command=relatorio_estoque).pack(pady=5)
tk.Button(root, text="Sair", width=25, command=sair).pack(pady=20)

root.mainloop()
