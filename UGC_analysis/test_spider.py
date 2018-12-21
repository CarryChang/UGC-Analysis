from txt_analysis import spider
import json
def test1():
    id = "1438461721"
    result = spider.crawl(id)
    # 1k +
    # https://star.ele.me/shopui/?qt=shopcomment&shop_id=1553452950
    ##http://waimai.baidu.com/waimai/comment/getshop?display=json&shop_id=1570745324&page=0&count=99
    # https://star.ele.me/shopui/?qt=shopcomment&shop_id=1438461721
    with open("crawler.txt", "w", encoding="utf-8") as f:
        # f.write(str(result))
        # json.dump(result, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(",", ":"))
        json.dump(result, f, ensure_ascii=False)

if __name__ == "__main__":
    test1()
