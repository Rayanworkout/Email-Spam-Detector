import os
import pickle
import string

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

class SpamDetector:
    def __init__(self, model_name: str = "email_classifier.pkl") -> None:
        self.vectorizer = None
        self.model = None
        
        script_dir = os.path.dirname(__file__)
        model_path = os.path.join(script_dir, model_name)
        
        # Load model and vectorizer
        with open(model_path, "rb") as file:
            saved_data = pickle.load(file)
            self.model = saved_data['model']
            self.vectorizer = saved_data['vectorizer']

    def __clean_text_data(self, text: str) -> str:
        stemmer = PorterStemmer()
        stop_words = set(stopwords.words("english"))

        text = text.lower()
        text = text.translate(str.maketrans("", "", string.punctuation))
        text = [stemmer.stem(word) for word in text.split() if word not in stop_words]

        return " ".join(text)

    def predict(self, text: str) -> str:
        cleaned_text = self.__clean_text_data(text)
        vectorized_email = self.vectorizer.transform([cleaned_text]).toarray()

        result = self.model.predict(vectorized_email)

        return "spam" if result[0] == 1 else "ham"

    def predict_many(self, texts: list) -> list:
        return [self.predict(text) for text in texts]
