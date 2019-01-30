# coding:utf-8
import sys
import jieba


class WordToken(object):
    def __init__(self):
        # 最小起始id号, 保留的用于表示特殊标记
        self.START_ID = 4
        self.word2id_dict = {}
        self.id2word_dict = {}


    def load_file_list(self, file_list, min_freq):
        """
        加载样本文件列表，全部切词后统计词频，按词频由高到低排序后顺次编号
        并存到self.word2id_dict和self.id2word_dict中
        """
        words_count = {}
        for file in file_list:
            # 加载单个文件
            with open(file, 'r',encoding='UTF-8') as file_object:
                for line in file_object.readlines():
                    # 单行
                    line = line.strip()
                    # 分词
                    seg_list = jieba.cut(line)
                    # 统计words_count:{str,count}
                    for str in seg_list:
                        if str in words_count:
                            words_count[str] = words_count[str] + 1
                        else:
                            words_count[str] = 1
        # sorted_list[[words_count,str]]
        sorted_list = [[v[1], v[0]] for v in words_count.items()]
        # 排序 - 降序
        sorted_list.sort(reverse=True)
        # 编号，元素
        for index, item in enumerate(sorted_list):
            word = item[1]
            # 在样本中出现频率超过min_freq才会进入词表
            # 由于是降序，当出现item[0] < min_freq 时，剩余的数据频率均小于min_freq，因此break
            if item[0] < min_freq:
                break
            # 按照当前sorted_list顺序，将词语顺序保存至 word2id_dict，编号从START_ID开始递增  词语:编号，使用词语查询编号
            self.word2id_dict[word] = self.START_ID + index
            # 按照当前sorted_list顺序，将词语顺序保存至 id2word_dict，编号从START_ID开始递增  编号:词语，使用编号查询词语
            self.id2word_dict[self.START_ID + index] = word
        return index

    def word2id(self, word):
        # if not isinstance(word, unicode):
        #     print("Exception: error word not unicode")
        #     sys.exit(1)
        if word in self.word2id_dict:
            return self.word2id_dict[word]
        else:
            return None

    def id2word(self, id):
        id = int(id)
        if id in self.id2word_dict:
            return self.id2word_dict[id]
        else:
            return None

