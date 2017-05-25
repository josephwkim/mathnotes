import logging
import csv
import os
import random
import scipy.ndimage
from PIL import Image, ImageDraw
import sys
import numpy as np


logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO,
                    stream=sys.stdout)

__version__ = "v2.0"


def _load_csv(filepath, delimiter=',', quotechar="'"):
    """
    Load a CSV file.

    Parameters
    ----------
    filepath : str
        Path to a CSV file
    delimiter : str, optional
    quotechar : str, optional

    Returns
    -------
    list of dicts : Each line of the CSV file is one element of the list.
    """
    data = []
    csv_dir = os.path.dirname(filepath)
    with open(filepath, 'rt') as csvfile:
        reader = csv.DictReader(csvfile,
                                delimiter=delimiter,
                                quotechar=quotechar)
        for row in reader:
            if 'path' in row:
                row['path'] = os.path.abspath(os.path.join(csv_dir,
                                                           row['path']))
            data.append(row)
    return data


def generate_index(csv_filepath):
    """
    Generate an index 0...k for the k labels.

    Parameters
    ----------
    csv_filepath : str
        Path to 'test.csv' or 'train.csv'

    Returns
    -------
    dict : Maps a symbol_id as in test.csv and
        train.csv to an integer in 0...k, where k is the total
        number of unique labels.
    """
    symbol_id2index = {}
    data = _load_csv(csv_filepath)
    i = 0
    for item in data:
        if item['symbol_id'] not in symbol_id2index:
            symbol_id2index[item['symbol_id']] = i
            i += 1

    return symbol_id2index


def load_images(csv_filepath, symbol_id2index, one_hot=True, flatten=False):
    """
    Load the images into a 4D uint8 numpy array [index, y, x, depth].

    Parameters
    ----------
    csv_filepath : str
        'test.csv' or 'train.csv'
    symbol_id2index : dict
        Dictionary generated by generate_index
    one_hot : bool, optional
        Make label vector as 1-hot encoding, otherwise index
    flatten : bool, optional
        Flatten feature vector

    Returns
    -------
    images, labels : Images is a 4D uint8 numpy array [index, y, x, depth]
                     and labels is a 2D uint8 numpy array [index][1-hot enc].
    """
    WIDTH, HEIGHT = 32, 32
    dataset_path = os.path.dirname(csv_filepath)  # Main directory of HASY
    data = _load_csv(csv_filepath)
    if flatten:
        images = np.zeros((len(data), WIDTH * HEIGHT))
    else:
        images = np.zeros((len(data), WIDTH, HEIGHT, 1))
    labels = []
    for i, data_item in enumerate(data):
        fname = os.path.join(dataset_path, data_item['path'])
        if flatten:
            img = scipy.ndimage.imread(fname, flatten=False, mode='L')
            images[i, :] = img.flatten()
        else:
            images[i, :, :, 0] = scipy.ndimage.imread(fname,
                                                      flatten=False,
                                                      mode='L')
        label = symbol_id2index[data_item['symbol_id']]
        labels.append(label)
    data = images, np.array(labels)
    if one_hot:
        data = (data[0], np.eye(len(symbol_id2index))[data[1]])
    return data

###All code ABOVE this line was taken from the dataset and is not original###
###The dataset and any code above this line can be attributed to Martin Thoma
###and the sponsors of the HASYv2 dataset.


def loadData(): #returns tuple of (train,test)
    #train contains a 3D array, where each element of the first index is a 1X1024 list representing the image values
    #the matrix of 0s and 1s is an encoding of which index it is, all 0's except the correct index which is a 1
    #test is of identical format.
    trainpath = "C:/Users/Joe/Documents/15-112/Term Project/HASYv2/classification-task/fold-1/train2.csv"
    testpath = "C:/Users/Joe/Documents/15-112/Term Project/HASYv2/classification-task/fold-1/test2.csv"
    trainS2I = generate_index(trainpath)
    testS2I = generate_index(testpath)
    difference = set(trainS2I)-set(testS2I)
    train = load_images(trainpath,trainS2I,flatten=True)
    test = load_images(testpath,testS2I,flatten=True)
    return train,test

def resizeData(): #returns a list of len 4 with data reshaped into correct
    #formats
    trainX=loadData()[0][0]
    trainY=loadData()[0][1]
    testX=loadData()[1][0]
    testY=loadData()[1][1]
    for a in trainX:
        a=np.reshape(a,(1024,1))
    print ("done with trainX")
    for b in trainY:
        b=np.reshape(b,(369,1))
    print ("done with trainY")
    for c in testX:
        c=np.reshape(c,(1024,1))
    print ("done with testX")
    for d in testY:
        d=np.reshape(d,(369,1))
    print ("done with testY")
    return [trainX,trainY,testX,testY]







