import tweepy


def connnect_to_twtter():
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

def images_to_video(input_pattern,duration,fps=24,pix_fmt='yuv420p',s='1920×1080',c='libx264',f='mp4',b='4M'):
    import ffmpeg
    output_file = f"video_from_images.{f}"
    (
        ffmpeg.input(input_pattern, pattern_type='glob', framerate=fps)
        .output(output_file, pix_fmt=pix_fmt,s=s,c=c,f=f,b=b,frames=duration*fps).run()
    )

    return output_file
    


