# import necessary packages
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
import csv
from collections import OrderedDict

# opening trash.csv to find synonyms and hyponyms for original elements in trash.csv to create a more inclusive dataset

with open('trash.csv') as file_obj:
    # create reader object by passing the file 
    # object to reader Bucmethod
    reader_obj = csv.reader(file_obj)
    # creates container arrays
    addtocsv = [[]]
    synonyms1 = []
    hyponyms1 = []
    new_words = []
    # adds synonyms and hyponyms for words in original csv to 2d array (addtocsv)
    for row in reader_obj:
        for item in row[1:]:
            for syn in wn.synsets(item):
                for i in syn.lemmas():
                    synonyms1.append(i.name())
            syns = wn.synsets(item)
            for word in syns:
                for hyp in word.hyponyms():
                    for i in hyp.lemmas():
                        hyponyms1.append(i.name())
        new_words.extend(synonyms1)
        new_words.extend(hyponyms1)
        addtocsv.append(new_words)
        # clear for no duplicates 
        synonyms1.clear()
        hyponyms1.clear()
        new_words = []
    # creates new csv using words in 2d array and writes to it
    with open("new_trash.csv","w+") as my_csv:
        csvWriter = csv.writer(my_csv,delimiter=',')
        csvWriter.writerows(addtocsv)

