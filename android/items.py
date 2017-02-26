import scrapy 
class apkItem(scrapy.Item):
    #ID
    packageName =scrapy.Field()
    APPName=scrapy.Field()
    APPType=scrapy.Field()
    version=scrapy.Field()
    download_url=scrapy.Field()
    file_store_url=scrapy.Field()
    permission=scrapy.Field()
    description=scrapy.Field()