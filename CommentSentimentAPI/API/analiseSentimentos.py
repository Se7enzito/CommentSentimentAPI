import nltk
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator
from langdetect import detect

# Variável global
analyzer = None

def setup_analise():
    global analyzer
    nltk.data.path.append('./CommentSentimentAPI/data/nltk_data')
    nltk.download('vader_lexicon', download_dir='./CommentSentimentAPI/data/nltk_data')
    nltk.download('punkt', download_dir='./CommentSentimentAPI/data/nltk_data')
    analyzer = SentimentIntensityAnalyzer()

def traduzir_para_ingles(texto: str) -> str:
    try:
        idioma_detectado = detect(texto)

        if idioma_detectado == "en":
            return texto 
        else:
            return GoogleTranslator(source='auto', target='en').translate(texto)
    except Exception:
        return texto

def analisar_sentimento(texto):
    if texto == 'N/A':
        return 'Neutro'
    
    texto_traduzido = traduzir_para_ingles(texto)
    vs = analyzer.polarity_scores(texto_traduzido)
    score = vs['compound']
    if score >= 0.05:
        return 'Positivo'
    elif score <= -0.05:
        return 'Negativo'
    else:
        return 'Neutro'

def find_sentiment_polarity_textblob(texto):
    texto_traduzido = traduzir_para_ingles(texto)
    blob = TextBlob(texto_traduzido)
    polarity = 0
    
    for sentence in blob.sentences:
        polarity += sentence.sentiment.polarity
        
    return polarity

def find_sentiment_subjectivity_textblob(texto):
    texto_traduzido = traduzir_para_ingles(texto)
    blob = TextBlob(texto_traduzido)
    subjectivity = 0
    
    for sentence in blob.sentences:
        subjectivity += sentence.sentiment.subjectivity
        
    return subjectivity

if __name__ == '__main__':
    pass