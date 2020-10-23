class InstagramAccount:
    
    def __init__(self, username, password):
        self.login_data = {
            'username' : username,
            'password' : password
        }

        self.__niche_accounts = []

    @property
    def niche_accounts(self) -> list:
        return self.__niche_accounts

    @niche_accounts.setter
    def niche_accounts(self, accounts : list) -> None:
        self.__niche_accounts = accounts
    