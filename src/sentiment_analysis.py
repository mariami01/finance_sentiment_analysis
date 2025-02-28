import pandas as pd
import re 

PROCESSED_FILE = "../data/processed_data.csv"
OUTPUT_FILE = "../data/sentiment_analysis.csv"
SENTIMENT_DICT_FILE = "../data/LoughranMcDonald_SentimentWordLists_2018.xlsx"


def load_sentiment_words(file_path):
    try:
        positive_words = pd.read_excel(file_path, sheet_name="Positive", header=None)[0].str.upper().tolist()
        negative_words = pd.read_excel(file_path, sheet_name="Negative", header=None)[0].str.upper().tolist()
        return positive_words, negative_words
    except Exception as e:
        print(f"Error loading sentiment words: {e}")
        return [], []


def classify_headline(headline, positive_words, negative_words):
    # Classifies a headline as Positive, Negative, or Neutral using sentiment words
    words = re.findall(r'\b[A-Z]+\b', headline.upper()) 

    pos_count = sum(1 for word in words if word in positive_words)
    neg_count = sum(1 for word in words if word in negative_words)

    if pos_count > neg_count:
        return "Positive"
    elif neg_count > pos_count:
        return "Negative"
    else:
        return "Neutral"



def analyze_sentiment(headlines_file):
    # Loads processed headlines, applies sentiment analysis, and saves results
    df = pd.read_csv(headlines_file)
    positive_words, negative_words = load_sentiment_words(SENTIMENT_DICT_FILE)
    df["Sentiment"] = df["Headline"].apply(lambda x: classify_headline(str(x), positive_words, negative_words))
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Sentiment analysis completed!!!! :))")

if __name__ == "__main__":
    analyze_sentiment(PROCESSED_FILE)