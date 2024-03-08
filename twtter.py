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


def images_to_video(input_pattern, name, duration=10, fps=1/10, pix_fmt='yuv420p', size='1920:1080', codec='libvpx-vp9', format='webm', bitrate='4M'):  
    import ffmpeg
    output_file = f"./data/{name}.{format}"  
    (  
        ffmpeg.input(input_pattern, pattern_type='glob', framerate=fps,t=duration)  
        .output(output_file, pix_fmt=pix_fmt, vcodec=codec, vf='scale={}'.format(size), video_bitrate=bitrate)  
        .run()  
    )  
  
    return output_file

def ocr(image_path):
    import pytesseract
    from PIL import Image
    from utils import translate,text_segment,text_join
    # Open the image
    image = Image.open(image_path)

    # Extract text from the image
    text = pytesseract.image_to_string(image)

    # Print the extracted text
    text = text_join(text)
    text = text_segment(text)

    translate_text = translate(text)
    print(translate_text)
    
    return translate_text

def make_subtitle(text,subtitle_name,start="00:00:00.500",end="00:00:09.000"):
    from webvtt import WebVTT, Caption
    vtt = WebVTT()

    # creating a caption with a list of lines
    caption = Caption(
        start,
        end,
        [text]
    )

    # adding a caption
    vtt.captions.append(caption)
    vtt.save(subtitle_name)

def process_twtter_image(image_path,video_name):
    from utils import merge_video_subtitle,draw_text_on_image
    text = ocr(image_path)
    subtitle_path = "./data/"+video_name+".vtt"
    make_subtitle(text,subtitle_path)
    draw_text_on_image(image_path,text)
    video_path = images_to_video(image_path,video_name)
    # merge_video_subtitle(video_path,subtitle_path,"./data/"+video_name+"_merge.webm")



if __name__ == "__main__":
    process_twtter_image("./data/Screenshot from 2024-03-08 11-23-44.png","test")
