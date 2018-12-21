import re
import tkinter as tk
from threading import Thread
from txt_analysis import picturing
from txt_analysis.spider import crawl
from txt_analysis import spider
from snownlp import SnowNLP
import json
import matplotlib.pyplot as plt
# 显示中文
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
#有中文出现的情况，需要u'内容'
import numpy as np
# 设定变量参数
ALL = "all comments"
ALL1 = "all comments"
positive = "good comments"
medium = "medium comments"
negative = "bad comments"
taste_pos = " taste_pos"
taste_neg = " taste_neg"
taste = " taste"
speed_pos = " speed_pos"
speed_neg = " speed_neg"
speed = " speed"
weight_pos = " weight_pos"
weight_neg = " weight_neg"
weight = " weight"
service_pos = " service_pos"
service_neg = " service_neg"
service = " service"
price_pos = " price_pos"
price_neg = " price_neg"
price = " price"
start = 7
height = 30
width = 60
re_space = re.compile('(\s+)')
all_direction = tk.E + tk.N + tk.W + tk.S
result = None
def get_result():
    global result
    try:
        ##将地址传入数据采集，并将信息采集到本地
        result1 = spider.crawl(url_tv.get())
        with open("resource.txt", "w", encoding="utf-8") as f:
            json.dump(result1, f, ensure_ascii=False,indent=2)
        result = crawl(url_tv.get())
        prompt_text.set("在线评论数据采集完毕，可以进行后续分析")
    except ValueError:
        prompt_text.set("地址有误，请重新输入!")
def data_collecting():
    #点击输入框时，开启多线程，将信息发送给prompt_text
    prompt_text.set("正在采集信息，请稍后......")
    ############采集功能使用多线程来维护界面的流畅
    t = Thread(target=get_result)
    t.start()
###########使用传参
def test_tag(parse_result, sentence, type_, foreground, i, check_tv, j):
    index = start
    if check_tv.get():
        result = parse_result[type_]
        for a in result:
            index = sentence.index(a, index)
            text.tag_add("tag%d_%d" % (i, j), "%d.%d" % (i, index), "%d.%d" % (i, index + len(a)))
            text.tag_config("tag%d_%d" % (i, j), foreground=foreground)
            index += len(a)
            j += 1
    return j
def text_tag_config(sentence, i):
    sentence = re_space.sub(r' ', sentence)
    # print(i, sentence)
    #########增加情感极性分数显示
    sentence = "%5d. %s" % (i, sentence)
    text.insert(tk.END, "%s\n" % sentence)
# 增加对于积极和消极的极性评价
def text_tag_config1(sentence, i, score):
    # sentence = re_space.sub(r' ', sentence)
    # print(i, sentence)
    #########增加情感极性分数显示
    sentence_1 = "%5d. %s %s" % (i, sentence, score)
    text.insert(tk.END, "%s\n" % sentence_1)
########进行情感趋势画图
def emotion_analysis(which):
    col = 20
    if result is not None:
        sentiments_list = []
        text.delete(1.0, tk.END)
        comments = result["content"]
        scores = result["score"]
        comments = [comments[a[0]] for a in result["useful_comment_id"]]
        scores = [scores[a[0]] for a in result["useful_comment_id"]]
        if which == ALL1:
            j_1 = 0
            for i in range(len(comments)):
                print(comments[i])
                s = SnowNLP(comments[i])
                # score = round(s.sentiments,3)
                score = s.sentiments
                sentiments_list.append(score)
                j_1 += 1
            text_tag_config1(comments[i], j_1, score)
        plt.hist(sentiments_list, bins=col)
        plt.xlabel("情感值")
        plt.ylabel("评论数目")
        plt.title('整体情感极性分布图')
        plt.show()
        plt.close()
def emotion_pic(which):
    col = 20
    # 使用关键字找取对应的评论
    taste_keywords = ["闻","口感","吃",'喝','尝','味','下饭','咬','味道','卖相','新鲜','嫩']
    speed_keywords = ["送",'速','到达','快','慢','催','快递','送达']
    weight_keywords = ['量','分量','轻重','斤','少']
    service_keywords = ["服务","态度",'语气']
    price_keywords = ["价格", "钱",'实惠','价','贵','便宜']
    if result is not None:
        sentiments_list = []
        text.delete(1.0, tk.END)
        comments = result["content"]
        scores = result["score"]
        comments = [comments[a[0]] for a in result["useful_comment_id"]]
        scores = [scores[a[0]] for a in result["useful_comment_id"]]
        if which == taste:
            j1 = 1
            for i in range(len(scores)):
                for keyword in taste_keywords:
                    if keyword in comments[i]:
                        ###对符合条件的抓取出来，并计算情感极性
                        s = SnowNLP(comments[i])
                        score = s.sentiments
                        sentiments_list.append(score)
                        text_tag_config1(comments[i], j1, score)
                        j1 += 1
            plt.hist(sentiments_list, bins=col)
            plt.xlabel("情感值")
            plt.ylabel("评论数目")
            plt.title('味道情感极性分布图')
            plt.show()
            plt.close()
        elif which == speed:
            j2 = 1
            for i in range(len(scores)):
                for keyword in speed_keywords:
                    if keyword in comments[i]:
                        ###对符合条件的抓取出来，并计算情感极性
                        s = SnowNLP(comments[i])
                        score = s.sentiments
                        sentiments_list.append(score)
                        text_tag_config1(comments[i], j2, score)
                        j2 += 1
            plt.hist(sentiments_list, bins=col)
            plt.xlabel("情感值")
            plt.ylabel("评论数目")
            plt.title('配送情感极性分布图')
            plt.show()
            plt.close()
        elif which == weight:
            j3 = 1
            for i in range(len(scores)):
                for keyword in weight_keywords:
                    if keyword in comments[i]:
                        ###对符合条件的抓取出来，并计算情感极性
                        s = SnowNLP(comments[i])
                        score = s.sentiments
                        sentiments_list.append(score)
                        text_tag_config1(comments[i], j3, score)
                        j3 += 1
            plt.hist(sentiments_list, bins=col)
            plt.xlabel("情感值")
            plt.ylabel("评论数目")
            plt.title('份量情感极性分布图')
            plt.show()
            plt.close()
        elif which == service:
            j4 = 1
            for i in range(len(scores)):
                for keyword in service_keywords:
                    if keyword in comments[i]:
                        ###对符合条件的抓取出来，并计算情感极性
                        s = SnowNLP(comments[i])
                        score = s.sentiments
                        sentiments_list.append(score)
                        text_tag_config1(comments[i], j4, score)
                        j4 += 1
            plt.hist(sentiments_list, bins=col)
            plt.xlabel("情感值")
            plt.ylabel("评论数目")
            plt.title('服务情感极性分布图')
            plt.show()
            plt.close()
        elif which == price:
            j5 = 1
            for i in range(len(scores)):
                for keyword in price_keywords:
                    if keyword in comments[i]:
                        ###对符合条件的抓取出来，并计算情感极性
                        s = SnowNLP(comments[i])
                        score = s.sentiments
                        sentiments_list.append(score)
                        text_tag_config1(comments[i], j5, score)
                        j5 += 1
            plt.hist(sentiments_list, bins=col)
            plt.xlabel("情感值")
            plt.ylabel("评论数目")
            plt.title('价格情感极性分布图')
            plt.show()
            plt.close()
def all_display(which):
    if result is not None:
        text.delete(1.0, tk.END)
        comments = result["content"]
        if which == ALL:
            i = 1
            for comment in comments:
                text_tag_config(comment, i)
                i += 1
def all_button_event(which):
    # 使用关键字找取对应的评论
    taste_keywords = ["闻","口感","吃",'喝','尝','味','下饭','咬','味道','卖相','新鲜','嫩']
    speed_keywords = ["送",'速','到达','快','慢','催','快递','送达']
    weight_keywords = ['量','分量','轻重','斤','少']
    service_keywords = ["服务","态度",'语气']
    price_keywords = ["价格", "钱",'实惠','价','贵','便宜']
    if result is not None:
        text.delete(1.0, tk.END)
        comments = result["content"]
        scores = result["score"]
        comments = [comments[a[0]] for a in result["useful_comment_id"]]
        scores = [scores[a[0]] for a in result["useful_comment_id"]]
        # 按照评分和情感分数（snownlp展示）展示评论极性分数
        if which == positive:
            j6 = 1
            for i in range(len(scores)):
                s = SnowNLP(comments[i])
                score = s.sentiments
                if scores[i] >= 4 and score > 0.7:
                    text_tag_config1(comments[i], j6, score)
                    j6 += 1
        elif which == medium:
            j7 = 1
            for i in range(len(scores)):
                s = SnowNLP(comments[i])
                score = s.sentiments
                if 2 <= scores[i] < 4 and 0.3 <= score <= 0.7:
                    text_tag_config1(comments[i], j7, score)
                    j7 += 1
        elif which == negative:
            j8 = 1
            for i in range(len(scores)):
                s = SnowNLP(comments[i])
                score = s.sentiments
                if scores[i] < 2 and score < 0.3:
                    text_tag_config1(comments[i], j8, score)
                    j8 += 1
        ###################后续分类打分
        elif which == taste_pos:
            j9 = 1
            for i in range(len(scores)):
                for keyword in taste_keywords:
                    if keyword in comments[i]:
                        ###对符合条件的抓取出来，并计算情感极性
                        s = SnowNLP(comments[i])
                        score = s.sentiments
                        if scores[i] >= 4 and score > 0.5:
                            text_tag_config1(comments[i], j9, score)
                            j9 += 1
        elif which == taste_neg:
            j10 = 1
            for i in range(len(scores)):
                for keyword in taste_keywords:
                    if keyword in comments[i]:
                        ###对符合条件的抓取出来，并计算情感极性
                        s = SnowNLP(comments[i])
                        score = s.sentiments
                        if scores[i] < 4 and score <= 0.5:
                            text_tag_config1(comments[i], j10, score)
                            j10 += 1
        elif which == speed_pos:
            j11 = 1
            for i in range(len(scores)):
                for keyword in speed_keywords:
                    if keyword in comments[i]:
                        ###对符合条件的抓取出来，并计算情感极性
                        s = SnowNLP(comments[i])
                        score = s.sentiments
                        if scores[i] >= 4 and score > 0.5:
                            text_tag_config1(comments[i], j11, score)
                            j11 += 1
        elif which == speed_neg:
            j12 = 1
            for i in range(len(scores)):
                for keyword in speed_keywords:
                    if keyword in comments[i]:
                        ###对符合条件的抓取出来，并计算情感极性
                        s = SnowNLP(comments[i])
                        score = s.sentiments
                        if scores[i] < 4 and score <= 0.5:
                            text_tag_config1(comments[i], j12, score)
                            j12 += 1
        elif which == weight_pos:
            j13 = 1
            for i in range(len(scores)):
                for keyword in weight_keywords:
                    if keyword in comments[i]:
                        ###对符合条件的抓取出来，并计算情感极性
                        s = SnowNLP(comments[i])
                        score = s.sentiments
                        if scores[i] >= 4 and score > 0.5:
                            text_tag_config1(comments[i], j13, score)
                            j13 += 1
        elif which == weight_neg:
            j14 = 1
            for i in range(len(scores)):
                for keyword in weight_keywords:
                    if keyword in comments[i]:
                        ###对符合条件的抓取出来，并计算情感极性
                        s = SnowNLP(comments[i])
                        score = s.sentiments
                        if scores[i] < 4 and score <= 0.5:
                            text_tag_config1(comments[i], j14, score)
                            j14 += 1
        elif which == service_pos:
            j15 = 1
            for i in range(len(scores)):
                for keyword in service_keywords:
                    if keyword in comments[i]:
                        ###对符合条件的抓取出来，并计算情感极性
                        s = SnowNLP(comments[i])
                        score = s.sentiments
                        if scores[i] >= 4 and score > 0.5:
                            text_tag_config1(comments[i], j15, score)
                            j15 += 1
        elif which == service_neg:
            j16 = 1
            for i in range(len(scores)):
                for keyword in service_keywords:
                    if keyword in comments[i]:
                        ###对符合条件的抓取出来，并计算情感极性
                        s = SnowNLP(comments[i])
                        score = s.sentiments
                        if scores[i] < 4 and score <= 0.5:
                            text_tag_config1(comments[i], j16, score)
                            j16 += 1
        elif which == price_pos:
            j17 = 1
            for i in range(len(scores)):
                for keyword in price_keywords:
                    if keyword in comments[i]:
                        ###对符合条件的抓取出来，并计算情感极性
                        s = SnowNLP(comments[i])
                        score = s.sentiments
                        if scores[i] >= 4 and score > 0.5:
                            text_tag_config1(comments[i], j17, score)
                            j17 += 1
        elif which == price_neg:
            j18 = 1
            for i in range(len(scores)):
                for keyword in price_keywords:
                    if keyword in comments[i]:
                        ###对符合条件的抓取出来，并计算情感极性
                        s = SnowNLP(comments[i])
                        score = s.sentiments
                        if scores[i] < 4 and score <= 0.5:
                            text_tag_config1(comments[i], j18, score)
                            j18 += 1
root = tk.Tk()
root.resizable(False, False)
# 开始文本处理
frame1 = tk.Frame(root, bd=1, relief=tk.SUNKEN)
frame1.pack(fill=tk.BOTH, expand=tk.YES, anchor=tk.CENTER)
# 输入框定义
row_num = 0
url_tv = tk.StringVar()
url_tv_column_span = 9
tk.Entry(frame1,textvariable=url_tv).grid(
    row=row_num, column=0, columnspan=url_tv_column_span,padx=2, sticky=all_direction)
####绑定按钮事件，将采集绑定到多线程开始采集按钮
tk.Button(frame1, text="开始采集",command=data_collecting).grid(
    row=row_num, column=url_tv_column_span, sticky=all_direction)
row_num = 1
prompt_text = tk.StringVar()
tk.Label(frame1, textvariable=prompt_text).grid(row=row_num, column=0, columnspan=8, pady=5, sticky=all_direction)
prompt_text.set("请在上面输入数据采集的链接")
# 设置按钮
row_num = 2
columnspan = 2
tk.Button(frame1, text="所有评论展示", command=lambda: all_display(ALL)).grid(
    row=row_num, column=columnspan * 0, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
##使用commands绑定动作
tk.Button(frame1, text="总体情感趋势", command=lambda: emotion_analysis(ALL1)).grid(
    row=row_num, column=columnspan * 1, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="积极评论分析", command=lambda: all_button_event(positive)).grid(
    row=row_num, column=columnspan * 2, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="一般评论分析", command=lambda: all_button_event(medium)).grid(
    row=row_num, column=columnspan * 3, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="消极评论分析", command=lambda: all_button_event(negative)).grid(
    row=row_num, column=columnspan * 4, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
row_num = 3
tk.Button(frame1, text="味道积极评论", command=lambda: all_button_event(taste_pos)).grid(
    row=row_num, column=columnspan * 0, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="配送积极评论", command=lambda: all_button_event(speed_pos)).grid(
    row=row_num, column=columnspan * 1, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="份量积极评论", command=lambda: all_button_event(weight_pos)).grid(
    row=row_num, column=columnspan * 2, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="服务积极评论", command=lambda: all_button_event(service_pos)).grid(
    row=row_num, column=columnspan * 3, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="价格积极评论", command=lambda: all_button_event(price_pos)).grid(
    row=row_num, column=columnspan * 4, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
row_num = 4
tk.Button(frame1, text="味道消极评论", command=lambda: all_button_event(taste_neg)).grid(
    row=row_num, column=columnspan * 0, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="配送消极评论", command=lambda: all_button_event(speed_neg)).grid(
    row=row_num, column=columnspan * 1, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="份量消极评论", command=lambda: all_button_event(weight_neg)).grid(
    row=row_num, column=columnspan * 2, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="服务消极评论", command=lambda: all_button_event(service_neg)).grid(
    row=row_num, column=columnspan * 3, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="价格消极评论", command=lambda: all_button_event(price_neg)).grid(
    row=row_num, column=columnspan * 4, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
row_num = 5
tk.Button(frame1, text="味道情感趋势", command=lambda: emotion_pic(taste)).grid(
    row=row_num, column=columnspan * 0, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="配送情感趋势", command=lambda: emotion_pic(speed)).grid(
    row=row_num, column=columnspan * 1, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="份量情感趋势", command=lambda: emotion_pic(weight)).grid(
    row=row_num, column=columnspan * 2, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="服务情感趋势", command=lambda: emotion_pic(service)).grid(
    row=row_num, column=columnspan * 3, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="价格情感趋势", command=lambda: emotion_pic(price)).grid(
    row=row_num, column=columnspan * 4, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
#统计分析
frame0 = tk.LabelFrame(root, text="评论数字图表区", padx=2, pady=2, relief=tk.GROOVE)
frame0.pack(fill=tk.BOTH, expand=tk.YES)
columnspan = 7
# 调节按钮之间的行距，可视化文本之中的数据
##配送时间汇总，推荐商品汇总，终端分布，质量分布，按钮绑定事件，row表示行数
tk.Button(frame0, text="整体评分分析", command=lambda: picturing.score_detail(result)).grid(
    row=1, column=columnspan * 4, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame0, text="指标评分分析", command=lambda: picturing.average_score(result)).grid(
    row=1, column=columnspan * 0, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame0, text="终端统计分析", command=lambda: picturing.s_from(result)).grid(
    row=1, column=columnspan * 1, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame0, text="热推商品展示", command=lambda: picturing.recommend_dishes2(result)).grid(
    row=1, column=columnspan * 2, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame0, text="配送时间分析", command=lambda: picturing.cost_time(result)).grid(
    row=1, column=columnspan * 3, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
# 开始文本处理
frame2 = tk.Frame(root, bd=1, relief=tk.SUNKEN)
frame2.pack(fill=tk.BOTH, expand=tk.YES, anchor=tk.CENTER)
row_num = 5
#文本框更改hight和width更改大小
text = tk.Text(frame2, height=30, width=56)
text.grid(row=row_num, column=0, columnspan=11, padx=10, pady=10)
scrollbar = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=text.yview)
scrollbar.grid(row=row_num, column=11, rowspan=1, sticky=all_direction)
text.configure(yscrollcommand=scrollbar.set)
root.title('情感分析在电商评价中的应用demo')
root.mainloop()