
import spacy

nlp = spacy.load("en_core_web_sm")


def text_join(text):
    import re
    text = re.sub(r"\n\s*\n", "\n", text)
    text = text.replace('\n', ' ')
    doc = nlp.make_doc(text)
    print(doc)
    return doc.text
    

def text_segment(text):
    doc = nlp(text)
    ret = ""
    print(type(doc.sents))
    for sent in doc.sents:
        print(sent.text)
        ret+=sent.text+"\n"

    return ret


def translate(text,src='en',dest='zh-cn'):
    from googletrans import Translator
    translator = Translator()
    translate_text = translator.translate(text,src=src,dest=dest) 
    return translate_text.text


def merge_video_subtitle(input_video,input_subtitle,output_video):
    import ffmpeg
    
    ffmpeg.input(input_video).output(output_video,vf='subtitles=' + input_subtitle).run()
    print(input_video,input_subtitle,output_video)
    return output_video

def draw_text_on_image(image_path,text,font_size=24):
    from PIL import Image, ImageDraw, ImageFont  
    import textwrap
    # 打开图片  
    image = Image.open(image_path)  
    
    # 创建一个可以在给定图像上绘图的对象  
    draw = ImageDraw.Draw(image)  
    
    # 选择一个字体和大小  
    # 你需要有一个.ttf字体文件，并指定其路径  
    font = ImageFont.truetype('song.ttf', font_size)  
    
     # 获取图像和字体的尺寸
    image_width, image_height = image.size

    text_wrapper = textwrap.TextWrapper(width=image_width // font_size)
    lines = text_wrapper.wrap(text)

    l,t,r,b = font.getbbox(lines[0])
    text_height =  (b-t) *len(lines)
    color = (255, 255, 255)  # RGB颜色，白色  
    
    # 在图片上绘制文本  
    x = 0
    y = (image_height - text_height) // 2

    # 绘制文字
    line_height = b-t
    for line in lines:
        line_width = font.getlength(line)
        x = (image_width - line_width) // 2
        draw.text((x, y), line, color, font=font)
        y += line_height
    
    # 保存修改后的图片  
    image_path = image_path.rsplit('.', 1)[0] + "_text."+image_path.rsplit('.', 1)[1]
    image.save(image_path)
    return image_path
