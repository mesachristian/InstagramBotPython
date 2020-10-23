from instagramHttpManager import InstagramHttpManager

from main.exceptions.badCredentialsException import BadCredentialsException
from main.exceptions.badResponseException import BadResponseException

import unittest
from time import sleep

class InstagramHttpManagerTest(unittest.TestCase):
    
    http_manager = None
    
    def test_it(self):
        self.login()
        print("============= WAIT =============")
        sleep(10)
        self.logout()

    def login(self):
        bad_login_info = {
            'username' : 'luciacastellanoss_',
            'password' : ''
        }

        correct_login_info = {
            'username' : 'luciacastellanoss_',
            'password' : ''
        }
        
        self.http_manager = InstagramHttpManager()
        with self.assertRaises(BadCredentialsException):
            self.http_manager.login(bad_login_info)

        self.http_manager.login(correct_login_info)
        self.assertIsNotNone(self.http_manager.csrftoken)

    def logout(self):
        self.assertIsNotNone(self.http_manager)
        response = self.http_manager.logout()
        print(response)

if __name__ == '__main__':
    unittest.main()