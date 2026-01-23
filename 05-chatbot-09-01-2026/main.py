import nltk
import random
import string
import json

from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

nltk.download('punkt')
nltk.download('stopwords')

intents = {
    "greeting": {
        "patterns": ["Hi", "Hello", "Hey", "Good morning", "Good evening"],
        "responses": ["Hello!", "Hi there!", "Greetings!"]
    },
    "goodbye": {
        "patterns": ["Bye", "See you later", "Goodbye"],
        "responses": ["Goodbye!", "See you later!", "Take care!"]
    },
    "thanks": {
        "patterns": ["Thanks", "Thank you", "Much appreciated"],
        "responses": ["You're welcome!", "No problem!", "Anytime!"]
    },
    "about": {
        "patterns": ["What is this?", "Tell me about yourself", "Who are you?"],
        "responses": ["I am a chatbot created to assist you.", "I'm here to help you with your questions."]
    }
}

# text preprocessing function

stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)


# Prepare training data
X = []

y = []

for intent, data in intents.items():
    for pattern in data['patterns']:
        X.append(preprocess_text(pattern))
        y.append(intent)

vectorizer = TfidfVectorizer()
X_vectors = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vectors, y)

# chatbot response function
def get_chatbot_response(user_input):
    processed_input = preprocess_text(user_input)
    input_vector = vectorizer.transform([processed_input])
    predicted_intent = model.predict(input_vector)[0]
    return random.choice(intents[predicted_intent]['responses'])

# run the chatbot

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Chatbot: Goodbye!")
        break
    response = get_chatbot_response(user_input)
    print(f"Chatbot: {response}")