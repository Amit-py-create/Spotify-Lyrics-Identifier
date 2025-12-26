import pandas as pd
import re
import nltk

from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

nltk.download('stopwords')

# Load CSV
df = pd.read_csv("spotify_songs.csv")

# Text preprocessing
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return " ".join(words)

df["clean_lyrics"] = df["lyrics"].apply(clean_text)

# Tokenization
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(df["clean_lyrics"])

sequences = tokenizer.texts_to_sequences(df["clean_lyrics"])
padded_sequences = pad_sequences(sequences, maxlen=50)

# Prediction function
def predict_song(snippet):
    snippet = clean_text(snippet)
    seq = tokenizer.texts_to_sequences([snippet])
    pad_seq = pad_sequences(seq, maxlen=50)
    similarity = cosine_similarity(pad_seq, padded_sequences)
    index = similarity.argmax()
    return df.iloc[index]["track_name"], df.iloc[index]["artist_name"]

# Run test
if __name__ == "__main__":
    text = "I been on my own for long enough"
    song, artist = predict_song(text)
    print("Song:", song)
    print("Artist:", artist)
correct = 0

for i in range(len(df)):
    snippet = df.iloc[i]["lyrics"][:30]
    predicted, _ = predict_song(snippet)
    if predicted == df.iloc[i]["track_name"]:
        correct += 1

accuracy = (correct / len(df)) * 100
print("Model Accuracy:", accuracy, "%")
