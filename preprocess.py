# _*_ coding: utf-8 _*_
import re,os
import jieba


def load_into_sentence(file_name):
    """
    Read the whole file into one long sentence.
    :param file_name: the path indicating the file
    :return: the long sentence containing the content of the file
    """
    if not os.path.exists(file_name):
        raise ValueError("The file {0} does not exist!".format(file_name))
    with open(file_name,'r') as fp:
        lines = fp.readlines()
        return ''.join(lines).replace("\n",' ').decode('utf-8')


def replace_numbers(sentence):
    num_pattern = ur'[0123456789０１２３４５６７８９]+(\.|．)?[0123456789０１２３４５６７８９]*(%|％)?'
    return re.sub(num_pattern,u"NUM",sentence)


def replace_punctuations(sentence):
    punctuation = re.compile(u"[-~!@#$%^&*()_+`=\[\]\\\{\}\"|;':,./<>?·！@#￥%……&*（）——+【】、；‘：“”，。、《》？「『」』]")
    return re.sub(punctuation,u'',sentence)


def process_sogou_text(filename,output_file):
    """
    Process the sogou news:
        1. Extract the content between tags "<content>" and "</content>"
        2. Replace the numbers as word NUM
        3. Replace punctuations as empty strings
        4. Use jieba to do word segmentation
    :param filename:
    :return: Output a file in which each line contains one passage
    """
    sogou_file_sentence = load_into_sentence(filename)
    content_pattern = re.compile(ur'<content>(.*?)</content>')
    contents = re.findall(content_pattern, sogou_file_sentence)
    total = len(contents)
    with open(output_file,'w') as fw:
        print total
        for con in contents:
            total -= 1
            con = replace_numbers(con)
            con = replace_punctuations(con)
            con = u" ".join(jieba.cut(con))
            fw.write((con+u"\n").encode('utf-8'))
            if total%500 == 0:
                print total

def process_wiki_text(input_file,output_file):
    """
    Process the wiki file:
        1. Extract the content between tags "<doc....>" and "</doc>"
        2. Remove the repetitive words in tags like {zh-cn}
        3. Replace the numbers as word NUM
        4. Replace punctuations as empty srings
        5. Use jieba to do word segmentations
    :param input_file: wiki input file
    :param output_file: processed output file
    :return:
    """
    file_sentence = load_into_sentence(input_file)
    doc_pattern = re.compile(ur'<doc.*?id.*?url.*?title.*?>(.*?)</doc>')
    repetitive_words_pattern = re.compile(ur'-\{.*?zh.*?:([^;]*?)(;.*?)?\}-')
    docs = re.findall(doc_pattern,file_sentence)
    total = len(docs)
    with open(output_file,'w') as fw:
        print total
        for doc in  docs:
            total-=1
            doc = u' '.join(doc.split(u" ")[2:])
            doc = re.sub(repetitive_words_pattern,r'\1',doc)
            doc = replace_numbers(doc)
            doc = replace_punctuations(doc)
            doc = u" ".join(jieba.cut(doc))
            fw.write((doc+u"\n").encode('utf-8'))
            if total%500==0:
                print total

def _num_pattern_():
    num_pattern = ur'[0123456789０１２３４５６７８９]+(\.|．)?[0123456789０１２３４５６７８９]*(%|％)?'
    file_wiki00 = u"16"
    doc_matches = re.findall(num_pattern,file_wiki00)
    print "Total match number is {}".format(len(doc_matches))
    print (("The first ten matches are: "+"\n{}"*1+"\n").format(*doc_matches[:1]))
    print re.sub(num_pattern,"XX",file_wiki00)

def _doc_pattern_regular_expression_test():
    doc_pattern = re.compile(ur'<doc.*?id.*?url.*?title.*?>')
    file_wiki00 = load_into_sentence('wiki_00_jianti.dat')
    doc_matches = re.findall(doc_pattern,file_wiki00)
    print u"Total match number is {}".format(len(doc_matches))
    print (u"The first ten matches are: "+u"\n{}"*100+u"\n").format(*doc_matches[:100])

def _zh_pattern_regular_expression_test():
    zh_pattern = re.compile(ur'-\{.*?zh.*?:([^;]*?)(;.*?)?\}-')
    file_wiki00 = load_into_sentence('wiki_05_jianti.dat')
    doc_matches = re.findall(zh_pattern,file_wiki00)
    print u"Total match number is {}".format(len(doc_matches))
    for i in xrange(len(doc_matches)):
        if len(doc_matches[i][0])>200 or len(doc_matches[i][1])>200:
            print (u"1:{},2:{}\n".format(*doc_matches[i]))

def _sogou_content_pattern_test():
    content_pattern = re.compile(ur'<content>(.*?)</content>')
    sogou_file = load_into_sentence("sogou_news_jianti.dat")
    print "\n" in sogou_file
    contents = re.findall(content_pattern,sogou_file)
    print "match number is {}".format(len(contents))
    for c in contents[:100]:
        print c


def _wiki_doc_pattern_test():
    doc_pattern = re.compile(ur'<doc.*?id.*?url.*?title.*?>(.*?)</doc>') #DOTALL mode,
    wiki_file = load_into_sentence('wiki_00_jianti.dat')
    print "\n" in wiki_file
    docs = re.findall(doc_pattern,wiki_file)
    print "match number is {}".format(len(docs))
    for d in docs[:100]:
        print u' '.join(d.split(u" ")[2:])


if __name__ == "__main__":
    #_sogou_content_pattern_test()
    #_sogou_content_pattern_test()
    #process_sogou_text("sogou_news_jianti.dat","sogou_news_jianti_processed.dat")
    process_wiki_text("wiki_05_jianti.dat",'wiki_05_jianti_processed.dat')
    #_num_pattern_()