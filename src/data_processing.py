import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os 


nltk.download("stopwords")
nltk.download("wordnet")


lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

RAW_FILE = "../data/ffnews_data.csv"
PROCESSED_FILE = "../data/processed_data.csv"


def load_data(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    df = pd.read_csv(file_path)
    return df

def clean_text(text):
    # prepares text data for sentiment analysis: lowercase, remove special chars, stopwords, and lemmatize
    text = text.lower()
    text = re.sub(r"[^a-zA-Z]", " ", text)
    text = text.split() 
    text = [lemmatizer.lemmatize(word) for word in text if word not in stop_words]
    text = " ".join(text)
    return text

def clean_data(df):
    # removes duplicated rows based on 'Headline' and 'Timestamp' columns, na values, and cleans text data
    before = df.shape[0]
    df = df.dropna(subset=["Headline", "Timestamp"])
    df = df.drop_duplicates(subset=["Headline", "Timestamp"], keep="first")
    after = df.shape[0] 
    
    print(f"Removed {before - after} duplicate rows.")
    df["Headline"] = df["Headline"].apply(clean_text)
    return df


def save_cleaned_data(df, file_path):
    df.to_csv(file_path, index=False)
    print(f"Cleaned data saved to: {file_path} :)")


def main():
    df = load_data(RAW_FILE)
    if df is not None:
        df = clean_data(df)
        save_cleaned_data(df, PROCESSED_FILE)

if __name__ == "__main__":
    main()