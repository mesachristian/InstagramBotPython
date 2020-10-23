from abc import ABC, abstractmethod
from main.instagramAccount import InstagramAccount
from main.instagramHttpManager import InstagramHttpManager
from main.exceptions.badCredentialsException import BadCredentialsException
from main.exceptions.badResponseException import BadResponseException
from main.strategies.basicOperations import BasicOperation

class Strategy(ABC):

    def __init__(self, instagramAccount : InstagramAccount):
        self.instagramAccount = instagramAccount
        self.instagramHttpManager = InstagramHttpManager()
        self.run = True
        self.followBanned = False
        self.likeBanned = False
        self.unfollowBanned = False
        self.commentBanned = False
        self.check_login()
        
    def check_login(self):
        try:
            self.instagramHttpManager.login(self.instagramAccount.login_data)
            print(f'Correct login in {self.instagramAccount.login_data}')

        except BadCredentialsException as exception:
            print(exception.message)
            self.run = False

        except BadResponseException as exception:
            print(exception.message)
            self.run = False

    def execute_basic_operation(self, basicOperation : BasicOperation, resource_id : str , msg = None ):
        """
        Execute basic operation handles the exceptions of basic operations because they can be forbidden
        for the account so if that happens then the class attributes of banned are set True.

        Attributes: 
        -----------
        - resource_id: Couldbe media or user account id.
        - msg: Is used for comments.

        Examples:
        ---------
        - growStrategy.execute_basic_operation(BasicOperation.LIKE, '2406339833130538543')
        - growStrategy.execute_basic_operation(BasicOperation.COMMENT, '2406339833130538543', msg = 'So Cool!')
        """
        try:
            if basicOperation == BasicOperation.LIKE : 
                self.instagramHttpManager.like(resource_id)

            elif basicOperation == BasicOperation.FOLLOW : 
                self.instagramHttpManager.follow(resource_id)

            elif basicOperation == BasicOperation.UNFOLLOW : 
                self.instagramHttpManager.unfollow(resource_id)

            elif basicOperation == BasicOperation.COMMENT : 
                if msg != None : 
                    self.instagramHttpManager.comment( msg = msg , media_id= resource_id)
        
        except BadResponseException as exception:
            print(exception.message)
            if exception.status_code == 403:
                if basicOperation == BasicOperation.LIKE : 
                    self.likeBanned = True

                elif basicOperation == BasicOperation.FOLLOW : 
                    self.followBanned = True

                elif basicOperation == BasicOperation.UNFOLLOW : 
                    self.unfollowBanned = True

                elif basicOperation == BasicOperation.COMMENT : 
                    self.commentBanned = True
        
    def logout(self):
        try:
            self.instagramHttpManager.logout
        except BadResponseException as exception:
            print('Error in logout')
            print(exception.message)
        finally:
            print('\nSuccesful logout!')
            
    @abstractmethod
    def execute(self, instagram_account : InstagramAccount):
        pass

class GrowStrategy:
    
    def __init__(self, strategy : Strategy):
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy : Strategy) -> None:
        self._strategy = strategy

    def execute_strategy(self) -> None:
        self._strategy.execute()


