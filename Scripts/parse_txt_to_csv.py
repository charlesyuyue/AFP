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
    f_stop = open(r"stopwords.txt", encoding="utf-8-sig")
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
    # sorted_freq_dict = sorted(freq_dict.items(), key=lambda asd: asd[1], reverse=True)
    return freq_dict

def extract_desired_txt_as_string(txt_file, section_string):
    '''
        Given a text file, read in, remove all empty lines and return as one line of string
    '''
    # check if file exist
    if not os.path.exists(txt_file):
        print(txt_file, "not exists. Please check")
        return ""

    # Initialize
    extracted_text = ""
    if_to_be_recorded = False
    starting_string = RULE_DICT[section_string]["starting_string"]
    ending_string = RULE_DICT[section_string]["ending_string"]

    with open(txt_file, 'r', encoding='utf-8-sig') as text_file:
        for line in text_file.readlines():
            if line.strip():
                if not if_to_be_recorded:
                    # if have not started to record, check if it is the starting string
                    if starting_string in line:
                        if_to_be_recorded = True
                        extracted_text += line.replace('\n','')
                else:
                    # if in the process of recording, check if it is the ending string
                    if ending_string in line:
                        break
                    else:
                        # record the current line
                        extracted_text += line.replace('\n', '')

    # Remove non chinese characters
    print(extracted_text)
    res_string = filter_out_non_chinese_characters(extracted_text)
    return res_string

def output_dict_as_csv(output_dict, file_path, section_string):
    """
        Helper function to output dictionary of word counts to a csv
    """
    #
    output_dir_path = os.path.join(os.path.dirname(file_path),
                                   section_string)
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
    output_filename = os.path.basename(file_path).replace(".txt","") + ".csv"
    output_csv_path = os.path.join(output_dir_path,
                                   output_filename)

    with open(output_csv_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in output_dict.items():
            writer.writerow([key, value])

def read_in_parsing_rule_definition():
    '''
        Read parsing rules into a dictionary of dictionary
    '''
    rule_dict = {}
    with open("parsing_rules.csv", encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader, None)  # skip the headers:
        for row in csv_reader:
            rule_dict[row[0]] = {}
            rule_dict[row[0]]["starting_string"] = row[1]
            rule_dict[row[0]]["ending_string"] = row[2]
    return rule_dict


def parse(file_path, section_string):
    '''
        Parse the given text file, look for the desired section,
        and output word count as a csv file
    '''
    # Read the text file into one string
    txt_string = extract_desired_txt_as_string(file_path, section_string)

    # Extract the desired text section
    # txt_string = extract_desired_text_section(txt_string, section_string)
    # print(txt_string) # For testing purposes

    # Segregated into a list and remove stop words
    seg_list = remove_stop_words(jieba.cut(txt_string))

    # Convert the list into a dictionary
    word_dict = count_word_frequency_as_dict(seg_list)

    # Output the dictionary as a csv file
    output_dict_as_csv(word_dict, file_path, section_string)

if __name__ == "__main__":
    # Read in rule definition csv
    RULE_DICT = read_in_parsing_rule_definition()

    # for each file name, parse and output
    f = r"F:\AFP\data\ChinaAnnualReports\2007\000768.SZ.txt"
    section_string = "acct_policy"
    parse(f, section_string)
