import tkinter as tk
from api.coingecko_api import buscar_preco_cripto

def mostrar_tela_cotacao(root, voltar_tela):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Consultar Criptomoeda", font=("Arial", 16)).pack(pady=10)

    entrada = tk.Entry(root, font=("Arial", 12))
    entrada.insert(0, "bitcoin")
    entrada.pack(pady=5)

    resultado = tk.Label(root, text="", font=("Arial", 12))
    resultado.pack(pady=10)

    def buscar():
        cripto = entrada.get().lower()
        preco = buscar_preco_cripto(cripto)
        if preco:
            resultado.config(text=f"{cripto.upper()}:\nBRL: R$ {preco['brl']} | USD: ${preco['usd']}", fg="green")
        else:
            resultado.config(text="Erro ao buscar cotação.", fg="red")

    tk.Button(root, text="Buscar", command=buscar, font=("Arial", 12)).pack(pady=5)
    tk.Button(root, text="Voltar", command=voltar_tela, font=("Arial", 10)).pack(pady=10)
