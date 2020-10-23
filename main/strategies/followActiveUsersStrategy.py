from main.strategies.growStrategy import Strategy
from main.instagramAccount import InstagramAccount
from main.instagramHttpManager import InstagramHttpManager
from main.exceptions.badCredentialsException import BadCredentialsException
from main.exceptions.badResponseException import BadResponseException
from main.strategies.basicOperations import BasicOperation

from time import sleep
from random import randint 

class FollowActiveUsersStrategy(Strategy):
    
    def __init__(self, instagramAccount : InstagramAccount):
        super().__init__(instagramAccount)

    def execute(self):

        while self.run:
            accounts = self.instagramAccount.niche_accounts

            for account in accounts:
                print("=" * 50) 
                print(account + ":")

                less_liked_media = self.get_account_less_liked_media(account, 36, 10)

                for media in less_liked_media:
                    shortcode = media['shortcode']
                    users_who_liked = self.instagramHttpManager.get_userlist_that_like_media(shortcode)                    
                    print("*" * 20)
                    print(f'For media {shortcode}')

                    for username in users_who_liked:
                        
                        self.follow_protocol(username)
                        if(self.followBanned):
                            break
                        print(f'{username} followed!!')
                    
                    if(self.followBanned):
                        break

                if(self.followBanned):
                    self.run = False
                    print('*' * 40)
                    print('FOLLOW BANNED!!!')
                    print('*' * 40)
                    break

                    
                sleep(8)

            self.run = False 


        print('End of follow active users strategy')
        self.logout()

    def get_last_n_shortcodes_from(self, n : int, username :str) -> list:
        media = []
        account_info = self.instagramHttpManager.get_user_info(username)
        account_id = account_info['user_id'] 

        media.extend(account_info['media'])
        
        end_cursor = account_info['end_cursor']
        
        range_of_media = int((n - 12) / 12)
        for i in range(0, range_of_media):
            (next_publications, end_cursor) = self.instagramHttpManager.get_media_from_username_after(account_id, end_cursor)
            media.extend(next_publications)
            sleep(randint(5,7))

        return media
        
    def get_account_less_liked_media(self, username : str, total_media : int, return_size : int ) -> list:
        
        shortcodes = self.get_last_n_shortcodes_from(n=total_media, username=username)
        
        less_liked_media = []
        for i in range(0, return_size):
            less_liked_media.append({ 'shortcode' : '' , 'likes' : 10000000})
        
        for shortcode in shortcodes:
            media_info = self.instagramHttpManager.get_media_info(shortcode)
            likes = media_info['likes']

            for index, media in enumerate(less_liked_media):
                if likes < media['likes']:
                    less_liked_media[index] = {'shortcode' : shortcode, 'likes' : likes}
                    break
                    
        return less_liked_media

    def follow_protocol(self, username : str):
        user_info = self.instagramHttpManager.get_user_info(username)
    
        if user_info is not None:
            if user_info['followed_by_viewer'] == False and user_info['follows_viewer'] == False:
                
                sleep(randint(3,4))

                if user_info['is_private'] == False : 

                    user_media = user_info['media']
                    if len(user_media) > 5:
                        media_info = self.instagramHttpManager.get_media_info(user_media[1])
                        self.execute_basic_operation(BasicOperation.LIKE, media_info['media_id'])

                        sleep(randint(3,5))

                        media_info = self.instagramHttpManager.get_media_info(user_media[4])
                        self.execute_basic_operation(BasicOperation.LIKE, media_info['media_id'])
                
                else:
                    if user_info['requested_by_viewer'] == False:
                        self.execute_basic_operation(BasicOperation.FOLLOW, user_info['user_id'])
                    return

                self.execute_basic_operation(BasicOperation.FOLLOW, user_info['user_id'])