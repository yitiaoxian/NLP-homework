import os

from pyltp import Segmentor
from pyltp import Postagger
from pyltp import SentenceSplitter

class BookPostag:
    '''
    生成标注语料类
    :keyword dan表示 d 副词 a 形容词 n 名词
    '''
    ltp_model_path = "E:\\NLP-homework\\ltp-data-v3.3.1\\ltp_data"
    #ltp模型路径
    book_root_path = "E:\\NLP-homework\\book"
    #书籍路径
    postag_root_path = "E:\\NLP-homework\\BookPostag"
    #语料路径

    segmentor = Segmentor()
    segmentor.load(ltp_model_path + "\\cws.model")

    postagger = Postagger()
    postagger.load(ltp_model_path + "\\pos.model")

    def segmentor(self,sentence = "测试测试啊哈哈哈"):
        '''
        pyltp的分词模型
        :param sentence:
        :return:
        '''
        words = self.segmentor.segment(sentence)
        words_list = list(words)
        # for word in words_list:
        #     print word
        # seg.release()
        return words_list

    def postagger(self,word_list):
        '''
        pyltp的词性标注模型
        :param word_list:
        :return:
        '''
        postags = self.postagger.postag(word_list)  # 词性标注
        dan_list = []
        for word, tag in zip(word_list, postags):
            if tag == "n" or tag == "a" or tag == "d":
                if len(word) > 3:
                    print(word + '/' + tag)
                    dan_list.append(word)
        # postagger.release()  # 释放模型
        return dan_list

    def getDAN(self):
        '''
        读取文本文件,获取danlist
        :return:
        '''
        #txts = []
        dan_list = []
        files = os.listdir(self.book_root_path)
        for file in files:
            fileposition = self.book_root_path + "\\" + file
            print("file name:", fileposition)
            with open(fileposition,"r",encoding="utf-8")as f:
                lines = f.readline()
                for line in lines :
                    #txts.append(line)
                    if line != "":
                        sentences = SentenceSplitter.split(line)
                        print("sentences:", sentences)
                        for sentence in sentences:
                            words = self.segmentor(sentence)
                            dan_list_line = self.postagger(words)
                            dan_list += dan_list_line
                f.close()
        return list(set(dan_list))



    #def getDAN(self):

        '''
        #path  文章路径;
        :param path:
        :return:
        '''
      #  dan_list = []
       # rf = open(path,"r")
        #lines = rf.readline()
        #rf.close()
        #for line in lines:
         #   if line != "":
          #      sents = SentenceSplitter.split(line)
           #     for sent in sents :
            #        words = self.segmentor(sent)
             #       dan_list_line = self.postagger(words)
              #      dan_list += dan_list_line

        #return list(set(dan_list))

    def getResult(self):
        allResult = []
        txtPathList = self.getAllPath()
        for txtPath in txtPathList:
            dan_list =self.getDAN(txtPath)
            allResult += dan_list
        print('getResult1:',len(allResult))
        print('getResult2:',len(set(allResult)))
        resultList = sorted(list(set(allResult)))
        self.writeDan(self.postag_root_path,"Postag.txt",resultList)
        return resultList

    def writeDan(self,path,filename,sortedList):
        wf = open(path+"\\"+filename,"w")
        for elem in sortedList:
            wf.write(elem)
            # wf.write("\n")
        wf.close()

    def splitTxt(self,path = postag_root_path+"\\Postag.txt"):

        rf = open(path,"r")
        lines = rf.readline()
        rf.close()
        print("splitTxt中的lines长度：",len(lines))
        self.writeDan(self.postag_root_path,"liu1.txt",lines[0:4000])
        self.writeDan(self.postag_root_path,"ci1.txt",lines[4000:8000])
        self.writeDan(self.postag_root_path,"xing1.txt",lines[8000:])

import time

start = time.time()
listx = []
bookpostag = BookPostag()
listx = bookpostag.getDAN()
#bookpostag.getResult()
#bookpostag.splitTxt()
end = time.time()

print("语料构造花费时间：",end-start)