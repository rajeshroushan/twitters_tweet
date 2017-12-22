import datetime

# These Credential will be used for getting RDS DATA
RDS_HOST = "vidooly-web.csmobbfeq2q4.us-east-1.rds.amazonaws.com"
RDS_USER = "vishnu"
RDS_PASSWORD = "7%vGtPo"
RDS_DATABASE = "vidooly_v1"
RDS_TABLE = "channelinfo"

# RDS_HOST = "localhost"
# RDS_USER = "root"
# RDS_PASSWORD = "1234"
# RDS_DATABASE = "vidooly"
# RDS_TABLE = "channelinfo"

# These Credential will be used for getting data from dataScienceTable
LOCAL_HOST = "10.1.2.226"
LOCAL_USER = "root"
LOCAL_PASSWORD = "root"
LOCAL_DATABASE = "socialprofile"
LOCAL_TABLE = "fb_page_public_data_since_until"

# red shift credentials
REDSHIFT_DATABASE = "datascience"
REDSHIFT_USER = "datascience"
REDSHIFT_PASSWORD = "D@+b3jEVu"
REDSHIFT_HOST = "redshift-master.cnajb4gvwej7.us-east-1.redshift.amazonaws.com"
REDSHIFT_PORT = "5439"

# oauth credentials
CONSUMER_KEY = ["HXhJ7weLPFtpdt1YEFvbUJgsm",
                "mx3ptTtt3mKniqXq81VyDO4Ob",
                "nLhVcBwWxCvblOH11ImdSUhIG",
                "dzR49IKFjQkaV3vA8wSpR4LwS",
                "HoOkONzeORx47McPFkIWTiWcq",
                "ruP3t3KhFB7b1Hexbfy46samb",
                "X6I6kCkkgFN3yQuPr1kVdn6fC",
                "lPCj3ncb9bbP8uPBtf04HqV5w",
                "yxaWHrNxTMg2TdnR4Islqteps",
                "Ul4azCnnfS842i0aHXUZHOMNx",
                "t08nUnyfaZViDERkPXpBNADXT"]

CONSUMER_SECRET = ["S6YFlae3ky01XLd8y0tYRVWaVtQ2qWw7O3HbFe3cCi4qlgNS8Y",
                   "pgnCjwwP15rBXSgNYJyyKvxay4gr4I13GwXgrXK1OfJxGYJRVj",
                   "qFGGGxyeEXX1obmveG9ExQk23XGvvOvvWPJVEkYHBwlDyuUI6r",
                   "w6Ak12YJCpu6XAyKrdbPnH8DCgA0sKKkMytj2ZvV4HSmJj0Ftz",
                   "KwZxNw3J6ptnzltljAIv3vt0m3Nb9rvh0YwatgDDB0VQpgSGLj",
                   "tGs06cSqkBaup6Oaroqi3C4y2bRK02yDAEVz92zlmXhhirfoRL",
                   "VyOfh9PiLrAhB5kQih78NhTIkzCqHJwyWihQ9R10SHriie90ZS",
                   "KlgbASazkzMAGvpgbVqcz2dYcWyNJnQOAqQyrMAtUBssrmNwS6",
                   "CqKAD816ICVcMr3Qt3J2FOmEVGqLQZ0ol8c7P8UCiByieoAyg4",
                   "7rhQxoXnQrUnVI6dwXPePEO8LTfFo4szXqQsPBB4tdPBCDjTMG",
                   "3uVeUU16w41GiLWq9yusSpvqyqECXwdjen3mbsDsrSMXYo54Ji"]

OAUTH_TOKEN = ["2989161382-BVVF8qe42ZCMT7mulSueCe9mxbqkrQ5XE5iePts",
               "957791172-vaGzGrMGqUD496tt2INaBod4LT58xoaKYYZSqDFd",
               "3185165544-dLMOICNsxd9QCU1gS3MLKTY0guPYXDJ17yxDWEq",
               "732443628128243712-6Qc4iXze81tGceOYS0OdFcg47FFzrog",
               "82650490-9yhfKBVwqzJWhJuYpbMItT9mJM1Dzy3CPQ1cVTfVZ",
               "2497879820-O2vBf2q0mxmU26wkWJAUQ5cTGqgfhUzT46xreIz",
               "3185165544-E5Q2hykkf7Ffv0rReW3uUUIlVHfDLMp9ks9Mpt3",
               "832139272622858241-JVFZiA9YnJC1cN0UPFxqtxSM3DuKd9L",
               "162626099-nB07q7CQpFvDKahqkQ6PObuE1JGcRtoRZuyer7Q6",
               "129410911-PeeKQHOnpoBUnyytgsEBaxsA0Rhi40iyygIRV53O",
               "832579810031501312-IebwS9ALvcsJrdTFcCpVZDAHaKw9rTw"]

ACCESS_TOKEN_SECRET = ["pB6p71BZe2XX99eMzD4KpXKb6UtfFUtTFxLKHRitr3Y8F",
                       "YX83cQWsidfJA6QmyDfMXhRjYpTj4sVHEKTJBw217wStY",
                       "v5SDgCl5ZX6Dd5zgYZXzi7kqPUDd6Di5S5ScBKqAkZaBA",
                       "F9bRAQrlS7BB3d0pfc0DoNINg6MceB5m94FOGrLjQKofC",
                       "HoF6ZGkDG8oHJhFD7ksZzNRHz6MDUSwrc9juwE4iWjvmo",
                       "lwTNfd5juincphG2Gf1G5UFok0x94rGCIfBABQDUieBs9",
                       "NDXxtyAO1upxPOk100yUz3oXyQ24i0bo83ofxGaa4pBFs",
                       "MwurFaVYYidqs8VI7vQEcpr4xxFt3l5APUwWRePl4cQmm",
                       "6ARIqdyDZNWmeyQoZNvZBSQRHgAr8vkkuXNbDrSqOk8U8",
                       "2SpCOR6C8jAVKveEDwdikhHNf4dXYmwW67aab79eHxXo5",
                       "w9QQKEiByb34bJgXppWjQMI1Sqm9QGLzKz25jf05cMjB5"]

# other constants parameters
offset_file = "/home/ubuntu/ebs/workspace/data/twitter_data/offset_file"
DATA_URL_PATH = ""
