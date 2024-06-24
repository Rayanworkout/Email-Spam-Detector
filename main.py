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
