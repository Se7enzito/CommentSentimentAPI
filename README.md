# 📊 CommentSentimentAPI

Este projeto aplica técnicas de Processamento de Linguagem Natural (NLP) para analisar sentimentos de comentários relacionados ao futebol em redes sociais.

Com ele, é possível identificar padrões de polaridade (positiva, neutra e negativa), visualizar resultados em gráficos e nuvens de palavras e gerar insights relevantes para clubes, empresas e profissionais.

## 🧰 **Funcionalidades**

* Coleta de comentários do **Twitter** (via API), uso de comentários **simulados** ou uso de **datasets**;
* Limpeza e pré-processamento dos textos;
* Tradução automática dos textos para inglês antes da análise (garantindo melhor entendimento pelo modelo);
* Análise de sentimentos com **VADER** (do NLTK) e **TextBlob**;
* Visualização com **gráficos de distribuição** e **nuvem de palavras;**
* Geração de logs numerados para depuração;
* Listagem de exemplos de comentários negativos;
* Análise com **ML** sobre os comentários negativos, com funcionalidade de identificar comentários ofensivos;

### 🎲 Datasets

#### 📋 Datasets existentes no projeto

- [Tokyo Olympics 2020 Tweets](https://www.kaggle.com/datasets/gpreda/tokyo-olympics-2020-tweets/data)

#### ❓Como adicionar novos datasets

## 📦 **Estrutura do projeto**

```
 project/				# Diretório do projeto
├── CommentSentimentAPI/		# Diretório principal da API contendo o código-fonte.
│   ├── __init__.py			# Arquivo que transforma a pasta em pacote Python, permitindo importar módulos de forma organizada
│   ├── API/				# Pacote com os módulos principais da API, como análise de sentimento, coleta de comentários e logging.
│   │   ├── __init__.py			# Indica que a pasta API é um pacote Python, essencial para os imports funcionarem corretamente
│   │   ├── analiseSentimentos.py	# Funções de análise e tradução
│   │   ├── comentariosTwitter.py	# Coleta real do Twitter
│   │   ├── comentariosSimulados.py	# Geração de comentários simulados
│   │   └── logAPI.py			# Criação e configuração de logs
│   ├── data/				# Dados necessários para processamento, como datasets e recursos NLTK.
│   │   ├── datasets/			# Datasets utilizados para aprendizado de máquina
│   │   └── nltk_data/			# Dados baixados pelo NLTK (vader_lexicon)
│   ├── logs/				# Logs gerados durante a execução da API
│   │   └── log_1.log, log_2.log...	# Logs de execução numerados
│   ├── CommentSentimentAPI.py		# Código de API para desenvolvedores
├── docs/				# Documentos utilizados no desenvolvimento do projeto
|   ├── image/				# Imagens utilizadas no README_Antigo.md
|   ├── API_Usage_Example.py		# Exemplo da maneira de utilizar a API
|   ├── API_USAGE.md			# Explicação sobre como utilizar a API
|   ├── base_codigo.py			# Código utilizado como base para a ideia da API
|   ├── README_Antigo.md		# README de quando este era um projeto de faculdade
|   ├── Resumo Projeto... Folder	# Resumo do projeto utilizado para uma feira de tecnologia
|   └── Resumo Projeto... Escrito	# Resumo do projeto utilizado para uma feira de tecnologia
├── main.py				# Código principal do aplicativo, código de uso geral para gerar relatórios e pesquisas
├── LICENSE				# Licença do projeto
├── SECUTIRY.md				# Instruções para relatar vunerabilidades no código
├── .gitignore				# Arquivos ignorados pelo github
├── requirements.txt			# Requerimentos para o código rodar
└── README.md				# Este arquivo

```

## ✅ **Pré-requisitos**

* Python 3.8+
* [Tweepy]()
* [NLTK]()
* [Deep-translator](https://pypi.org/project/deep-translator/)
* [Pandas]()
* [Matplotlib]()
* [WordCloud]()
* [langdetect]()
* [tqdm]()
* [TextBlob]()

## ⚙️ **Instalação**

Clone o repositório e instale as dependências:

```
git clone https://github.com/Se7enzito/CommentSentimentAPI.git
cd CommentSentimentAPI
pip install -r requirements.txt
```

## 🚀 **Como executar**

**1.** Baixe os dados necessários do NLTK:

> Isso é feito automaticamente pelo código na primeira execução, salvando em `./data/nltk_data`

**2.** Configure se vai rodar com Twitter ou dados simulados:

No arquivo `main.py`, configure:

self.TWITTER_MODE = False   # False = simulados, True = coleta real

**3.** Execute:

python main.py

Você verá no console:

* Quantidade de comentários coletados
* Exemplos de comentários negativos
* E abrirá janelas com gráficos e nuvem de palavras

## 📌 **Sobre a tradução**

Para garantir que palavras em português sejam corretamente interpretadas pelo VADER (que é otimizado para inglês), o projeto traduz cada comentário antes de analisar.

> Feito com [deep-translator](https://pypi.org/project/deep-translator/) e a API do Google Translator.

## 🪵 **Logs**

* Todos os erros ou problemas são registrados em arquivos numerados na pasta `logs/`
* Exemplo: `logs/log_1.log`

## 🧪 **Exemplos esperados**

### Comentários Simulados

| Comentário original               | Sentimento |
| ---------------------------------- | ---------- |
| "Esse time é fantástico!"        | Positivo   |
| "Que jogo ruim..."                 | Negativo   |
| "Gostei da partida!"               | Positivo   |
| "Horrível, não volto a assistir" | Negativo   |
| "Bom desempenho do goleiro"        | Positivo   |

### Dataset (Tokyo Olympics 2020)

## Uso da API

Para a documentação completa, consulte [API_USAGE.md](docs/API_USAGE.md).

Para um exemplo completo, consulte [API_Usage_Example.py](docs/API_Usage_Example.py).

Para exemplos rápidos, veja abaixo.

```python

```

## ✏️ **Como contribuir / ideias futuras**

* Terminar função de pegar comentários do Twitter
* Melhorar análise para detectar ironia
* Adaptar VADER para léxico em português
* Usar modelos mais robustos (ex.: transformers)
* Expandir para outras redes (Instagram, YouTube)
* Análise temporal (evolução de sentimentos ao longo do tempo)

## 📄 **Licença**

Este projeto foi desenvolvido como parte de um estudo acadêmico / artigo científico.

Sinta-se livre para usar, estudar e melhorar com os devidos créditos.
