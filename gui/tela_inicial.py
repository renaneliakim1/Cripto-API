import tkinter as tk
from PIL import Image, ImageTk
import os


def mostrar_tela_inicial(root, mudar_tela):
    for widget in root.winfo_children():
        widget.destroy()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_imagem = os.path.join(base_dir, "..", "assets", "fundo.png")

    try:
        imagem_fundo_original = Image.open(caminho_imagem).convert("RGBA")
    except FileNotFoundError:
        imagem_fundo_original = Image.new("RGBA", (800, 600), color="#1e213d")

    alpha = 0.3
    alpha_layer = Image.new("L", imagem_fundo_original.size, int(255 * alpha))
    imagem_fundo_original.putalpha(alpha_layer)

    def atualizar_imagem_fundo(event=None):
        imagem_resized = imagem_fundo_original.resize(
            (root.winfo_width(), root.winfo_height()), Image.LANCZOS
        )
        bg_image = ImageTk.PhotoImage(imagem_resized)
        fundo_label.config(image=bg_image)
        fundo_label.image = bg_image

    fundo_label = tk.Label(root)
    fundo_label.place(x=0, y=0, relwidth=1, relheight=1)

    atualizar_imagem_fundo()
    root.bind("<Configure>", atualizar_imagem_fundo)

    accent_color = "#0077b6"
    text_color = "#ffffff"

    # Título  não fica transparente

    label = tk.Label(
        root,
        text="🚀 Bem-vindo ao CryptoApp",
        font=("Segoe UI", 18, "bold"),
        fg=accent_color
    )
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
        pady=8,
    )
    botao.pack(pady=15)

    footer = tk.Label(
        root,
        text="2025. Desenvolvido por Renã Eliakim",
        font=("Segoe UI", 9, "italic"),
        fg=text_color,
        bg="#1e213d",  
        anchor="center"
    )
    footer.pack(side="bottom", fill="x")
