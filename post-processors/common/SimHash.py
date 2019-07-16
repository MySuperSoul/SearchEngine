import jieba.posseg as posseg
from simhash import Simhash

class SimHashFilter(object):
    def __init__(self, hash_bits):
        self.hash_bits = hash_bits

    def HammingDistance(self, code_1, code_2):
        x = (code_1 ^ code_2) & ((1 << self.hash_bits) - 1)
        ans = 0
        while x:
            ans += 1
            x &= x - 1
        return ans

    def GetCodeForText(self, text):
        tokens = self.GetTokens(text)
        return Simhash(tokens, self.hash_bits).value

    def GetTokens(self, text):
        word_list=[word.word for word in posseg.cut(text) if word.flag[0] not in ['u','x','w','o','p','c','m','q']]
        return word_list

    def IsSimilarByText(self, text_1, text_2):
        similarity = self.Distance(text_1, text_2)
        return (similarity > 0.95, similarity)

    def IsSimilarByCode(self, code_1, code_2):
        similarity = (100 - self.HammingDistance(code_1, code_2) * 100 / self.hash_bits) / 100
        return (similarity > 0.95, similarity)

    def Distance(self, text_1, text_2):
        code_1 = self.GetCodeForText(text_1)
        code_2 = self.GetCodeForText(text_2)
        similarity = (100 - self.HammingDistance(code_1, code_2) * 100 / self.hash_bits) / 100
        return similarity