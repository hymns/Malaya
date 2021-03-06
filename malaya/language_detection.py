import pickle
import os
from .text_functions import simple_textcleaning_language_detection
from .utils import download_file
from . import home

bow_pkl = home+'/bow-language-detection.pkl'
multinomial_pkl = home+'/multinomial-language-detection.pkl'

lang_labels = {0: 'OTHER',1: 'ENGLISH',2: 'INDONESIA',3: 'MALAY'}
MULTINOMIAL, BOW = None, None

if not os.path.isfile(bow_pkl):
    print('downloading pickled bag-of-word language detection')
    download_file("http://s3-ap-southeast-1.amazonaws.com/huseinhouse-storage/bow-language-detection.pkl", bow_pkl)
if not os.path.isfile(multinomial_pkl):
    print('downloading pickled multinomial language detection model')
    download_file("https://s3-ap-southeast-1.amazonaws.com/huseinhouse-storage/multinomial-language-detection.pkl", multinomial_pkl)
with open(bow_pkl,'rb') as fopen:
    BOW = pickle.load(fopen)
with open(multinomial_pkl,'rb') as fopen:
    MULTINOMIAL = pickle.load(fopen)

def get_language_labels():
    return lang_labels

def detect_language(string, get_proba=False):
    assert (isinstance(string, str)), "input must be a string"
    global MULTINOMIAL, BOW
    strings = [simple_textcleaning_language_detection(string)]
    if get_proba:
        result = MULTINOMIAL.predict_proba(BOW.transform(strings))[0]
        return {lang_labels[i]:result[i] for i in range(len(result))}
    else:
        return lang_labels[MULTINOMIAL.predict(BOW.transform(strings))[0]]

def detect_languages(strings, get_proba=False):
    assert (isinstance(strings, list) and isinstance(strings[0], str)), "input must be list of strings"
    global MULTINOMIAL, BOW
    strings = [simple_textcleaning_language_detection(string) for string in strings]
    if get_proba:
        results = MULTINOMIAL.predict_proba(BOW.transform(strings))
        outputs = []
        for result in results:
            outputs.append({lang_labels[i]:result[i] for i in range(len(result))})
        return outputs
    else:
        return [lang_labels[result] for result in MULTINOMIAL.predict(BOW.transform(strings))]
