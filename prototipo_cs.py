import tkinter as tk
from tkinter import messagebox


# dados do sistema
clientes = {
    "11": {"nome": "João"},
    "22": {"nome": "Maria"}
}

produtos = {
    1: {"nome": "Dipirona 500mg", "preco": 8.50, "estoque": 10},
    2: {"nome": "Ibuprofeno 200mg", "preco": 12.00, "estoque": 15},
    3: {"nome": "Vitamina C", "preco": 5.00, "estoque": 20},
}

carrinho = []
cliente_logado = None

def trocar_tela(frame):
    frame_login.pack_forget()
    frame_produtos.pack_forget()
    frame_carrinho.pack_forget()

    frame.pack(fill="both", expand=True)


def login():
    global cliente_logado
    cpf = cpf_entry.get()

    if cpf in clientes:
        cliente_logado = cpf
        atualizar_produtos()
        trocar_tela(frame_produtos)
    else:
        messagebox.showerror("Erro", "CPF não cadastrado.")


def atualizar_produtos():
    for widget in produtos_area.winfo_children():
        widget.destroy()

    tk.Label(produtos_area, text=f"Bem-vindo, {clientes[cliente_logado]['nome']}!",
             font=("Arial", 14)).pack(pady=10)

    for pid, p in produtos.items():
        card = tk.Frame(produtos_area, bd=1, relief="solid", padx=10, pady=10)
        card.pack(pady=5)

        tk.Label(card, text=f"{p['nome']}", font=("Arial", 12)).pack(anchor="w")
        tk.Label(card, text=f"Preço: R$ {p['preco']:.2f} | Estoque: {p['estoque']}",
                 font=("Arial", 10)).pack(anchor="w")

        tk.Button(card, text="Adicionar ao carrinho",
                  command=lambda pid=pid: adicionar_carrinho(pid)).pack(pady=5)


def adicionar_carrinho(pid):
    if produtos[pid]["estoque"] <= 0:
        messagebox.showwarning("Sem estoque", "Produto indisponível.")
        return

    produtos[pid]["estoque"] -= 1
    carrinho.append(pid)

    atualizar_produtos()


def abrir_carrinho():
    for widget in carrinho_area.winfo_children():
        widget.destroy()

    tk.Label(carrinho_area, text="Seu Carrinho", font=("Arial", 16)).pack(pady=10)

    total = 0
    for pid in carrinho:
        p = produtos[pid]
        total += p["preco"]

        tk.Label(carrinho_area, text=f"{p['nome']} - R$ {p['preco']:.2f}",
                 font=("Arial", 12)).pack()

    tk.Label(carrinho_area, text=f"Total: R$ {total:.2f}", font=("Arial", 14)).pack(pady=10)

    trocar_tela(frame_carrinho)


def finalizar_pedido():
    if not carrinho:
        messagebox.showwarning("Carrinho vazio", "Você não tem itens no carrinho.")
        return

    codigo = abs(hash(tuple(carrinho))) % 1000000

    messagebox.showinfo("Pedido finalizado", f"Código do Pedido: {codigo}")

    carrinho.clear()

    abrir_carrinho()  # atualiza carrinho vazio

# pagina principal
root = tk.Tk()
root.title("Farmácia - Sistema")
root.geometry("400x500")

# login
frame_login = tk.Frame(root)

tk.Label(frame_login, text="Login via CPF", font=("Arial", 16)).pack(pady=20)
cpf_entry = tk.Entry(frame_login, font=("Arial", 14))
cpf_entry.pack(pady=10)

tk.Button(frame_login, text="Entrar", font=("Arial", 12),
          command=login).pack(pady=10)

tk.Label(frame_login, text="CPF: 11 (João), 22 (Maria)", font=("Arial", 10)).pack()

# produtos
frame_produtos = tk.Frame(root)

tk.Button(frame_produtos, text="Ver Carrinho",
          command=abrir_carrinho).pack(anchor="ne", padx=10, pady=10)

produtos_area = tk.Frame(frame_produtos)
produtos_area.pack(pady=20)

# carrinho
frame_carrinho = tk.Frame(root)

carrinho_area = tk.Frame(frame_carrinho)
carrinho_area.pack(pady=20)

tk.Button(frame_carrinho, text="Voltar",
          command=lambda: trocar_tela(frame_produtos)).pack(pady=5)

tk.Button(frame_carrinho, text="Finalizar Pedido", font=("Arial", 12),
          command=finalizar_pedido).pack(pady=10)

# tela login
trocar_tela(frame_login)
root.mainloop()
