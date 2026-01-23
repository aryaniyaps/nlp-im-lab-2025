import pandas as pd
from datasets import load_dataset
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load and prepare data
dataset = load_dataset("snips_built_in_intents")
full_df = pd.DataFrame(dataset['train'])
train_df, test_df = train_test_split(full_df, test_size=0.2, random_state=42, stratify=full_df['label'])

label_names = dataset['train'].features['label'].names
X_train = train_df['text'].tolist()
y_train = train_df['label'].tolist()

# Train model
tfidf_vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), min_df=2)
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_tfidf, y_train)

def predict_intent(text):
    text_tfidf = tfidf_vectorizer.transform([text])
    predicted_label = model.predict(text_tfidf)[0]
    confidence = model.predict_proba(text_tfidf)[0][predicted_label]
    return label_names[predicted_label], confidence

# Interactive classifier
print(f"Intents: {', '.join(label_names)}")

while True:
    user_text = input("> ")
    if user_text.lower() in ['quit', 'exit', 'q']:
        break
    if user_text.strip():
        intent, confidence = predict_intent(user_text)
        print(f"{intent} ({confidence:.0%})")