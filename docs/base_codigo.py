# análise_sentimentos_futebol.py
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Simulação de dados (exemplo)
comentarios = [
"Esse time é fantástico!",
"Que jogo ruim...",
"Gostei da partida!",
"Horrível, não volto a assistir",
"Bom desempenho do goleiro"
] * 200 # Replicando para ter ~1000 dados

# Função para analisar sentimento
def analisar_sentimento(texto):
    analise = TextBlob(texto)

    if analise.sentiment.polarity > 0:
        return 'Positivo'
    elif analise.sentiment.polarity == 0:
        return 'Neutro'
    else:
        return 'Negativo'

# Criar DataFrame
df = pd.DataFrame({'comentario': comentarios})
df['sentimento'] = df['comentario'].apply(analisar_sentimento)

# Contagem de sentimentos
contagem = df['sentimento'].value_counts()

# Plotar gráfico de barras
contagem.plot(kind='bar', color=['green', 'blue', 'red'])
plt.title('Distribuição de Sentimentos')
plt.xlabel('Sentimento')
plt.ylabel('Quantidade')
plt.show()

# Gerar nuvem de palavras
texto_todos = ' '.join(df['comentario'])
wordcloud = WordCloud(width=800, height=400,
background_color='white').generate(texto_todos)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()