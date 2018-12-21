import matplotlib.pyplot as plt
from pylab import mpl
from txt_analysis import spider
from random import choice
###加载score_detail
def score_detail(result):
    if result is not None:
        # 导入json数据
        label_scores = sorted(result["score_detail"].items())
        # labels
        labels = "1分", "2分", "3分", "4分", "5分"
        # sizes
        sizes = [pair[1] for pair in label_scores]
        # explode
        the_max = max(sizes)
        the_index = sizes.index(the_max)
        explode = [0, 0, 0, 0, 0]
        explode[the_index] = 0.1
        explode = tuple(explode)
        plt.pie(sizes, explode=explode, labels=labels,
                autopct="%1.2f%%", shadow=True, startangle=0)
        plt.title("整体评分分析", loc="left", fontsize=20)
        plt.axis("equal")
        plt.show()
        plt.close()
#dish_score统计
def dish_score_detail(result):
    if result is not None:
        # 导入
        label_scores = result["dish_score"]
        # labels
        labels = "1分", "2分", "3分", "4分", "5分"
        # sizes
        sizes = [label_scores.count(i) for i in range(5)]
        # explode
        the_max = max(sizes)
        the_index = sizes.index(the_max)
        explode = [0, 0, 0, 0, 0]
        explode[the_index] = 0.1
        explode = tuple(explode)
        plt.pie(sizes, explode=explode, labels=labels,
                autopct="%1.2f%%", shadow=True, startangle=0)
        plt.title("商品质量评分分析", loc="left", fontsize=20)
        plt.axis("equal")
        plt.show()
        plt.close()
def bar_auto_label(rects, suffix="分"):
    colors = ["g", "r", "c", "m", "y", "b", "chartreuse", "lightgreen", "skyblue",
              "dodgerblue", "slateblue", "blueviolet", "purple", "mediumorchid",
              "fuchsia", "hotpink", "lightcoral", "coral", "darkorange", "olive",
              "lawngreen", "yellowgreen", "springgreen", "cyan", "indigo", "darkmagenta",
              "orchid", "lightpink", "darkred", "orangered", "goldenrod", "lime", "aqua",
              "steelblue", "plum", "m", "tomato", "greenyellow", "darkgreen", "darkcyan",
              "violet", "crimson"]
    for i, rect in enumerate(rects):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, 1.01 * height, "%s%s" % (float(height), suffix))
        color = choice(colors)
        colors.remove(color)
        rect.set_color(color)
#各项评价平均指标统计
def average_score(result):
    import numpy as np
    if result is not None:
        # 导入json数据
        average_scores = result["average_score"]
        title = "评价指标平均分数"
        y_label = "分数"
        labels = ("质量", "服务", "整体")
        label_pos = (0, 1, 2)
        heights = (average_scores["average_dish_score"],
                   average_scores["average_service_score"],
                   average_scores["average_score"])
        plt.title(title, fontsize=20)
        plt.ylabel(y_label)
        plt.ylim(0, 5)
        plt.xticks(label_pos, labels)
        rect = plt.bar(label_pos, heights, width=0.35, align="center")
        bar_auto_label(rect)
        plt.show()
        plt.close()
#订餐平台分析统计
def s_from(result):
    if result is not None:
        sfrom = result["sfrom"]
        title = "使用终端分析"
        # total sources
        sources = tuple(set(sfrom))
        # size
        sizes = [sfrom.count(source) for source in sources]
        plt.pie(sizes, labels=sources, autopct="%1.2f%%", shadow=True, startangle=0)
        plt.title(title, loc="left", fontsize=20)
        plt.axis("equal")
        plt.show()
        plt.close()
def barh_auto_label(rects, suffix="次"):
    colors = ["g", "r", "c", "m", "y", "b", "chartreuse", "lightgreen", "skyblue",
              "dodgerblue", "slateblue", "blueviolet", "purple", "mediumorchid",
              "fuchsia", "hotpink", "lightcoral", "coral", "darkorange", "olive",
              "lawngreen", "yellowgreen", "springgreen", "cyan", "indigo", "darkmagenta",
              "orchid", "lightpink", "darkred", "orangered", "goldenrod", "lime", "aqua",
              "steelblue", "plum", "m", "tomato", "greenyellow", "darkgreen", "darkcyan",
              "violet", "crimson"]
    for i, rect in enumerate(rects):
        width = rect.get_width()
        plt.text(1.01 * width, rect.get_y(), "%s%s" % (int(width), suffix))
        color = choice(colors)
        colors.remove(color)
        rect.set_color(color)
####获取热卖单品
def recommend_dishes2(result):
    if result is not None:
        # 导入json数据
        ##########直接导入推荐单品数据
        recommend_dishes = sorted(result["recommend_dishes"].items(), key=lambda dish: dish[1])[-30:]
        title = "推荐单品展示"
        x_label = "次"
        labels = [dish[0] for dish in recommend_dishes]
        label_pos = tuple(range(len(labels)))
        heights = tuple([dish[1] for dish in recommend_dishes])
        plt.title(title, fontsize=20)
        plt.xlabel(x_label)
        plt.yticks(label_pos, labels)
        rects = plt.barh(label_pos, width=heights, alpha=0.35, align="center")
        barh_auto_label(rects)
        plt.show()
        plt.close()
def cost_time(result):
    if result is not None:
        # 导入json数据
        cost_times = result["cost_time"]
        title = "送餐时间可视化分布"
        sources = ("<30min)", "30-45min)", "45-60min)", "60-75min", "大于75min")
        sizes = [0] * len(sources)
        for a_time in cost_times:
            ############使用限定时间
            if a_time <= 30:
                sizes[0] += 1
            elif a_time <= 45:
                sizes[1] += 1
            elif a_time <= 60:
                sizes[2] += 1
            elif a_time <= 75:
                sizes[3] += 1
            else:
                sizes[4] += 1
        the_max = max(sizes)
        the_index = sizes.index(the_max)
        explode = [0, 0, 0, 0, 0]
        explode[the_index] = 0.1
        explode = tuple(explode)
        # 使用饼图
        plt.pie(sizes, labels=sources, explode=explode, autopct="%1.2f%%", shadow=True, startangle=0)
        plt.title(title, loc="left", fontsize=20)
        ####使用正圆
        plt.axis("equal")
        plt.show()
        plt.close()
def _test():
    shop_id = "1452459851"
    # 采集结果
    result = spider.crawl(shop_id)
    # 1采集score_detail
    score_detail(result)
    # 2采集average_score
    average_score(result)
    # 3采集sfrom
    s_from(result)
    # 4采集recommend_dishes
    recommend_dishes2(result)
    # 5采集cost_time
    cost_time(result)
if __name__ == "__main__":
    pass
    _test()