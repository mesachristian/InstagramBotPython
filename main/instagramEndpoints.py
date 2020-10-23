class InstagramEndpoints:
    """
    This class contains all the instagram http endpoints
    """
    BASE_URL = 'https://www.instagram.com/'
    LOGIN_URL = BASE_URL + 'accounts/login/ajax/'
    LOGOUT_URL = BASE_URL + 'accounts/logout/ajax/'
    USER_INFO_URL = BASE_URL + '%s/?__a=1'
    FOLLOW_URL = BASE_URL + 'web/friendships/%s/follow/'
    UNFOLLOW_URL = BASE_URL + 'web/friendships/%s/unfollow/'
    LIKE_URL = BASE_URL + 'web/likes/%s/like/'
    USER_LIKE_URL = BASE_URL + 'graphql/query/?query_hash=%s%s%s'
    BEGIN ='e0f59e4a1c8d78d0161873bc2ee7ec44&variables=%7B%22shortcode%22%3A%22' #This is used for complete user like url
    END = '%22%2C%22include_reel%22%3Atrue%2C%22first%22%3A80%7D' #This is used for complete user like url
    LOCATIONS_URL = BASE_URL + 'explore/locations/?__a=1' # Explore all posible locations
    HASHTAG_URL = BASE_URL + 'explore/tags/%s/?__a=1'
    MEDIA_URL = BASE_URL + 'p/%s/?__a=1'
    LOCATION_URL = BASE_URL + 'explore/locations/%s/%s/?__a=1'
    COMMENT_URL = BASE_URL + 'web/comments/%s/add/'
    
    FOLLOWERS_URL = BASE_URL + 'graphql/query/?query_hash=%s%s%s'
    FOLLOWERS_URL_BEGIN = '56066f031e6239f35a904ac20c9f37d9&variables=%7B%22id%22%3A%22'
    FOLLOWERS_URL_END = '%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A15%2C%22after%22%3A%22QVFDZmtlVVRESVhNdGJXQUpEVVN5T1l1UVZGUzU5RTlBeDl0d1kweUZ1UHplWkdzamhPWXA2eXBPRk5IX0REX2trZnhURU1mRjNiYzk2bFN2WFFLblZIVQ%3D%3D%22%7D'
    
    USERS_LIKE_URL = BASE_URL + 'graphql/query/?query_hash=%s%s%s'
    USER_LIKE_BEGIN = 'd5d763b1e2acf209d62d22d184488e57&variables=%7B%22shortcode%22%3A%22'
    USER_LIKE_END = '%22%2C%22include_reel%22%3Atrue%2C%22first%22%3A24%7D'


    FOLLOW_QUERY_URL = BASE_URL + 'graphql/query/?query_hash=%s%s%s'
    FOLLOW_QUERY_URL_BEGIN = 'd04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%22'
    FOLLOW_QUERY_URL_END = '%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A24%7D'
    
    CITY_QUERY_URL = BASE_URL + 'graphql/query/?query_hash=%s%s%s%s%s'
    CITY_QUERY_URL_BEGIN = '1b84447a4d8b6d6d0426fefb34514485&variables=%7B%22id%22%3A%22'
    CITY_QUERY_URL_BETWEEN = '%22%2C%22first%22%3A12%2C%22after%22%3A%22'
    CITY_QUERY_URL_END = '%22%7D'

    FOLLOWERS_QUERY_URL = BASE_URL +'%s%s%s%s%s' 
    FOLLOWERS_QUERY_BEGIN = 'graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%22'
    FOLLOWRES_QUERY_MIDDLE = '%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A'
    FOLLOWERS_QUERY_END = '%7D'

    MEDIA_QUERY_URL = BASE_URL + '%s%s%s%s%s'
    MEDIA_QUERY_URL_BEGIN = 'graphql/query/?query_hash=18a7b935ab438c4514b1f742d8fa07a7&variables=%7B%22id%22%3A%22'
    MEDIA_QUERY_URL_MIDDLE = '%22%2C%22first%22%3A12%2C%22after%22%3A%22'
    MEDIA_QUERY_URL_END = '%3D%3D%22%7D'