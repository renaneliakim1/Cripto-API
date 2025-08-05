import tkinter as tk

def mostrar_tela_inicial(root, mudar_tela):
    for widget in root.winfo_children():
        widget.destroy()

        

    label = tk.Label(root, text="Bem-vindo ao CryptoApp", font=("Arial", 16))
    label.pack(pady=20)

    botao = tk.Button(root, text="Ir para Cotação", command=mudar_tela, font=("Arial", 12))
    botao.pack(pady=10)

    rodape = tk.Label(root, text="Desenvolvido em Python", font=("Arial", 8))
    rodape.pack(side="bottom", pady=20)
