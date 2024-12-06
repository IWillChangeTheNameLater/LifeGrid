from email.message import EmailMessage

from ..utils import format_template, read_template


def confirmation_email(confirmation_link: str) -> EmailMessage:
    msg = EmailMessage()
    msg['Subject'] = 'Confirm your email'

    body = read_template('confirmation_email.html')
    body = format_template(
        body, (('{confirmation_link}', confirmation_link), ),
        ignore_missed=False
    )
    msg.set_content(body, subtype='html')

    return msg
