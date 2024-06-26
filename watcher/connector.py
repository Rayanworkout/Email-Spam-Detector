import imaplib
import email
import atexit

from email.header import decode_header
from enum import Enum


class EmailStatus(Enum):
    UNSEEN = "UNSEEN"
    SEEN = "SEEN"
    ANSWERED = "ANSWERED"
    FLAGGED = "FLAGGED"
    DELETED = "DELETED"
    DRAFT = "DRAFT"
    RECENT = "RECENT"


class Connector:
    """
    Connect to an outlook account and fetch some email based on the status, thnen you can process the email.
    """

    def __init__(
        self,
        username: str,
        password: str,
        imap_server: str = "outlook.office365.com",
        port: int = 993,
    ) -> None:

        # CREDENTIALS
        self.username = username
        self.password = password

        # IMAP SERVER
        self.imap_server = imap_server
        self.port = port
        self.mail = self.__login()

        # Register the cleanup method to be called on program exit
        atexit.register(self.__exit__)

    def __login(self) -> imaplib.IMAP4_SSL:
        # Establish IMAP connection
        self.mail = imaplib.IMAP4_SSL(self.imap_server, self.port)
        self.mail.login(self.username, self.password)

        return self.mail

    def __exit__(self) -> None:
        if self.mail:
            try:
                # Check if we are in the SELECTED state before closing
                if self.mail.state == "SELECTED":
                    self.mail.close()

                # Always logout to properly end the session
                self.mail.logout()
            except Exception as e:
                print(f"Error while closing or logging out: {e}")

    def get_folder(
        self, folder: str = "inbox", status: EmailStatus = EmailStatus.UNSEEN
    ) -> list[str] | None:
        """
        Fetch a specific folder's email based on the status and return the decoded messages.
        """

        # Ensure the status is a valid EmailStatus enum member
        if not isinstance(status, EmailStatus):
            raise ValueError(
                f'Invalid status: "{status}". Must be an instance of EmailStatus enum.\nValid statuses: {", ".join([s.value for s in EmailStatus])}'
            )

        # Select the mailbox (folder)
        self.mail.select(folder)

        # Search for messages
        messages_fetch_status, messages = self.mail.search(None, status.value)

        if messages_fetch_status == "OK":
            # All messages end in a length 1 list, encoded as bytes
            # like [b'1 2 3 4 5 6 7 8 9 10'] where each number is a message number.
            messages = messages[0].split()

            if not messages:
                print(f'No messages found in "{folder}" with status "{status.value}".')
                return None

            # Decode the messages
            messages = [self.__decode_message(entry) for entry in messages]

            return messages

        else:
            print(f"Failed to fetch messages from {folder} with status {status.value}.")
            raise Exception(
                f"Failed to fetch messages from {folder}: {messages_fetch_status}"
            )

    def __decode_message(self, message: bytes) -> tuple | None:
        message = message.decode("utf-8")

        for num in message.split():
            status, data = self.mail.fetch(num, "(RFC822)")

            if status == "OK":
                raw_email = data[0][1]

                # Parse the raw email message
                msg = email.message_from_bytes(raw_email)

                # Extract email details
                try:
                    subject = decode_header(msg["Subject"])[0][0]
                    from_ = decode_header(msg.get("From"))[0][0]
                except KeyError:
                    print(f"Failed to decode subject or from for message {num}.")
                    return None

                for part in msg.walk():
                    if part is not None:
                        content_type = part.get_content_type()
                        # content_disposition = str(part.get("Content-Disposition"))

                        email_body = part.get_payload(decode=True)

                        if content_type == "text/plain":

                            # Finally decode the email body and return it along with the subject and from
                            decoded_content = email_body.decode(
                                "utf-8", errors="ignore"
                            )

                            full_email = f"Subject: {subject}\nFrom: {from_}\n\n{decoded_content}"

                            return (from_, subject, full_email)

            else:
                print(f"Failed to fetch message {num}: {status}")
                return None
