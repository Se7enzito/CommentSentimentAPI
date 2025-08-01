import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator

# Variável global
analyzer = None

def setup_analise():
    global analyzer
    nltk.data.path.append('./data/nltk_data')
    nltk.download('vader_lexicon', download_dir='./data/nltk_data')
    analyzer = SentimentIntensityAnalyzer()

def traduzir_para_ingles(texto: str) -> str:
    try:
        return GoogleTranslator(source='auto', target='en').translate(texto)
    except Exception as e:
        return texto

def analisar_sentimento(texto):
    texto_traduzido = traduzir_para_ingles(texto)
    vs = analyzer.polarity_scores(texto_traduzido)
    score = vs['compound']
    if score >= 0.05:
        return 'Positivo'
    elif score <= -0.05:
        return 'Negativo'
    else:
        return 'Neutro'

if __name__ == '__main__':
    pass