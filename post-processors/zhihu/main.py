from zhihu.AutoTagHandler import AutoTagHandler
from zhihu.AutoSummaryHandler import AutoSummaryHandler

if __name__ == '__main__':
    tag_handler = AutoTagHandler()
    summary_handler = AutoSummaryHandler()

    # do something
    print(tag_handler.GetTags(''))
    print(summary_handler.GetSummary(''))