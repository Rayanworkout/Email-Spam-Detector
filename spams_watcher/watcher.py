import os
import sys
import time

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

# Initialize the spam detector
detector = SpamDetector()

while True:
    try:
        messages = conn.get_folder(folder="inbox", status=EmailStatus.UNSEEN)

        if messages is not None:
            for message in messages:

                from_, subject, full_message = message

                is_spam = detector.predict(full_message)
                result = "spam" if is_spam else "ham"

                print(f'Message from "{from_}" is a {result}.')

        time.sleep(3600 * 2)  # Check every 2 hours

    except KeyboardInterrupt:
        print("Exiting the program.")
        exit(0)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(60)
