# # -*- coding: utf-8 -*-
# from bs4 import BeautifulSoup
# from ..drivers import *
# from ..items import *
# from scrapy.http import Request
# import pymysql
# import time
#
# class MyzhihuSpider(scrapy.Spider):
#     name = 'myzhihu'
#     host = "www.zhihu.com"
#
#     hot_url = "https://www.zhihu.com/hot"
#     search_content_url = "https://zhihu.com/search?q=%s&type=content"
#     search_people_url = "https://www.zhihu.com/org/%s/activities"
#     post_url = "https://www.zhihu.com/people/%s/posts?page=%d"
#     question_url = "https://www.zhihu.com/question/%s"
#     search_by_content_people_url = "https://www.zhihu.com/search?type=people&q=%s"
#
#     cookie = 'd_c0="AGDA5FopyAqPTvziFdi8dD3eXlqzh20KqRk=|1478011305"; _zap=c10f66b0-99be-4a61-a45b-426e19a54181; __utma=51854390.24507632.1478012020.1486214219.1487327727.5; __utmv=51854390.100--|2=registration_date=20161023=1^3=entry_date=20161023=1; _xsrf=ljqz6FjmpqxiSxlsL6bGRxPb1MCEsYDK; q_c1=d5151da565bc4ce885ed3a1685b0b183|1546283420000|1478011305000; __gads=ID=0ce148bfb56a0267:T=1546285296:S=ALNI_Maaz0yAn7eb6wyciuMdMprbp6bGfg; tgw_l7_route=7bacb9af7224ed68945ce419f4dea76d; capsion_ticket="2|1:0|10:1546788630|14:capsion_ticket|44:ZWNlY2YyMGNmZTlkNDU1MGE0NTM1MzgyM2E4MTg1NWY=|4f94055b66b098d1a1a05da5d99be8a6748141af505d54442d38d8cec015e9f1"; z_c0="2|1:0|10:1546788642|4:z_c0|92:Mi4xR0c2YkF3QUFBQUFBWU1Ea1dpbklDaVlBQUFCZ0FsVk5JbTBmWFFEbDZtZUR3ZmdONTA4TF9wclNCM1V0a3VhQ01R|a3b88958136073b39bebb610dc555894821a16e97caf5f0610870dd2b762cc12"; tst=r'
#     Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
#
#     def __init__(self):
#         self.mysql_database = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='zhihu', charset='utf8')
#
#     def parse(self, response):
#         pass
#
#     # from the database to get contents for search
#     def get_crawl_data(self, database_table_name):
#         sql_clause = "select * from %s" % database_table_name
#         try:
#             database_cursor = self.mysql_database.cursor()
#             database_cursor.execute(sql_clause)
#             self.mysql_database.commit()
#
#             results = database_cursor.fetchall()
#             return results
#         except Exception as e:
#             self.mysql_database.rollback()
#             raise e
#
#     def start_requests(self):
#         yield Request(self.hot_url, callback=self.parse_hot_info, meta={
#             'key' : 'hot',
#             'cookie' : self.cookie,
#             'agent' :  self.Agent
#         })
#
#         key_list = self.get_crawl_data('content')
#         for key in key_list:
#             key_item = key[0]
#             url = self.search_content_url % key_item
#             t_url = self.search_by_content_people_url % key_item
#             yield Request(url, callback=self.parse_content_through_keyword, meta={
#                 'key': 'search_content',
#                 'keyword': key_item
#             })
#
#             yield Request(t_url, callback=self.parse_search_people_by_content, meta={
#                 'key' : 'search_people_by_content'
#             })
#
#         people_list = self.get_crawl_data('people')
#         for people in people_list:
#             people = people[0]
#             url = self.search_people_url % people
#             yield Request(url, callback=self.parse_people_through_keyword, meta={
#                 'key': 'search_people',
#                 'keyword': people
#             })
#
#         question_list = self.get_crawl_data('question')
#         for question in question_list:
#             question = question[0]
#             url = self.question_url % question
#             yield Request(url, callback=self.parse_question, meta={
#                 'key' : 'search_question'
#             })
#
#     def parse_search_people_by_content(self, response):
#         soup = BeautifulSoup(response.text, "html.parser")
#         t_url = str(response.url)
#         key = t_url.split('=')[-1]
#
#         people_list = soup.find_all(class_='List-item')
#         for p in people_list:
#             try:
#                 link = "https:" + p.find(class_='UserLink').a.get('href')
#                 people_id = link.split('/')[-1]
#                 name = p.find(class_='Highlight').get_text()
#                 num_list = p.find(class_='ContentItem-status').find_all('a')
#                 answer_num = num_list[0].get_text()
#                 article_num = num_list[1].get_text()
#                 focus_num = num_list[2].get_text()
#
#                 people_item = search_people_by_content_info()
#                 people_item['key'] = key
#                 people_item['user_name'] = name
#                 people_item['link'] = link
#                 people_item['num_answer'] = answer_num
#                 people_item['num_article'] = article_num
#                 people_item['num_focus'] = focus_num
#                 yield people_item
#             except Exception as e:
#                 continue
#
#     def parse_question(self, response):
#         soup = BeautifulSoup(response.text, "html.parser")
#         t_url = str(response.url)
#         q_id = t_url.split('/')[-1]
#
#         question_answer_items = soup.find_all('div', 'List-item')
#         for answer_item in question_answer_items:
#             answer_item_content = answer_item.find(class_='AuthorInfo-content')
#             try:
#                 question_answerer_name = answer_item_content.contents[0].get_text()
#                 question_answerer_intro = answer_item_content.contents[1].get_text()
#                 question_answerer_agree_num = answer_item.find(class_='ContentItem-actions').contents[0].get_text()
#                 question_answerer_comment_num = answer_item.find(class_='ContentItem-actions').contents[1].get_text()
#                 question_content = answer_item.find(class_='RichContent-inner').span.get_text()
#
#                 q_a_item = question_answer_info()
#                 q_a_item['question_id'] = q_id
#                 q_a_item['answer_people_name']= question_answerer_name
#                 q_a_item['answer_people_intro'] = question_answerer_intro
#                 q_a_item['agree_num'] = question_answerer_agree_num
#                 q_a_item['comment_num'] = question_answerer_comment_num
#                 yield q_a_item
#             except Exception as e:
#                 continue
#
#     def parse_people_through_keyword(self, response):
#         soup = BeautifulSoup(response.text, "html.parser")
#         t_url = str(response.url)
#         user_id = t_url.split('/')[4]
#         try:
#             name = soup.find(class_='ProfileHeader-name').get_text()
#             work = ''
#             live = ''
#             education = ''
#             pro = ''
#             intro = ''
#             # then get other information
#
#             info = soup.find_all(class_='ProfileHeader-detailItem')
#             for item in info:
#                 i = item.find(class_='ProfileHeader-detailLabel').get_text()
#                 c = item.find(class_='ProfileHeader-detailValue').get_text()
#                 if (i.find('所在行业') >= 0):
#                     work = c
#                 elif (i.find('居住地') >= 0):
#                     live = c
#                 elif (i.find('职业经历') >= 0):
#                     pro = c
#                 elif (i.find('教育经历') >= 0):
#                     education = c
#                 elif (i.find('个人简介') == 0):
#                     intro = c
#
#             num_list = soup.find_all(class_='Tabs-meta')
#             num_answer = num_list[0].get_text()
#             num_ask = num_list[1].get_text()
#             num_post = num_list[2].get_text()
#             num_column = num_list[3].get_text()
#
#             follow_list = soup.find_all(class_='NumberBoard-itemValue')
#
#             num_following = follow_list[0].get_text()
#             num_followed = follow_list[1].get_text()
#
#             people_icon = search_people_info()
#             people_icon['user_name'] = name
#             people_icon['abode'] = live
#             people_icon['industry'] = work
#             people_icon['workexp'] = pro
#             people_icon['education'] = education
#             people_icon['introduction'] = intro
#             people_icon['answer_num'] = num_answer
#             people_icon['ask_num'] = num_ask
#             people_icon['post_num'] = num_post
#             people_icon['column_num'] = num_column
#             people_icon['following_num'] = num_following
#             people_icon['follower_num'] = num_followed
#             yield people_icon
#
#             #to find post data
#             post_num = (int)(num_post)
#
#             # get page num of the posts
#             if (post_num % 20 == 0):
#                 page_num = (post_num // 20)
#             else:
#                 page_num = (post_num // 20 + 1)
#
#             for page in range(1, page_num + 1):
#                 search_post_url = self.post_url % (user_id, page)
#                 time.sleep(1)
#                 yield Request(search_post_url, callback=self.parse_post, meta={
#                     'key': 'search_post'
#                 })
#
#         except:
#             return
#
#
#     def parse_hot_info(self, response):
#         soup = BeautifulSoup(response.text, "html.parser")
#         print("已登录")
#         print("开始爬取最新热度信息")
#
#         content_item = soup.find_all(class_='HotItem')
#         for item in content_item:
#             try:
#                 link = item.find(class_='HotItem-content').a.get('href')
#                 title = item.find(class_='HotItem-content').a.get('title')
#                 hot_degree = item.find(class_='HotItem-metrics').get_text().split(' ')[0] + "万"
#
#                 hot_item = hotInfo()
#                 hot_item['title'] = title
#                 hot_item['link'] = link
#                 hot_item['hot_degree'] = hot_degree
#
#                 yield hot_item
#             except:
#                 continue
#
#         print("今日热度信息爬取完毕", end='\n')
#
#     #to parse search contents with key words
#     def parse_content_through_keyword(self, response):
#         soup = BeautifulSoup(response.text, "html.parser")
#         q_items = soup.find_all(class_='List-item')
#
#         for q in q_items:
#             try:
#                 title = q.find(class_='ContentItem-title').get_text()
#                 link = q.find(class_='ContentItem-title').a.get('href')
#                 q_key_id = link.split("/")[2]
#                 num_agree = q.find(class_='ContentItem-actions').button.get_text()
#                 num_comment = q.find(class_='ContentItem-action').get_text()
#                 if(num_comment.find('添加评论') >= 0):
#                     num_comment = '0'
#                 link = "https://zhihu.com%s" % link
#
#
#                 s_c_item = search_content_info()
#                 s_c_item['content_title'] = title
#                 s_c_item['content_link'] = link
#                 s_c_item['agree_num'] = num_agree
#                 s_c_item['comment_num'] = num_comment
#                 yield s_c_item
#             except:
#                 continue
#
#     def parse_post(self, response):
#         soup = BeautifulSoup(response.text, "html.parser")
#         item_lists = soup.find_all(class_='List-item')
#
#         r_url = str(response.url)
#         user_id = r_url.split('/')[4]
#         for item in item_lists:
#             try:
#                 title = item.find(class_='ContentItem-title').get_text()
#                 link = "https://www.zhihu.com" + item.find(class_='ContentItem-title').a.get('href')
#                 num_up = item.find(class_='ContentItem-actions').contents[0].get_text()
#                 num_comment = item.find(class_='ContentItem-actions').contents[1].get_text()
#                 if (num_comment.find('添加评论') >= 0):
#                     num_comment = '0'
#             except:
#                 continue
#
#             post = post_info()
#             post['user_id'] = user_id
#             post['post_title'] = title
#             post['post_link'] = link
#             post['agree_num'] = num_up
#             post['comment_num'] = num_comment
#             yield post