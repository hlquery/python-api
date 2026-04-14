class HlqueryException(Exception):
    pass


class AuthenticationException(HlqueryException):
    pass


class RequestException(HlqueryException):
    pass


class ValidationException(HlqueryException):
    pass


class CollectionException(HlqueryException):
    pass


class DocumentException(HlqueryException):
    pass


class SearchException(HlqueryException):
    pass
