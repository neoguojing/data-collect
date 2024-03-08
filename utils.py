
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