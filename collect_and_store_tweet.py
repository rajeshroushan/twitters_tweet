import pymongo
from get_twitter_api_clients import TwitterAuthClient
import json
import mongo_connector


class CollectTwitterData(object):
    def __init__(self):
        self.tw_api_url = "https://api.twitter.com/1.1/search/tweets.json?q="

    def validate_parm(self, req):
        valid = 0
        url = self.tw_api_url
        if req.get("q") is not None:
            url += req.get("q")
            valid = 1
        if req.get("geocode") is not None:
            url += "&" + "geocode=" + req.get("geocode")

        if req.get("lang") is not None:
            url += "&" + "lang=" + req.get("lang")

        if req.get("locale") is not None:
            url += "&" + "locale=" + req.get("locale")

        if req.get("result_type") is not None:
            url += "&" + "result_type=" + req.get("result_type")

        if req.get("until") is not None:
            url += "&" + "until=" + req.get("until")

        if req.get("since_id") is not None:
            url += "&" + "since_id=" + req.get("since_id")

        if req.get("include_entities") is not None:
            url += "&" + "include_entities=" + req.get("include_entities")
        return valid, url

    @staticmethod
    def store_tweet_in_mongo(json_data, search_term):
        try:
            if isinstance(json_data, dict):
                collection_name = mongo_connector.get_mongo_collection()
                if json_data.get("statuses"):
                    for item in json_data.get("statuses"):
                        item["query"] = search_term
                        collection_name.insert(item)
        except Exception as e:
            print e

    def collect_tweet_json(self, req):
        responses = dict()
        valid, url = self.validate_parm(req)
        if valid == 1:
            twitter_client = TwitterAuthClient()
            all_auth_client = twitter_client.get_all_auth_client()
            data = all_auth_client[0].request(url)
            responses = json.loads(data[1])
            self.store_tweet_in_mongo(json.loads(data[1]), req.get("q"))
            responses["error"] = "false"
        else:
            responses["error"] = "true"
            responses["message"] = "please check request param"
        return responses

    @staticmethod
    def get_stored_tweets(self, query):
        response = dict
        if query.get("created_at"):
            collection_name = mongo_connector.get_mongo_collection()
            response=  collection_name.find_one({"created_at":query.get("created_at")})
        return response

if __name__ == '__main__':
    collect_tweet = CollectTwitterData()
    collect_tweet.get_stored_tweets()
