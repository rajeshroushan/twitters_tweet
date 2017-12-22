import time
import sys
import json
import os
import boto3
import datetime

import constants
from get_twitter_api_clients import TwitterAuthClient
from connect_to_my_sql import QueryClass


class CollectTwitterData(object):
    def __init__(self):
        self.offset_file = constants.offset_file
        self.__mysql_conn = QueryClass(constants.RDS_HOST, constants.RDS_USER, constants.RDS_PASSWORD,
                                       constants.RDS_DATABASE)
        self.tw_api_url = "https://api.twitter.com/1.1/users/show.json?screen_name="
        self.cnt = 0

    def connect_to_mysql(self):
        """This function will be used return  mysql connections"""
        return self.__mysql_conn

    def get_twitter_screen_name(self):
        """
        :return:This function will collect unique screen_name from mysql
        table channelinfo in bunch of 600
        """
        with open(self.offset_file) as _file:
            offset = int(_file.readline())
        limit = 600
        _sql = """select DISTINCT twUser from %s where twUser !='' limit %s offset %s;""" % (constants.RDS_TABLE, limit, offset)
        conn = self.connect_to_mysql()
        print _sql
        try:
            results = conn.execute_query(_sql, 'select')
        except Exception as e:
            time.sleep(15)
            results = conn.execute_query(_sql, 'select')

        with open(self.offset_file, "w+") as _file:
            _file.write(str(offset+limit))
        return results

    def close_db_connection(self):
        """close all db connections"""
        self.__mysql_conn.close_connections()

    def get_twitter_user_profile(self, twitter_users, client):
        """
        This function will collect the twitter users public profile data
        :param twitter_users:twitter screen name
        :param client:twitter auth client
        :return:None
        """
        with open(constants.DATA_URL_PATH, 'a+') as buff:
            for page in twitter_users:
                if isinstance(page, list):
                    user = page[0]
                else:
                    user = page
                url = self.tw_api_url + user
                try:
                    data = client.request(url)
                    self.cnt +=1
                    user_data = json.loads(data[1])
                    # print user_data
                    if user_data.get("id") and user_data.get("name") and user_data.get("screen_name"):
                        data = dict()
                        data["id"] = user_data.get("id")
                        data["name"] = user_data.get("name")
                        data["screen_name"] = user_data.get("screen_name")
                        if user_data.get("location"):
                            data["location"] = user_data.get("location")
                        if user_data.get("followers_count"):
                            data["followers_count"] = user_data.get("followers_count")
                        if user_data.get("friends_count"):
                            data["friends_count"] = user_data.get("friends_count")
                        if user_data.get("favourites_count"):
                            data["favourites_count"] = user_data.get("favourites_count")
                        if user_data.get("statuses_count"):
                            data["statuses_count"] = user_data.get("statuses_count")
                        if user_data.get("lang"):
                            data["lang"] = user_data.get("lang")
                        today = datetime.date.today()
                        data["date"] = str(today)
                        json.dump(data, buff)
                        buff.write("\n")
                except Exception as e:
                    print e.message
        print "total it run count is " + str(self.cnt)


def put_data_file_over_s3(_file):
    """
    This function will upload the data file over s3
    :param _file:file to be uploaded
    :return:
    """
    s3 = boto3.resource('s3')
    today = datetime.date.today()
    data_url_path = "channelstats/rsyslog/twitter/public_data_of_page" \
                    "/%s/%s/%s/" % (today.year, today.strftime('%m'), today.strftime('%d'))

    s3.Bucket('lambda-inin').upload_file(_file,
                                         data_url_path + _file.split("/")[-1],
                                         ExtraArgs={'ContentType': 'text'})


def upload_file(offset=None, start_time=None):
    """
    This function will upload the file and print execution time
    :param offset:offset
    :param start_time:as name suggest
    :return:None
    """
    try:
        new_file_name = constants.DATA_URL_PATH + str(int(time.time())) + "_" + offset
        os.rename(constants.DATA_URL_PATH, new_file_name)
        put_data_file_over_s3(new_file_name)
        execution_time = time.time() - start_time
        print("--- %s total execution time ---" % execution_time)
    except Exception as e:
      print e.message


def collect_additional_users_data():
    """
    This function will collect all the twitter screen which
    are not present in the table channelinfo
    :return:None
    """
    today = datetime.date.today()
    start_time = time.time()
    check_dir = "/home/ubuntu/ebs/workspace/data/twitter_data/%s/%s/%s/" % (
    today.year, today.strftime('%m'), today.strftime('%d'))
    if not os.path.exists(check_dir):
        os.makedirs(check_dir)
    constants.DATA_URL_PATH = check_dir + "twitter_public_data"
    clients = TwitterAuthClient().get_all_auth_client()
    twitter_obj = CollectTwitterData()
    today = datetime.date.today()
    users_tw = []
    with open("twitter_handle") as tw_handle:
        for handle in tw_handle:
            users_tw.append(handle)
    twitter_obj.get_twitter_user_profile(users_tw, clients[0])
    upload_file("last_offset", start_time)


def collect_twitter_data():
    """
    This function will collect the twusers and call another method to collect twitter data
    :return:None
    """
    today = datetime.date.today()
    check_dir = "/home/ubuntu/ebs/workspace/data/twitter_data/%s/%s/%s/" % (today.year, today.strftime('%m'), today.strftime('%d'))
    if not os.path.exists(check_dir):
        os.makedirs(check_dir)
    constants.DATA_URL_PATH = check_dir + "twitter_public_data"
    clients = TwitterAuthClient().get_all_auth_client()

    while True:
        start_time = time.time()
        twitter_obj = CollectTwitterData()
        for client in clients:
            twitter_users = twitter_obj.get_twitter_screen_name()
            if len(twitter_users) > 0:
                twitter_obj.get_twitter_user_profile(twitter_users, client)
            else:
                with open(twitter_obj.offset_file, 'w+') as f1:
                    f1.write(str(0))
                upload_file("last_offset", start_time)
                sys.exit(0)
        with open(constants.offset_file) as _f2:
            offset = _f2.readline()
        upload_file(offset, start_time)
        execution_time = time.time() - start_time
        sleeping_time = 15*60 - execution_time
        print "sleeping time is" + str(sleeping_time)
        if sleeping_time > 0:
            time.sleep(sleeping_time)
            twitter_obj.close_db_connection()

if __name__ == '__main__':
    collect_additional_users_data()
    collect_twitter_data()
    twitter_obj = CollectTwitterData()
    with open(constants.offset_file, 'w+') as f1:
        f1.write(str(0))