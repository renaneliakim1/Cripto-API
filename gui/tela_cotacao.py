import tkinter as tk
import requests
from api.coingecko_api import buscar_preco_cripto
from datetime import datetime

def mostrar_tela_cotacao(root, voltar_tela):
    for widget in root.winfo_children():
        widget.destroy()

    bg_color = "#f0f4f8"
    accent_color = "#0077b6"
    text_color = "#333"
    root.configure(bg=bg_color)

    tk.Label(
        root,
        text="💰 Consultar Criptomoeda",
        font=("Segoe UI", 16, "bold"),
        fg=accent_color,
        bg=bg_color
    ).pack(pady=20)

    entrada = tk.Entry(root, font=("Segoe UI", 12), width=25, relief="solid", bd=1)
    entrada.insert(0, "bitcoin")
    entrada.pack(pady=8)

    resultado = tk.Label(root, text="", font=("Segoe UI", 12), bg=bg_color)
    resultado.pack(pady=10)

    def buscar():
        cripto = entrada.get().lower()
        preco = buscar_preco_cripto(cripto)
        if preco:
            resultado.config(
                text=f"{cripto.upper()}:\n💵 BRL: R$ {preco['brl']}  |  💲 USD: ${preco['usd']}",
                fg="green"
            )
        else:
            resultado.config(text="❌ Ativo não encontrado ou erro na API", fg="red")

    botoes_frame = tk.Frame(root, bg=bg_color)
    botoes_frame.pack(pady=10)

    tk.Button(
        botoes_frame,
        text="Buscar",
        command=buscar,
        font=("Segoe UI", 11),
        bg=accent_color,
        fg="white",
        relief="flat",
        activebackground="#023e8a",
        padx=15,
        pady=5
    ).pack(side="left", padx=5)

    tk.Button(
        botoes_frame,
        text="Voltar",
        command=voltar_tela,
        font=("Segoe UI", 11),
        bg="#ced4da",
        fg="black",
        relief="flat",
        padx=15,
        pady=5
    ).pack(side="left", padx=5)

    cotacoes_label = tk.Label(
        root,
        text="Carregando cotações...",
        font=("Segoe UI", 10),
        justify="left",
        bg=bg_color,
        fg="#444"
    )
    cotacoes_label.pack(pady=(10, 5))

    status_label = tk.Label(
        root,
        text="🔄 Atualizando...",
        font=("Segoe UI", 9, "italic"),
        bg=bg_color,
        fg="#888"
    )
    status_label.pack()

    def atualizar_ativos():
        url = "https://api.coingecko.com/api/v3/simple/price"
        ativos = ["bitcoin", "ethereum", "solana", "cardano", "dogecoin"]
        params = {
            "ids": ",".join(ativos),
            "vs_currencies": "brl,usd"
        }

        status_label.config(text="🔄 Atualizando...")

        try:
            res = requests.get(url, params=params, timeout=3)
            res.raise_for_status()
            data = res.json()

            texto = "📊 Cotações populares (atualiza a cada 30 seg.):\n\n"
            for ativo in ativos:
                brl = data[ativo]["brl"]
                usd = data[ativo]["usd"]
                texto += f"• {ativo.title():<10} R$ {brl:<10} | $ {usd}\n"

            cotacoes_label.config(text=texto)

            agora = datetime.now().strftime("%H:%M:%S")
            status_label.config(text=f"✅ Última atualização: {agora}")

        except Exception as e:
            print(f"[Erro API] {e}")
            status_label.config(text="⚠️ Tentando novamente...")





        root.after(30000, atualizar_ativos)

    atualizar_ativos()
