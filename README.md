# Email Spam Detector

This project is a basic email classifier that uses random forest to classify emails as spam or not ham (legit).
I grabbed 3 datasets from the web and I combined them into one.

The dataset is split into 80% training and 20% testing. Current accuracy is 0.96, but the sample is very small.

I also included the model that I trained on the dataset. You can use it to classify emails without having to train the model yourself.


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

If you just want to run the model without training it, you can use the model that I trained.

There is some boilerplate code inside `main.py` to show basic usage of the model. Note that some abstraction is made inside spam_detector.py to make it easier to use the model.

```python
from spam_detector import SpamDetector

detector = SpamDetector()

email = "Congratulations! You have been selected as a winner. Text WON to 44255 to claim your prize."

print(detector.predict(email))

emails_list = [
    "Hello, how are you?",
    "Get free money now! You have been selected as winner of our prize",
]

bulk_result = detector.predict_many(emails_list)

print(bulk_result)
```

If you want to train the model, you need to use the `train_model.ipynb` notebook. It contains the code to train the model and save it as a pickle file.
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