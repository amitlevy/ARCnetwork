import matplotlib.pyplot as plt
import json
import os
import numpy as np
import shutil
import tensorflow as tf
import tensorflow.keras as keras

np.random.seed(1)

directory = r"C:\Users\Jeffrey\Desktop\ARC-master\combined"

# copy matrix1 on top of matrix 2 in place
def copy_to(matrix1,matrix2):
    for i in range(len(matrix1)):
        for j in range(len(matrix1[0])):
            matrix2[i][j] = matrix1[i][j]

# getting black and white ARC questions
def get_data(directory):

    X = []
    Y = []
    
    for filename in os.listdir(directory):
        if "Copy" in filename:
            continue
        with open(directory+"\\"+filename, 'r') as f:
            current = [[],[]]
            X.append(current)
            data = json.load(f)
            examples = data['train']
            question = data['test']
            
            for example in examples:
                temp = np.ones((19,19))*0.5
                copy_to(example['input'],temp)
                X[-1][0].append(temp)
                temp = np.ones((19,19))*0.5
                copy_to(example['output'],temp)
                X[-1][0].append(temp)
            while len(X[-1][0]) < 20:
                X[-1][0].append(np.ones((19,19))*0.5)
            X[-1][0] = list(np.array(X[-1][0]).flatten())
            for example in question[:1]:
                temp = np.ones((19,19))*0.5
                copy_to(example['input'],temp)
                X[-1][1].append(temp)
                temp = np.ones((19,19))*0.5
                copy_to(example['output'],temp)
                temp = list(temp.flatten())
                Y.append(temp)
            X[-1][1] = list(np.array(X[-1][1]).flatten())
            X[-1][0] += X[-1][1]
            del X[-1][1]
            X[-1] = X[-1][0]
            examples_size = np.array(data['examples_size'])
            question_size = np.array(data['question_size'])
            examples_size.flatten()
            examples_size.resize(20)
            examples_size = [x/10 for x in examples_size]
            X[-1] = list(X[-1])
            Y[-1] = list(Y[-1])
            X[-1] += list(examples_size)
            X[-1] += list(question_size[0]/10)
            Y[-1] += list(question_size[1]/10)
            print(filename)
    return np.array(X),np.array(Y)




# creating the network
model = keras.models.Sequential()
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(500, activation=tf.nn.relu))
model.add(keras.layers.Dense(500, activation=tf.nn.relu)) 
model.add(keras.layers.Dense(500, activation=tf.nn.relu))
model.add(keras.layers.Dense(19*19+2, activation=tf.nn.sigmoid))

X,Y = get_data(directory)
Xeval,Yeval = get_data(eval_direct)

model.compile(optimizer = 'adam',
              loss = 'binary_crossentropy',
              #validation_split = 0.2,
              metrics = ['accuracy'])


model.fit(X,Y, epochs = 100, batch_size = 20)


# testing success rate according to competition goals
# show = True to display correct matches
def test(X,Y,model,show=False):
    assert len(X) == len(Y)
    correct = 0
    wrong = 0
    P = model.predict(X)
    for i in range(len(X)):
        currentp = list(P[i])[:-2]
        currenty = list(Y[i])[:]
        lines = int(currenty[-2]*10)
        rows = int(currenty[-1]*10)
        # converting to forms that can be checked for equivalency
        currenty = currenty[:-2]
        currenty = np.array(currenty)
        currentp = np.array(currentp)
        currenty.resize((19,19))
        currentp.resize((19,19))
        currentp = currentp.round()
        if sim(currentp,currenty,lines,rows,show):
            correct += 1
        else:
            wrong+=1

    print("correct",correct,"wrong",wrong)

# checks if two matrices are equivilent according to the competition rules
# show = True to display correct matches
def sim(matrix1,matrix2,m,n,show=False):
    for i in range(m):
        for j in range(n):
            if matrix1[i][j] != matrix2[i][j]:
                return False
    if show:
        plt.figure()
        plt.subplot(2,1,1)
        plt.imshow(matrix1)
        plt.subplot(2,1,2)
        plt.imshow(matrix2)
        plt.show()
    return True

 
test(X,Y,model)

