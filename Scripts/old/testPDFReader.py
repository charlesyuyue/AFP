# Try to use PyPDF2 to only extracts texts

import PyPDF2
filename = "C:/Users/William/Desktop/AFP/r/ruida2014.pdf"
pdf = PyPDF2.PdfFileReader(open(filename, "rb"))
for page in pdf.pages:
    str = page.extractText()
    content = str.replace("\n", " ")

    print(content.encode('gbk','ignore').decode('gbk','ignore'))
    #print (page.extractText())

#
# text_content = []
# foundTitle = 0
# ifInSection = 0
# for line in text.splitlines():
#     if ifInSection == 1:
#         if line.strip():
#             if "税项" in line:
#                 break
#             text_content.append(line)
#     else:
#         if line.strip():
#             if "会计政策" in line and "会计估计" in line:
#                 if foundTitle == 1 and ifInSection == 0:
#                     text_content.clear()
#                     foundTitle = 0
#                 foundTitle = 1
#                 text_content.append(line)
#             elif "遵循企业会计" in line:
#                 ifInSection = 1
# print(text_content)