#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver as wd
import time
import json
import requests
import re
import random
import sys
import datetime
import math

def getArticles():
    sys.stderr.write("注意事项：\n")
    sys.stderr.write("请注意所有的红字提示\n")
    print("请注意所有的红字提示")
    sys.stderr.write("必须安装Chrome和/或chromedriver\n")
    sys.stderr.write("macOS未安装可以执行`$brew install chromedriver`\n")
    time.sleep(2)

    # 链接和header
    wechat_imp_url_root = r"https://mp.weixin.qq.com/"
    header = {
        "HOST": "mp.weixin.qq.com",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }

    def login_wechat(user, password):
        # 登录微信
        driver = wd.Chrome()
        driver.get(wechat_imp_url_root)
        time.sleep(5)
        print("正在尝试登录微信公众号平台")
        # 清空账号框中的内容
        try:
            driver.find_element_by_id("account").clear()
            driver.find_element_by_id("account").send_keys(user)
            driver.find_element_by_id("password").clear()
            driver.find_element_by_id("password").send_keys(password)
        except:
            sys.stderr.write("自动识别数据框失败，需要手动输入，需要尽快\n")
            time.sleep(10)
        try:
            driver.find_element_by_xpath("./*//a[@id='loginBt']").click()
        except:
            sys.stderr.write("请手动点击登录\n")
        sys.stderr.write("请点击：记住账号 \n")
        time.sleep(5)
        sys.stderr.write("正在登录，请等待\n")
        time.sleep(10)
        sys.stderr.write("请扫描二维码并在手机上确认登录！\n")
        time.sleep(10)
        # 重新载入公众号登录页，登录之后会显示公众号后台首页，从这个返回内容中获取cookies信息
        print("正在重载主网页")
        driver.get('https://mp.weixin.qq.com/')
        # 获取cookies
        cookie_items = driver.get_cookies()
        # 获取到的cookies是列表形式，将cookies转成json形式并存入本地名为cookie的文本中
        with open('cookie.json', 'w', encoding='utf-8') as f:
            post = {item['name']: item['value'] for item in cookie_items}
            # 这一步：延长字典
            cookie_str = json.dumps(post)
            f.write(cookie_str)
        print("cookies信息已保存到本地cookie.json文件")
        print("登录完毕！")

    def get_links(query):
        print("正在获取token信息")
        sys.stderr.write("注意红色字迹提示\n")
        with open("cookie.json", 'r', encoding='utf-8') as f:
            cookie = f.read()
        cookies = json.loads(cookie)
        response = requests.get(url=wechat_imp_url_root, cookies=cookies)
        token = re.findall(r'token=(\d+)', str(response.url))[0]
        # 检验正确
        print('token已经取得：{}'.format(token))
        search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
        query_id = {
            'action': 'search_biz',
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'query': query,
            'begin': '0',
            'count': '5'
        }
        search_response = requests.get(url=search_url, cookies=cookies, headers=header, params=query_id)
        lists = search_response.json().get('list')[0]
        # 获取这个公众号的fakeid，后面爬取公众号文章需要此字段
        fakeid = lists.get('fakeid')
        print("本次虚拟ID已经取得：", fakeid)

        article_url_init = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
        article_id = {
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'action': 'list_ex',
            'begin': '0',  # 不同页，此参数变化，变化规则为每页加5
            'count': '5',
            'query': '',
            'fakeid': fakeid,
            'type': '9'
        }
        article_response = requests.get(url=article_url_init, headers=header, cookies=cookies, params=article_id)
        # print(article_response.json())
        totalNumber = article_response.json().get("app_msg_cnt")
        totalPages = totalNumber / 5
        # 总页数
        # 打开记录循环结果的文档
        with open("articles.txt", 'a+', encoding='utf-8') as result_file:
            # result_file.write("\n" + "-" * 15 + str(datetime.datetime.now()) + "-" * 15 + '\n')
            print("最终结果记录文件已经打开")
            print("循环开始")
            print("-----各变量已经构建，正在获得第1页的数据-----")
            ######################################################################################
            for page in range(116, int(math.ceil(totalPages))):
                page_params = {
                    'token': token,
                    'lang': 'zh_CN',
                    'f': 'json',
                    'ajax': '1',
                    'random': random.random(),
                    'action': 'list_ex',
                    'begin': '{}'.format(str(page * 5)),
                    'count': '5',
                    'query': '',
                    'fakeid': fakeid,
                    'type': '9'
                }
                print("-----正在获得第{}页数据-----".format(page + 1))
                articlesJson = requests.get(url=article_url_init, headers=header, cookies=cookies, params=page_params)
                articles = articlesJson.json().get("app_msg_list")
                for art in articles:
                    art_title = art.get("title")
                    art_class = art.get("digest")
                    art_link = art.get("link")
                    if art_class == "表白":
                        result_file.write("Title,{},link,{}\n".format(art_title, art_link))
                if page % 10 == 0:
                    sys.stderr.write("系统休眠，防止操作频繁\n")
                    time.sleep(600)



                    # 开始获取文章链接的循环

    def main():
        # 用户名和密码
        reloadCookies = True
        if reloadCookies:
            user = ''
            if not user:
                user = input("请输入用户名：")
            password = ''
            if not password:
                password = input("请输入密码：")
            login_wechat(user, password)
        get_links('复旦微生活')

    if __name__ == "__main__":
        main()
