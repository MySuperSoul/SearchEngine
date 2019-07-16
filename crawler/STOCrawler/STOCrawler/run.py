from scrapy import cmdline
import sys

sys.path.append('/Users/huangyifei/projects/SearchEngine/crawler/')

name = 'sto-spider'
cmd = 'scrapy crawl {0}'.format(name)

cmdline.execute(cmd.split())