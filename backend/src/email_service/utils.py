from email.message import EmailMessage
from pathlib import Path
from smtplib import SMTP_SSL
import sys

from pydantic import ConfigDict, EmailStr, validate_call

from config import settings


@validate_call(config=ConfigDict(arbitrary_types_allowed=True))
def send_email(
    msg: EmailMessage,
    to_: EmailStr|list[EmailStr]|None = None,
    from_: EmailStr|None = settings.smtp_user,
    sync_addrs: bool = True
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


def read_template(
    template_name: str|Path, templates_dir_path: str|Path|None = None
) -> str:
    template_path = Path(template_name)
    if not template_path.is_absolute():
        if templates_dir_path is None:
            templates_dir_path = Path(sys.path[0])/'email_service'/'templates'
        else:
            templates_dir_path = Path(templates_dir_path)

        template_path = templates_dir_path/template_name

    return template_path.read_text()
