import re
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import pandas as pd

from API.logAPI import setup_logging
from API.comentariosTwitter import get_comentarios
from API.comentariosSimulados import comentarios_simulados
from API.analiseSentimentos import analisar_sentimento, setup_analise

# === Aplicativo de Análise ===
class App():
    # === Configurações Aplicativo ===
    def __init__(self) -> None:
        self.TWITTER_MODE = False

    # === Código Principal Aplicativo ===
    def run(self) -> None:
        setup_analise()
        logger = setup_logging()

        if self.TWITTER_MODE:
            comentarios = get_comentarios(logger)
        else:
            comentarios = comentarios_simulados()
            
        print(f'[DEBUG] Foram coletados ao todos {len(comentarios)} comentários.')
        
        df = pd.DataFrame({'comentario': comentarios})
        df['comentario_limpo'] = df['comentario'].apply(self.limpar_texto)
        df['sentimento'] = df['comentario_limpo'].apply(analisar_sentimento)
        
        print(df)
        
        # === Visualização ===
        plt.figure(figsize=(6,4))
        sns.countplot(data=df, x='sentimento', hue='sentimento', palette='Set2', legend=False)
        plt.title('Distribuição de sentimentos')
        plt.show()
        
        # === Nuvem de palavras ===
        texto = ' '.join(df['comentario_limpo'])
        wordcloud = WordCloud(width=800, height=400,
        background_color='white').generate(texto)
        plt.figure(figsize=(10,5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()
        
        # === Exibir primeiros comentários negativos ===
        negativos = df[df['sentimento'] == 'Negativo']
        print("Exemplos de comentários negativos:")
        print(negativos['comentario'].head())
        
    # === Código Limpeza do Texto ===
    def limpar_texto(self, texto: str) -> str:
        texto = texto.lower()
        
        texto = re.sub(r"http\\S+", "", texto)
        texto = re.sub(r"@[A-Za-z0-9_]+", "", texto)
        texto = re.sub(r"[^a-zà-ÿ ]", "", texto)
        
        return texto

if __name__ == '__main__':
    app = App()
    
    app.run()