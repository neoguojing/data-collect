
import subprocess
import os

target_dir = "./data"

def dowload_webm(url):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    # 定义命令
    command = f"yt-dlp --write-auto-subs --sub-lang zh-Hans,en -P '{target_dir}' -P 'temp:tmp' -P 'subtitle:subs' -o '%(uploader)s/%(title)s.%(ext)s' {url}"
    # 执行命令
    try:
        # 使用 subprocess.run() 方法执行命令
        subprocess.run(command, shell=True, check=True)
        print("dowload success")
    except subprocess.CalledProcessError as e:
        print("download failed:", e)
    
    return 

def dowload_video(url):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    from yt_dlp import YoutubeDL
    ydl_opts = {
        'outtmpl': f"{target_dir}/%(title)s.%(ext)s",
        # 'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ["zh-Hans","en"],
        'postprocessors': [],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info = ydl.extract_info(url, download=False)
        video_file = ydl.prepare_filename(info)
        subtitle_file_zh = video_file.rsplit('.', 1)[0] + '.zh-Hans.' + "vtt"
        if not os.path.exists(subtitle_file_zh):
            subtitle_file_zh = None
        subtitle_file_en = video_file.rsplit('.', 1)[0] + '.en.' + "vtt"
        if not os.path.exists(subtitle_file_en):
            subtitle_file_en = None
    print(video_file,subtitle_file_zh,subtitle_file_en)
    return video_file,subtitle_file_zh,subtitle_file_en

def pre_process_video(filepath,output_video=None,output_audio=None,output_subtitle=None,):
    import ffmpeg
    output_audio = './data/output_audio.wav'
    output_video = './data/output_video.webm'

    # 剥离音频
    if output_audio is not None:
        ffmpeg.input(filepath).output(output_audio, acodec='pcm_s16le').run()

    # 剥离字幕
    if output_subtitle is not None:
        ffmpeg.input(filepath).output(output_subtitle, f='webvtt').run()
    # 裸视频流
    if output_video is not None:
        ffmpeg.input(filepath).output(output_video, vcodec='copy', an=None, sn=None).run()

    return output_video,output_audio,output_subtitle

def subtile_translate(src,dst):
    import webvtt
    from googletrans import Translator
    translator = Translator()
    
    vtt = webvtt.read(src)
    src_text = ""
    for caption in vtt:
        src_text += caption.text

    print(src_text)
    translate_text = translator.translate(src_text,src='en',dest='zh-cn') 
    dst_texts = translate_text.text.split("。")

    del_idx = []
    
    for idx,caption in enumerate(vtt.captions):
        if idx >= len(dst_texts) or dst_texts[idx] == "":
            caption.text = ""
            del_idx.append(idx)
            continue
        caption.text = dst_texts[idx]

    print(len(vtt.captions),len(dst_texts),del_idx)
    for i in reversed(del_idx):
        del vtt.captions[i]

    vtt.save(dst)
    return dst

def merge_video_subtitle(input_video,input_subtitle):
    import ffmpeg
    output_video = 'merge_video_subtitle.webm'

    ffmpeg.input(input_video).output(output_video, vf='subtitles=' + input_subtitle).run()
    return output_video

def proccess_youtube_video(url):
    video_path,subtitle_path_zh,subtitle_path_en = dowload_video(url)

    if subtitle_path_zh is None and subtitle_path_en is not None:
        subtitle_path_zh = video_path.rsplit('.', 1)[0] + '.zh-Hans.' + "vtt"
        subtile_translate(subtitle_path_en,subtitle_path_zh)
        merge_video_subtitle(video_path,subtitle_path_zh)

    

    





if __name__ == "__main__":
    # proccess_youtube_video("https://youtu.be/MUqNwgPjJvQ?feature=shared")
    pre_process_video("./data/Transformer models： Encoders.webm")
    # dowload_webm("https://youtube.com/shorts/uvLsfzCEir8?feature=shared")
    # video,audio,subtile = pre_process_video("The Newest Computer Chips aren’t “Electronic” [iOXn4vqYOJA].webm")
    # subtile_translate("The Newest Computer Chips aren’t “Electronic” [iOXn4vqYOJA].en.vtt")
    # merge_video_subtitle()

