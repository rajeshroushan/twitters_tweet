import json
import constants
import oauth2 as oauth


class TwitterUserProfile(object):
    """This will generate the auth client and return the same"""
    def __init__(self, consumer_key, consumer_secret, oauth_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.oauth_token = oauth_token
        self.access_token_secret = access_token_secret
        self.oauth_version = 1.0

    def twitter_authorization(self):
        """This function will return the individual auth_client"""
        consumer = oauth.Consumer(key=self.consumer_key, secret=self.consumer_secret)
        access_token = oauth.Token(key=self.oauth_token, secret=self.access_token_secret)
        client = oauth.Client(consumer, access_token)
        return client


class TwitterAuthClient(TwitterUserProfile):
    """This class will be used to generate multiple auth client and will store the same"""
    def __init__(self):
        self.consumer_key = constants.CONSUMER_KEY
        self.consumer_secret = constants.CONSUMER_SECRET
        self.oauth_token = constants.OAUTH_TOKEN
        self.access_token_secret = constants.ACCESS_TOKEN_SECRET
        self.all_auth_client = []

    def get_all_auth_client(self):
        """This function will return all the individual auth_client"""
        url = "https://api.twitter.com/1.1/users/lookup.json?screen_name=roushanrajeshii"
        for index in range(len(self.consumer_key)):
            twitter_auth_client = TwitterUserProfile(self.consumer_key[index],
                                                     self.consumer_secret[index],
                                                     self.oauth_token[index],
                                                     self.access_token_secret[index])
            sample_data = twitter_auth_client.twitter_authorization().request(url)
            print sample_data[0]["status"]
            if int(sample_data[0]["status"]) == 200:
                self.all_auth_client.append(twitter_auth_client.twitter_authorization())
        return self.all_auth_client


if __name__ == '__main__':
    """ test function """
    twitter_client = TwitterAuthClient()
    all_auth_client = twitter_client.get_all_auth_client()
    print all_auth_client
    data = all_auth_client[0].request("https://api.twitter.com/1.1/search/tweets.json?q=modi")
    print json.loads(data[1])