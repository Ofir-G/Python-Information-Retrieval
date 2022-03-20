from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import snowball
from nltk.stem import WordNetLemmatizer
import collections
from collections import defaultdict
import nltk
import string
from collections import Counter

from inv_index import InvIndex


def main():
    my_file = open("d1.txt", "r")
    docfile = my_file.read()
    docs_list = docfile.replace('\n', ' ').split(".")

    my_file = open("d2.txt", "r")
    docs_list.append(my_file.read())

    my_file = open("d3.txt", "r")
    docs_list.append(my_file.read())

    my_file = open("d4.txt", "r")
    docs_list.append(my_file.read())

    inverted_index = InvIndex().IndexConstuct(docs_list)

    print('Enter your query:')
    query = input()

    final_match = InvIndex().process_and_search(query, inverted_index)

    if not final_match:
        print("No matches were found.")
    else:
        print("Found in Docs ID: ")
        for docid in final_match:
            print(str(docid))


main()
