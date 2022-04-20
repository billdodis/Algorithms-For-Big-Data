import random
import time
import math
import hashlib
import numpy

# ======================================================================================================================
#                                                Vasileios Ntontis 3300
#                                             Zisis-Prokopios Talamagkas 3340
# ======================================================================================================================
#         SOS - you have to enter pip3 install pandas on cmd, so numpy can run and dont throw error! - SOS
# ======================================================================================================================
# At the start of the program, the user has to choose between the 2 files shown to him as a terminal 'menu'. After he
# has to choose how many documents we are going to read and get info from. Following, the user has to insert
# to our program the number of permutations he was for the usage of minhash algorithm and after the execution
# of the algorithm, we print the time spent and the signature matrix.
# Then, the user chooses between Jaccard and Signature similarities from a terminal 'menu' (a or b). For the jaccard
# similarity the program chooses 2 random documents and prints the Jaccard similarity
# (calculated with ordered lists and with sets) and the time passed for the execution to the user,
# so we can compare those to calculations. User has to insert the number of the closest neighbours of every document.
# At the end, user chooses again from a terminal 'menu' between LSH and Brude Force algorithms,
# in case of choosing LSH he has to insert how many rows will have every band for the algorithm ,the programs prints
# the average similarity and terminates. At the end the user has a choice to view his selected documents' neighbors.
#
#             *** DATA HAS TO BE IN THE SAME DIRECTORY WITH THIS PYTHON FILE SO IT CAN RUN PROPERLY ***
# ======================================================================================================================
import numpy as np

WordIDs = []
frozensets = []     # pinakas me ola ta frozensets
wordlist = []
myhashes = []   # pinakas me ola ta hash functions
nullwordlist = []   # support array for creating arxikou mhtrwou
listt = []  # Arxiko Mhtrwo
keylists = []   # array with the permutations
sig = []    # mhtrwo upografwn
klist = []
bvlist = []
bvlistdistances = []    # list
bvdicts = []
myneighborsdict = []
avgsimslist = []
lshdicts = []
arraytotuple = []
candidatekeys = []
candidatekeysone = []
candidatekeystwo = []
avgsim = 0
arrayforlsh = []


def DataToFrozensets(data, num):
    y = 1
    for i in range(3, len(data)):
        line = data[i].split()
        if int(line[0]) > y:
            array = frozenset(WordIDs)
            frozensets.append(array)
            WordIDs.clear()
            y = y + 1
        if int(line[0]) <= num:
            WordIDs.append(int(line[1]))
        else:
            break
    dictOfFrozensets = {frozensets[i]: i for i in range(len(frozensets))}
    # print('\nDictionary of frozensets as keys: ', dictOfFrozensets)
    return dictOfFrozensets


def MyReadDataRoutine(choice, numdoc):
    if choice == 'a':
        with open("DATA_1-docword.enron.txt", "r") as myfile:
            data = myfile.read().splitlines()
            # is an array which holds every line in a cell.data[line of file]=line
            dictionary = DataToFrozensets(data, numdoc)
            # print('\nDictionary of frozensets as keys: ', dictionary)

    elif choice == 'b':
        with open("DATA_2-docword.nips.txt", "r") as myfile:
            data = myfile.read().splitlines()
            dictionary = DataToFrozensets(data, numdoc)
            # print('\nDictionary of frozensets as keys: ', dictionary)

    return


def MyJacSimWithSets(doc1, doc2):        # |𝐴∩𝐵| / |𝐴|+|𝐵|−|𝐴∩𝐵|
    comparisons = 0
    intersectionCounter = 0
    start_time = time.time()
    len1 = len(frozensets[doc1-1])
    len2 = len(frozensets[doc2-1])
    for wordid1 in frozensets[doc1-1]:
        for wordid2 in frozensets[doc2-1]:
            comparisons += 1
            if wordid1 == wordid2:
                intersectionCounter += 1
    # end_time = time.time()
    # timee = end_time - end_time
    # print('With Sets - time: ', timee)
    print('comparisons', comparisons)
    Jacsim = intersectionCounter / (len1 + len2 - intersectionCounter)
    return (time.time() - start_time), Jacsim


def MyJacSimWithOrderedLists(doc1, doc2, flaag):        # |𝐴∩𝐵| / |𝐴|+|𝐵|−|𝐴∩𝐵|
    comparisons = 0
    fset1 = frozensets[doc1-1]
    L1 = sorted(fset1)
    # print(len(frozensets))
    # print(doc2)
    fset2 = frozensets[doc2-1]
    L2 = sorted(fset2)
    pos1 = 0;
    pos2 = 0;
    intersectionCounter = 0
    len1 = len(L1)
    len2 = len(L2)
    start_time = time.time()
    while pos1 < len1 and pos2 < len2:
        comparisons += 1
        if L1[pos1] == L2[pos2]:
            intersectionCounter += 1;
            pos1 += 1;
            pos2 += 1
        else:
            comparisons += 1
            if L1[pos1] < L2[pos2]:
                pos1 += 1
            else:
                pos2 += 1
    # end_time = time.time()
    # timee = end_time - end_time
    # print('With Ordered Lists - time: ', timee)
    # print("Intersection: ", intersectionCounter)
    # print('comparisons', comparisons)
    Jacsim = intersectionCounter / (len1 + len2 - intersectionCounter)
    if flaag == 1:
        return Jacsim
    return (time.time() - start_time), Jacsim


def MyMinHash(words, k):            # dont use list frozensets as an argument because we already can take it here.
    for z in range(k):
        h = create_random_hash_function()
        randomHash = {x: h(x) for x in range(words)}
        myHashKeysOrderedByValues = sorted(randomHash, key=randomHash.get)
        myHash = {myHashKeysOrderedByValues[x]: x for x in range(words)}
        myhashes.append(myHash)
    y = 0
    cccc = 0
    for i in range(len(frozensets)):
        y += 1
        for wordid in frozensets[i]:
            wordlist[wordid-1].append(y)
            listt[y-1][wordid-1] = 1
            cccc += 1
    counter = 0
    for x in myhashes:
        keylists.append([])
        keylist = list(x.keys())
        keylists[counter] = keylist
        counter += 1
    for i in range(words):                          # words einai o arithmos grammwn
        for y in range(len(sig)):                   # len(sig) einai o arithmos documents
            if listt[y][i] == 1:          # listtt[y][i] giati exume lista apo listes ara to (i,y) einai [y][i] se emas
                for z in range(k):              # k einai o arithmos metathesewn
                    if keylists[z][i] < sig[y][z]:      # keylists lista apo listes
                        # sthn thesi Z krataei lista me th sthlh metathesis gia thn z metathesi
                        sig[y][z] = keylists[z][i] + 1  # + 1 gia na exume swsto to anagnwristiko tou document
    # print(sig)
    return


def MySigSim(doc1, doc2, numpermutationsss, flaag):
    summ = 0
    start_time = time.time()
    for i in range(numpermutationsss):
        if sig[doc1-1][i] == sig[doc2-1][i]:
            summ += 1
    end_time = time.time() - start_time
    if flaag == 1:
        return summ/numpermutationsss
    print('SigSim --- %2f seconds ---' % end_time)
    return summ/numpermutationsss


def AvgSimWithBrudeForce(docsnum, numneighbors):
    prefinalavgsim = 0
    start_time = time.time()
    for i in range(docsnum):
        documentlist = []
        distances = []
        for y in range(docsnum):
            if i != y:
                if i > y:
                    documentlist.append(bvlist[y][i])
                    distances.append(bvlistdistances[y][i])
                else:
                    if userchose == 'a':
                        jcsm = MyJacSimWithOrderedLists(i+1, y+1, 1)
                    else:
                        jcsm = MySigSim(i+1, y+1, int(numpermutations), 1)
                    documentlist.append(jcsm)
                    dist = 1 - jcsm
                    distances.append(dist)
            else:
                documentlist.append(2)
                distances.append(0)
        bvlist.append(documentlist)
        bvlistdistances.append(distances)
        docdict = {ze: bvlistdistances[i][ze] for ze in range(len(bvlistdistances[i]))}
        sort_by_value = dict(sorted(docdict.items(), key=lambda item: item[1]))
        avgdistance = sum(sort_by_value.values())/(docsnum-1)
        lista = []
        docsidlist = []
        mindistances = []
        for y in range(numneighbors):
            docsidlist.append(numpy.inf)
            mindistances.append(1)
        sortedvalues = list(sort_by_value.values())
        for z in range(numneighbors):
            mindistances[z] = sortedvalues[z]
            docsidlist[z] = get_key(sortedvalues[z], docdict)
        for z in range(numneighbors):
            lista.append([docsidlist[z], mindistances[z]])
        neighbordict = {lista[za][0]: lista[za][1] for za in range(len(lista))}
        myneighborsdict.append(neighbordict)
        bvdicts.append(sort_by_value)
    for x in myneighborsdict:
        summm = sum(x.values())
        averagee = summm / len(x.keys())
        avgsimslist.append(averagee)
    for xi in avgsimslist:
        prefinalavgsim += xi
    end_time = time.time()
    timespent = end_time - start_time
    print('Brude Force algorithm --- %2f seconds ---' % timespent)
    return prefinalavgsim/docsnum


def get_key(val, diction):
    for key, value in diction.items():
         if val == value:
             return key


def LSH(rowsperband, docsnum, lshc, numneighbors):
    rows = rowsperband
    jacc = 0
    avgsim = 0
    if lshc == 0:
        avgsim = AvgSimWithBrudeForce(docsnum, numneighbors)
    canddocumentlist = []
    canddistances = []
    startingrowsperband = rows
    numbands = len(sig[0])/startingrowsperband
    numbands = math.floor(numbands)
    rowsperband = math.floor(rowsperband)

    # s = (1/numbands)**(1/rows)

    # hashf = create_random_hash_function()
    val = 0
    start_time = time.time()
    for i in range(numbands):
        banddict = {}
        for z in range(docsnum):
            for y in range(val, int(rowsperband)):
                arraytotuple.append(sig[z][y])
            tuplee = tuple(arraytotuple)
            hashvalue = hash(tuplee)        # kados
            banddict[z] = hashvalue
            arraytotuple.clear()
        sorted_dict = dict(sorted(banddict.items(), key=lambda item: item[1]))
        keys = list(sorted_dict.items())
        values = list(sorted_dict.values())
        for z in range(len(values)-1):
            for y in range(len(values)-1):
                if values[z] == values[y+1]:         # so we dont have duplicate
                    if z != y+1:
                        if [keys[z], keys[z + 1]] not in candidatekeys:
                            candidatekeys.append([keys[z], keys[z + 1]])
        val = int(rowsperband)
        rowsperband = int(rowsperband) + int(startingrowsperband)
    for i in range(len(candidatekeys)):
        arrr = list(candidatekeys[i])
        arrr[0] = list(arrr[0])
        arrr[1] = list(arrr[1])
        if userchose == 'a':
            jcsm = MyJacSimWithOrderedLists(arrr[0][0], arrr[1][0], 1)
        else:
            jcsm = MySigSim(arrr[0][0], arrr[1][0], int(numpermutations), 1)
        jacc += jcsm
        arrayforlsh.append(jacc)
        arrayforlsh.append(len(candidatekeys))
        canddocumentlist.append(jcsm)
        dist = 1 - jcsm
        canddistances.append(dist)
    for i in range(docsnum):
        counter = 0
        for x in candidatekeys:
            if x[0] == i or x[1] == i:
                counter += 1
        if counter < numneighbors and rows != 1:
            print('Rows per band value was not minimized, so it was divided by 2.\n')
            rows = rows/2
            if rows < 1:
                rows = 1
            candidatekeys.clear()
            avgsim2 = LSH(rows, docsnum, 1, numneighbors)
            break
    end_time = time.time()
    timespent = end_time - start_time
    if lshc == 1:
        return
    rows = math.floor(rows)
    print('LSH algorithm rowsPerBand variable = '+str(rows)+'\n')
    print('LSH algorithm --- %2f seconds ---' % timespent)
    lengthh = len(arrayforlsh)
    return arrayforlsh[lengthh-2]/arrayforlsh[lengthh-1]


def create_random_hash_function(p=2**33-355, m=2**32-1):
    a = random.randint(1, p-1)
    b = random.randint(0, p-1)
    return lambda x: 1 + (((a * x + b) % p) % m)


print("a. DATA_1-docword.enron.txt\n")
print("b. DATA_2-docword.nips.txt\n")
choice = input("Enter your choice (a or b): \n")
while choice != 'a' and choice != 'b':
    choice = input("Error : Wrong input. Choose a or b!!!\n")
if choice == 'a':
    with open('DATA_1-docword.enron.txt') as f:
        first_line = f.readline()
        words = f.readline()
elif choice == 'b':
    with open('DATA_2-docword.nips.txt') as f:
        first_line = f.readline()
        words = f.readline()
numDocuments = input("Insert an integer for the number of documents : \n")
while int(numDocuments) > int(first_line) or int(numDocuments) <= 0:
    numDocuments = input("Error : Insert an integer between 1 and "+first_line+"!!!\n")
MyReadDataRoutine(choice, int(numDocuments))
k = input('Insert the number of random permutations for Min Hash algorithm : \n')
for i in range(int(words)):
    wordlist.append([])
    nullwordlist.append(0)
listt = numpy.zeros((int(first_line), int(words)))
# sig = numpy.matrix(numpy.ones((int(first_line), 4)) * numpy.inf)
for y in range(int(numDocuments)):
    sig.append([])
    for i in range(int(k)):
        sig[y].append(numpy.inf)
# sig = numpy.array(sig).ravel()
MyMinHash(int(words), int(k))
print('a. Jaccard Similarity.\n')
print('b. Signature Similarity.\n')
userchose = input('Choose simirality calculation algorithm (a or b) : \n')
while userchose != 'a' and userchose != 'b':
    userchose = input('Eroor: Wrong input. Choose a or b!!! : \n')
docsneed = input('Do you want to input the 2 document numbers? (Yes or No)\n')
while docsneed != 'Yes' and docsneed != 'yes' and docsneed != 'YES' and docsneed != 'No' and docsneed != 'no' \
        and docsneed != 'NO':
    docsneed = input('Error: Wrong input. Choose Yes or No!\n')
if docsneed == 'Yes' or docsneed == 'yes' or docsneed == 'YES':
    firstdoc = input('Insert the number of the first document : \n')
    seconddoc = input('Insert the number of the first document : \n')
    while firstdoc == seconddoc:
        seconddoc = input('Error: Second documents number is same wih the first. Insert a different different number '
                          'than', firstdoc, '\n')
else:
    firstdoc = random.randint(1, int(numDocuments))
    seconddoc = random.randint(1, int(numDocuments))
    while firstdoc == seconddoc:
        seconddoc = random.randint(1, int(numDocuments))
if userchose == 'a':
    timeee, jcsim = MyJacSimWithOrderedLists(firstdoc, seconddoc, 0)
    print("With Ordered Lists --- %2f seconds ---" % timeee)
    print('Jaccard Similarity(Ordered Lists) of documents with number', firstdoc, 'and', seconddoc, 'is : ', jcsim, '\n')
    time2, jcsim2 = MyJacSimWithSets(firstdoc, seconddoc)
    print("With Sets --- %2f seconds ---" % time2)
    print('Jaccard Similarity(Sets) of documents with number', firstdoc, 'and', seconddoc, 'is : ', jcsim2, '\n')
elif userchose == 'b':
    numpermutations = input('Insert the number of rows to be involved in the SigSim algorithm : (between 1 and '+k+')\n')
    while int(numpermutations) > int(k) or int(numpermutations) < 1:
        numpermutations = input('Wrong input : Has to be between 1 and '+int(k)+'!!!\n')
    sigsim = MySigSim(int(firstdoc), int(seconddoc), int(numpermutations), 0)
    print('Signature Similarity of documents with number', firstdoc, 'and', seconddoc, 'is : ', sigsim, '\n')
print('a. LSH algorithm.\n')
print('b. Brude Force algorithm.\n')
lastchoice = input('Choose between LSH and Brude Force algorithm (a or b) : \n')
while lastchoice != 'a' and lastchoice != 'b':
    lastchoice = input('Error: Wrong input. Choose a or b!!! : \n')
numofdocuments = input('Insert the number of the documents to be involved : \n')
numofneighbors = input('Insert the number of the neighbors to be involved (2-5) : \n')
if lastchoice == 'b':
    avgsimbv = AvgSimWithBrudeForce(int(numofdocuments), int(numofneighbors))
    print('Average Similarity with Brude Force algorithm is : ', avgsimbv, '\n')
else:
    # lstchoice = input('Do you want the algorithm to minimize the rows of every band?(Yes or No) : \n')
    # while lstchoice != 'Yes' and lstchoice != 'yes' and lstchoice != 'YES' and lstchoice != 'No' \
    #        and lstchoice != 'no' and lstchoice != 'NO':
    #    lstchoice = input('Error: Wrong input. Choose Yes or No!\n')
    # if lstchoice == 'Yes' or lstchoice == 'YES' or lstchoice == 'yes':
    #    flag = True
    #    rowsperbandd = int(k)/4
    #    if rowsperbandd < 1:
    #        rowsperbandd = 1
    # else:
    rowsperbandd = input('Insert the number of rows per band : \n')
    # flag = False
    avgsimlsh = LSH(int(rowsperbandd), int(numofdocuments), 0, int(numofneighbors))
    print('Average Similarity with LSH algorithm is : ', avgsimlsh, '\n')
yesorno = input('Do you want to see the neighbours of some specific Doc ids??\n')
while yesorno != 'Yes' and yesorno != 'yes' and yesorno != 'YES' and yesorno != 'No' and yesorno != 'no' \
        and yesorno != 'NO':
    yesorno = input('Error: Wrong input. Choose Yes or No!\n')
if yesorno == 'Yes' or yesorno == 'yes' or yesorno == 'YES':
    docrow = input('Please insert the DOC ids splitted by commas : (e.g 3,7,15,29)\n')
    docrow = docrow.split(',')
    for x in range(len(docrow)):
        if int(docrow[x]) < int(numofdocuments):
            keyzz = list(myneighborsdict[int(docrow[x]) - 1].keys())
            print('Neighbours of document '+docrow[x]+' are documents : ')
            print(keyzz)
        else:
            print('You inserted Docid number higher than the numofdocuments which are involved in the algorithms.\n')
            print('We terminate the program here.')
            print('Goodbye!')
            exit(1)
print('\nGoodbye!')