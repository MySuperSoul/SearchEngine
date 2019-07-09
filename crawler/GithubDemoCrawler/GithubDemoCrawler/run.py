from scrapy import cmdline

name = 'github-spider'
cmd = 'scrapy crawl {0}'.format(name)

cmdline.execute(cmd.split())