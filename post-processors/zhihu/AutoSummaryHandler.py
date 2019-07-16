from textrank4zh import TextRank4Sentence

class AutoSummaryHandler():
    def __init__(self):
        self.tr4w = TextRank4Sentence()

    def GetSummary(self, content) -> str:
        self.tr4w.analyze(text=content, lower=True, source='all_filters')
        key_sentences = self.tr4w.get_key_sentences(num=2)
        summary = '. '.join(sentence['sentence'] for sentence in key_sentences)
        return summary