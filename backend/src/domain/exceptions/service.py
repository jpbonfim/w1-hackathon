class BadRequestError(Exception):
    pass


class NotFoundError(Exception):
    pass


class EntityNotFound(Exception):
    pass


class Unauthorized(Exception):
    pass

class CouldNotValidateCredentials(Exception):
    pass