from __future__ import print_function
from keras.layers import Dense, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Conv1D, MaxPooling1D

from keras.models import Sequential
import keras
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import numpy as np


def main():
    set, classes, sequenceList = ParseFile(R'E:\EDocuments\school\DataScience\datasets\train_set.fasta')
    x_train, x_test, y_train, y_test = train_test_split(set, classes, test_size=0.2, random_state=42)

    model = create_model()
    doedeshit(model, x_train, y_train, x_test, y_test)


def ParseFile(path):
    """Method to parse the file containing the signal peptides.
    arg1: path to file
    return1: array containing for each amino acid the by the label encoder assigned value + the hydrophylic value
        e.g. 'MAR' might be [1, 1.9, 2, 1.8, 3, -4.5]
    return2: list indicating which peptides are signal peptides"""
    sequenceList = ReadFasta(path)
    le = preprocessing.LabelEncoder()
    hydrophylicDict = {'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5, 'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5, 'L': 3.8,
                       'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6, 'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2}

    le.fit(list(hydrophylicDict.keys()))
    aminoAcidList, classList = [], []

    for seq in sequenceList:
        if len(seq.sequence) == 70:
            tmpAminoList = np.array(le.transform(split(seq.sequence)))
            tmpHydrophylicList = [hydrophylicDict[aa] for aa in list(seq.sequence)]
            seqArray = []
            for i in range(0, len(seq.sequence)):
                seqArray.extend([[tmpAminoList[i]], [tmpHydrophylicList[i]]])
            aminoAcidList.append([seqArray[x:x + 14] for x in range(0, len(seqArray), 14)])
            # aminoAcidList.append([seqArray])
            classList.append(int(seq.signal))
    array = np.array(aminoAcidList)
    return array, classList, sequenceList


def ReadFasta(path):
    """method for parsing a fasta file to a list of sequence objects.
    arg1: path to the fasta file
    return1: list of sequence objects"""
    sequenceList = []
    with open(path) as f:
        for line in f:
            if line.startswith('>'):
                sequenceList.append(
                    Sequence(line.strip(), f.readline().strip(), f.readline().strip()))
    return sequenceList


def SetModel():
    # input_shape = (1, 140, 1)
    input_shape = (10, 14, 1)
    num_classes = 1

    model = Sequential()
    model.add(Conv2D(32, kernel_size=(1, 1), strides=(1, 1),
                     activation='relu',
                     input_shape=input_shape))
    # model.add(MaxPooling2D(pool_size=(1, 1), strides=(2, 2), input_shape=input_shape))
    # model.add(Conv2D(64, (5, 5), activation='relu'))
    # model.add(MaxPooling2D(pool_size=(1, 1)))
    # model.add(Flatten())
    # model.add(Dense(1000, activation='relu'))
    # model.add(Dense(num_classes, activation='softmax'))
    # model.add(MaxPooling1D(pool_size=1, strides=1))
    # model.add(Dense(num_classes, activation='softmax'))

    # model.add(Dense(1, activation="softmax", input_shape=input_shape))  # als 1 niet werkt 140 proberen
    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adam(),
                  metrics=['accuracy'])
    return model


def create_model(time_window_size, metric):
    model = Sequential()

    model.add(Conv1D(filters=256, kernel_size=5, padding='same', activation='relu',
                     input_shape=(time_window_size, 1)))
    model.add(MaxPooling1D(pool_size=4))

    model.add(LSTM(64))

    model.add(Dense(units=time_window_size, activation='linear'))

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=[metric])

    # model.compile(optimizer='adam', loss='mean_squared_error', metrics=[metric])
    # model.compile(optimizer="sgd", loss="mse", metrics=[metric])

    print(model.summary())
    return model


def doedeshit(model, x_train, y_train, x_test, y_test):

    history = AccuracyHistory()
    print(x_train)
    print(y_train)
    print(len(x_train))
    print(len(y_train))
    print(len(x_train[0]))
    print(len(x_train[0][0]))

    model.fit(x_train, np.array(y_train),
              batch_size=1,
              epochs=10,
              verbose=1,
              validation_data=(x_test, y_test),
              callbacks=[history]
              )
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])


def split(seq):
    """Method for returning a list of chars that make up a string
    arg1: string to split up in chars
    return1: list of chars"""
    return [char for char in seq]


class AccuracyHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.acc = []

    def on_epoch_end(self, batch, logs={}):
        self.acc.append(logs.get('acc'))


class Sequence:
    """Object representing a DNA sequence with multiple attributes"""

    def __init__(self, header, sequence, localization):
        """constructor for the Sequence class object.
        arg1: header of the sequence
        arg2: the actual sequence
        arg3: localization of the sequence"""
        self.header = header
        self.sequence = sequence
        self.localization = localization
        self.aminoAcidList = []

        if '|NO_SP|' in header:
            self.signal = False
        else:
            self.signal = True


if __name__ == '__main__':
    main()
