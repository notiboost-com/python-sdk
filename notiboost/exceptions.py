class NotiBoostException(Exception):
    def __init__(self, message: str, status_code: int = 0, response: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response or {}

