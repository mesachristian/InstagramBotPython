from time import sleep
from main.instagramAccount import InstagramAccount
from main.strategies.followActiveUsersStrategy import FollowActiveUsersStrategy
from main.instagramEndpoints import InstagramEndpoints

from main.strategies.growStrategy import GrowStrategy
from main.strategies.followActiveUsersStrategy import FollowActiveUsersStrategy
from main.strategies.testStrategy import TestStrategy

def main():
    login_info = {
        'username' : 'luciacastellanoss_',
        'password' : ''
    }

    accounts = ['cats_of_instagram', 'dogsandhugs']

    
    lucia = InstagramAccount(login_info['username'], login_info['password'])
    lucia.niche_accounts = accounts
    print('Cuentas: ')
    print(lucia.niche_accounts)

    strategy = GrowStrategy(FollowActiveUsersStrategy(lucia))

    strategy.execute_strategy()

if __name__ == "__main__":
    main()