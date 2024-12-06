from email.message import EmailMessage

from ..utils import read_template


def confirmation_email(confirmation_link: str) -> EmailMessage:
    msg = EmailMessage()
    msg['Subject'] = 'Confirm your email'

    body = read_template('confirmation_email.html')
    body = body.replace('{confirmation_link}', confirmation_link)
    msg.set_content(body, subtype='html')

    return msg
