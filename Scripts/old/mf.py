import edgar
import pandas as pd
import io
import re

states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida",
          "Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
          "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada",
          "New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma",
          "Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont",
          "Virginia","Washington","West Virginia","Wisconsin","Wyoming"]


def extractRelevantText(doc):
    output = []
    fyear = -1
    res = ""
    buffer = ""
    recording = 0
    for line in doc.splitlines():
        if line.strip():
            if fyear is -1:
                if "For the fiscal year ended" in line:
                    # Get the page number of the "financial report" section
                    y = re.sub("[^0-9]", "", line)  # Remove non-numeric characters
                    fyear = int(y[-4:])

            if "Item 1A." in line:
                recording = 0
            elif "Item 3." in line:
                recording = 0
            elif "Item 7A." in line:
                recording = 0

            if "Item 1." in line:
                recording = 1
            elif "Item 1B." in line:
                recording = 1
            elif "Item 2." in line:
                recording = 1
            elif "Item 6." in line:
                recording = 1
            elif "Item 7." in line:
                recording = 1

            if recording is 1:
                buffer += line + " "
            else:
                res += buffer
                buffer = ""
    output.append(fyear)
    output.append(res)
    return output


def extractYear(doc):
    fyear = -1
    for line in doc.splitlines():
        if line.strip():
            if "For the fiscal year ended" in line:
                # Get the page number of the "financial report" section
                y = re.sub("[^0-9]", "", line)  # Remove non-numeric characters
                fyear = int(y[-4:])
                return fyear
    return fyear

def countStatesApperance(doc):
    table = {}
    for word in doc.split():
        if word in states:
            table[word] = 1
    return len(table)
ed = edgar.Edgar()


c = "785814"
c = c.zfill(10)

#n = ed.getCompanyNameByCik(c)
company = edgar.Company("INTEGRATED HEALTH SVCS INC", c)
tree = company.getAllFilings(filingType="10-K")
docs = edgar.getDocuments(tree, noOfDocuments=30)
with io.open("C:/Users/William/Desktop/Output.txt", "w", encoding="utf-8") as f:
    f.write(docs[0])
if len(docs) > 0:
    print(countStatesApperance( docs[0]  ))
    print(extractYear(docs[0]))


# For each 10-K
# determine which fiscal year it is



#with io.open("C:/Users/William/Desktop/Output.txt", "w", encoding="utf-8") as f:
#    f.write(docs[0])

# count the number of states


# read in name - cik look up table
# comp_name_cik = pd.read_csv("C:/Users/William/Desktop/namecik.csv")
# comp_name_cik = comp_name_cik[pd.notnull(comp_name_cik['cik'])]

# For each company in the look up table
# for row in comp_name_cik.iterrows():
#     name = row[1][6]
#     cik = str(int(row[1][7]))
#
#     # Retrieve all 10-K from EDGAR
#     company = edgar.Company(name, cik)
#     tree = company.getAllFilings(filingType="10-K")
#     docs = edgar.getDocuments(tree, noOfDocuments=30)
#
#     # For each 10-K
#     # determine which fiscal year it is
#
#     # count the number of states
#
