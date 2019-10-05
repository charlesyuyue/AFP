'''
Module to calculate similarity scores from two csv files
'''
import csv
import math

def read_csv_into_dict(csv_path):
    '''
    Read the frequency count csv files into a dictionary
    '''
    res_dict = {}
    with open(csv_path, encoding='utf-8-sig') as csv_path:
        csv_reader = csv.reader(csv_path)
        for row in csv_reader:
            if row:
                res_dict[row[0]] = int(row[1])
    return res_dict

def calc_cos_similarity(dict_1, dict_2):
    '''
    Merge and calculate VSM score
    '''

    # Get all unique words from two dictionaries
    unique_word_set = set()
    for word in dict_1.keys():
        unique_word_set.add(word)
    for word in dict_2.keys():
        unique_word_set.add(word)
    unique_word_list = list(unique_word_set)
    unique_word_index_dict = {k: v for v, k in enumerate(unique_word_list)}

    # Initialize vectors
    v1 = [0] * len(unique_word_list)
    v2 = [0] * len(unique_word_list)

    # count Vector 1
    for word, freq in dict_1.items():
        v1[unique_word_index_dict[word]] = freq

    # count Vector 2
    for word, freq in dict_2.items():
        v2[unique_word_index_dict[word]] = freq

    # Calculate the dot product
    dot_product = 0
    i = 0
    while i < len(unique_word_list):
        dot_product = dot_product + v1[i] * v2[i]
        i = i + 1

    # Calculate the mods of two vectors
    i = 0
    mod_first_vector = 0
    while i < len(unique_word_list):
        mod_first_vector = mod_first_vector + v1[i] * v1[i]
        i = i + 1

    i = 0
    mod_second_vector = 0
    while i < len(unique_word_list):
        mod_second_vector = mod_second_vector + v2[i] * v2[i]
        i = i + 1

    score = float(dot_product) / (math.sqrt(mod_first_vector) * math.sqrt(mod_second_vector))
    return score

# Testing
s = calc_cos_similarity(read_csv_into_dict(r"F:\AFP\data\ChinaAnnualReports\2007\acct_policy\000001.SZ.csv"),
                    read_csv_into_dict(r"F:\AFP\data\ChinaAnnualReports\2007\acct_policy\000001.SZ.csv"))
print(s)