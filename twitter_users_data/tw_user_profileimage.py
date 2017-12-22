import os
import time
import oauth2 as oauth
import threading
from Queue import Queue
import sys
import json
import requests
sys.path.append("/home/ubuntu/Workspace/Data_Crawling/")
#sys.path.append("/home/ubuntu/Workspace/Data_Crawling/twitter_user_data")

from log import logger
from storage import VidoolyV1Sql
from get_twitter_api_clients import TwitterAuthClient


class TwitterUserProfile(object):

    def __init__(self):
        self.consumer_key = os.environ.get("oauth_consumer_key", None)
        self.consumer_secret = os.environ.get("oauth_consumer_secret", None)
        self.oauth_token = os.environ.get("oauth_token", None)
        self.access_token_secret = os.environ.get("access_token_secret", None)
        self.oauth_version = 1.0
        self.uri = 'https://api.twitter.com/1.1/users/show.json?screen_name={0}'
        self.vidoolyv1 = VidoolyV1Sql()
        # self.twitter_authorization()
        self.BaseDir = os.environ.get('LogPath')

    def get_auth_client(self):
        twClient  = TwitterAuthClient()
        auth_clients = twClient.get_all_auth_client()
        #for auth_client in auth_clients:
        return auth_clients

    def get_user_profileimage(self):
        filepath = os.path.join(self.BaseDir, 'twitter/image/')
        """This function will fetch the pageid, accesstoken, mcnid, channelid from the database"""
        _sql = """
                    select DISTINCT twUser from %s where twUser !='' limit 163500, 30000;
               """ % (self.vidoolyv1.channel_info)
        try:
            query_data = self.vidoolyv1.execute_query(_sql, 'select', arraysize=800)
            #print list(query_data)
        except requests.exceptions.SSLError:
            pass
        except requests.exceptions.ConnectionError:
            pass
        except Exception as e:
            print e.message
            time.sleep(5)
            query_data = self.vidoolyv1.execute_query(_sql, 'select')
        auth_clients = self.get_auth_client()
        print len(auth_clients)
        for index, twUsers in enumerate(query_data):
            if (index+1) > len(auth_clients):
                index = (index+1) % len(auth_clients)
            print index, '--'*50
            client = auth_clients[index % len(twUsers)]
            
            for twUser in twUsers:
                try:
                    response, data = client.request(self.uri.format(twUser[0]))
                    print response.status
                    if response.status == 200:
                        data = json.loads(data)
                        #print data
                        # if 'picture' in data.keys():
                        image_url = data.get('profile_image_url', None)
                        name = data.get('name', None)
                        name = name if name else twUser[0]
                        logger.info("%s TWITTER_IMAGE_DATA : %s", name, data)
                        # download the image
                        _image = requests.get(image_url, stream=True)
                        print _image.status_code
                        if _image.status_code == 200:
                            _image_type = _image.headers.get('Content-Type')
                            _ext = _image_type.strip().split('/')[-1]
                            with open(filepath + name + '.' + _ext, 'wb') as w:
                                for chunk in _image:
                                    w.write(chunk)
                        else:
                            print _image.json()
                    else:
                        print r.json()
                except requests.exceptions.SSLError:
                    time.sleep(300)
                except requests.exceptions.ConnectionError:
                    time.sleep(300)
                except Exception as e:
                    pass
            print 'going to sleep'
            time.sleep(400)


if __name__ == '__main__':
    obj = TwitterUserProfile()
    obj.get_user_profileimage()


