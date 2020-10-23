from main.strategies.growStrategy import Strategy
from main.instagramAccount import InstagramAccount

from time import sleep

class TestStrategy(Strategy):
    
    def __init__(self, instagramAccount : InstagramAccount):
        super().__init__(instagramAccount)

    def execute(self):
        username = '__.jordan12'
        user_info = self.instagramHttpManager.get_user_info(username)
        print(user_info)

        sleep(20)

        print('End of test strategy')
        self.logout()
