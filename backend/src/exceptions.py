from fastapi import HTTPException, status


class LifeGridException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ''

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(LifeGridException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'The user already exists'


class UserIsNotPresentException(LifeGridException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'User is not present'


class IncorrectEmailOrPasswordException(LifeGridException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Incorrect email or password'


class EmailAlreadyVerified(LifeGridException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'The email has already been verified'


class TokenExpiredException(LifeGridException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Token has expired'


class TokenAbsentException(LifeGridException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Token is absent'


class IncorrectTokenFormatException(LifeGridException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Incorrect token format'


class TokenAlreadyRevoked(LifeGridException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'The token has already been revoked'
