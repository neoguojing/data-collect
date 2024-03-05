import tweepy

from config import config

# 获取用户名和密码
# twtter_token = config["credentials"]['twtter_token']
twtter_token = ''

token = f"Bearer {twtter_token}"
print("token:", token)
client = tweepy.Client(bearer_token=twtter_token)

user_info = client.get_users(usernames="SpaceX")

for user in user_info.data:
    print(user.username, user.profile_image_url)