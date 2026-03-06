from textblob import TextBlob

def analisar_texto(post):
    sentimento = TextBlob(post).sentiment.polarity
    return 1 if sentimento < -0.3 else 0
