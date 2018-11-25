
import requests
import re
import os
import pymysql
import traceback
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from bs4 import BeautifulSoup

class Spider:
    kd = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'}
    count = 0
    #url = 'https://www.zhihu.com/question/27601907/answer/44284004'
    def getHTML(self, url):
        try:
            driver = webdriver.Chrome()
            driver.get(url)
            try:
                driver.find_element_by_class_name("QuestionMainAction").click()
            except NoSuchElementException:
                pass
            try:
                driver.find_element_by_css_selector(
                    "button[class='Button QuestionRichText-more Button--plain']").click()
            except NoSuchElementException:
                return "获取网页异常"
            for i in range(50):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.3)
            html = driver.page_source
            return html
        except:
            return "获取网页异常"

    def vo(self,mp):
        if not 'voter' in mp:
            return 0
        s = mp['voter']
        if s == None:
            return 0
        s = s.replace('\n', ' ')
        for e in s.split(' ')[::-1]:
            e = e.replace(',', '')
            if (e.isdigit()):
                return int(e)
        return 0
    def getimg(self,tag):
        '''获取一个Tag对象的内容'''
        content = ''
        if tag != None:
            for line in tag.stripped_strings:
                try:
                    if "zhimg.com" in line:
                        # print(line)
                        ss1 = "https: // pic.*jpg"
                        relx = re.compile(r'https://pic.*?(jpg|png|gif)')
                        # name = img.split("com/v2")[1]

                        match = relx.search(line)
                        imglist = ""
                        imglist = match.group(0)
                        print(imglist)
                        # if  match:
                        #   imglist=match.group(0)
                        #   print(imglist)
                        name = imglist.split("com/v2")[1]
                        path = "article\\static\\" + "img1\\" + name
                        img = "/static/img1/" + name
                        r = requests.get(imglist, headers=self.kd)
                        line = re.sub(r'https://pic.*?(jpg|png|gif)', img, line)
                        if not os.path.exists(path):
                            with open(path, 'wb') as f:
                                f.write(r.content)
                                f.close()
                                print(path + ' 文件保存成功')
                        else:
                            print('文件已经存在')
                        # match = relx.search(line)
                        # imglist=""
                        # if  match:
                        #    imglist=match.group()
                        # print(imglist)
                        # if len(imglist)!=0:
                        #   for imgurl in imglist:
                        #
                        #       myurl =imgurl
                        #       print(imglist[i])

                except:
                    continue
                content += "<p>" + line + "</p>"
        return content
    def getContentOfTag(self,tag):
        content = ''
        if tag != None:
            for line in tag.stripped_strings:
                content += "<p>" + line + "</p>"
        return content
    def getcontent(self,url):
        #print("self", self, type)
        html=self.getHTML( url)
        soup = BeautifulSoup(html, 'html.parser')
        # 问题标题
        question_title = self.getContentOfTag(soup.find("h1", class_="QuestionHeader-title"))
        # 问题描述
        question_desc = self.getContentOfTag(soup.find("span", class_="RichText ztext"))
        # 总共有的回答数量
        all_answer_count = self.getContentOfTag(soup.find("h4", class_="List-headerText"))
        # 所有回答信息，包含作者用户名头像、作者个性签名、回答被点赞数、答案等。
        answers = soup.find_all("div", class_="List-item")
        # 当前获取到的回答数量
        current_answer_count = len(answers)

        #############下面针对每个回答进行分别提取信息#############
        answers_map_list = []  # 存储所有答案的信息
        for answer in answers:
            answers_map = {}  # 存储每一个答案的信息
            # 获取答案内容
            answer_tag = answer.find("span", class_="RichText ztext CopyrightRichText-richText")
            answer_content = self.getContentOfTag(answer_tag)

            # 获取用户名
            username_tag = answer.find("span", class_="UserLink AuthorInfo-name")
            username = self.getContentOfTag(username_tag)

            # 获取用户个性签名
            userdesc_tag = answer.find("div", class_="RichText ztext AuthorInfo-badgeText")
            userdesc = self.getContentOfTag(userdesc_tag)

            # 获取答案获赞数
            voter_tag = answer.find("span", class_="Voters")
            voter = self.getContentOfTag(voter_tag)

            answers_map["answer_content"] = answer_content
            answers_map["username"] = username
            answers_map["userdesc"] = userdesc
            answers_map["voter"] = voter
            answers_map["answer_tag"]=answer_tag
            answers_map_list.append(answers_map)
        answers_map_list.sort(key=self.vo, reverse=True)
        # 将提取的问题和答案信息保存到文件
        sep = "-*-"
        # 文件名不能出现的字符
        no_file_name = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]
        file_name = question_title.strip()
        for c in no_file_name:
            file_name = file_name.replace(c, "")

        # with open(file_name + ".txt", "w", encoding='utf-8') as file:
        #     file.write(question_title)
        #     file.write(question_desc)
        #     file.write(all_answer_count)
        #     file.write("#"*10 + "当前获取回答数：" + str(current_answer_count) + "#"*10 + '\n\n\n')
        str1 = "#" + "当前获取回答数：" + str(current_answer_count) + "#" * 10 + '\n\n\n'
        num = 5
        start = 0
        for am in answers_map_list:
            try:
                print(am["username"])
                problem = question_title[3:-4] + " 来自用户" + (am["username"])[3:-4] + "的回答"
                problem = re.sub(r'<p>', "", problem)
                problem = re.sub(r'</p>', "", problem)
                title = problem
                ##print(am["userdesc"])
                ##print(am["voter"])
                ##print("【answer.begin】" + sep*7 + "\n")
                ##字数过少直接抛弃
                ins = True
                if len(am["answer_content"]) < 300:
                    print(len(am["answer_content"]))
                    ins = False
                if ins:
                    ##self.getContentOfTag(am["answer_tag"])
                    print(1)
                    content = self.getimg(am["answer_tag"])
                    content=content.replace("'","\'")
                    db = pymysql.connect(host="localhost", port=3307, user="root", passwd="123456",
                                         db="sexeducation",
                                         charset='utf8')
                    cursor = db.cursor()
                    sql = (
                            "insert into article (title,content,type_id)" + " VALUES ('" + title + "', '" + content + "', '" + "10" + "' )").encode(
                        "utf8")
                    cursor.execute(sql)
                    db.commit()

                    self.count = self.count + 1
                    print("完成" + str(self.count) + "条数据")
                    start = start + 1
                    if start >= num:
                        break
                    # #print(sep*8 + "【answer.end】\n\n")
            except:
                traceback.print_exc()
                continue
        print("爬取网页完成")
s=Spider()
url_list=["https://www.zhihu.com/question/27601907/answer/157618006","https://www.zhihu.com/question/26373325/answer/184593916","https://www.zhihu.com/question/19946750/answer/70501990","https://www.zhihu.com/question/20164909/answer/14188528"]
for url in url_list:
  s.getcontent(url)