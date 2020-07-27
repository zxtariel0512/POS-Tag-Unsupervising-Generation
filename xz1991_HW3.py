#!/usr/bin/env python
# coding: utf-8

# In[5]:


oov = 1 / 1000
#f = open('/Users/apple/Desktop/NLP/HW3/WSJ_POS_CORPUS_FOR_STUDENTS/WSJ_02-21.pos','r')
f = open('WSJ_02-21.pos','r')
lines = f.read().splitlines()

tagNum = {} # total number of each tag
for i in range(len(lines)):
    if lines[i] == '':
        tagName1 = 'start'
        tagName2 = 'end'
        if tagName1 in tagNum:
            tagNum[tagName1] += 1
            tagNum[tagName2] += 1
        else:
            tagNum[tagName1] = 2
            tagNum[tagName2] = 2
        continue
    l = lines[i].split('\t')
    tag = l[1]
    if tag in tagNum:
        tagNum[tag] = tagNum[tag] + 1
    else:
        tagNum[tag] = 1
# for keys,values in tagNum.items():
#     print(keys)
#     print(values)

tran = {} # for transition matrix
for i in range(len(lines) - 1):
    if lines[i] == '':
        lPrev = lines[i - 1].split('\t')
        tagPrev = lPrev[1]
        if tagPrev in tran:
            if 'end' in tran[tagPrev]:
                tran[tagPrev]['end'] += 1
            else:
                tran[tagPrev]['end'] = 1
        else:
            tran[tagPrev] = {}
            tran[tagPrev]['end'] = 1
        lNext = lines[i + 1].split('\t')
        tagNext = lNext[1]
        if 'start' in tran:
            if tagNext in tran['start']:
                tran['start'][tagNext] += 1
            else:
                tran['start'][tagNext] = 1
        else:
            tran['start'] = {}
            tran['start'][tagNext] = 1
        continue
    l = lines[i].split('\t')
    tag = l[1]
    if lines[i + 1] == '':
            continue
    lNext = lines[i + 1].split('\t')
    tagNext = lNext[1]
    if tag in tran:
        if tagNext in tran[tag]:
            tran[tag][tagNext] += 1
        else:
            tran[tag][tagNext] = 1
    else:
        tran[tag] = {}
        tran[tag][tagNext] = 1
    tran[tag]['start'] = 0
# for keys,values in tran.items():
#     print(keys)
#     print(values)

tranMat = {} # transition matrix
for keys, values in tran.items():
    tag = keys
    nextDic = values
    tranMat[tag] = {}
    total = 0
    for keys, values in nextDic.items():
        total += values
    for keys, values in tran[tag].items():
        tranMat[tag][keys] = values / total
# for keys, values in tranMat.items():
#     print(keys)
#     print(values)

wordType = {} # for a given tag, number of each words
for i in range(len(lines)):
    if lines[i] == '':
        continue
    l = lines[i].split('\t')
    tag = l[1]
#     word = l[0].lower()
    word = l[0]
    if tag in wordType:
        if word in wordType[tag]:
            wordType[tag][word] += 1
        else:
            wordType[tag][word] = 1
    else:
        wordType[tag] = {}
        wordType[tag][word] = 1
# for keys, values in wordType.items():
#     print(keys)
#     print(values)

wordNum = {} # word number for different tags
for keys, values in wordType.items():
    tag = keys
    tagDic = values
    for keys, values in tagDic.items():
        word = keys
        num = values
        if word in wordNum:
            wordNum[word][tag] = num
        else:
            wordNum[word] = {}
            wordNum[word][tag] = num
# for keys, values in wordNum.items():
#     print(keys)
#     print(values)

wordProb = {} # word probability for different tags
for keys, values in wordNum.items():
    word = keys
    tagDic = values
    wordProb[word] = {}
    for keys, values in tagDic.items():
        tag = keys
        num = values
        totalNum = tagNum[tag]
        wordProb[word][tag] = num / totalNum
# for keys, values in wordProb.items():
#     print(keys)
#     print(values)

f.close()







# start to analyze
# file = open('/Users/apple/Desktop/NLP/HW3/WSJ_POS_CORPUS_FOR_STUDENTS/WSJ_23.words','r')
file = open('WSJ_23.words','r')
content = file.read()
s1 = content.split('\n\n')
sentence = []
test = open('/Users/apple/Desktop/NLP/HW3/xz1991-HW3/submission.pos','w+')
for i in range(len(s1)):
    sentence.append(s1[i].split('\n'))
# for i in range(len(sentence)):
#     print(sentence[i])
new = 0
for i in range(len(sentence)):
    if i != 0:
        new = 1
    likelihood = {} # likelihood matrix for each sentence
#     likelihood['start'] = {}
    sent = sentence[i]
    # columns
    for i in range(len(sent)):
        if sent[i] in wordNum:
            tagDic = wordNum.get(sent[i])
            for keys, values in tagDic.items():
                if keys not in likelihood:
                    likelihood[keys] = {}
        
    # rows
    for keys, values in likelihood.items():
        for i in range(len(sent)):
            values[i] = 0
    
#     likelihood['start'][0] = 1 # start: 1 0 0 ... 0 0
    # fill the matrix column by column
    for i in range(len(sent)):
        # jump first column (0 step)
#         if i == 0:
#             continue
        # 1th column deals differently
        if i == 0:
            for keys, values in likelihood.items():
#                 if keys == 'start':
#                     continue
                currTag = keys
                tagRow = values
                if sent[0] in wordProb:
                    if currTag not in wordProb[sent[0]]:
                        prob = 0
                    else:
                        prob = wordProb[sent[0]][currTag]
                    if currTag not in tranMat['start']:
                        tranProb = 0
                    else:
                        tranProb = tranMat['start'][currTag]
                else:
                    prob = oov
                    tranProb = oov
                tagRow[0] = prob * tranProb
        else:
            for keys, values in likelihood.items():
#                 if keys == 'start' or keys == 'end':
#                     continue
                currTag = keys
                tagRow = values
                final = 0
                for keys, values in likelihood.items():
#                     if keys == 'start' or keys == 'end':
#                         continue
                    compareTag = keys
                    if sent[i] in wordProb:
                        if currTag not in wordProb[sent[i]]:
                            prob = 0
                        else:
                            prob = wordProb[sent[i]][currTag]
                        if currTag not in tranMat[compareTag]:
                            tranProb = 0
                        else:
                            tranProb = tranMat[compareTag][currTag]
                    else:
                        prob = oov
                        tranProb = oov
                    currVal = prob * tranProb * likelihood[compareTag][i - 1]
                    if currVal > final:
                        final = currVal
                tagRow[i] = final
    
    # tag
    for i in range(len(sent)):
#         if i == 0 or i == len(sent) + 1:
#             continue
        currWord = sent[i]
        currTag = ''
        currProb = 0
        for keys, values in likelihood.items():
            if values[i] > currProb:
                currProb = values[i]
                currTag = keys
        if new == 1:
            test.write('\n')
            new = 0
        print(currWord + '\t' + currTag + '\n')
        test.write(currWord + '\t' + currTag + '\n')
#     for keys, values in likelihood.items():
#         print(keys)
#         print(values)


test.close()
        
    
    
    
    
    
        


# In[ ]:





# In[ ]:





# In[ ]:




