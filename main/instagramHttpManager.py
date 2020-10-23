from main.instagramEndpoints import InstagramEndpoints
from main.exceptions.badCredentialsException import BadCredentialsException
from main.exceptions.badResponseException import BadResponseException

import requests
from datetime import datetime
import json
import time

class InstagramHttpManager(InstagramEndpoints):
    
    """
    This class handles http request to instagram service
    """

    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'

    def __init__(self):
        self.session = requests.Session()
        self.csrftoken = ""
        self.session.headers = {'user-agent':self.USER_AGENT}

    def login(self, login_info):
        """
        This methods logs in into an account using the username and
        the password. It also saves session information like cookies
        and csrftoken in the header.
        
        Attributes:
        ----------
        - login_info : {'username' : <username> , 'password' : <password>}

        Raises:
        ------- 
        - BadCredentialsException
        - BadResponseException
        """

        time = int(datetime.now().timestamp())
        username = login_info['username']
        password = login_info['password']

        login_data = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',  # Send plain password
            'queryParams': {},
            'optIntoOneTap': 'false'
        }
        
        request = self.session.get(self.BASE_URL)
        self.session.headers.update({'X-CSRFToken':request.cookies['csrftoken']})
        login = self.session.post(self.LOGIN_URL,login_data,allow_redirects=True)
        
        if(login.status_code == 200):
            self.session.headers.update({'X-CSRFToken':login.cookies['csrftoken']})
            response = json.loads(login.text)

            if(response['authenticated'] == True):
                self.csrftoken = login.cookies['csrftoken']
            else:
                raise BadCredentialsException(username)
        
        else:
            raise BadResponseException(login.status_code)

    def logout(self):
        """
        Logout of the account

        Raises:
        -------
        - BadResponseException
        """
        logout_post = {'one_tap_app_login': 0}
        request = self.session.post(self.LOGOUT_URL,data=logout_post)

        if(request.status_code != 200):
            raise BadResponseException(request.status_code)
        
        response = json.loads(request.text)
        
        #self.session.config['keep_alive'] = False

        return response
    
    def follow(self,user_id):
        """
        Follow an account given the user id.

        Attributes: 
        -----------
            user_id : User's id as a stirng. Ex:'8546523470'
        Raises:
        -------
            - BadResponseException 
        """
        follow_url_final = self.FOLLOW_URL % user_id
        
        request = self.session.post(follow_url_final)
        status_code = request.status_code 
        if status_code != 200 :
            raise BadResponseException(status_code)

    def unfollow(self,user_id):
        """
        Unfollow an account given the user id of 
        the account.

        Attributes: 
        -----------
            user_id : User's id as a stirng. Ex:'8546523470'
        Raises:
        -------
            - BadResponseException 
        """
        unfollow_url_final = self.UNFOLLOW_URL % user_id
        
        request = self.session.post(unfollow_url_final)
        status_code = request.status_code 
        if status_code != 200 :
            raise BadResponseException(status_code)

    def like(self,media_id):
        """
        Like media given the media id.

        Attributes: 
        -----------
            media_id : Media's id as a stirng. Ex:'1756292553433305074'
        Raises:
        -------
            - BadResponseException 
        """
        like_final_url = self.LIKE_URL % media_id
        
        request = self.session.post(like_final_url)
        status_code = request.status_code 
        if status_code != 200 :
            raise BadResponseException(status_code)

    def comment(self,msg,media_id):
        """
        Give a comment on media.

        Parameters:
        -----------
            msg: str
                This is the message the account is going to put.
            media_id: str
                This is the id of the publiation
        Example:
        --------
            Bot.comment('Nice Picture!','1756292553433305074')
        Raises:
        --------
            - BadResponseException
        """
        final_url = self.COMMENT_URL % media_id
        data = {
            'comment_text' : msg,
            'replied_to_comment_id' : None
        }

        request = self.session.post(final_url,data)
        status_code = request.status_code 
        if status_code != 200 :
            raise BadResponseException(status_code)

    def get_media_info(self,shortcode):
        """
        Get more detailed info of a publication given
        the shortcode.
        
        Example:
        --------
            media_info = Bot.get_media_info('BwKfHibAiIn')
        Parameters:
        -----------
            shortcode: str
                Shortcode of the publication
        Returns:
        --------
            A dictonary with the following keys:
            - media_id(str): Id of the publication.
            - viewer_has_liked(bool)
            - owner(str): Owner of the publication.
        """
        final_url = self.MEDIA_URL % shortcode
        try:
            media_info = {
                'media_id': '',
                'viewer_has_liked' : False,
                'likes' : 0,
                'owner' : ''
            }
            request = self.session.get(final_url)
            if(request.status_code == 200):
                response = json.loads(request.text)

                media_info['media_id'] = response['graphql']['shortcode_media']['id']
                media_info['viewer_has_liked'] = response['graphql']['shortcode_media']['viewer_has_liked'] 
                media_info['likes'] = response['graphql']['shortcode_media']['edge_media_preview_like']['count']
                media_info['owner'] = response['graphql']['shortcode_media']['owner']['username']
                
                return media_info
        except:
            print('Error in media info request')

    def get_user_info(self,username):
        """
        This function delivers the user info given his username

        Example:
        --------
            C.get_user_info('mariacamila0406')
        Parameters:
        -----------
            username: str
        Returns:
        --------
            A dictonary with the next keys:
            'username' : str
            'user_id' : int
            'followed_by_viewer' : bool
            'requested_by_viewer' : bool
            'followers' : int
            'follows_viewer' : bool
            'follow' : int
            'mutual_followed_by' : int
            'is_private' : bool
            'is_verified' : bool
        """
        information =	{
            'username' : '',
            'user_id' : '',
            'followed_by_viewer' : '',
            'requested_by_viewer' : '',
            'followers' : 0,
            'follows_viewer' : '',
            'follow' : 0,
            'mutual_followed_by' : 0,
            'is_private' : '',
            'is_verified' : '',
            'end_cursor' : '',
            'media' : []
        }

        final_url = self.USER_INFO_URL % username
        
        try:
            print(final_url)
            request = self.session.get(final_url)
            print(request.status_code)
            if(request.status_code == 200):
                user_info = json.loads(request.text.encode("utf-8"))

                information['username'] = username
                information['user_id'] = user_info['graphql']['user']['id']
                information['followed_by_viewer'] = user_info['graphql']['user']['followed_by_viewer']
                information['requested_by_viewer'] = user_info['graphql']['user']['requested_by_viewer']
                information['followers'] = user_info['graphql']['user']['edge_followed_by']['count']
                information['follows_viewer'] = user_info['graphql']['user']['follows_viewer']
                information['follow'] = user_info['graphql']['user']['edge_follow']['count']
                information['mutual_followed_by'] = user_info['graphql']['user']['edge_mutual_followed_by']['count']
                information['is_private'] = user_info['graphql']['user']['is_private']
                information['is_verified'] = user_info['graphql']['user']['is_verified']                
                
                information['end_cursor'] = user_info['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']  
                if information['end_cursor'] is not None:
                    information['end_cursor'] = information['end_cursor'][0:-2]
                total_media = user_info['graphql']['user']['edge_owner_to_timeline_media']['count']

                if information['is_private'] == False or information['followed_by_viewer']: 
                    if total_media >= 12 :
                        for i in range(0,12):
                            media_shortcode = user_info['graphql']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['shortcode']
                            information['media'].append(media_shortcode)
                    else:
                        for i in range(0, total_media):
                            media_shortcode = user_info['graphql']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['shortcode']
                            information['media'].append(media_shortcode)
                
                return information

        except Exception as e:
            print(e)
    
    def get_media_from_username_after(self, user_id : str, end_cursor : str) -> (list, str):
        shortcodes = []
        new_end_cursor = ''
        final_url = self.MEDIA_QUERY_URL % (self.MEDIA_QUERY_URL_BEGIN, user_id, self.MEDIA_QUERY_URL_MIDDLE, end_cursor, self.MEDIA_QUERY_URL_END)

        try: 
            request = self.session.get(final_url) 

            if request.status_code == 200:
                response = json.loads(request.text)
                new_end_cursor = response['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor'] 
                new_end_cursor = new_end_cursor[0:-2] 
                for i in range(0,12):
                    shortcode = response['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['shortcode']
                    if shortcode != None:
                        shortcodes.append(shortcode)

        except:
            print(f'Error while getting media from {user_id} with end cursor {end_cursor}')

        return (shortcodes, new_end_cursor)

    def get_media_with_city(self,code,city_name,top_posts):
        """
        Given the code and the name of a city this
        function could return a list of 9 elements
        with the shortcodes of the last media or
        the top post.

        Example:
        --------
            C.get_media_with_city('204517928','chicago-illinois',False)
        Parameters:
        -----------
            code: str
            city_name: str
            top_post: bool (Get top post)
        Returns:
        --------
            A list with media shortcodes.
        """
        final_url = self.LOCATION_URL % (code,city_name)
        media_shortcodes = []
        shortcode = ""
        try:
            request = self.session.get(final_url)
            if(request.status_code == 200):
                response = json.loads(request.text)
                for i in range(0,9):
                    if(top_posts == True):
                        shortcode = response['graphql']['location']['edge_location_to_top_posts']['edges'][i]['node']['shortcode']
                    else:
                        shortcode = response['graphql']['location']['edge_location_to_media']['edges'][i]['node']['shortcode']
                    
                    media_shortcodes.append(shortcode)
            else:
                print('Error on the request')
        except:
            print('Error while making the request')

        return media_shortcodes

    def get_media_with_hashtag(self,hashtag,top_posts):
        """
        Given the hashtag name this function return 9 
        shortcodes of the top o last publications

        Parameters:
        -----------
            hashtag: str
            top_post: bool
        Example:
        --------
            media = get_media_with_hashtag('locuraypasion',true)
        Returns:
        --------
            List with shortcodes
        """
        final_url = self.HASHTAG_URL % hashtag
        media_shortcodes = []
        shortcode = ""
        try:
            request = self.session.get(final_url)
            if(request.status_code == 200):
                response = json.loads(request.text)
                for i  in range(0,9):
                    if(top_posts == True): # If we want the list of the top post
                        shortcode = response['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges'][i]['node']['shortcode']
                    else: # If we want the last post publicated
                        shortcode = response['graphql']['hashtag']['edge_hashtag_to_media']['edges'][i]['node']['shortcode']
                    
                    media_shortcodes.append(shortcode)
        except:
            print('Error while making the request')

        return media_shortcodes
         
    def get_userlist_with_username(self,username,n):
        """
        Get the users that follow an account
        given the username of the account.

        Parameters:
        -----------
            username: str
            n: int
        Example:
        --------
            followers = Bot.get_userlist_with_username('cristiano')
        Returns:
        --------
            A list with the usernames of
            length: 24 + n*12.
        """
        accounts = []
        #GET 120 ACCOUNTS
        user_id = self.get_user_info(username)
        user_id = user_id['user_id']

        # FIRST 24 ACCOUNTS
        query_url = self.FOLLOWERS_QUERY_URL % (self.FOLLOWERS_QUERY_BEGIN,user_id,self.FOLLOWRES_QUERY_MIDDLE,'24',self.FOLLOWERS_QUERY_END)
        end_cursor = ''
        successful_request = False
        try:
            request = self.session.get(query_url)
            if(request.status_code == 200):
                successful_request = True
                response = json.loads(request.text)
                end_cursor = response['data']['user']['edge_followed_by']['page_info']['end_cursor']
                for i in range(0,24):
                    acc_username = response['data']['user']['edge_followed_by']['edges'][i]['node']['username']
                    accounts.append(acc_username)
            else:
                raise Exception()
        except:
            print('Error!!!!!')
        
        #Be sure that the first request was succesful
        if(successful_request):
            for i in range(0,n): # Get the next 96 accounts
                final_url = self.BASE_URL + ('%s%s%s%s%s')
                middle = '%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A12%2C%22after%22%3A%22'
                end = '%3D%3D%22%7D'

                end_cursor = end_cursor[0:-2] # Take out last '=='

                final_url = final_url % (self.FOLLOWERS_QUERY_BEGIN,user_id,middle,end_cursor,end)
                request = self.session.get(final_url)

                if(request.status_code == 200):
                    response = json.loads(request.text)
                    end_cursor = response['data']['user']['edge_followed_by']['page_info']['end_cursor']
                    for i in range(0,12):
                        acc_username = response['data']['user']['edge_followed_by']['edges'][i]['node']['username']
                        accounts.append(acc_username)
                
                time.sleep(3)

            return accounts

    def get_userlist_that_like_media(self,shortcode):
        """
        Get the userlist that liked a
        publication.

        Example:
        --------
            userlist = self.get_userlist_that_like_media('Bijuhysca')
        Parameters:
        -----------
            shortcode: str
        Returns:
        --------
            A list of the username that liked
            the media.
        """
        final_url = self.USER_LIKE_URL % (self.USER_LIKE_BEGIN,shortcode,self.USER_LIKE_END)
        request = self.session.get(final_url)

        if(request.status_code == 200):
            userlist = []
            response = json.loads(request.text)
            for i in range(0,24):
                userlist.append(response['data']['shortcode_media']['edge_liked_by']['edges'][i]['node']['username'])

            return userlist

    def get_shortcodes_with_username(self,username):
        """
        Get the last 9 publications
        of an account.

        Example:
        --------
            media = C.get_shortcodes_with_username('aliciakeys')
        Prameters:
        ----------
            username: str
        Returns:
        -------
            A list with 9 shortcodes.
        """
        final_url = self.USER_INFO_URL % username
        shortcode = ''
        shortcode_list = []
        try:
            request = self.session.get(final_url)
            if(request.status_code == 200):
                response = json.loads(request.text)
                for i in range(0,9):
                    shortcode = response['graphql']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['shortcode']
                    shortcode_list.append(shortcode)
        except:
            print('ERROR')
        return shortcode_list
    