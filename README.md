# Email Spam Detector


This project is a basic email classifier that uses random forest to classify emails as spam or not ham (legit).
I grabbed 3 datasets from the web and I combined them into one.

The dataset is split into 80% training and 20% testing. Current accuracy is **0.96**, but the sample is very small.

I included the model that I trained with a dataset slice. It is ready to use so you don't need to train it yourself.


## Installation


Clone the repository and install the required libraries:

```bash
git clone https://github.com/Rayanworkout/Email-Spam-Detector.git
cd Email-Spam-Detector

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the required libraries
pip install -r requirements.txt
```


## Quick Start

If you just want to run the model without training it, there are a few ways to use it.

There is some boilerplate code inside `example_usages/main.py` to show the basic usage. Note that some abstraction is made inside `spam_detector.py` to make it easier to use the model.

```python
from spam_detector import SpamDetector

detector = SpamDetector()

email = "Congratulations! You have been selected as a winner. Text WON to 44255 to claim your prize."

is_spam = detector.predict(email)

print(is_spam) # True

emails_list = [
    "Hello, how are you?",
    "Get free money now! You have been selected as winner of our prize",
]

bulk_result = detector.predict_many(emails_list)

print(bulk_result) # [False, True]
```

There is also a flask app example that can be used as an API. You need to install Flask to run it.

```python
from spam_detector import SpamDetector

detector = SpamDetector()

# Endpoint to predict single email
@app.route("/predict", methods=["POST"])
def predict_email():
    data = request.get_json()
    email = data["email"]
    result = detector.predict(email)
    return jsonify({"result": result})


# Endpoint to predict multiple emails
@app.route("/predict_bulk", methods=["POST"])
def predict_emails_bulk():
    data = request.get_json()
    emails_list = data["emails"]
    bulk_result = detector.predict_many(emails_list)
    return jsonify({"results": bulk_result})


if __name__ == "__main__":
    app.run(debug=True)


# Example usage with curl:

# single email
# curl -X POST -H "Content-Type: application/json" -d '{"email": "Congratulations! You have been selected as a winner. Text WON to 44255 to claim your prize."}' http://localhost:5000/predict

# multiple emails
# curl -X POST -H "Content-Type: application/json" -d '{"emails": ["Hello, how are you?", "Get free money now! You have been selected as winner of our prize"]}' http://localhost:5000/predict_bulk
```


If you wish to monitor your emails as they arrive, I made 2 example scripts inside the `watcher` directory. There is a `connector` class that you can use to connect to your email server and fetch emails. **It currently supports outlook only, but it can be easily modified to support other email providers.**

The way to use this class is showed inside `watcher.py`. Here for example we monitor unseen emails and predict if they are spam or not.

```python
# CREDENTIALS
OUTLOOK_EMAIL = os.getenv("OUTLOOK_EMAIL")
OUTLOOK_PASSWORD = os.getenv("OUTLOOK_PASSWORD")

# Login to email server
conn = Connector(OUTLOOK_EMAIL, OUTLOOK_PASSWORD)

while True:
    messages = conn.get_folder(folder="inbox", status=EmailStatus.UNSEEN)

    if messages is not None:
        # Initialize the spam detector
        detector = SpamDetector()

        for message in messages:
            
            from_, subject, full_message = message
            
            is_spam = detector.predict(full_message)
            result = "spam" if is_spam else "ham"
            
            print(f'Message from "{from_}" is a {result}.')

    time.sleep(3600 * 2) # Check every 2 hours
```


### Training the model


If you want to train the model, you need to use the `notebooks/train_model.ipynb` notebook. It contains the code to train the model and save it as a pickle file.
Make sure you have the required libraries installed and `dataset.csv` in the same directory as the notebook.

```bash
cd Email-Spam-Detector

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

jupyter notebook
```

In the first cell, you can modify the `DATASET_SIZE` variable to change the size of the dataset. The default value is 6000, because my computer cannot handle the entire dataset, which is 16315 lines long.

_Disclaimer: the smaller the dataset, the less accurate the model will be, right now with 6000 lines, the model has an accuracy of 0.96, but it still makes mistakes._


After training the model and save it to a pickle file, you can use it as shown in the quick start section, with one difference: you need to load the model when initializing the `SpamDetector` class.

```python
from spam_detector import SpamDetector

detector = SpamDetector(model_name="your_trained_model.pkl")

email = "Congratulations! You have been selected as a winner. Text WON to 44255 to claim your prize."

print(detector.predict(email))

# Etc ...
```