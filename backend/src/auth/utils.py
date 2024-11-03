from fastapi import Response

from auth.models import Tokens


def set_tokens_in_cookies(response: Response, tokens: Tokens) -> None:
    response.set_cookie('access_jwt', tokens.access_token)
    response.set_cookie('refresh_jwt', tokens.refresh_token)
