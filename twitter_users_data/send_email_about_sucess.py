import send_mail_to_client
import commands
import datetime


def send_custom_mail(message=None):
    to = 'rajesh@vidooly.com'
    subject = "twitter_users_public_data"
    body = ""

    data_file = ['public_data_of_twitter_page']

    for line in data_file:
        _msg = get_body_str()
        body += "number of files tha have been uploaded in " + line + "\n" + _msg + "\n \n"

    body += message
    send_mail_to_client.send_email(to, subject, body)


def get_body_str():
    today = datetime.date.today()
    base_command = "s3cmd ls s3://lambda-inin/channelstats/rsyslog/twitter/public_data_of_page"
    _command = base_command + "/%s/%s/%s/ | wc -l" % (today.year, today.strftime('%m'), today.strftime('%d'))
    out = commands.getstatusoutput(_command)
    return out[1]

if __name__ == '__main__':
    send_custom_mail()
