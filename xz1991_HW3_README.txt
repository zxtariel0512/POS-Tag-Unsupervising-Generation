* Running

The submission file includes six files:
- submission.pos: the tagged file to be checked
- xz1991_HW3.py: the python programming file of the main program
- xz1991_HW3_README.txt: a README instruction file to explain the running way and algorithm of the program
- WSJ_02-21.pos: the training file (provided)
- WSJ_23.words: the testing file which is tagged in submission.pos (provided)
- WSJ_24.pos: a sample file (provided)

The program uses ‘WSJ_02-21.pos’ as a standard library, and tags WSJ_23.words as final test. The program OPENS THESE TWO FILES INSIDE THE CODE INSTEAD OF IN COMMAND LINE.

————————————————————————————————————————————————————

* ALGORITHMS

The program computes dictionaries below:
-    ‘tagNum’: total number of each tag
-    ‘tran’: number of each kind of tag follows a certain tag
- ** ’tranMat’: the transition matrix
-    ‘wordType’: for a certain tag, number of each word
- ‘  ‘wordNum’: for a certain word, number of each tag it can have
-    ‘wordProb’: the probability of each tag for a certain word
- ** ‘likelihood’: the probability of the tag of a certain word when appears in a sentence

Above, the ‘tranMat’ denotes the ‘A’ and the ‘likelihood’ denotes the ‘B’ in the ‘QAOB’ model for HMM. All previous dictionaries (i.e. matrices) are used to compute the final ‘wordProb’ dictionary, which is later on used to decide the tag for a certain word.

The program first compute the transition matrix as follows:
1. Find the total number of tags that can appear after a given tag, denote as ‘total’
2. Find the number of a certain tag that appears after that given tag, denote as ‘num’
3. Compute that entry by: num / total

The program then input the test file, which is later on tagged (here is the file ‘WSJ_23.words’). The program analyzes and tags the file sentence by sentence, by re-creating (i.e. re-calculating) the ‘likelihood’ matrix sentence by sentence. The ‘likelihood’ matrix for a given sentence is computed as follows:
1. Find all possible tags for all words in that given sentence.
2. Denote the matrix row as each possible tag, and the column by each word.
3. For a certain entry a_32, assume the third row is the ‘NN’ tag, and the second column is the ‘fish’ column, then a_32 = max_{all rows i i.e. all possible tags} (Prob(fish appears to be ‘NN’) * Prob(‘NN’ follows by current tag i) * Prob(previous word appears to be tag i)). Here notices that for the first column (i.e. the first word), there is no need to multiply the last term. 
4. If a certain word is not found in the training file (here is the ‘WSJ_02-21.pos’), then the word is denoted as ‘OOV’, and the attribute values are denoted as a constant 1 / 1000.

With the ‘likelihood’ matrix computed as above, we tag the file as follows:
For a certain word (i.e. a certain column), find the row with the largest value, and then tag that word as the tag denoted in that row.