from email.message import EmailMessage
from pathlib import Path
from smtplib import SMTP_SSL
from typing import Iterable, Tuple

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
    template_name: str|Path,
    templates_dir_path: str|Path = settings.email_templates_dir_path
) -> str:
    templates_dir_path = Path(templates_dir_path)
    template_path = Path(template_name)
    if not template_path.is_absolute():
        template_path = templates_dir_path/template_name

    return template_path.read_text()


def format_template(
    template: str,
    substitutions: Iterable[Tuple[str, str]],
    ignore_missed: bool = False,
) -> str:
    for s in substitutions:
        if not ignore_missed and s[0] not in template:
            raise ValueError(
                f'The template does not contain the "{s[0]}" substring'
            )
        template = template.replace(s[0], s[1])

    return template
