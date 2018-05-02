from getArticles import *
from analyzeArticle import *
from drawWordMap import *
import sys

def main():
    sys.stderr.write("请留心红色提示字符！\n")
    print("程序开始")
    getArticles()
    analyzeArticle()
    drawWordMap()

if __name__ == "__main__":
    main()
