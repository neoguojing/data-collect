
import subprocess

def dowload_webm(url):
    # 定义命令
    command = f"yt-dlp -o '%(upload_date>%Y)s/%(title)s.%(ext)s' {url}"
    # 执行命令
    try:
        # 使用 subprocess.run() 方法执行命令
        subprocess.run(command, shell=True, check=True)
        print("dowload success")
    except subprocess.CalledProcessError as e:
        print("download failed:", e)

def pre_process_video(filepath):
    import ffmpeg
    output_audio = 'output_audio.mp3'
    output_subtitle = 'output_subtitle.vtt'
    output_video = 'output_video.webm'

    # 剥离音频
    # ffmpeg.input(filepath).output(output_audio, acodec='mp3').run()

    # 剥离字幕
    ffmpeg.input(filepath).output(output_subtitle, f='webvtt').run()

    ffmpeg.input(filepath).output(output_video, vcodec='copy', an=None, sn=None).run()
    return output_video,output_audio,output_subtitle

def subtile_translate(filepath):
    import webvtt
    from googletrans import Translator
    translator = Translator()
    
    vtt = webvtt.read(filepath)
    for caption in vtt:
        print(caption.start)
        print(caption.end)
        print(caption.text)
        translate_text = translator.translate(caption.text,src='en',dest='zh-cn') 
        caption.text = translate_text.text
        print(translate_text)
    vtt.save("trans.vtt")

def merge_video_subtitle():
    import ffmpeg

    input_video = 'output_audio.webm'
    input_subtitle = 'trans.vtt'
    output_video = 'merge_video_subtitle.webm'

    ffmpeg.input(input_video).output(output_video, vf='subtitles=' + input_subtitle).run()
    return output_video

if __name__ == "__main__":
    # video,audio,subtile = pre_process_video("The Newest Computer Chips aren’t “Electronic” [iOXn4vqYOJA].webm")
    # subtile_translate("The Newest Computer Chips aren’t “Electronic” [iOXn4vqYOJA].en.vtt")
    merge_video_subtitle()

