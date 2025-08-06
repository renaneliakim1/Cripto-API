CryptoApp

Visão Geral do Projeto

O CryptoApp é uma aplicação desktop desenvolvida em Python utilizando a biblioteca tkinter para a interface gráfica. O objetivo principal do aplicativo é fornecer aos usuários cotações de criptomoedas em tempo real, permitindo-lhes acompanhar o mercado de forma simples e intuitiva. A aplicação é projetada para ser fácil de usar e visualmente agradável, com um foco na experiência do usuário.

Funcionalidades

Atualmente, o CryptoApp oferece as seguintes funcionalidades:

•
Cotações de Criptomoedas: Exibição de preços atualizados de diversas criptomoedas.

•
Interface Intuitiva: Navegação simples entre as telas inicial e de cotação.

•
Design Responsivo: A interface se adapta a diferentes tamanhos de janela.

•
Personalização Visual: Utilização de imagens de fundo e ícones para uma experiência visual aprimorada.

Tecnologias Utilizadas

O CryptoApp foi construído com as seguintes tecnologias:

•
Python 3: Linguagem de programação principal.

•
Tkinter: Biblioteca padrão do Python para criação de interfaces gráficas de usuário (GUI).

•
Pillow (PIL Fork): Biblioteca para manipulação de imagens, utilizada para o tratamento da imagem de fundo.

API de Cotação de Criptomoedas

O CryptoApp utiliza a CoinGecko API para obter os dados de cotação das criptomoedas. A CoinGecko é uma das maiores plataformas independentes de agregação de dados de criptomoedas do mundo, fornecendo informações abrangentes e confiáveis sobre o mercado de criptoativos.

Endpoints Principais Utilizados (Exemplos)

Embora o código fornecido não especifique os endpoints exatos, a CoinGecko API oferece uma variedade de endpoints para acessar dados de preços, mercado, históricos e metadados. Os endpoints mais relevantes para uma aplicação de cotação de criptomoedas seriam:

•
/simple/price: Para obter o preço atual de uma ou mais criptomoedas em diferentes moedas fiduciárias.

•
Exemplo de Requisição: https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd,brl

•
Exemplo de Resposta (JSON):



•
/coins/markets: Para obter uma lista de criptomoedas com dados de mercado (preço, capitalização de mercado, volume, etc.).

•
Exemplo de Requisição: https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false

•
Exemplo de Resposta (JSON - truncado para brevidade):



Requisições e Limites

A CoinGecko API possui limites de taxa para garantir a estabilidade do serviço. Para a API pública (gratuita), o limite é de 50-100 chamadas por minuto. Para uso mais intensivo ou acesso a dados mais avançados, a CoinGecko oferece planos pagos com limites de taxa mais elevados e funcionalidades adicionais.

É fundamental implementar um tratamento de erros e um mecanismo de rate limiting no aplicativo para evitar exceder os limites da API e garantir uma experiência de usuário fluida.

Como Executar o Projeto

Para executar o CryptoApp em sua máquina local, siga os passos abaixo:

Pré-requisitos

Certifique-se de ter o Python 3 instalado em seu sistema. Você pode baixá-lo em python.org.

Instalação das Dependências

1.
Clone o repositório (se aplicável):

2.
Crie um ambiente virtual (recomendado):

3.
Instale as bibliotecas necessárias:

Estrutura de Pastas (Sugestão)

Para que o aplicativo funcione corretamente com os caminhos de imagem, a estrutura de pastas deve ser semelhante a esta:

Plain Text


CryptoApp/
├── main.py
├── gui/
│   ├── __init__.py
│   ├── tela_inicial.py
│   └── tela_cotacao.py  # (Assumindo que existe um arquivo para a tela de cotação)
└── assets/
    ├── bitcoin.ico
    └── fundo.png


Execução

Após instalar as dependências e organizar a estrutura de pastas, execute o arquivo main.py:

Bash


python main.py


Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo LICENSE para mais detalhes.

Contato

Desenvolvido por Renã Eliakim.

Para dúvidas ou sugestões, entre em contato através de renaneliakim1@gmail.com.

