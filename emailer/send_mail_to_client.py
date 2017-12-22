import mandrill
import requests
from base64 import b64encode


def send_email(to, subject, body):
    mandrill_api_key = 'cwNBWRdwZIir-XXhG3gLVA'
    mandrill_client = mandrill.Mandrill(mandrill_api_key)
    try:
        body = '<p>' + body.replace("\n", "<br>")
    except Exception as e:
        body = '<p>' + body

    _message = dict()
    _message['from_email'] = 'info@vidooly.com'
    _message['from_name'] = 'Vidooly'

    to = to.strip().split(",")
    all_mail = []

    for mail_id in to:
        to_template = dict()
        to_template['email'] = mail_id
        to_template['type'] = 'to'
        all_mail.append(to_template)

    _message['to'] = all_mail
    _message['subject'] = subject
    _message['html'] = body

    result = mandrill_client.messages.send(message=_message)
    print result


def sample_email():
    imgurl = 'http://python.mfamt.org/files/images/pics/hoover-tower-fog.jpg'
    img = requests.get(imgurl)
    imgdata = b64encode(img.content)

    MANDRILL_API_KEY = 'cwNBWRdwZIir-XXhG3gLVA'
    mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
    message = { 'from_email': 'info@vidooly.com',
      'from_name': 'Vidooly',
      'to': [{
        'email': 'vikas@vidooly.com',
        'name': 'Whoever',
        'type': 'to'
       },
          {
              'email': 'rajesh@vidooly.com',
              'name': 'Whoever',
              'type': 'to'
          }
      ],
      'subject': "Sending you a pic of Stanford campus",
      'html': "<p>Here's a photo of the <a href='https://www.flickr.com/photos/zokuga/15138926354/'>Stanford campus</a>",
      'attachments': [{'name': 'stanfordimage.jpg',
        'type': 'image/jpeg',
        'content': imgdata
      }]
    }
    result = mandrill_client.messages.send(message = message)
    print(result)

if __name__ == '__main__':
    send_email('rajesh@vidooly.com, vikas@vidooly.com', 'TESTING','Hello World')