# doubanTop250Crawler

## 1. 简介
初学爬虫写的一个小项目，目标是：

* 爬取[豆瓣读书Top250](https://book.douban.com/top250)的书籍信息，挑选了书名、网址链接、封面链接、作者、评分、评分人数和评论人数共7个字段进行爬取
* 将爬取到的数据写入MySQL数据库进行保存

## 2. 注意
* 代理池搭建参考[jhao104/proxy_pool](https://github.com/jhao104/proxy_pool)项目
* 通过随机生成bid进行简易反爬策略参考自：[Scrapy中 CrawlSpider 使用](https://zhuanlan.zhihu.com/p/84554363)和[单机30分钟抓取豆瓣电影7万+数据](https://zhuanlan.zhihu.com/p/24035574)
* 豆瓣读书页面中作者一栏常包含空格（` `）和换行符（`\n`），在写入数据库前需要注意
* 需要修改settings.py中的数据库配置信息，也可以修改并发、延迟等等参数；如果需要使用代理池，需要修改middlewares.py中的代理池地址
* 运行代码前需要新建MySQL数据库和表，具体SQL语句可参考如下：
    ```SQL
    CREATE DATABASE IF NOT EXISTS your_database;

    DROP TABLE IF EXISTS your_table;

    CREATE TABLE your_table(
        title VARCHAR(255) PRIMARY KEY,
        url VARCHAR(255),
        img_url VARCHAR(255),
        author VARCHAR(255),
        rate FLOAT,
        votes_num INT,
        comments_num INT
    );
    ```
