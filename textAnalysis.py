# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 11:10:47 2023

@author: Hp
"""
#pip install nltk
import os
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize
import re
import string
#nltk.download('punkt') 
# =============================================================================
# 
# with open(r'E:\Black COffer\Data_extracted\123.0.txt', 'r') as file:
#     text = file.read()
# 
# # cleaning using stop words list
# 
# with open(r"E:\Black COffer\20211030 Test Assignment\StopWords\StopWords_Names.txt") as st_word_file:
#     stop_words = st_word_file.read()
#     
# stop_words = stop_words.split("\n")
# 
# words = text.split()
# 
# clean_words = [i for i in words if not i in stop_words]
# =============================================================================


with open(r'E:\Black COffer\Data_extracted\123.0.txt', 'r') as file:
    text_file = file.read()
    
st_file_1 = r"E:\Black COffer\20211030 Test Assignment\StopWords\StopWords_Auditor.txt"
st_file_2 = r"E:\Black COffer\20211030 Test Assignment\StopWords\StopWords_Currencies.txt"
st_file_3 = r"E:\Black COffer\20211030 Test Assignment\StopWords\StopWords_DatesandNumbers.txt"
st_file_4 = r"E:\Black COffer\20211030 Test Assignment\StopWords\StopWords_Generic.txt"
st_file_5 = r"E:\Black COffer\20211030 Test Assignment\StopWords\StopWords_GenericLong.txt"
st_file_6 = r"E:\Black COffer\20211030 Test Assignment\StopWords\StopWords_Geographic.txt"
st_file_7 = r"E:\Black COffer\20211030 Test Assignment\StopWords\StopWords_Names.txt"

st_files = [st_file_1, st_file_2, st_file_3, st_file_4, st_file_5, st_file_6, st_file_7]


with open(r"E:\Black COffer\20211030 Test Assignment\MasterDictionary\negative-words.txt", 'r') as file:
    neg_words = file.read()

with open(r"E:\Black COffer\20211030 Test Assignment\MasterDictionary\positive-words.txt", 'r') as file:
    pos_words = file.read()
    
def st_words_clean(st_file, input_text):
    with open(st_file, 'r') as st_word_file:
        stop_words = st_word_file.read()
        
    stop_words = stop_words.split("\n")
    punctuations = set(string.punctuation)
    words = input_text.split()

    clean_words = [i for i in words if not i in stop_words and i not in punctuations]
    cleaned_text = ' '.join(clean_words)
    return cleaned_text


# Function to count vowels in a word
def count_vowels(word):
    vowels = "AEIOUaeiou"
    return sum(1 for char in word if char in vowels)

# Function to count syllables in a word
def count_syllables(word):
    # Handling exceptions for words ending with "es" or "ed"
    if word.endswith(('es', 'ed')):
        return count_vowels(word[:-2])
    return count_vowels(word)


scores_df = pd.DataFrame(columns=columns)
scores_list = []

directory = "Data_extracted_2"

for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory, filename)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            text_file = file.read()
        input_text = text_file
        
# stop words clean # Punctuation clean
        for st_file in st_files:
            cleaned_text = st_words_clean(st_file, input_text)  
            input_text = cleaned_text

        tokens = word_tokenize(input_text)   
        sentence = sent_tokenize((input_text))###
        total_characters = sum(len(i) for i in tokens) ###
        
        # Find matches using the pattern (case-insensitive)
        personal_pronouns = r'\b(?:I|we|my|ours|us)\b'
        matches = re.findall(personal_pronouns, input_text)
        
        matches = [i for i in matches if i.lower() != "us"]  
        
        positive_score = sum(1 for i in tokens if i.lower() in pos_words)
        negative_score = sum(1 for i in tokens if i.lower() in neg_words)
        polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
        subjectivity_score = (positive_score + negative_score) / (len(tokens) + 0.000001)
        
         ###
        word_count = len(tokens)
############        # Calculate the syllable count for each word  ###############
        syllable_counts = [count_syllables(word) for word in tokens]
        Total_syllable = sum(syllable_counts)
############        # Calculate the count of complex words ###############
        complex_word_count = sum(1 for word in words if count_syllables(word) > 2)
######## Analysis of Readibility                
        avg_sentence_length = len(tokens) / len(sentence)
        complex_word_perc = complex_word_count / word_count 
        
        Fog_Index = 0.4 * (avg_sentence_length + complex_word_perc)
            
        personal_pronouns = len(matches)
# AVG WORD LENGTH         
        average_word_length = total_characters / len(tokens) ####
        
        
        scores_list.append({
            'File': filename,
            'Positive Score': positive_score,
            'Negative Score': negative_score,
            'Polarity Score': polarity_score,
            'Subjectivity Score': subjectivity_score,
            'AVG SENTENCE LENGTH': avg_sentence_length,####
            'Average Number of Words Per Sentence': avg_sentence_length,####
            'Word count': word_count,
            
            'AVG WORD LENGTH': average_word_length, ###
            'syllable_counts' :  Total_syllable,
            'complex_word_count' : complex_word_count,
            'complex_word_percentage' : complex_word_perc,
            'Fog Index' :  Fog_Index,
            'personal_pronouns' : personal_pronouns,
        })

scores_df = pd.DataFrame(scores_list)

print(scores_df)

# Calculate the syllable count for each wordwor




# =============================================================================
# 
# clean3 = st_words_clean(st_file_1, input_text)
# clean4 = st_words_clean(st_file_2, clean3)
# 
# st_words_clean(st_file1, cleaned_text)
# 
# with open(st_file, 'r') as st_word_file:
#     stop_words = st_word_file.read()
#     
# stop_words = stop_words.split("\n")
# 
# words = text_file.split()
# 
# clean_words = [i for i in words if not i in stop_words]
# clean1 = ' '.join(clean_words)
# 
# =============================================================================
