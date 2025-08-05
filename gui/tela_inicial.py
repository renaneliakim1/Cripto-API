import tkinter as tk

def mostrar_tela_inicial(root, mudar_tela):
    for widget in root.winfo_children():
        widget.destroy()

    # Cores e estilos
    bg_color = "#f0f4f8"
    accent_color = "#0077b6"
    text_color = "#333"

    root.configure(bg=bg_color)

    label = tk.Label(root, text="🚀 Bem-vindo ao CryptoApp", font=("Segoe UI", 18, "bold"), fg=accent_color, bg=bg_color)
    label.pack(pady=30)

    botao = tk.Button(
        root,
        text="Ir para Cotação",
        command=mudar_tela,
        font=("Segoe UI", 12),
        bg=accent_color,
        fg="white",
        relief="flat",
        activebackground="#023e8a",
        padx=20,
        pady=8
    )
    botao.pack(pady=15)

    rodape = tk.Label(
        root,
        text="🛠️ Desenvolvido por Renã Eliakim",
        font=("Segoe UI", 9, "italic"),
        fg=text_color,
        bg=bg_color
    )
    rodape.pack(side="bottom", pady=20)
