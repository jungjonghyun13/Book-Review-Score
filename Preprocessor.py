# Preprocessor
from gensim.models import Doc2Vec
from konlpy.tag import Twitter

twitter = Twitter()
'''
전처리기는 학습된 특성변환 모델을 불어들여 
입력된 문자열을 벡터로 변환한다. 
'''
class Preprocessor:
    def __init__(self):
        self.para = ''
        # load train data
        # doc2vec 에서 필요한 데이터 형식으로 변경
        self.doc_vectorizer = Doc2Vec.load('model_jh/리뷰모음_train_랄라.model')

    def setPara(self, para):
        print(para)
        # self.sentences = para.split('\n')
        self.sentences = para

    def transMor(self, doc):  # morpheme 형태소
        # norm, stem은 optional
        return ['/'.join(t) for t in twitter.pos(doc, norm=True, stem=True)]

    def transVector(self):
        self.Vec = [self.doc_vectorizer.infer_vector(self.transMor(d)) for d in self.sentences]
        return self.Vec