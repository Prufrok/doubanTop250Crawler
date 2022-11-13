import scrapy


class DoubanItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    img_url = scrapy.Field()
    author = scrapy.Field()
    rate = scrapy.Field()
    votes_num = scrapy.Field()
    comments_num = scrapy.Field()

    def insert_sql(self):
        insert_sql = """
            INSERT INTO
                douban(
                    title,
                    url,
                    img_url,
                    author,
                    rate,
                    votes_num,
                    comments_num
                )
            VALUES
                (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            self['title'],
            self['url'],
            self['img_url'],
            self['author'],
            self['rate'],
            self['votes_num'],
            self['comments_num'],
        )
        return insert_sql, params