[![996.icu](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu)

[![Stargazers over time](https://starchart.cc/CarryChang/UGC-Analysis.svg)](https://starchart.cc/CarryChang/UGC-Analysis)

##### 饿了么星选平台的 UGC 进行分析
  1. 包括数据实时采集、预处理。
  2. 基于词典的主题提取
  3. Snownlp情感分析
  4. 可视化


##### 程序结构为：![结构图](https://github.com/CarryChang/UGC-Analysis/blob/master/pic/%E7%A8%8B%E5%BA%8F%E7%BB%93%E6%9E%84.png)
#####  UGC_Analysis.py利用Tkinter技术进行GUI设计，属于主文件，对spider.py网络爬虫程序和picturing.py数据可视化程序进行调度，它的作用就是将Spider.py文件采集出来的非结构化评论文本进行情感计算然后将计算出来的分数传给picturing.py进行可视化处理，然后将处理后的统计图传到主文件进行展示，对于spider.py采集出的结构化数据，如用户打分等结构化数据传给picturn.py进行统计绘图，然后传给主文件进行展示。
##### 本软件产生在互联网产业迅速发展的大背景下，随着在线购物平台、在线旅游平台等在线服务平台用户成数据呈现级数增长，平台上也会产生大量的的UGC(User Generated Content)用户生成内容，比如商品发表的评论、用户提交的照片、用户评分等等。UGC本身含有对于此项服务或产品的意见，对此进行意见挖掘可以帮助平台上的服务提供商进行必要的业务调整，平台对于UGC的展示能帮助消费者增加对于商品或服务的认知，但是大量UGC显示出的用户打分和评价出现不相符合的特征，为防止对潜在消费者出现误导，平台也需要对UGC进行必要的处理和展示，以此来显示平台本身以及销售商品的质量。所以本软件站在平台的角度，使用tkinter制作操作界面、使用matplotlib画出统计图，通过在线原始评论采集、评论情感计算并分类展示、以及对于用户打分、服务评分等结构化数据进行可视化等方式，以便于帮助平台更好的展示用户评论和售卖信息，增加商品销量。
![菜品分析](https://github.com/CarryChang/UGC-Analysis/blob/master/pic/统计.png)
#### 本软件特点
>1. 	改造了网络爬虫，使用fake_useragent加入随机轮换模拟浏览器header来确保爬虫的稳定和高效爬取。
![情感分析](https://github.com/CarryChang/UGC-Analysis/blob/master/pic/采集到的数据样式.png)
>2. 	利用Snownlp作为评论情感分析的库，直接在输出框输出情感值。
![情感分析](https://github.com/CarryChang/UGC-Analysis/blob/master/pic/%E6%83%85%E6%84%9F%E5%88%86%E6%9E%90.png)
>3. 	利用词典的方式找出主题，便于实时对评论进行筛选。
![主题分析](https://github.com/CarryChang/UGC-Analysis/blob/master/pic/配送.png)
![味道分析](https://github.com/CarryChang/UGC-Analysis/blob/master/pic/味道.png)
