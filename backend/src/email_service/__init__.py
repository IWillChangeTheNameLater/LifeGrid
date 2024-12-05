from email.message import EmailMessage
from smtplib import SMTP_SSL

from pydantic import ConfigDict, EmailStr, validate_call

from config import settings


@validate_call(config=ConfigDict(arbitrary_types_allowed=True))
def send_email(
    msg: EmailMessage,
    to_: EmailStr|list[EmailStr]|None = None,
    from_: EmailStr|None = settings.smtp_user,
    sync_addrs: bool = False
) -> None:
    if sync_addrs:
        from_ = msg['From'] = from_ or msg.get('From')

        if to_:
            msg['To'] = to_ if isinstance(to_, str) else ', '.join(to_)
        elif to_addrs := msg.get('To'):
            to_ = [a.strip() for a in to_addrs.split(',')]

    with SMTP_SSL(settings.smtp_host, settings.smtp_port) as server:
        server.login(settings.smtp_user, settings.smtp_pass)
        server.send_message(msg, from_, to_)
