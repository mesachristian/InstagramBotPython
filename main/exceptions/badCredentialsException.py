class BadCredentialsException(Exception):
    def __init__(self, username):
        self.message = f'Fail login in {username} account. Bad credentials'