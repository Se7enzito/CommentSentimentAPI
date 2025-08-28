# Como gerar datasets treinados para o sistema

## Utilizando ChatGPT e outras LLM's

- Colunas base de um dataset gerado para treino: Speaker [Opicional]; enunciado; número
  - Spekar -> Quem está falando
  - Enunciado -> Texto
  - Número -> Número para a emoção

| Número | Emoção   |
| ------- | ---------- |
| 1       | Neutro     |
| 2       | Felicidade |
| 3       | Raiva      |
| 4       | Surpresa   |
| 5       | Tristeza   |
| 6       | Disgosto   |
| 7       | Medo       |

Está são as emoções básicas conhecidas pelo nosso algoritmo de ML (Machine Learning), caso você deseje colocar novos tipos de emoções é necessário fazer modificações na hora de configurar o sistema, assim colocando que o número X é relacionado com a emoção Y.

### Lista de comandos para gerar um dataset de treino

1. Crie um dialogo randomico entre os personagens do seriado de TV "XX"
2. Você deve enumerar as emoções contidas nos enunciados entre 1 a 7, utilizando: 1- Neutro; 2- Felicidade; 3- Raiva; 4- Surpresa; 5- Tristeza; 6- Disgosto; 7-Medo;
3. Você tem que separar esses dialogos e enumerações em uma tabela CSV com as colunas: Speaker para quem estiver falando, enunciado para cada enunciado e numero para cada número de emoção

## Utilizando datasets ja existentes

- É necessário que no Dataset as emoções estejam enumeradas de acordo com a tabela abaixo:
  - OBS: Ainda vai ser criada a opção de colocar o próprio método para identificar emoções

| Número | Emoção   |
| ------- | ---------- |
| 0       | Neutro     |
| 1       | Felicidade |
| 2       | Raiva      |
| 3       | Medo       |
| 4       | Surpresa   |
| 5       | Tristeza   |
| 6       | Nojo       |
| 7       | Confiança |

Após os dados serem análisados pelo programa e enviados para a pasta de dados tratados, é necessário que os dados sejam enviados para o código de ML para que assim seja feito o aprendizado de máquina.
