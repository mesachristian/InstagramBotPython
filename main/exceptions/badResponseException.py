class BadResponseException(Exception):
    def __init__(self, status_code):
        self.status_code = status_code
        self.message = f'Wrong response. Status code : {status_code}'