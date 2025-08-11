import re
import time
import warnings
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
from tqdm import tqdm

from CommentSentimentAPI.API.logAPI import setup_logging
from CommentSentimentAPI.API.comentariosTwitter import get_comentarios
from CommentSentimentAPI.API.comentariosSimulados import comentarios_simulados
from CommentSentimentAPI.API.analiseSentimentos import analisar_sentimento, setup_analise, find_sentiment_polarity_textblob, find_sentiment_subjectivity_textblob

# === Aplicativo de Análise ===
class App():
    # === Configurações Aplicativo ===
    def __init__(self) -> None:
        self.TWITTER_MODE = False
        self.DATASET_MODE = True
        self.LIMIT = 200 # Caso queira desativar coloque -1
        self.RANDOM_DATA = True
        self.LINHA_COMENTARIOS = 'text'
        # text -> Tokyo 2020

    # === Código Principal Aplicativo ===
    def run(self) -> None:
        tqdm.pandas()
        
        setup_analise()
        logger = setup_logging()

        if self.DATASET_MODE:
            df = pd.read_csv("CommentSentimentAPI/data/datasets/tokyo_2020_tweets.csv")

            if self.LIMIT != -1:
                if self.RANDOM_DATA:
                    df = df.head(self.LIMIT)
                else:
                    df = df.sample(n=self.LIMIT, random_state=42)
            
            df = df.dropna(subset=[self.LINHA_COMENTARIOS])
            df[self.LINHA_COMENTARIOS] = df[self.LINHA_COMENTARIOS].astype(str)
            df['comentario_limpo'] = df[self.LINHA_COMENTARIOS].progress_apply(self.limpar_texto)
            df['sentimento'] = df['comentario_limpo'].progress_apply(analisar_sentimento)
        else:
            if self.TWITTER_MODE:
                comentarios = get_comentarios(logger)
            else:
                comentarios = comentarios_simulados()
                
            print(f'[DEBUG] Foram coletados ao todos {len(comentarios)} comentários.')
            
            df = pd.DataFrame({self.LINHA_COMENTARIOS: comentarios})
            df['comentario_limpo'] = df[self.LINHA_COMENTARIOS].progress_apply(self.limpar_texto)
            df['sentimento'] = df['comentario_limpo'].progress_apply(analisar_sentimento)
        
        self.show_wordcloud(df[self.LINHA_COMENTARIOS], title = 'Prevalent words in text')
        
        self.plot_sentiment(df, 'sentimento', 'Text')
        
        self.show_wordcloud(df.loc[df['sentimento']=='Positivo', 'text'], title = 'Prevalent words in texts (Positive sentiment)')
        self.show_wordcloud(df.loc[df['sentimento']=='Neutro', 'text'], title = 'Prevalent words in texts (Negative sentiment)')
        self.show_wordcloud(df.loc[df['sentimento']=='Negativo', 'text'], title = 'Prevalent words in texts (Neutral sentiment)')
        
        df['text_sentiment_polarity'] = df['comentario_limpo'].progress_apply(lambda x: find_sentiment_polarity_textblob(x))
        df['text_sentiment_subjectivity'] = df['comentario_limpo'].progress_apply(lambda x: find_sentiment_subjectivity_textblob(x))
        
        self.plot_sentiment_textblob(df, self.LINHA_COMENTARIOS, 'Text')
        
    # === Código Limpeza do Texto ===
    def limpar_texto(self, texto: str) -> str:
        if not isinstance(texto, str):
            return "N/A"
        
        texto = texto.lower()
        
        texto = re.sub(r"http\\S+", "", texto)
        texto = re.sub(r"@[A-Za-z0-9_]+", "", texto)
        texto = re.sub(r"[^a-zà-ÿ# ]", "", texto)
        
        return texto

    # === Código Conferência Dados Faltantes ===
    def missing_data(self, data):
        total = data.isnull().sum()
        percent = (data.isnull().sum()/data.isnull().count()*100)
        tt = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
        types = []
        
        for col in data.columns:
            dtype = str(data[col].dtype)
            types.append(dtype)
            
        tt['Types'] = types
        
        return(np.transpose(tt))

    # === Código Nuvem de Palavras ===
    def show_wordcloud(self, data, title=""):
        text = " ".join(t for t in data.dropna().astype(str))

        if not text.strip():
            print(f"[AVISO] Nenhum texto disponível para gerar wordcloud: {title}")
            return

        stopwords = set(STOPWORDS)
        stopwords.update([
            "t", "co", "https", "amp", "U", 
            "Olympics", "Tokyo2020", "TokyoOlympics", 
            "Olympic", "Olympics Tokyo2020", "Tokyo2020 Olympics"
        ])

        wordcloud = WordCloud(
            stopwords=stopwords, 
            scale=4, 
            max_font_size=50, 
            max_words=500,
            background_color="black"
        ).generate(text)

        fig = plt.figure(1, figsize=(16, 16))
        plt.axis('off')
        fig.suptitle(title, fontsize=20)
        fig.subplots_adjust(top=2.3)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.show()

    # === Código Gráfico de Sentimetnos ===
    def plot_sentiment(self, df, feature, title):
        counts = df[feature].value_counts()
        percent = counts/sum(counts)

        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 5))

        counts.plot(kind='bar', ax=ax1, color='green')
        percent.plot(kind='bar', ax=ax2, color='blue')
        ax1.set_ylabel(f'Counts : {title} sentiments', size=12)
        ax2.set_ylabel(f'Percentage : {title} sentiments', size=12)
        plt.suptitle(f"Sentiment analysis: {title}")
        plt.tight_layout()
        plt.show()

    # === Código Gráfico de Frequência ===
    def plot_sentiment_textblob(self, df, feature, title):
        polarity = df[feature+'_sentiment_polarity']
        subjectivity = df[feature+'_sentiment_subjectivity']

        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 5))

        polarity.plot(kind='kde', ax=ax1, color='magenta')
        subjectivity.plot(kind='kde', ax=ax2, color='green')
        ax1.set_ylabel(f'Sentiment polarity : {title}', size=12)
        ax2.set_ylabel(f'Sentiment subjectivity: {title}', size=12)
        plt.suptitle(f"Sentiment analysis (polarity & subjectivity): {title}")
        plt.tight_layout()
        plt.show()

# === Código Padrão Classe ===
if __name__ == '__main__':
    warnings.simplefilter('ignore')
    inicio = time.time()
    
    app = App()
    app.run()
    
    fim = time.time()
    duracao = fim - inicio
    
    minutos = int(duracao // 60)
    horas = int(minutos // 24)
    minutos = minutos % 24
    segundos = duracao % 60

    print(f"Tempo de execução: {horas} h {minutos} min {segundos:.2f} s")