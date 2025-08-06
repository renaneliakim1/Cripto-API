
<h1 align="center"> CryptoApp </h1>


📌Visão Geral do Projeto

O CryptoApp é uma aplicação desktop desenvolvida em Python utilizando a biblioteca tkinter para a interface gráfica. O objetivo principal do aplicativo é fornecer aos usuários cotações de criptomoedas em tempo real, permitindo-lhes acompanhar o mercado de forma simples e intuitiva. A aplicação é projetada para ser fácil de usar e visualmente agradável, com um foco na experiência do usuário.




![Demonstração do Projeto](.github/gif.gif)


⚠️ Limitações Conhecidas
Requer conexão com a internet para atualizar cotações

Gráficos podem demorar para carregar com conexões lentas

A API CoinGecko tem limite de 10-30 requisições por minuto


🛠️ Tecnologias Utilizadas

O CryptoApp foi construído com as seguintes tecnologias:

•Linguagem Principal: Python 3.8+

•Interface Gráfica: Tkinter

•Visualização de Dados: Matplotlib, mplfinance

•Requisições HTTP: Requests

•Processamento de Imagens: Pillow (PIL)

•Banco de Dados: SQLite3

•Estilização: Seaborn

•
Python 3: Linguagem de programação principal.

•
Tkinter: Biblioteca padrão do Python para criação de interfaces gráficas de usuário (GUI).

•
Pillow (PIL Fork): Biblioteca para manipulação de imagens, utilizada para o tratamento da imagem de fundo.

API de Cotação de Criptomoedas

O CryptoApp utiliza a CoinGecko API para obter os dados de cotação das criptomoedas. A CoinGecko é uma das maiores plataformas independentes de agregação de dados de criptomoedas do mundo, fornecendo informações abrangentes e confiáveis sobre o mercado de criptoativos.

Requisições e Limites

A CoinGecko API possui limites de taxa para garantir a estabilidade do serviço. Para a API pública (gratuita), o limite é de 50-100 chamadas por minuto. Para uso mais intensivo ou acesso a dados mais avançados, a CoinGecko oferece planos pagos com limites de taxa mais elevados e funcionalidades adicionais.


🌐 Endpoints principais:

https://api.coingecko.com/api/v3/simple/price

https://api.coingecko.com/api/v3/coins/{id}/market_chart

https://api.coingecko.com/api/v3/coins/{id}/ohlc

Como Executar o Projeto

Para executar o CryptoApp em sua máquina local, siga os passos abaixo:

Pré-requisitos

Certifique-se de ter o Python 3 instalado em seu sistema. Você pode baixá-lo em python.org.

🚀 Instalação das Dependências

1.
Clone o repositório (se aplicável):

git clone https://github.com/seu-usuario/CryptoApp.git
cd CryptoApp

2.
Instale as bibliotecas necessárias:

pip install requests matplotlib mplfinance Pillow numpy seaborn pandas


📂 Estrutura de Pastas 

CryptoApp/
├── main.py                # Ponto de entrada da aplicação
├── gui/
│   ├── tela_inicial.py    # Tela inicial com fundo personalizado
│   └── tela_cotacao.py    # Tela de cotações com gráficos
├── assets/
│   ├── bitcoin.ico        # Ícone do aplicativo
│   └── fundo.png          # Imagem de fundo da tela inicial
├── database/
│   └── crypto_history.db  # Banco de dados SQLite
├── requirements.txt       # Dependências do projeto
└── README.md              # Este arquivo




🔧 Execução

Após instalar as dependências e organizar a estrutura de pastas, execute o arquivo main.py:

Bash

python main.py



🖥️ Funcionalidades Principais
1. Tela Inicial
Interface limpa e moderna

Fundo personalizável com transparência

Botão de acesso rápido para cotações

2. Tela de Cotações
Busca de Criptomoedas:

Suporte a mais de 100 criptomoedas

Acesso rápido às principais (Bitcoin, Ethereum, etc.)

Visualização de Dados:

Gráficos de candlestick (OHLC)

Gráficos de linha tradicionais

Volume de negociação

Informações Detalhadas:

Preço em USD e BRL

Variação percentual (24h)

Capitalização de mercado

Volume de negociação (24h)

Histórico:

Armazenamento local das últimas consultas

Visualização em tabela organizada

3. Recursos Avançados
Cache inteligente para reduzir chamadas à API

Atualização automática de dados

Limpeza de cache manual

Banco de dados SQLite integrado

🌐 API Utilizada





📄 Licença
Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

👨‍💻 Desenvolvedor
Renã Eliakim
