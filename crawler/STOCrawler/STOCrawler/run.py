from scrapy import cmdline

name = 'sto-spider'
cmd = 'scrapy crawl {0}'.format(name)

cmdline.execute(cmd.split())