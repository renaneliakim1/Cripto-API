import tkinter as tk
import os
from gui.tela_inicial import mostrar_tela_inicial
from gui.tela_cotacao import mostrar_tela_cotacao_melhorada


def main():
    app = tk.Tk()
    app.title("CryptoApp")
    app.geometry("350x300")

    # CAMINHO PARA O ÍCONE (certifique-se que o arquivo iconB.ico está em assets/)
    icone_path = os.path.join("assets", "bitcoin.ico")
    app.iconbitmap(icone_path)  # AQUI aplica o ícone


    def ir_para_cotacao():
        
        mostrar_tela_cotacao_melhorada(app, voltar_para_inicial)

    def voltar_para_inicial():
        mostrar_tela_inicial(app, ir_para_cotacao)

    mostrar_tela_inicial(app, ir_para_cotacao)
    app.mainloop()


if __name__ == "__main__":
    main()
