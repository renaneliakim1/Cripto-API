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
import sqlite3
import os
import matplotlib.dates as mpdates
import time 

# Tentar importar mplfinance, se não conseguir, usar implementação alternativa
try:
    from mplfinance.original_flavor import candlestick_ohlc
    MPLFINANCE_AVAILABLE = True
except ImportError:
    MPLFINANCE_AVAILABLE = False
    print("mplfinance não disponível, usando gráficos de linha apenas")

plt.style.use("seaborn-v0_8-darkgrid")
sns.set_palette("husl")


class CryptoChartApp:
    def __init__(self, root):
        self.root = root
        self.current_crypto = "bitcoin"
        self.chart_canvas = None
        self.chart_type = "candlestick"
        self.cache = {}
        self.last_request_time = 0  
        self.setup_database()
        self.setup_ui()
        self.setup_responsive_layout()
        
        self.root.after(300000, self.clear_old_cache) 

    def make_api_request(self, url, params=None, max_retries=2):
        """Faz requisição à API com cache e rate limiting otimizado"""
        cache_key = f"{url}_{str(params)}"
        
        current_time = time.time()
        if cache_key in self.cache:
            cached_data, cache_time = self.cache[cache_key]
            if current_time - cache_time < 300:  # Cache válido por 5 minutos
                return cached_data
        
        time_since_last = current_time - self.last_request_time
        if time_since_last < 0.5:
            time.sleep(0.5 - time_since_last)
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, params=params, timeout=8)
                response.raise_for_status()
                data = response.json()
                
                self.cache[cache_key] = (data, current_time)
                self.last_request_time = time.time()
                
                return data
                
            except requests.exceptions.RequestException as e:
                print(f"Tentativa {attempt + 1} falhou: {e}")
                if attempt < max_retries - 1:
                    time.sleep(0.5)
                else:
                    print(f"Todas as tentativas falharam para {url}")
                    return None

    def clear_old_cache(self):
        """Limpa cache antigo para evitar vazamento de memória"""
        current_time = time.time()
        keys_to_remove = []
        
        for key, (data, cache_time) in self.cache.items():
            if current_time - cache_time > 600:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.cache[key]
        
        self.root.after(300000, self.clear_old_cache)

    def force_clear_cache(self):
        """Força limpeza completa do cache"""
        self.cache.clear()
        self.last_request_time = 0
        print("Cache limpo forçadamente")

    def setup_database(self):
        """Configura o banco de dados SQLite3"""
        os.makedirs("database", exist_ok=True)
        self.db_path = os.path.join("database", "crypto_history.db")
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crypto_name TEXT NOT NULL,
                search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                price_usd REAL,
                price_brl REAL,
                change_24h REAL
            )
        ''')
        self.conn.commit()

    def save_search_history(self, crypto_name, price_data):
        """Salva histórico de busca no banco de dados"""
        try:
            usd_price = price_data.get("usd", 0)
            brl_price = price_data.get("brl", 0)
            change_24h = price_data.get("usd_24h_change", 0)
            
            self.cursor.execute('''
                INSERT INTO search_history (crypto_name, price_usd, price_brl, change_24h)
                VALUES (?, ?, ?, ?)
            ''', (crypto_name, usd_price, brl_price, change_24h))
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao salvar histórico: {e}")

    def get_search_history(self):
        """Obtém histórico de buscas"""
        try:
            self.cursor.execute('''
                SELECT crypto_name, search_date, price_usd, price_brl, change_24h
                FROM search_history
                ORDER BY search_date DESC
                LIMIT 50
            ''')
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar histórico: {e}")
            return []

    def show_history_window(self):
        """Mostra janela com histórico de consultas"""
        import tkinter.ttk as ttk
        history_window = tk.Toplevel(self.root)
        history_window.title("📊 Histórico de Consultas")
        history_window.geometry("900x650")
        history_window.configure(bg="#1e1e2e")
        
        # Centralizar janela
        window_width = 900
        window_height = 650
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        history_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(history_window, bg="#1e1e2e")
        header_frame.pack(fill="x", padx=20, pady=10)
        
        header_label = tk.Label(
            header_frame,
            text="📊 Histórico de Consultas",
            font=("Segoe UI", 18, "bold"),
            fg="#89b4fa",
            bg="#1e1e2e"
        )
        header_label.pack(side="left")

        # Frame para lista
        list_frame = tk.Frame(history_window, bg="#313244", bd=2, relief="groove")
        list_frame.pack(fill="both", expand=True, padx=20, pady=10, ipadx=10, ipady=10)
        
        # Criar Treeview com estilo personalizado
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                       background="#313244",
                       foreground="#cdd6f4",
                       fieldbackground="#313244",
                       bordercolor="#45475a",
                       borderwidth=0,
                       font=("Segoe UI", 10))
        style.configure("Treeview.Heading", 
                        background="#45475a",
                        foreground="#89b4fa",
                        font=("Segoe UI", 11, "bold"),
                        relief="flat")
        style.map("Treeview", background=[("selected", "#585b70")])
        
        columns = ("Cripto", "Data", "Preço USD", "Preço BRL", "Variação 24h")
        tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=20)
        
        # Configurar colunas
        tree.column("Cripto", width=120, anchor="center")
        tree.column("Data", width=180, anchor="center")
        tree.column("Preço USD", width=180, anchor="center")
        tree.column("Preço BRL", width=180, anchor="center")
        tree.column("Variação 24h", width=150, anchor="center")
        
        for col in columns:
            tree.heading(col, text=col)
        
        # Adicionar scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Buscar e exibir histórico
        history_data = self.get_search_history()
        for row in history_data:
            crypto_name, search_date, price_usd, price_brl, change_24h = row
            try:
                date_obj = datetime.fromisoformat(search_date.replace('Z', '+00:00'))
                formatted_date = date_obj.strftime("%d/%m/%Y %H:%M")
            except Exception:
                formatted_date = search_date
            
            formatted_usd = f"${price_usd:,.4f}" if price_usd else "N/A"
            formatted_brl = f"R$ {price_brl:,.2f}" if price_brl else "N/A"
            
            # Colorir variação
            if change_24h:
                if change_24h >= 0:
                    formatted_change = f"▲ {change_24h:+.2f}%"
                    tree.tag_configure('positive', foreground='#a6e3a1')
                    tags = ('positive',)
                else:
                    formatted_change = f"▼ {change_24h:+.2f}%"
                    tree.tag_configure('negative', foreground='#f38ba8')
                    tags = ('negative',)
            else:
                formatted_change = "N/A"
                tags = ()
            
            tree.insert("", "end", values=(
                crypto_name.upper(),
                formatted_date,
                formatted_usd,
                formatted_brl,
                formatted_change
            ), tags=tags)
        
        # Botão fechar
        close_button = tk.Button(
            history_window,
            text="Fechar",
            command=history_window.destroy,
            font=("Segoe UI", 12, "bold"),
            bg="#585b70",
            fg="#cdd6f4",
            relief="flat",
            padx=25,
            pady=8,
            cursor="hand2",
            activebackground="#6c7086"
        )
        close_button.pack(pady=15)

    def setup_responsive_layout(self):
        """Configura o layout responsivo"""
        self.root.grid_rowconfigure(0, weight=0)  # Header
        self.root.grid_rowconfigure(1, weight=0)  # Search and Info
        self.root.grid_rowconfigure(2, weight=1)  # Chart (expandable)
        self.root.grid_rowconfigure(3, weight=0)  # Status
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def setup_ui(self):
        """Configura a interface do usuário"""
        bg_color = "#1e1e2e"
        accent_color = "#89b4fa"
        text_color = "#cdd6f4"
        card_color = "#313244"
        highlight_color = "#585b70"

        self.root.configure(bg=bg_color)
        self.root.title("📈 Crypto Professional Charts")

        # Header - Row 0
        header_frame = tk.Frame(self.root, bg=bg_color)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(20, 10))

        header_label = tk.Label(
            header_frame,
            text="📈 Crypto Professional Charts",
            font=("Segoe UI", 22, "bold"),
            fg=accent_color,
            bg=bg_color,
        )
        header_label.pack()

        # Search frame - Row 1, Column 0
        search_frame = tk.Frame(self.root, bg=card_color, bd=0, highlightbackground=highlight_color, highlightthickness=1)
        search_frame.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=10, ipady=10)

        # Container para centralizar conteúdo
        search_container = tk.Frame(search_frame, bg=card_color)
        search_container.pack(expand=True, fill="both", padx=15, pady=10)

        tk.Label(
            search_container,
            text="🔍 Buscar Criptomoeda:",
            font=("Segoe UI", 13, "bold"),
            fg=text_color,
            bg=card_color,
        ).pack(pady=(0, 10), anchor="w")

        # Frame para entrada e botão de busca
        search_entry_frame = tk.Frame(search_container, bg=card_color)
        search_entry_frame.pack(fill="x", pady=5)

        self.search_entry = tk.Entry(
            search_entry_frame,
            font=("Segoe UI", 13),
            width=25,
            relief="solid",
            bd=1,
            bg="#45475a",
            fg=text_color,
            insertbackground=text_color,
            highlightbackground=highlight_color,
            highlightthickness=1,
            highlightcolor=accent_color,
        )
        self.search_entry.insert(0, "bitcoin")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.search_crypto())

        # Botão de busca ao lado do campo de entrada
        search_button = tk.Button(
            search_entry_frame,
            text="Buscar",
            command=self.search_crypto,
            font=("Segoe UI", 11, "bold"),
            bg=accent_color,
            fg="#1e1e2e",
            relief="flat",
            activebackground="#74c0fc",
            padx=20,
            pady=5,
            cursor="hand2",
        )
        search_button.pack(side="left")

        # Acesso rápido
        quick_frame = tk.Frame(search_container, bg=card_color)
        quick_frame.pack(fill="x", pady=(15, 5))

        tk.Label(
            quick_frame,
            text="⚡ Acesso Rápido:",
            font=("Segoe UI", 11),
            fg=text_color,
            bg=card_color,
        ).pack(side="left", padx=(0, 10))

        quick_buttons_frame = tk.Frame(quick_frame, bg=card_color)
        quick_buttons_frame.pack(side="left", fill="x", expand=True)

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
                font=("Segoe UI", 10),
                bg=highlight_color,
                fg=text_color,
                relief="flat",
                activebackground="#6c7086",
                padx=12,
                pady=4,
                cursor="hand2",
            ).pack(side="left", padx=4)

        # Buttons frame
        buttons_frame = tk.Frame(search_container, bg=card_color)
        buttons_frame.pack(fill="x", pady=(15, 5))

        # Botões principais
        action_buttons = [
            ("🔄 Atualizar", self.refresh_chart, "#a6e3a1", "#74c0fc"),
            ("📊 Histórico", self.show_history_window, "#fab387", "#f9e2af"),
            ("🗑️ Limpar Cache", self.force_clear_cache, "#f38ba8", "#eba0ac"),
        ]

        for text, command, bg, active_bg in action_buttons:
            tk.Button(
                buttons_frame,
                text=text,
                command=command,
                font=("Segoe UI", 11, "bold"),
                bg=bg,
                fg="#1e1e2e",
                relief="flat",
                activebackground=active_bg,
                padx=15,
                pady=6,
                cursor="hand2",
            ).pack(side="left", padx=5, pady=5)

        # Info frame - Row 1, Column 1
        self.info_frame = tk.Frame(self.root, bg=card_color, bd=0, highlightbackground=highlight_color, highlightthickness=1)
        self.info_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=10)

        self.info_label = tk.Label(
            self.info_frame,
            text="💡 Digite o nome de uma criptomoeda e clique em Buscar",
            font=("Segoe UI", 12),
            fg=text_color,
            bg=card_color,
            justify="left",
            wraplength=400,
            anchor="nw",
            padx=20,
            pady=20
        )
        self.info_label.pack(fill="both", expand=True)

        # Chart frame - Row 2 (expandable)
        self.chart_frame = tk.Frame(self.root, bg=bg_color, bd=0, highlightbackground=highlight_color, highlightthickness=1)
        self.chart_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=20, pady=(0, 10))
        self.chart_frame.grid_rowconfigure(0, weight=1)
        self.chart_frame.grid_columnconfigure(0, weight=1)

        # Status frame - Row 3
        self.status_frame = tk.Frame(self.root, bg=card_color, bd=0, highlightbackground=highlight_color, highlightthickness=1)
        self.status_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 20))

        self.status_label = tk.Label(
            self.status_frame,
            text="🟢 Pronto para buscar",
            font=("Segoe UI", 10),
            fg="#a6e3a1",
            bg=card_color,
            padx=20,
            pady=8,
        )
        self.status_label.pack(side="left")

        # Adicionar versão e créditos
        version_label = tk.Label(
            self.status_frame,
            text="v1.0 | © 2023 Crypto Charts",
            font=("Segoe UI", 9),
            fg="#7f849c",
            bg=card_color,
            padx=20,
        )
        version_label.pack(side="right")

        self.root.bind('<Configure>', self.on_window_resize)

    def on_window_resize(self, event):
        """Manipula o redimensionamento da janela"""
        if event.widget == self.root:
            new_width = min(event.width - 100, 1000)
            self.info_label.configure(wraplength=new_width//2 - 50)
            
            if self.chart_canvas:
                self.resize_chart()

    def resize_chart(self):
        """Redimensiona o gráfico para se adaptar à janela"""
        if self.chart_canvas:
            chart_width = max(self.chart_frame.winfo_width() - 40, 800)
            chart_height = max(self.chart_frame.winfo_height() - 40, 500)
            
            if chart_width > 100 and chart_height > 100:
                fig = self.chart_canvas.figure
                fig.set_size_inches(chart_width/100, chart_height/100)
                self.chart_canvas.draw()

    def quick_search(self, crypto_id):
        """Busca rápida para criptomoedas populares"""
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, crypto_id)
        self.search_crypto()

    def search_crypto(self):
        """Busca e exibe dados da criptomoeda"""
        try:
            crypto = self.search_entry.get().lower().strip()
            if not crypto:
                self.show_error("Por favor, digite o nome de uma criptomoeda")
                return

            self.current_crypto = crypto
            self.status_label.config(text="🔄 Buscando dados...", fg="#f9e2af")
            self.root.update()

            current_price = self.get_current_price(crypto)
            if not current_price:
                self.show_error("❌ Criptomoeda não encontrada ou erro na API")
                return

            historical_data = self.get_historical_data(crypto)
            if not historical_data or not historical_data.get("prices"):
                self.show_error("❌ Erro ao buscar dados históricos. Aguarde um momento e tente novamente!.")
                return

            try:
                self.save_search_history(crypto, current_price)
            except Exception as e:
                print(f"Erro ao salvar histórico: {e}")

            self.update_info(crypto, current_price)
            self.chart_type = "candlestick"
            self.create_professional_chart(crypto, historical_data, current_price)

            self.status_label.config(text="✅ Dados atualizados com sucesso", fg="#a6e3a1")
            
        except Exception as e:
            print(f"Erro geral na busca: {e}")
            self.show_error("❌ Erro inesperado. Tente novamente.")
            self.status_label.config(text="❌ Erro", fg="#f38ba8")

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

        data = self.make_api_request(url, params)
        if data and crypto_id in data:
            return data[crypto_id]
        return None

    def get_historical_data(self, crypto_id, days=30):
        """Busca dados históricos da criptomoeda"""
        url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
        params = {"vs_currency": "usd", "days": days, "interval": "daily"}

        data = self.make_api_request(url, params)
        if data:
            return {
                "prices": data.get("prices", []),
                "market_caps": data.get("market_caps", []),
                "total_volumes": data.get("total_volumes", []),
            }
        return None

    def get_ohlc_data(self, crypto_id, days=30):
        """Busca dados OHLC para candlestick"""
        url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/ohlc"
        params = {"vs_currency": "usd", "days": days}

        data = self.make_api_request(url, params)
        if data:
            ohlc_data = []
            for candle in data:
                timestamp, open_price, high, low, close = candle
                date = datetime.fromtimestamp(timestamp / 1000)
                ohlc_data.append([date, open_price, high, low, close])

            return ohlc_data
        return None

    def update_info(self, crypto_name, price_data):
        """Atualiza informações da criptomoeda"""
        usd_price = price_data.get("usd", 0)
        brl_price = price_data.get("brl", 0)
        change_24h = price_data.get("usd_24h_change", 0)
        market_cap = price_data.get("usd_market_cap", 0)
        volume_24h = price_data.get("usd_24h_vol", 0)

        def format_number(num):
            if num >= 1e12:
                return f"${num/1e12:.2f}T"
            elif num >= 1e9:
                return f"${num/1e9:.2f}B"
            elif num >= 1e6:
                return f"${num/1e6:.2f}M"
            elif num >= 1e3:
                return f"${num/1e3:.2f}K"
            else:
                return f"${num:.2f}"

        change_color = "#a6e3a1" if change_24h >= 0 else "#f38ba8"
        change_symbol = "▲" if change_24h >= 0 else "▼"

        info_text = f"""
🪙 {crypto_name.upper()} 
💵 Preço: ${usd_price:,.4f} USD | R$ {brl_price:,.2f} BRL
{change_symbol} Variação 24h: {change_24h:+.2f}%
📊 Capitalização: {format_number(market_cap)} USD
📈 Volume 24h: {format_number(volume_24h)} USD
        """.strip()

        self.info_label.config(text=info_text, fg="#cdd6f4")

    def create_professional_chart(self, crypto_name, data, current_price):
        """Cria gráfico profissional com múltiplas visualizações"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        if hasattr(self, 'chart_canvas') and self.chart_canvas:
            try:
                self.chart_canvas.get_tk_widget().destroy()
                self.chart_canvas = None
            except Exception as e:
                print(f"Erro ao destruir canvas: {e}")

        prices = data["prices"]
        volumes = data["total_volumes"]

        if not prices:
            self.show_error("❌ Dados de preços não disponíveis")
            return

        # Obter dimensões do frame
        chart_width = max(self.chart_frame.winfo_width() - 40, 800)
        chart_height = max(self.chart_frame.winfo_height() - 40, 500)
        
        fig_width = max(chart_width / 100, 10)
        fig_height = max(chart_height / 100, 6)

        # Criar figura com tamanho responsivo
        fig = plt.figure(figsize=(fig_width, fig_height), facecolor="#1e1e2e")
        
        # Definir layout de grade para os subplots
        gs = plt.GridSpec(2, 1, height_ratios=[3, 1], hspace=0.1)
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1], sharex=ax1)

        ax1.set_facecolor("#313244")
        ax2.set_facecolor("#313244")

        candlestick_ok = False
        if MPLFINANCE_AVAILABLE:
            try:
                self.create_candlestick_chart(ax1, crypto_name, fig_width)
                if not ax1.get_lines() and not ax1.collections:
                    print("Candlestick vazio, fallback para linha.")
                else:
                    candlestick_ok = True
            except Exception as e:
                print(f"Erro ao criar candlestick: {e}")
        if not candlestick_ok:
            self.create_line_chart(ax1, crypto_name, prices, current_price, fig_width)

        if volumes:
            bars = ax2.bar(
                [datetime.fromtimestamp(p[0] / 1000) for p in prices],
                [v[1] for v in volumes],
                color="#fab387",
                alpha=0.7,
                width=0.8,
                label="Volume 24h",
            )

            volume_values = [v[1] for v in volumes]
            avg_volume = np.mean(volume_values)
            for i, (bar, vol) in enumerate(zip(bars, volume_values)):
                if vol > avg_volume * 1.5:
                    bar.set_color("#a6e3a1")
                    bar.set_alpha(0.9)

            ax2.set_ylabel("Volume (USD)", fontsize=10, color="#cdd6f4")
            ax2.tick_params(colors="#cdd6f4", labelsize=9)
            ax2.grid(True, alpha=0.2, color="#585b70")
            ax2.legend(
                loc="upper left",
                facecolor="#45475a",
                edgecolor="none",
                labelcolor="#cdd6f4",
                fontsize=9,
            )

            ax2.yaxis.set_major_formatter(
                plt.FuncFormatter(
                    lambda x, p: f"${x/1e9:.1f}B" if x >= 1e9 else f"${x/1e6:.1f}M"
                )
            )

        ax2.set_xlabel("Data", fontsize=10, color="#cdd6f4")

        # Formatação das datas
        date_formatter = DateFormatter("%d/%m")
        ax1.xaxis.set_major_formatter(date_formatter)
        ax2.xaxis.set_major_formatter(date_formatter)

        # Rotacionar labels das datas
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha="right")
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha="right")

        # Ajustar layout
        plt.tight_layout(pad=3.0)

        # Adicionar ao Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        self.chart_canvas = canvas

    def create_candlestick_chart(self, ax, crypto_name, fig_width):
        """Cria gráfico de candlestick"""
        if not MPLFINANCE_AVAILABLE:
            print("mplfinance não disponível, usando gráfico de linha")
            return

        ohlc_data = self.get_ohlc_data(self.current_crypto)
        if not ohlc_data:
            print("Dados OHLC não disponíveis, usando gráfico de linha")
            return

        dates = [candle[0] for candle in ohlc_data]
        ohlc_values = []
        for candle in ohlc_data:
            date, open_price, high, low, close = candle
            date_num = mpdates.date2num(date)
            ohlc_values.append([date_num, open_price, high, low, close])

        try:
            candlestick_ohlc(
                ax,
                ohlc_values,
                width=0.6,
                colorup="#a6e3a1",
                colordown="#f38ba8",
                alpha=0.9,
            )
            
            ax.set_title(f"{crypto_name.upper()} - Candlestick Chart (USD)", 
                        fontsize=12, 
                        color="#89b4fa", 
                        pad=20,
                        y=1.05)
            ax.set_ylabel("Preço (USD)", fontsize=10, color="#cdd6f4")
            ax.tick_params(colors="#cdd6f4", labelsize=9)
            ax.grid(True, alpha=0.2, color="#585b70")
            
            # Adicionar preço médio
            avg_price = np.mean([candle[4] for candle in ohlc_data])
            ax.axhline(
                y=avg_price,
                color="#f9e2af",
                linestyle="--",
                linewidth=1,
                alpha=0.7,
                label=f"Média: ${avg_price:.2f}"
            )
            
            ax.legend(
                loc="upper left",
                facecolor="#45475a",
                edgecolor="none",
                labelcolor="#cdd6f4",
                fontsize=9,
            )
            
            # Formatar eixo Y
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.2f}"))
            
        except Exception as e:
            print(f"Erro ao desenhar candlestick: {e}")
            return

    def create_line_chart(self, ax, crypto_name, prices, current_price, fig_width):
        """Cria gráfico de linha"""
        dates = [datetime.fromtimestamp(p[0] / 1000) for p in prices]
        price_values = [p[1] for p in prices]

        line = ax.plot(
            dates,
            price_values,
            linewidth=2.5,
            color="#89b4fa",
            label=f"{crypto_name.upper()} Price",
            alpha=0.9,
        )[0]

        ax.fill_between(dates, price_values, alpha=0.2, color="#89b4fa")

        max_price = max(price_values)
        min_price = min(price_values)
        max_idx = price_values.index(max_price)
        min_idx = price_values.index(min_price)

        ax.scatter(
            [dates[max_idx]],
            [max_price],
            color="#a6e3a1",
            s=100,
            zorder=5,
            label=f"Máximo: ${max_price:.2f}",
        )
        ax.scatter(
            [dates[min_idx]],
            [min_price],
            color="#f38ba8",
            s=100,
            zorder=5,
            label=f"Mínimo: ${min_price:.2f}",
        )

        current_usd = current_price.get("usd", price_values[-1])
        ax.axhline(
            y=current_usd,
            color="#f9e2af",
            linestyle="--",
            linewidth=1.5,
            alpha=0.8,
            label=f"Atual: ${current_usd:.2f}",
        )

        ax.set_title(
            f"{crypto_name.upper()} - Price Chart (30 days)",
            fontsize=12,
            color="#cdd6f4",
            pad=20,
            y=1.05,
        )
        ax.set_ylabel("Preço (USD)", fontsize=10, color="#cdd6f4")
        ax.tick_params(colors="#cdd6f4", labelsize=9)
        ax.grid(True, alpha=0.2, color="#585b70")
        ax.legend(
            loc="upper left",
            facecolor="#45475a",
            edgecolor="none",
            labelcolor="#cdd6f4",
            fontsize=9,
        )

        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.2f}"))

    def show_error(self, message):
        """Exibe mensagem de erro"""
        self.info_label.config(text=message, fg="#f38ba8")
        self.status_label.config(text="❌ Erro", fg="#f38ba8")

    def __del__(self):
        """Destrutor para fechar conexão com banco de dados"""
        if hasattr(self, 'conn'):
            self.conn.close()


def mostrar_tela_cotacao_melhorada(root, voltar_tela=None):
    """Função principal para mostrar a tela de cotação melhorada"""
    for widget in root.winfo_children():
        widget.destroy()

    app = CryptoChartApp(root)

    # Botão voltar se fornecido
    if voltar_tela:
        voltar_frame = tk.Frame(root, bg="#1e1e2e")
        voltar_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

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
    root.geometry("1200x800")
    root.minsize(1000, 700)
    root.state('zoomed')  # Maximizar janela

    mostrar_tela_cotacao_melhorada(root)

    root.mainloop()