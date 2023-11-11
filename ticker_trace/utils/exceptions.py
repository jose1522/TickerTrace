class DuplicateRecordException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class MissingRecordException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ExternalSourceException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
