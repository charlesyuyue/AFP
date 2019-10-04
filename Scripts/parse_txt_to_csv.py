'''
Module to parse a single txt file into a csv file, which contains words and frequencies
'''
import re
import os
import csv
import jieba

def filter_out_non_chinese_characters(text):
    '''
        Helper function to leave only Chinese characters in a string
    '''
    #context = context.decode("utf-8") # convert context from str to unicode
    filtrate = re.compile(u'[^\u4E00-\u9FA5]')  # non-Chinese unicode range
    text = filtrate.sub(r'', text)  # remove all non-Chinese characters
    #context = context.encode("utf-8")  # convert unicode back to str
    return text

def remove_stop_words(seg_list):
    '''
        Helper function to remove all stop words from a list
    '''
    f_stop = open(r"F:\AFP\data\stopwords.txt", encoding="utf8")
    f_stop_text = f_stop.read()
    f_stop.close()
    stop_word_set = set(f_stop_text.split('\n'))

    cleared_list = []
    for word in seg_list:
        if len(word) > 1 and word not in stop_word_set:
            cleared_list.append(word)
    return cleared_list

def count_word_frequency_as_dict(word_list):
    '''
        Count Word Frequency in each document
    '''
    freq_dict = {}
    for word in word_list:
        if word != "" and word in freq_dict:
            freq_dict[word] = freq_dict[word] + 1
        elif word != "":
            freq_dict[word] = 1

    # Sort the frequencies from high to low
    sorted_freq_dict = sorted(freq_dict.items(), key=lambda asd: asd[1], reverse=True)
    return sorted_freq_dict

def read_txt_file_as_string(txt_file):
    '''
        Given a text file, read in, remove all empty lines and return as one line of string
    '''
    # check if file exist
    if not os.path.exists(txt_file):
        print(txt_file, "not exists. Please check")
        return ""

    with open(txt_file, 'r', encoding='utf8') as text_file:
        txt_string = text_file.readlines()
        res_string = ""
        for str in txt_string:
            if str.strip():
                res_string += str.replace('\n','')

        # Remove non chinese characters
        res_string = filter_out_non_chinese_characters(res_string)
        return res_string

def output_dict_as_csv(output_dict, file_path, section_string):
    """
        Helper function to output dictionary of word counts to a csv
    """
    #
    output_csv_path = ""
    with open(output_csv_path, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in output_dict.items():
            writer.writerow([key, value])

def parse_for_chapter_text(file_path):
    '''
        Parsing
    '''
    # Read the text file into one string
    txt_string = read_txt_file_as_string(file_path)
    # print(txt_string) # For testing purposes

    # Segregated into a list and remove stop words
    seg_list = remove_stop_words(jieba.cut(txt_string))

    # Convert the list into a dictionary
    word_dict = count_word_frequency_as_dict(seg_list)

    # Output the dictionary as a csv file
    output_dict_as_csv(word_dict, file_path)
    # test for github integreation
if __name__ == "__main__":
    # for each file name, parse and output
    f = r"F:\AFP\data\ChinaAnnualReports\2007\000001.SZ.txt"
    parse_for_chapter_text(f)
