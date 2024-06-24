from spam_detector import SpamDetector


detector = SpamDetector()

email = "Congratulations! You have been selected as a winner. Text WON to 44255 to claim your prize."

print(detector.predict(email))