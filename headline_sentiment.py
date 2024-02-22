from transformers import pipeline
import pandas as pd

# Load model
sentiment_pipeline = pipeline(model="cardiffnlp/twitter-roberta-base-sentiment")

def sentiment_analyse(dataframe):
    # Analyses the sentiment of the article headlines using roberta
    # Convert from data frame to list
    headlines = dataframe['headline'].tolist()

    # Run NLP
    res = sentiment_pipeline(headlines, top_k=None)

    # Convert weird dictionary/list result to dictionary
    res_df = pd.DataFrame(res)

    dataframe['negative'] = res_df.apply(lambda row: next((item['score'] for item in row if item['label'] == 'LABEL_0'), None), axis=1)
    dataframe['neutral'] = res_df.apply(lambda row: next((item['score'] for item in row if item['label'] == 'LABEL_1'), None), axis=1)
    dataframe['positive'] = res_df.apply(lambda row: next((item['score'] for item in row if item['label'] == 'LABEL_2'), None), axis=1)

    dataframe['score'] = dataframe['positive'] - dataframe['negative']

    return(dataframe)

# Load and run on data
test = pd.read_json('data/clean/test.json')
test = sentiment_analyse(test)

print(test.head())

test.to_json('data/sentiment/test.json', orient='records', date_format='iso', default_handler=str)




