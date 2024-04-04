import pandas as pd
import re

# Functions
def extract_small_info(text):
    date = re.search(r'\b(\d{4}/\d{2}/\d{2})\b', text)
    source = re.search(r'Source:\s+([^|]+)', text)
    author = re.search(r'Author:\s+([^|]+)', text)
    column = re.search(r'Column:\s+(.+)', text)
    
    # Strip any excess space
    if date:
        date = date.group(1)
        date = pd.to_datetime(date, format='%Y/%m/%d', errors='coerce')
    if source:
        source = source.group(1).strip()
    if author:
        author = author.group(1).strip()
    if column:
        column = column.group(1).strip()
    
    return pd.Series({'date': date, 'source': source, 'author': author, 'column': column})

def clean_df(dataframe):
    # Used to clean scraped dataframe and returns the clean dataframe

    # Removes rows with no headline (not an article), or too many links (erroneously captured whole page in one entry).
    dataframe_filtered = dataframe[dataframe['headline'].apply(lambda x: len(x) > 0) & dataframe['link'].apply(lambda x: len(x) < 4)]

    # Concatenate headline lists so it's all one string
    dataframe_filtered.loc[:, 'headline'] = dataframe_filtered['headline'].apply(lambda x: ''.join(map(str, x[1:])) if isinstance(x, list) else x)

    # Convert link (sometimes repeated) to single link
    dataframe_filtered.loc[:, 'link'] = dataframe_filtered['link'].apply(lambda x: str(x[0]) if isinstance(x, list) else None)

    # Extract small
    dataframe_filtered.loc[:, ['date', 'source', 'author', 'column']] = dataframe_filtered['small'].apply(extract_small_info)

    # Drop small
    dataframe_clean = dataframe_filtered.drop('small', axis = 1)

    return(dataframe_clean)


# Australia
aus = pd.read_json('data/raw/aus.json')
aus_clean = clean_df(aus)
aus_clean.to_json('data/clean/aus.json', orient='records', date_format='iso', default_handler=str)

# New Zealand
# nz = pd.read_json('data/raw/nz.json')
# nz_clean = clean_df(nz)
# nz_clean.to_json('data/clean/nz.json', orient='records', date_format='iso', default_handler=str)

# # Canada
# canada = pd.read_json('data/raw/canada.json')
# canada_clean = clean_df(canada)
# canada_clean.to_json('data/clean/canada.json', orient='records', date_format='iso', default_handler=str)