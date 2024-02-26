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
print("Analysing NZ")
# NZ
nz = pd.read_json('data/clean/nz.json')
nz = sentiment_analyse(nz)
print(nz.head())
nz.to_json('data/sentiment/nz.json', orient='records', date_format='iso', default_handler=str)

print("Analysing Australia")
# Australia
aus = pd.read_json('data/clean/aus.json')
aus = sentiment_analyse(aus)
print(aus.head())
aus.to_json('data/sentiment/aus.json', orient='records', date_format='iso', default_handler=str)

print("Analysing Canada")
# Canada
canada = pd.read_json('data/clean/canada.json')
canada = sentiment_analyse(canada)
print(canada.head())
canada.to_json('data/sentiment/canada.json', orient='records', date_format='iso', default_handler=str)