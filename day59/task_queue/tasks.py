import time

def send_email_task(task: dict):
    """
    Simulate sending an email.
    task: {
        "recipient_email": str,
        "subject": str,
        "body": str
    }
    """
    print(f"Sending email to: {task['recipient_email']}")
    print(f"Subject: {task['subject']}")
    print(f"Body: {task['body']}")
    # Simulate delay for sending email
    time.sleep(2)
    print(f"Email sent to {task['recipient_email']}\n")
