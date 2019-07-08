from scrapy import cmdline

name = 'zhihu-spider'
cmd = 'scrapy crawl {0}'.format(name)

cmdline.execute(cmd.split())