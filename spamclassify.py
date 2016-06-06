#Daniel Morris
#Bayes Net Classifier
#Project 3

import math
import copy

def reademail(file):
    b = []
    listofemails = []
    f = open(file, 'r')
    line = f.read()
    a = line.split()
    for item in a:
        item = item.lower()
        b.append(item)
    i = 0
    j = 0
    while i<len(b):
        if (b[i] == '<subject>'):
            j = i + 1
            c = []
            while j<len(b) and b[j] != '</body>':
                if (b[j] == '</subject>' or b[j] == '<body>'):
                    j += 1
                else:
                    c.append(b[j])
                    j += 1
            listofemails.append(c)
        i += 1
    return listofemails

def trainfrequency(listofemails):
    frequency = {}
    for email in listofemails:
        email = set(email)
        for item in email:
            if item not in frequency:
                frequency[item] = 1
            else:
                frequency[item] += 1
    return(frequency)

def countemails(listofemails):
    emailcount = 0
    for email in listofemails:
        emailcount +=1
    return emailcount
    
def addzerotodict(totalvocab, vocab, vocab2):
    for item in totalvocab:
        if item not in vocab:
            vocab[item] = 0
        if item not in vocab2:
            vocab2[item] = 0
    return vocab, vocab2

def priors(emailsfile1, emailsfile2):
    spam = emailsfile1
    notspam = emailsfile2
    priors = spam / (spam +notspam)
    return priors

def invocab(listofemails, totalvocab):
    numberinvocab = 0
    for email in listofemails:
        email = set(email)
        for item in email:
            if item in totalvocab:
                numberinvocab += 1
    print((str(numberinvocab)) + "/" + str(len(totalvocab)))

def hmap(testemails, vocab, numberofemails, vocab2, numberofemails2, priorone, totalvocab, spam):
    i = 1
    wrongright = ''
    right = 0
    total = 0
    for email in testemails:
        numberinvocab = 0
        likelihood = 0
        likelihood2 = 0
        for item in totalvocab:
            if item in email and item in vocab:
                likelihood = math.log(((vocab[item] + 1)/(numberofemails + 2))) + likelihood

            else:
                likelihood = math.log((1 - ((vocab[item] + 1)/(numberofemails + 2)))) + likelihood
            if item in email and item in vocab2:
                likelihood2 = math.log(((vocab2[item] + 1)/(numberofemails2 + 2))) + likelihood2
                numberinvocab +=1

            else:
                likelihood2 = math.log((1 - ((vocab2[item] + 1)/(numberofemails2 + 2)))) + likelihood2
        
        probs = likelihood + math.log(priorone)
        probs2 = likelihood2 + math.log(1-priorone)
        
        if(spam == 1):
            if (probs < probs2):
                wrongright = ("ham wrong")
            else:
                wrongright = ("spam right")
                right +=1
        else:
            if (probs < probs2):
                wrongright = ("ham right")
                right +=1
            else:
                wrongright = ("spam wrong")
                
        print("TEST " + str(i) + " " + (str(numberinvocab)) + "/" + str(len(totalvocab)) + " " + "features true " + (str(round(probs,3)) + " " + str(round(probs2,3))) + " " + (wrongright))

        i += 1
        total +=1
    
    print(str(right) + " out of " + str(total) + " classified correctly.")
    return(right,total)

                  
def main():
    key = input("Enter 1 or 2.\n1 for small text files. 2 for large text files\n")
    if key == '1':
        vocab = reademail("train-spam-small.txt")
        vocab2 = reademail("train-ham-small.txt")
        emailsfile1 = countemails(vocab)
        emailsfile2 = countemails(vocab2)


        vocab = trainfrequency(vocab)
        vocab2 = trainfrequency(vocab2)
        totalvocab = dict(list(vocab.items()) + list(vocab2.items()))
        totalvocab = set(totalvocab)
        addzerotodict(totalvocab, vocab, vocab2)

        testemailsfile1 = reademail("test-spam-small.txt")
        testemailsfile2 = reademail("test-ham-small.txt")

        priorone = priors(emailsfile1, emailsfile2)
 
        x,y = hmap(testemailsfile1, vocab, emailsfile1, vocab2, emailsfile2, priorone, totalvocab, spam = 1)
        i, j = hmap(testemailsfile2, vocab, emailsfile1, vocab2, emailsfile2, priorone, totalvocab, spam = 0)
        print("Total: " + str(x+i) + "/" + str(y+j) + " emails classified correctly")
              
    else:
        vocab = reademail("train-spam.txt")
        vocab2 = reademail("train-ham.txt")
        emailsfile1 = countemails(vocab)
        emailsfile2 = countemails(vocab2)

        vocab = trainfrequency(vocab)
        vocab2 = trainfrequency(vocab2)
        totalvocab = dict(list(vocab.items()) + list(vocab2.items()))
        totalvocab = set(totalvocab)
        addzerotodict(totalvocab, vocab, vocab2)

        testemailsfile1 = reademail("test-spam.txt")
        testemailsfile2 = reademail("test-ham.txt")

        priorone = priors(emailsfile1, emailsfile2)

        x,y = hmap(testemailsfile1, vocab, emailsfile1, vocab2, emailsfile2, priorone, totalvocab, spam = 1)
        i, j = hmap(testemailsfile2, vocab, emailsfile1, vocab2, emailsfile2, priorone, totalvocab, spam = 0)
        print("Total: " + str(x+i) + "/" + str(y +j) + " emails classified correctly.")      
    
main ()

