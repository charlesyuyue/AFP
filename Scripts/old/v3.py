import io
import re
import jieba
import math
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.pdfpage import PDFPage


def extractAccountingPolicySection(path):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    extracted = ""
    foundTitle = 0
    ifInSection = 0

    pageCount = 1
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        if pageCount >= 40:
            interpreter.process_page(page)

            # Get all text in the current page
            data = retstr.getvalue()

            for line in data.splitlines():
                # if in the section of accounting disclosure
                if ifInSection == 1:
                    if line.strip():
                        # if reach section of taxation
                        if "税项" in line:
                            return extracted
                        extracted += line
                else:
                    if line.strip():
                        # if keywords "accounting policy" present
                        if "会计政策" in line and "会计估计" in line:
                            # if it is not in the target section, clear everything
                            if foundTitle == 1 and ifInSection == 0:
                                extracted = ""
                                foundTitle = 0
                            foundTitle = 1
                            extracted += line
                        # if found the subtitle of the target section
                        elif "遵循企业会计" in line:
                            ifInSection = 1
                            extracted += line
            data = ''
            retstr.truncate(0)
            retstr.seek(0)
        pageCount = pageCount + 1

    fp.close()
    device.close()
    retstr.close()
    return extracted


# Filter out  non-Chinese characters
def getChinese(context):
    #context = context.decode("utf-8") # convert context from str to unicode
    filtrate = re.compile(u'[^\u4E00-\u9FA5]')  # non-Chinese unicode range
    context = filtrate.sub(r'', context)  # remove all non-Chinese characters
    #context = context.encode("utf-8")  # convert unicode back to str
    return context

# Remove stopwords
def removeStopWords(seg_list):
    f_stop = open("C:/Users/William/Desktop/AFP/r/stopwords.txt", encoding="utf8")
    f_stop_text = f_stop.read()
    f_stop.close()
    f_stop_seg_list = f_stop_text.split('\n')
    clearedList = []
    for word in seg_list:
        if len(word) > 1 and word not in f_stop_seg_list:
            clearedList.append(word)
    return clearedList



# Count Word Frequency in each document
def CountKey(words):
    i = 0
    table = {}
    for word in words:
        if word != "" and word in table:
            num = table[word]
            table[word] = num + 1
        elif word != "":
            table[word] = 1

    # Sort the frequencies from high to low
    dic = sorted(table.items(), key=lambda asd: asd[1], reverse=True)
    return dic


# Merge and calculate VSM score
def MergeKeys(dic1, dic2):
    # Get all unique words
    arrayKey = []
    for i in range(len(dic1)):
        arrayKey.append(dic1[i][0])
    for i in range(len(dic2)):
        if dic2[i][0] not in arrayKey:
            arrayKey.append(dic2[i][0])

    v1 = [0] * len(arrayKey)
    v2 = [0] * len(arrayKey)

    # Count V1
    for i in range(len(dic1)):
        key = dic1[i][0]
        value = dic1[i][1]
        j = 0
        while j < len(arrayKey):
            if key == arrayKey[j]:
                v1[j] = value
                break
            else:
                j = j + 1
    # Count v2
    for i in range(len(dic2)):
        key = dic2[i][0]
        value = dic2[i][1]
        j = 0
        while j < len(arrayKey):
            if key == arrayKey[j]:
                v2[j] = value
                break
            else:
                j = j + 1

    # Calculate the dot product
    x = 0
    i = 0
    while i < len(arrayKey):
        x = x + v1[i] * v2[i]
        i = i + 1

    # Calculate the mods of two vectors
    i = 0
    sq1 = 0
    while i < len(arrayKey):
        sq1 = sq1 + v1[i] * v1[i]  # pow(a,2)
        i = i + 1

    i = 0
    sq2 = 0
    while i < len(arrayKey):
        sq2 = sq2 + v2[i] * v2[i]
        i = i + 1
    print(v1)
    print(v2)
    result = float(x) / (math.sqrt(sq1) * math.sqrt(sq2))
    return result


pdfDir = "C:/Users/William/Desktop/AFP/r/kangmei2016.pdf"
text = "we expect demand to increase"
seg_list = []
for word in text.split():
    seg_list.append(word)
#text = getChinese(text)
#seg_list = jieba.cut(text)
#seg_list = removeStopWords(seg_list)
dc1 = CountKey(seg_list)
print(dc1)

pdfDir = "C:/Users/William/Desktop/AFP/r/kangmei2018.pdf"
text = "we expect weakeness in sales"
seg_list = []
for word in text.split():
    seg_list.append(word)
#text = getChinese(text)
#seg_list = jieba.cut(text)
#seg_list = removeStopWords(seg_list)
dc2 = CountKey(seg_list)
print(dc2)
print(MergeKeys(dc1,dc2))
