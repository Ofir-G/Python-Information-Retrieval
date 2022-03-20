from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import snowball
from nltk.stem import WordNetLemmatizer
from collections import Counter
from collections import defaultdict
import nltk
import string


class InvIndex:

    def __init__(self):
        self.inv = {}

    def IndexConstuct(self, docs):

        stwords = set(stopwords.words('english'))
        wordnet_lemmatizer = WordNetLemmatizer()

        inverted_index = {}

        for docid, doc in enumerate(docs):
            trans = str.maketrans('', '', string.punctuation)
            doc = doc.translate(trans)
            for sent in sent_tokenize(doc):
                word_tokenizes = word_tokenize(sent)
                for i, word in enumerate(word_tokenizes):
                    word_tokenizes[i] = word_tokenizes[i].lower()
                    word_tokenizes[i] = wordnet_lemmatizer.lemmatize(word_tokenizes[i])
                word_tokenizes = [word for word in word_tokenizes if word not in stwords]

                counter = Counter(word_tokenizes)
                for key in counter.keys():
                    if key in inverted_index:
                        inverted_index[key] += [[docid + 1, counter[key]]]
                    else:
                        inverted_index[key] = [[docid + 1, counter[key]]]

        return inverted_index

    def intersect(self, list, list2):
        i = 0
        j = 0
        answer = []
        while i < len(list) and j < len(list2):
            if list[i][0] == list2[j][0]:
                answer.append(list[i])
                i += 1
                j += 1
            elif list[i][0] < list2[j][0]:
                i += 1
            else:
                j += 1

        return answer

    def process_and_search(self, query, inverted_index):
        stwords = set(stopwords.words('english'))
        wordnet_lemmatizer = WordNetLemmatizer()

        merge_matches = []
        matched_documents = set()
        trans = str.maketrans('', '', string.punctuation)
        query = query.translate(trans)
        words = word_tokenize(query)
        for word in words:
            word_lower = word.lower()
            if word_lower not in stwords:
                word_stem = wordnet_lemmatizer.lemmatize(word_lower)
                if (word_stem in inverted_index):
                    match = inverted_index.get(word_stem)
                    merge_matches += [match]
                else:
                    merge_matches = []
                    break

        answer = []
        i = 0
        final_match = []

        if (len(merge_matches) > 1):
            answer = merge_matches[1]

            for match in merge_matches:
                answer = self.intersect(match, answer)

            for docid in answer:
                final_match.append(docid[0])

        else:
            answer = merge_matches

            for match in answer:
                for docid in match:
                    final_match.append(docid[0])

        return final_match
