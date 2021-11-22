import re
import os

from gensim.models import Word2Vec

from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.parsing.preprocessing import STOPWORDS

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from BlockParser import infer_titles
import fitz

from sentenceRanker import summarize

def unique(list1):
 
    # intilize a null list
    unique_list = []
     
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list and x!='':
            unique_list.append(x)
    # print list
    return unique_list


def get_titles(doc_path='GerrishBlei2010.pdf'):
    titles=[]
    fp = open(doc_path, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    # Get the outlines of the document if they exist, otherwise infer form fonts.

    try:
        outlines = document.get_outlines()

        for (level,title,dest,a,se) in outlines:

            titles.append(title)


    except:
        print("No outlines")
        titles = infer_titles(doc_path)
    return titles

def split(txt, seps):
    default_sep = seps[0]

    # we skip seps[0] because that's the default separator
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep)]

def denumerate_titles(titles):
    new_titles=[]
    for title in titles:
        title=title.replace("\t"," ")
        title = re.sub(r'\d', "", title).strip()
        new_titles.append(title)
        new_titles.append(title.upper())
    return new_titles
    


def get_blocks(doc_path,titles):
    doc = fitz.open(doc_path)
    myText=''
    for page in doc:
        myText=myText+page.getText("text")
    textBlocks=split(myText, titles)
    return textBlocks


    
def get_abstract_and_intro(textBlocks, corpus, first_doc):
    if len(my_blocks)>2:
        if "Abstract" in my_blocks[1]:
            intro=corpus+my_blocks[2].lstrip("01231456789")
        else:
            intro=corpus+my_blocks[1].lstrip("01231456789") + my_blocks[2].lstrip("01231456789")
                
    else:
        intro=corpus+my_blocks[1]

    #intro= re.sub(r"http\S+", "", intro)

    

    intro=intro.replace("-\n","")
    intro=intro.replace(" ,",",")
    intro=intro.replace("\n-","")
    intro=intro.replace("\n"," ")
    intro=re.sub("[\(\[].*?[\)\]]", "", intro)
    intro=re.sub("\S*@\S*\s?","@",intro)
    intro=intro.replace(" )","")
    intro=intro.replace(")","")
    intro=intro.replace("fig.","figure")
    intro=intro.replace("Fig.","figure")
    intro=intro.replace("et al.","")
    intro=intro.replace("-","")
    return intro

def get_all_body(textBlocks, corpus, first_doc):
    intro=""
    for block in textBlocks:
        intro=intro+block.lstrip("01231456789")

    intro=intro.replace("-\n","")
    intro=intro.replace(" ,",",")
    intro=intro.replace("\n-","")
    intro=intro.replace("\n"," ")
    intro=re.sub("[\(\[].*?[\)\]]", "", intro)
    intro=re.sub("\S*@\S*\s?","@",intro)
    intro=intro.replace(" )","")
    intro=intro.replace(")","")
    intro=intro.replace("fig.","figure")
    intro=intro.replace("Fig.","figure")
    intro=intro.replace("et al.","")
    intro=intro.replace("-","")
    return intro

def exclude_sentence(sentence, summary):
    if summary:
        excluders=["&","@","We ","Our ", " our ", " we ", "\t", "   ", "Keywords:", " figure", " fig ", " table", "Figure", " Fig ", "Table", "Conference"]
    else:
        excluders=["&","@", "\t", "   ", "Keywords:", " figure", " fig ", " table", "Figure", " Fig ", "Table", "Conference"]
    excluded=False
    for e in excluders:
        if  e in sentence:
            excluded = True
            break
    if len(sentence.split(" "))<2:
        excluded = True
    return excluded

def include_sentence(sentence, includers):
    sentence1=re.sub(pattern=r'[\!"#$%&\*+,-./:;<=>?@^`()~=]', 
                        repl='', 
                        string=sentence.strip()
                       )
    include=False
    for includer in includers:
        if includer in sentence1:
            include=True
            break
    return include
    

def tokenize_sentence(sentence):
    tokens=[]
    sentence=re.sub(pattern=r'[\!"#$%&\*+,-./:;<=>?@^`()~=]', 
                        repl='', 
                        string=sentence.strip()
                       )
    tokens=sentence.lower().split(" ")
    
    return tokens

def hasStopwords(sentence, stopwords):
    has=False
    for stopword in stopwords:
        spaced= " "+stopword + " "
        if spaced.lower() in sentence.lower():
            has=True
            break

    return has


print('Starting up...')
intro_corpus=""
full_corpus=""
pdf_path='Documents'

first_doc=True

for filename in os.listdir(pdf_path):
    if(".pdf") in filename:
        my_path=pdf_path+'/'+filename

        my_list=get_titles(my_path)
        my_list=denumerate_titles(my_list)

        my_blocks=get_blocks(my_path,my_list)

        intro_corpus=get_abstract_and_intro(my_blocks, intro_corpus, first_doc)
        full_corpus=get_all_body(my_blocks, full_corpus, first_doc)

        if first_doc:
            first_doc=False
    if first_doc:
        print("No documents found")

print('Corpus extracted')

#Building the vocab corpus
raw_lines=full_corpus.split(".")
corpus_sentences=[]

for line in raw_lines:
    if not exclude_sentence(line, False)and line.isascii():
        line1=line.replace("  "," ").lstrip("01231456789")
        corpus_sentences.append(tokenize_sentence(line1))
    
print (corpus_sentences[1][1])

#Building the candidate for summarization text

raw_lines=intro_corpus.split(".")

summary_text=""

print('Summary candidate extracted')

key_words=["gan", "vision", "computer","imagetoimage"]
corpus_sentences.append(key_words)
corpus_sentences.append(key_words)

model = Word2Vec(corpus_sentences, min_count=2, seed=1, workers=1)
model.train(corpus_sentences, total_examples=model.corpus_count, epochs=10)

print('Word2Vec built')

model.wv.save_word2vec_format('custom_model.txt', binary=False)

similar=[]

all_stopwords = STOPWORDS


for word in key_words:
    top10=model.wv.most_similar(positive=[word], topn=6)
    for entry in top10:
        if entry[0] not in STOPWORDS:
            similar.append(entry[0])

similar=unique(similar+key_words)

abridged_text=""

for line in raw_lines:
    if not exclude_sentence(line, True)and line.isascii() and include_sentence(line, similar) and hasStopwords(line, all_stopwords):
        line1=line.replace("  "," ").strip().lstrip("01231456789")
        abridged_text=abridged_text+line1+". "

text_file = open("MyCorpus.txt", "w", encoding="utf-8")
text_file.write(abridged_text)
text_file.close()

print('Done.')

summary=summarize("MyCorpus.txt",5) #second argument is desired number of sentences
print (summary)

