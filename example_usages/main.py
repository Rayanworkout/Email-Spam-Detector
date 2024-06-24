import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, parent_dir)

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
