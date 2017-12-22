import constants
import logging
import psycopg2
import datetime
import send_email_about_sucess

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Db(object):
    def __init__(self):
        self.host = constants.REDSHIFT_HOST
        self.port = constants.REDSHIFT_PORT
        self.user = constants.REDSHIFT_USER
        self.password = constants.REDSHIFT_PASSWORD
        self.database = constants.REDSHIFT_DATABASE

    def connect_to_red_shift(self):
        try:
            conn = psycopg2.connect(host=self.host, port=self.port,
                                    user=self.user, password=self.password,
                                    database=self.database)
            cursor = conn.cursor()
            return cursor, conn
        except Exception as e:
            logging.info("error while connecting to redshift %s" % str(e.message))


def get_query_string(data_file_tobe_push, table_name):
    """
    :param data_file_tobe_push:file data to be pushed in redshift table
    :param table_name:as name suggest
    :return:
    """
    _query = ""
    if table_name is "tw_users_data":
        _query = """
                    copy %s from '%s'
                    credentials 'aws_access_key_id=AKIAIJ35D7BOKM454CYQ;aws_secret_access_key=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'
                    json 's3://lambda-inin/channelstats/rsyslog/twitter/public_data_of_page/json_path/twitter_data.json' MAXERROR 10
                """ % (table_name, data_file_tobe_push)

    return _query


def get_file_to_be_pushe_to_red_shift():
    """
    :return:daily basis uploaded file path to s3
    """
    today = datetime.date.today()
    tw_users_data = "s3://lambda-inin/channelstats/rsyslog/twitter/public_data_of_page/%s/%s/%s/"\
                    % (today.year,
                       today.strftime('%m'),
                       today.strftime('%d'))
    s3_files = [tw_users_data]

    return s3_files


def push_data_red_shift():
    """
    This function will just push the collected yesterday data in redshift table
    :return:None
    """
    msg = ""
    s3_file_tobe_push = get_file_to_be_pushe_to_red_shift()
    query_tw_users_data = get_query_string(s3_file_tobe_push[0], 'tw_users_data')
    print query_tw_users_data
    try:
        execute_query(query_tw_users_data)
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        _query = "select count(*) from tw_users_data where date = '%s';" % today
        db = Db()
        cursor, conn = db.connect_to_red_shift()
        cursor.execute(_query)
        total_row_added_is = cursor.fetchall()
        logging.info(" data has been pushed successfully")
        msg += "total row inserted in red shift  table tw_users_data is :: \n" + str(total_row_added_is[0][0])

    except Exception as e:
        msg += e.message
        pass
    return msg


def execute_query(query):
    """
    just execute the redshift query
    :param query:as name suggest
    :return:None
    """
    db = Db()
    cursor, conn = db.connect_to_red_shift()
    try:
        cursor.execute(query)
        conn.commit()
        logging.info(" data has been pushed successfully")
    except Exception as e:
        print e.message


if __name__ == '__main__':
    _message = push_data_red_shift()
    send_email_about_sucess.send_custom_mail(_message)
