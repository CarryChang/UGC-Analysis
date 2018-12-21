import re
import json
import requests
# from fake_useragent import UserAgent
#首先先在输入的地址中提取店铺ID，然后将店铺ID和找到的接口进行匹配得到一个地址链接
##然后将得到的地址链接导入到网络爬虫中去得到json1文件
#最后解析jason文件得到内容
class Crawler:
    def __init__(self):
        #1625734074
        self.base_url = "http://waimai.baidu.com/waimai/comment/getshop?display=json&shop_id=%s&page=%s&count=99"
        self.shop_id = None
        self.page_num = 1
        self.info = {}
    def crawl(self, url=None, shop_id=None):
        self._get_shop_id(url, shop_id)
        i = 0
        while i < self.page_num:
            self._get_json_request(self.base_url % (self.shop_id, i + 1))
            i += 1
        self.page_num = 1
        self._filter()
        return self.info
    def _filter(self):
        for i, sentence in enumerate(self.info["content"]):
            rubbish_comment = False
            if self._is_english(sentence):
                rubbish_comment = True
            elif self._is_numeric(sentence):
                rubbish_comment = True
            elif self._is_too_short(sentence):
                rubbish_comment = True
            elif self._is_word_repeat(sentence):
                rubbish_comment = True
            if rubbish_comment:
                if self.info["score"][i] >= 4:
                    self.info["rubbish_comment_id"].append((i, 1))
                else:
                    self.info["rubbish_comment_id"].append((i, 0))
            else:
                if self.info["score"][i] >= 4:
                    self.info["useful_comment_id"].append((i, 1))
                else:
                    self.info["useful_comment_id"].append((i, 0))
    @staticmethod
    def _is_too_short(sentence):
        #########过滤文本字数
        if len(sentence) < 2:
            return True
        if len(re.findall(r'[\u4e00-\u9fa5]', sentence)) <= len(sentence) * 0.4:
            return True
        return False
    @staticmethod
    def _is_numeric(sentence):
        match = re.findall("\d+", sentence)
        if match is not None and sum([len(m) for m in match]) >= len(sentence) * 0.75:
            return True
        return False
    @staticmethod
    def _is_english(sentence):
        match = re.findall("[a-zA-Z]+", sentence)
        if match is not None and sum([len(m) for m in match]) >= len(sentence) * 0.75:
            return True
        return False
    @staticmethod
    def _is_word_repeat(sentence):
        repeat_words, length = [], 0
        for word in sentence:
            times = sentence.count(word)
            if times >= 4 and word not in repeat_words:
                repeat_words.append(word)
                length += times
        if length > len(sentence) / 2:
            return True
        return False
    def _get_shop_id(self, url, id):
        if url is not None:
            shop_id = re.search("\d+", url)
            if shop_id is None:
                raise ValueError("Bad url")
            self.shop_id = shop_id.group()
        elif id is not None:
            self.shop_id = id
        else:
            raise ValueError("Bad url")
    def _get_json_request(self, url):
        try:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'max-age=0',
                'cookie': 'WMID=279740f5f48dad8d6c5a2981bfe66b48; WMST=1544622441',
                'dnt': '1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            }
            result = requests.get(url, headers=headers)
        except requests.ConnectionError:
            raise ValueError("requests.ConnectionError")
        content = json.loads(result.text)
        result = content["result"]
        if self.page_num == 1:
            self._get_initial_info(result)
        content = result["content"]
        for a_json in content:
            self._get_a_json_info(a_json)
    def _get_initial_info(self, result):
        # 提取输入翻页地址
        self.page_num = result["comment_num"] // 99 + 1
        average_score = {}
        average_score["average_dish_score"] = float(result["average_dish_score"])
        average_score["average_service_score"] = float(result["average_service_score"])
        average_score["average_score"] = float(result["average_score"])
        self.info["average_score"] = average_score
        # get the score detail
        self.info["score_detail"] = result["score_detail"]
        # get the weeks score
        weeks_score = {}
        for key, value in result["weeks_score"].items():
            weeks_score[key] = float(value)
        self.info["weeks_score"] = weeks_score
        # get the recommend dished
        self.info["recommend_dishes"] = result["recommend_dishes"]
        # get the comment num
        self.info["comment_num"] = result['comment_num']
        # initialize the self.info variable
        self.info["content"] = []
        self.info["cost_time"] = []
        self.info["service_score"] = []
        self.info["dish_score"] = []
        self.info["sfrom"] = []
        self.info["score"] = []
        self.info["create_time"] = []
        self.info["arrive_time"] = []
        self.info["useful_comment_id"] = []
        self.info["rubbish_comment_id"] = []
    def _get_a_json_info(self, a_json):
        self.info["content"].append(a_json["content"])
        self.info["cost_time"].append(a_json["cost_time"])
        self.info["service_score"].append(int(a_json["service_score"]))
        self.info["dish_score"].append(int(a_json["dish_score"]))
        self.info["score"].append(int(a_json["score"]))
        self.info["sfrom"].append(a_json["sfrom"][3:] if "na-" in a_json["sfrom"] else a_json["sfrom"])
        self.info["create_time"].append(a_json["create_time"])
        self.info["arrive_time"].append(a_json["arrive_time"])
_crawler = Crawler()
crawl = _crawler.crawl
def __test1():
    shop_id = "1430806214"
    # shop_id = "1452459851"
    crawler = Crawler()
    a = crawler.crawl(shop_id)
    pass
if __name__ == "__main__":
    pass
    __test1()
