import os
import sys

from connector import Connector, EmailStatus
from dotenv import load_dotenv

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from spam_detector import SpamDetector

load_dotenv()


# CREDENTIALS
OUTLOOK_EMAIL = os.getenv("OUTLOOK_EMAIL")
OUTLOOK_PASSWORD = os.getenv("OUTLOOK_PASSWORD")

conn = Connector(OUTLOOK_EMAIL, OUTLOOK_PASSWORD)

messages = conn.get_folder(folder="inbox", status=EmailStatus.UNSEEN)

if messages is not None:
    # Initialize the spam detector
    detector = SpamDetector()

    for message in messages:
        
        from_, subject, full_message = message
        
        is_spam = detector.predict(full_message)
        result = "spam" if is_spam else "ham"
        
        print(f'Message from "{from_}" is a {result}.')
