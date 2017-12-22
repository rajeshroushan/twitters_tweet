from flask import Flask, request
import json
from collect_and_store_tweet import CollectTwitterData

app = Flask(__name__)


@app.route('/api/twitter/', methods=['GET'])
def get_tweet():
    try:
        req = request.args.to_dict()
        twitter_data_handler = CollectTwitterData()
        data = twitter_data_handler.collect_tweet_json(req)
        response = app.response_class(
           response=json.dumps(data),
           status=200,
           mimetype='application/json'
        )
    except Exception as e:
        print e
        response = {"error":"true", "message":"unexpected error occurs"}
    return response


@app.route('/api/get_stored_twitter/', methods=['GET'])
def fetch_tweet():
    try:
        req = request.args.to_dict()
        twitter_data_handler = CollectTwitterData()
        data = twitter_data_handler.get_stored_tweets(req)
        response = app.response_class(
           response=json.dumps(data),
           status=200,
           mimetype='application/json'
        )
    except Exception as e:
        print e
        response = {"error":"true", "message":"unexpected error occurs"}
    return response

if __name__ == '__main__':
   app.run()