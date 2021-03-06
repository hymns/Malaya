import malaya

def test_pretrained_bayes_sentiment():
    positive_text = 'Kerajaan negeri Kelantan mempersoalkan motif kenyataan Menteri Kewangan Lim Guan Eng yang hanya menyebut Kelantan penerima terbesar bantuan kewangan dari Kerajaan Persekutuan. Sedangkan menurut Timbalan Menteri Besarnya, Datuk Mohd Amar Nik Abdullah, negeri lain yang lebih maju dari Kelantan turut mendapat pembiayaan dan pinjaman.'
    news_sentiment = malaya.pretrained_bayes_sentiment()
    assert news_sentiment.predict(positive_text)[0][0] == 'negative'

def test_bahdanau_sentiment():
    malaya.get_available_sentiment_models()
    negative_text = 'kerajaan sebenarnya sangat bencikan rakyatnya, minyak naik dan segalanya'
    news_sentiment = malaya.deep_sentiment('bahdanau')
    assert len(news_sentiment.predict(negative_text)['attention']) > 1

def test_attention_sentiment():
    malaya.get_available_sentiment_models()
    negative_text = 'kerajaan sebenarnya sangat bencikan rakyatnya, minyak naik dan segalanya'
    news_sentiment = malaya.deep_sentiment('attention')
    assert len(news_sentiment.predict(negative_text)['attention']) > 1

def test_luong_sentiment():
    malaya.get_available_sentiment_models()
    negative_text = 'kerajaan sebenarnya sangat bencikan rakyatnya, minyak naik dan segalanya'
    news_sentiment = malaya.deep_sentiment('luong')
    assert len(news_sentiment.predict(negative_text)['attention']) > 1

def test_normal_sentiment():
    malaya.get_available_sentiment_models()
    negative_text = 'kerajaan sebenarnya sangat bencikan rakyatnya, minyak naik dan segalanya'
    news_sentiment = malaya.deep_sentiment('normal')
    assert news_sentiment.predict(negative_text)['negative'] > 0

def test_bayes_sentiment():
    import pandas as pd
    df = pd.read_csv('tests/02032018.csv',sep=';')
    df = df.iloc[3:,1:]
    df.columns = ['text','label']
    dataset = [[df.iloc[i,0],df.iloc[i,1]] for i in range(df.shape[0])]
    bayes=malaya.bayes_sentiment(dataset)
    assert len(bayes.predict(dataset[0][0])) > 0
