from wordcloud import WordCloud, ImageColorGenerator
import re
import jieba
from collections import Counter
import PIL.Image as Image
import numpy as np
import matplotlib.pyplot as plt

def drawWordMap():
    with open("words.txt", 'r', encoding='utf-8') as f:
        regex1 = re.compile('<span.*?</span>')  # 匹配表情
        regex2 = re.compile('\s{2,}')  # 匹配两个以上占位符。
        Signatures = [regex2.sub(' ', regex1.sub('', signature, re.S)) for signature in f]
        text = ' '.join(Signatures)

    wordlist = []
    for word in jieba.cut(text, cut_all=True):
        if not word in ['哥哥', '小哥', '小姐', "姐姐", '有机', '一个', '一辈', '一次']:
            wordlist.append(word)
    counted = Counter(wordlist)

    for key in counted.keys():
        if counted[key] <= 1:
            wordlist.remove(key)

    word_space_split = ' '.join(wordlist)
    coloring = np.array(Image.open("IMG_1622.JPG"))

    my_wordcloud = WordCloud(background_color="white", max_words=300,
                             mask=coloring, max_font_size=60, random_state=42, scale=2,
                             font_path="/System/Library/Fonts/STHeiti Light.ttc").generate(word_space_split)

    foreground = ImageColorGenerator(coloring)

    # 以下代码显示图片
    plt.imshow(my_wordcloud)
    plt.axis("off")
    # 绘制词云
    plt.figure()
    # recolor wordcloud and show
    # we could also give color_func=image_colors directly in the constructor
    plt.imshow(my_wordcloud.recolor(color_func=foreground))
    plt.axis("off")
    # 绘制背景图片为颜色的图片
    plt.figure()
    plt.imshow(coloring, cmap=plt.cm.gray)
    plt.axis("off")
    # 保存图片
    my_wordcloud.to_file("result.jpg")

