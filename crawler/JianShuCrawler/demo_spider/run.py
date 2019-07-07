from scrapy import cmdline

name = 'demo-spider'
cmd = 'scrapy crawl {0}'.format(name)

cmdline.execute(cmd.split())