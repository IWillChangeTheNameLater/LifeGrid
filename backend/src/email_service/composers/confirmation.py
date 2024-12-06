from email.message import EmailMessage
from pathlib import Path


def confirmation_email(confirmation_link: str) -> EmailMessage:
    msg = EmailMessage()
    msg['Subject'] = 'Confirm your email'

    template_path = Path(
        __file__
    ).parent.parent/'templates'/'confirmation_email.html'
    with open(template_path, 'r') as file:
        body = file.read()
    body = body.replace('{confirmation_link}', confirmation_link)
    msg.set_content(body, subtype='html')

    return msg
