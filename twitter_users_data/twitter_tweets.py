from get_twitter_api_clients import TwitterAuthClient
import json


def collect_twitter_data():
    clients = TwitterAuthClient().get_all_auth_client()
    client = clients[0]
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?count=200&screen_name=MyDubai"
    with open("twitter_data.csv", "w+")as _file:
        while True:
            data = client.request(url)
            user_data = json.loads(data[1])
            print len(user_data)
            for item in user_data:
                if item.get("created_at"):
                    _file.write(str(item.get("created_at").encode('utf-8').strip()))
                    _file.write("\t")
                else:
                    _file.write("\t")
                if item.get("text"):
                    _file.write(str(item.get("text").encode('utf-8').strip().replace('\n', ' ').replace('\r', '')))
                    _file.write("\t")
                else:
                    _file.write("\t")
                if item.get("retweet_count"):
                    _file.write(str(item.get("retweet_count")))
                    _file.write("\t")
                else:
                    _file.write("\t")
                if item.get("favorite_count"):
                    _file.write(str(item.get("favorite_count")))
                    _file.write("\t")
                else:
                    _file.write("\t")
                _file.write("\n")
            break


if __name__ == '__main__':
    collect_twitter_data()