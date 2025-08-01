import tweepy

def get_comentarios(logger):
    """
    Coleta tweets relacionados ao tema futebol.
    Se ocorrer erro, registra no log.
    """
    try:
        twitter_api_key = 'SUA_API_KEY'
        twitter_api_secret = 'SUA_API_SECRET'
        twitter_access_token = 'SEU_ACCESS_TOKEN'
        twitter_access_token_secret = 'SEU_ACCESS_SECRET'

        # Autenticação
        auth = tweepy.OAuth1UserHandler(
            twitter_api_key, twitter_api_secret,
            twitter_access_token, twitter_access_token_secret
        )
        api = tweepy.API(auth)

        # Testa conexão
        api.verify_credentials()
        print('[DEBUG] Autenticação bem-sucedida!')

        # Coleta de tweets
        query = "futebol OR brasileirão OR copa"
        tweets = tweepy.Cursor(api.search_tweets, q=query, lang='pt', tweet_mode='extended').items(1000)

        comentarios = [tweet.full_text for tweet in tweets if hasattr(tweet, 'full_text')]
        return comentarios

    except Exception as e:
        logger.error("Erro ao autenticar ou coletar tweets: %s", str(e))
        print("Ocorreu um erro. Veja o log para mais detalhes.")
        return []

if __name__ == '__main__':
    pass