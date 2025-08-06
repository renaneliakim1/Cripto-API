import tkinter as tk
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import numpy as np
from matplotlib.patches import Rectangle
import seaborn as sns

# Configurar estilo profissional para os gráficos
plt.style.use("seaborn-v0_8-darkgrid")
sns.set_palette("husl")


class CryptoChartApp:
    def __init__(self, root):
        self.root = root
        self.current_crypto = "bitcoin"
        self.chart_canvas = None
        self.setup_ui()

    def setup_ui(self):
        """Configura a interface do usuário"""
        bg_color = "#1e1e2e"
        accent_color = "#89b4fa"
        text_color = "#cdd6f4"
        card_color = "#313244"

        self.root.configure(bg=bg_color)
        self.root.title("📈 Crypto Professional Charts")

        # Header
        header_frame = tk.Frame(self.root, bg=bg_color)
        header_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            header_frame,
            text="📈 Crypto Professional Charts",
            font=("Segoe UI", 18, "bold"),
            fg=accent_color,
            bg=bg_color,
        ).pack()

        # Search frame
        search_frame = tk.Frame(self.root, bg=card_color, relief="solid", bd=1)
        search_frame.pack(fill="x", padx=20, pady=10, ipady=10)

        tk.Label(
            search_frame,
            text="🔍 Buscar Criptomoeda:",
            font=("Segoe UI", 12, "bold"),
            fg=text_color,
            bg=card_color,
        ).pack(pady=5)

        self.search_entry = tk.Entry(
            search_frame,
            font=("Segoe UI", 12),
            width=30,
            relief="solid",
            bd=1,
            bg="#45475a",
            fg=text_color,
            insertbackground=text_color,
        )
        self.search_entry.insert(0, "bitcoin")
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<Return>", lambda e: self.search_crypto())

        # Buttons frame
        buttons_frame = tk.Frame(search_frame, bg=card_color)
        buttons_frame.pack(pady=10)

        tk.Button(
            buttons_frame,
            text="🔍 Buscar",
            command=self.search_crypto,
            font=("Segoe UI", 11, "bold"),
            bg=accent_color,
            fg="#1e1e2e",
            relief="flat",
            activebackground="#74c0fc",
            padx=20,
            pady=8,
            cursor="hand2",
        ).pack(side="left", padx=5)

        tk.Button(
            buttons_frame,
            text="🔄 Atualizar",
            command=self.refresh_chart,
            font=("Segoe UI", 11, "bold"),
            bg="#a6e3a1",
            fg="#1e1e2e",
            relief="flat",
            activebackground="#94d3a2",
            padx=20,
            pady=8,
            cursor="hand2",
        ).pack(side="left", padx=5)

        # Quick access buttons
        quick_frame = tk.Frame(search_frame, bg=card_color)
        quick_frame.pack(pady=5)

        tk.Label(
            quick_frame,
            text="⚡ Acesso Rápido:",
            font=("Segoe UI", 10),
            fg=text_color,
            bg=card_color,
        ).pack()

        quick_buttons_frame = tk.Frame(quick_frame, bg=card_color)
        quick_buttons_frame.pack(pady=5)

        popular_cryptos = [
            ("₿ Bitcoin", "bitcoin"),
            ("Ξ Ethereum", "ethereum"),
            ("◎ Solana", "solana"),
            ("₳ Cardano", "cardano"),
            ("Ð Dogecoin", "dogecoin"),
        ]

        for name, crypto_id in popular_cryptos:
            tk.Button(
                quick_buttons_frame,
                text=name,
                command=lambda c=crypto_id: self.quick_search(c),
                font=("Segoe UI", 9),
                bg="#585b70",
                fg=text_color,
                relief="flat",
                activebackground="#6c7086",
                padx=10,
                pady=3,
                cursor="hand2",
            ).pack(side="left", padx=2)

        # Info frame
        self.info_frame = tk.Frame(self.root, bg=card_color, relief="solid", bd=1)
        self.info_frame.pack(fill="x", padx=20, pady=10, ipady=10)

        self.info_label = tk.Label(
            self.info_frame,
            text="💡 Digite o nome de uma criptomoeda e clique em Buscar",
            font=("Segoe UI", 11),
            fg=text_color,
            bg=card_color,
            justify="center",
        )
        self.info_label.pack(pady=10)

        # Chart frame
        self.chart_frame = tk.Frame(self.root, bg=bg_color)
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Status frame
        self.status_frame = tk.Frame(self.root, bg=card_color, relief="solid", bd=1)
        self.status_frame.pack(fill="x", padx=20, pady=(0, 20), ipady=5)

        self.status_label = tk.Label(
            self.status_frame,
            text="🟢 Pronto para buscar",
            font=("Segoe UI", 10),
            fg="#a6e3a1",
            bg=card_color,
        )
        self.status_label.pack(pady=5)

    def quick_search(self, crypto_id):
        """Busca rápida para criptomoedas populares"""
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, crypto_id)
        self.search_crypto()

    def search_crypto(self):
        """Busca e exibe dados da criptomoeda"""
        crypto = self.search_entry.get().lower().strip()
        if not crypto:
            self.show_error("Por favor, digite o nome de uma criptomoeda")
            return

        self.current_crypto = crypto
        self.status_label.config(text="🔄 Buscando dados...", fg="#f9e2af")
        self.root.update()

        # Buscar preço atual
        current_price = self.get_current_price(crypto)
        if not current_price:
            self.show_error("❌ Criptomoeda não encontrada ou erro na API")
            return

        # Buscar dados históricos
        historical_data = self.get_historical_data(crypto)
        if not historical_data:
            self.show_error("❌ Erro ao buscar dados históricos. Aguarde um momento e tente novamente!.")
            return

        # Atualizar informações
        self.update_info(crypto, current_price)

        # Criar gráfico profissional
        self.create_professional_chart(crypto, historical_data, current_price)

        self.status_label.config(text="✅ Dados atualizados com sucesso", fg="#a6e3a1")

    def refresh_chart(self):
        """Atualiza o gráfico atual"""
        if self.current_crypto:
            self.search_crypto()

    def get_current_price(self, crypto_id):
        """Busca preço atual da criptomoeda"""
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": crypto_id,
            "vs_currencies": "usd,brl",
            "include_24hr_change": "true",
            "include_market_cap": "true",
            "include_24hr_vol": "true",
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if crypto_id in data:
                return data[crypto_id]
            return None

        except Exception as e:
            print(f"Erro ao buscar preço: {e}")
            return None

    def get_historical_data(self, crypto_id, days=30):
        """Busca dados históricos da criptomoeda"""
        url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
        params = {"vs_currency": "usd", "days": days, "interval": "daily"}

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            return {
                "prices": data.get("prices", []),
                "market_caps": data.get("market_caps", []),
                "total_volumes": data.get("total_volumes", []),
            }

        except Exception as e:
            print(f"Erro ao buscar histórico: {e}")
            return None

    def update_info(self, crypto_name, price_data):
        """Atualiza informações da criptomoeda"""
        usd_price = price_data.get("usd", 0)
        brl_price = price_data.get("brl", 0)
        change_24h = price_data.get("usd_24h_change", 0)
        market_cap = price_data.get("usd_market_cap", 0)
        volume_24h = price_data.get("usd_24h_vol", 0)

        # Formatação de números
        def format_number(num):
            if num >= 1e9:
                return f"{num/1e9:.2f}B"
            elif num >= 1e6:
                return f"{num/1e6:.2f}M"
            elif num >= 1e3:
                return f"{num/1e3:.2f}K"
            else:
                return f"{num:.2f}"

        change_color = "#a6e3a1" if change_24h >= 0 else "#f38ba8"
        change_symbol = "📈" if change_24h >= 0 else "📉"

        info_text = f"""
🪙 {crypto_name.upper()}
💵 Preço: ${usd_price:,.4f} USD | R$ {brl_price:,.2f} BRL
{change_symbol} Variação 24h: {change_24h:+.2f}%
📊 Market Cap: ${format_number(market_cap)} USD
📈 Volume 24h: ${format_number(volume_24h)} USD
        """.strip()

        self.info_label.config(text=info_text, fg="#cdd6f4")

    def create_professional_chart(self, crypto_name, data, current_price):
        """Cria gráfico profissional com múltiplas visualizações"""
        # Limpar gráfico anterior
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        prices = data["prices"]
        volumes = data["total_volumes"]

        if not prices:
            return

        # Preparar dados
        dates = [datetime.fromtimestamp(p[0] / 1000) for p in prices]
        price_values = [p[1] for p in prices]
        volume_values = [v[1] for v in volumes] if volumes else []

        # Criar figura com subplots
        fig, (ax1, ax2) = plt.subplots(
            2,
            1,
            figsize=(12, 10),
            gridspec_kw={"height_ratios": [3, 1]},
            facecolor="#1e1e2e",
        )

        # Configurar cores do tema escuro
        fig.patch.set_facecolor("#1e1e2e")

        # Gráfico de preços (subplot superior)
        ax1.set_facecolor("#313244")

        # Linha principal do preço
        line = ax1.plot(
            dates,
            price_values,
            linewidth=2.5,
            color="#89b4fa",
            label=f"{crypto_name.upper()} Price",
            alpha=0.9,
        )[0]

        # Área preenchida sob a linha
        ax1.fill_between(dates, price_values, alpha=0.3, color="#89b4fa")

        # Adicionar pontos de máximo e mínimo
        max_price = max(price_values)
        min_price = min(price_values)
        max_idx = price_values.index(max_price)
        min_idx = price_values.index(min_price)

        ax1.scatter(
            [dates[max_idx]],
            [max_price],
            color="#a6e3a1",
            s=100,
            zorder=5,
            label=f"Máximo: ${max_price:.4f}",
        )
        ax1.scatter(
            [dates[min_idx]],
            [min_price],
            color="#f38ba8",
            s=100,
            zorder=5,
            label=f"Mínimo: ${min_price:.4f}",
        )

        # Linha de preço atual
        current_usd = current_price.get("usd", price_values[-1])
        ax1.axhline(
            y=current_usd,
            color="#f9e2af",
            linestyle="--",
            linewidth=2,
            alpha=0.8,
            label=f"Atual: ${current_usd:.4f}",
        )

        # Configurações do eixo de preços
        ax1.set_title(
            f"📈 {crypto_name.upper()} - Análise de Preço (30 dias)",
            fontsize=16,
            fontweight="bold",
            color="#cdd6f4",
            pad=20,
        )
        ax1.set_ylabel("Preço (USD)", fontsize=12, color="#cdd6f4")
        ax1.tick_params(colors="#cdd6f4")
        ax1.grid(True, alpha=0.3, color="#585b70")
        ax1.legend(
            loc="upper left",
            facecolor="#45475a",
            edgecolor="none",
            labelcolor="#cdd6f4",
        )

        # Formatação do eixo Y para preços
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.4f}"))

        # Gráfico de volume (subplot inferior)
        if volume_values:
            ax2.set_facecolor("#313244")
            bars = ax2.bar(
                dates,
                volume_values,
                color="#fab387",
                alpha=0.7,
                width=0.8,
                label="Volume 24h",
            )

            # Destacar barras de maior volume
            avg_volume = np.mean(volume_values)
            for i, (bar, vol) in enumerate(zip(bars, volume_values)):
                if vol > avg_volume * 1.5:
                    bar.set_color("#a6e3a1")
                    bar.set_alpha(0.9)

            ax2.set_ylabel("Volume (USD)", fontsize=12, color="#cdd6f4")
            ax2.tick_params(colors="#cdd6f4")
            ax2.grid(True, alpha=0.3, color="#585b70")
            ax2.legend(
                loc="upper left",
                facecolor="#45475a",
                edgecolor="none",
                labelcolor="#cdd6f4",
            )

            # Formatação do eixo Y para volume
            ax2.yaxis.set_major_formatter(
                plt.FuncFormatter(
                    lambda x, p: f"${x/1e9:.1f}B" if x >= 1e9 else f"${x/1e6:.1f}M"
                )
            )

        # Configuração do eixo X (datas)
        ax2.set_xlabel("Data", fontsize=12, color="#cdd6f4")

        # Formatação das datas
        date_formatter = DateFormatter("%d/%m")
        ax1.xaxis.set_major_formatter(date_formatter)
        ax2.xaxis.set_major_formatter(date_formatter)

        # Rotacionar labels das datas
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)

        # Ajustar layout
        plt.tight_layout()

        # Adicionar ao Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        self.chart_canvas = canvas

    def show_error(self, message):
        """Exibe mensagem de erro"""
        self.info_label.config(text=message, fg="#f38ba8")
        self.status_label.config(text="❌ Erro", fg="#f38ba8")


def mostrar_tela_cotacao_melhorada(root, voltar_tela=None):
    """Função principal para mostrar a tela de cotação melhorada"""
    for widget in root.winfo_children():
        widget.destroy()

    app = CryptoChartApp(root)

    # Botão voltar se fornecido
    if voltar_tela:
        voltar_frame = tk.Frame(root, bg="#1e1e2e")
        voltar_frame.pack(fill="x", padx=20, pady=10)

        tk.Button(
            voltar_frame,
            text="← Voltar",
            command=voltar_tela,
            font=("Segoe UI", 11),
            bg="#585b70",
            fg="#cdd6f4",
            relief="flat",
            activebackground="#6c7086",
            padx=15,
            pady=5,
            cursor="hand2",
        ).pack(side="left")

    # Carregar Bitcoin por padrão
    root.after(1000, app.search_crypto)


# Exemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x800")
    root.minsize(800, 600)

    mostrar_tela_cotacao_melhorada(root)

    root.mainloop()
