import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
try:
    from transformers import pipeline
except ImportError:
    pipeline = None

class SentimentAnalysis: 
    def __init__(self):
        self.df = None

    def load_data(self, path):
        print(f"Now loading from {path}...")
        self.df = pd.read_csv(path)

    def get_text_columns(self):
        results = []
        text_columns = self.df.select_dtypes(include=['object'])

        for column in text_columns.columns:
            avg_length = text_columns[column].dropna().apply(len).mean()  
            unique_entries = text_columns[column].nunique()
            
            results.append({
                'Column Name': column,
                'Average Entry Length': avg_length,
                'Unique Entries': unique_entries
            })
        result_df = pd.DataFrame(results)
    
        return result_df
    
    def vader_sentiment_analysis(self, data):
        analyzer = SentimentIntensityAnalyzer()
        scores = []
        sentiments = []

        for text in data:
            sentiment_scores = analyzer.polarity_scores(text)
            compound_score = sentiment_scores['compound']
            
            scores.append(compound_score)
            
            if compound_score >= 0.05:
                sentiments.append('positive')
            elif compound_score <= -0.05:
                sentiments.append('negative')
            else:
                sentiments.append('neutral')

        return scores, sentiments
    
    def textblob_sentiment_analysis(self, data):
        polarity_scores = []
        subjectivity_scores = []
        sentiments = []

        for text in data:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # polarity_scores
            subjectivity = blob.sentiment.subjectivity  # subjectivity_scores
            
            if polarity > 0:
                sentiment = 'positive'
            elif polarity == 0:
                sentiment = 'neutral'
            else:
                sentiment = 'negative'
            
            polarity_scores.append(polarity)
            subjectivity_scores.append(subjectivity)
            sentiments.append(sentiment)

        return polarity_scores, subjectivity_scores, sentiments

    def distilbert_sentiment_analysis(self, data):
        sentiment_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

        sentiments = []
        scores = []

        for text in data:
            result = sentiment_model(text)[0]  
            
            label = result['label']
            score = float(result['score'])
            
            if label in ['4 stars', '5 stars']:
                sentiment = 'positive'
            elif label == '3 stars':
                sentiment = 'neutral'
            else:
                sentiment = 'negative'
            
            sentiments.append(sentiment)
            scores.append(score)

        return scores, sentiments

def main():
    analysis = SentimentAnalysis()
    path = input("Please give the input:") 
    analysis.load_data(path)
    text_columns = analysis.get_text_columns()

    print("\nAvailable text columns:") 
    print(text_columns)

    column_number= input("\nPlease enter the name of the column to analyze:")
    data = analysis.df[column_number]

    print("\nPlease choose the type of sentiment analysis:")
    print("1. VADER Sentiment Analysis")
    print("2. TextBlob Sentiment Analysis")
    print("3. DistilBERT Sentiment Analysis")

    test_type = input("\nEnter the number corresponding to the sentiment analysis method: ") 
    
    if test_type == '1':
        print("\nRunning VADER Sentiment Analysis...")
        sentiments, scores = analysis.vader_sentiment_analysis(data)
        results_df = pd.DataFrame({
            'Text': data,
            'Sentiment': sentiments,
            'Score': scores
        })
    elif test_type == '2':
        print("\nRunning TextBlob Sentiment Analysis...")
        sentiments, polarities, subjectivities = analysis.textblob_sentiment_analysis(data)
        results_df = pd.DataFrame({
            'Text': data,
            'Sentiment': sentiments,
            'Polarity': polarities,
            'Subjectivity': subjectivities
        })
    elif test_type == '3':
        print("\nRunning DistilBERT Sentiment Analysis...")
        sentiments, scores = analysis.distilbert_sentiment_analysis(data)
        results_df = pd.DataFrame({
            'Text': data,
            'Sentiment': sentiments,
            'Score': scores
        })
    else:
        print("Invalid selection. Please choose 1, 2, or 3.")
        return
    
    print("\nSentiment Analysis Results:")
    print(results_df)


if __name__ == '__main__':
    main()
