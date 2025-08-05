import tkinter as tk
from gui.tela_inicial import mostrar_tela_inicial
from gui.tela_cotacao import mostrar_tela_cotacao

def main():
    app = tk.Tk()
    app.title("CryptoApp")
    app.geometry("350x300")

    def ir_para_cotacao():
        mostrar_tela_cotacao(app, voltar_para_inicial)

    def voltar_para_inicial():
        mostrar_tela_inicial(app, ir_para_cotacao)

    mostrar_tela_inicial(app, ir_para_cotacao)
    app.mainloop()

    

if __name__ == "__main__":
    main()
