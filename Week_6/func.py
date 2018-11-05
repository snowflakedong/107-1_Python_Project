import chardet
import os.path
import glob
import sys
import re

def readdir(path, confidence=0.6):
    '''path : Specific Directory Path and Filename Extension.
    confidence[0.0-1.0] : Specific the detect encode confidence.
    File will be ignore if below this value.
    '''
    title = []
    documents = []
    unknown = 0
    for file in glob.glob(path):
        with open(file, 'rb') as f:
            text = f.read()
            encode = chardet.detect(text)
            if (encode['confidence'] < confidence):
                if(unknown == 0):
                    print('Unknown encode file :')
                unknown += 1
                print(file)
            else:
                title.append(os.path.splitext(os.path.basename(file))[0])
                documents.append(text.decode(encode['encoding']))
    print()
    if(unknown > 0):
        print('Number of unknown encoding files :', unknown)
        print('Number of read files :', len(documents))
    print('Number of files :', len(glob.glob(path)))
    return title, documents


def savetofile(path, data, confidence=0.6, default_encode = 'utf-8'):
    '''path : save data to file, specific file_path file_name, and file_extension.
    data : input data to save.
    confidence: detect encode confidence throttle
    default_encode: use default_encode if confidence lower than throttle
    '''
    if os.path.isfile(path):
        with open(path, 'rb') as f:
            text = f.read()
            encode = chardet.detect(text)
        if (encode['confidence'] < confidence):
            print('Unknown encode file! Use default encode: ', default_encode)
            original = list(map(str.strip, open(path, 'r+', encoding=default_encode).readlines()))
        else:
            original = list(map(str.strip, open(path, 'r+', encoding=encode['encoding']).readlines()))
    else:
        original = []
    original = sorted(original)
    with open(path, 'a+') as f:
        for i in range(len(data)):
            text = data[i]
            for i in text:
                if i not in original:
                    f.write(i + '\n')
    return
    
