#Aryaman Gulati 

from porter import create_stem 

import math


class TextModel(object):
    """A class supporting complex models of text."""
  
    def __init__(self):
        """Create an empty TextModel."""
        #
        # Create dictionaries for each characteristic
        #
        self.words = {}           # For counting words
        self.wordlengths = {}     # For counting word lengths
        self.stems = {}           # For counting stems
        self.sentencelengths = {} # For counting sentence lengths
        self.punctuation = {}     # for counting punctuation
        #
        # Create another of your own
        #
        self.myparameter2 = {}     # For counting punctuation 
    
    def __repr__(self): #given, when printing it prints out twice. Need to get rid of one I imagine. How to get this not to print 
        """Display the contents of a TextModel."""
        s = 'Words:\n' + str(self.words) + '\n\n'
        s += 'Word lengths:\n' + str(self.wordlengths) + '\n\n'
        s += 'Stems:\n' + str(self.stems) + '\n\n'
        s += 'Sentence lengths:\n' + str(self.sentencelengths) + '\n\n'
        s += 'Punctuation:\n' + str(self.punctuation) + '\n\n'
        return s
    
    def readTextFromFile(self, filename): #functionworks
        """Accept a filename (a string) and set self.text to all of the text in that file, represented as a single, very large string."""
        f= open(filename)
        self.text = f.read()
        f.close()
        self.text = self.text.replace("\n"," ")
        return(self.text)

    def makeSentenceLengths(self): #works
       """ should use the text in the input string s to create the self.sentence lengths dictionary """
       LoW = self.text.split()
       self.makesentencelengths = {}
       SC = 0
       for wrd in LoW:
           SC+=1
           if wrd[-1] in '.?!':
               if SC not in self.makesentencelengths:
                   self.makesentencelengths[SC] = 1
               else:
                   self.makesentencelengths[SC] += 1
               SC = 0
       self.sentencelengths = self.makesentencelengths

    
    def cleanString(self, s): #works
       """ This method should accept a string s and return a string with no punctuation and no upper-case letters."""
       import string
       for p in string.punctuation:
           s = s.replace(p, "")
           s = s.lower()
       return s
    
    def makeWordLengths(self): 
        """creates a dictionary of the word-length features"""

        self.wordlength = {}
        chr = 0
        cleanstring = self.cleanString(self.text)
        for i in range(len(cleanstring)):
            chr += 1
            if cleanstring[i] == " ":
                chr -= 1
                if chr in self.wordlength:
                    self.wordlength[chr] += 1
                else:
                    self.wordlength[chr] = 1
                chr = 0
            if i == len(cleanstring)-1:
                if chr in self.wordlength:
                    self.wordlength[chr] += 1
                else:
                    self.wordlength[chr] = 1

        self.wordlengths = self.wordlength


    def makeWords(self): #works
        """makes a dictionary of words themselves (cleaned!)"""
        cleanstring2 = self.cleanString(self.text)
        self.makeWords = {}
        splitstring = cleanstring2.split()
        for i in range(len(splitstring)):
            wd = splitstring[i]
            if wd in self.makeWords:
                self.makeWords[wd] += 1
            else:
                self.makeWords[wd] = 1
        self.words = self.makeWords
    

    def makeStems(self): #works
        """need a function that accepts words and outputs stem"""
        cleanStr = self.cleanString(self.text)
        self.stems1 = {}
        wordsList = cleanStr.split()
        for i in wordsList:
            stem = create_stem(i)
            if stem in self.stems1:
                self.stems1[stem] += 1
            else:
                self.stems1[stem] = 1
        self.stems = self.stems1
    
    def makePunctuation(self): #works 
        """ will make a dictionary of the punctuation of the text"""

        self.punctuation = {} #will contain ?,',!,comma,.,""
        count = 0
        LOC = list(self.text)
        for i in LOC:
            if i == "?":
                if "?" in self.punctuation:
                    self.punctuation[i] += 1
                else:
                    self.punctuation[i] = 1
            
            if i == "'":
                if "'" in self.punctuation:
                    self.punctuation[i] += 1
                else:
                    self.punctuation[i] = 1
            
            if i == "!":
                if "!" in self.punctuation:
                    self.punctuation[i] += 1
                else:
                    self.punctuation[i] = 1
            
            if i == ",":
                if "," in self.punctuation:
                    self.punctuation[i] += 1
                else:
                    self.punctuation[i] = 1
            
            if i == ".":
                if "." in self.punctuation:
                    self.punctuation[i] += 1
                else:
                    self.punctuation[i] = 1
            
            if i == '"':
                if '"' in self.punctuation:
                    self.punctuation[i] += 1
                else:
                    self.punctuation[i] = 1
        
        self.myparameter2 = self.punctuation

# final methods and analysis 

    def createAllDictionaries(self):
        """Create out all five of self's
            dictionaries in full.
        """
        self.makeSentenceLengths()
        self.makeWords()
        self.makeStems()
        self.makeWordLengths()  
        self.makePunctuation()
        
    def normalizeDictionary(self, d):
        """normalizes the dictionary using a porportion of 1 in add1 and then multiplying the integer for each term in the dictionary d"""
        nd = {}
        add1 = sum(d.values())
        for k in d:
            nd[k]=d[k]/add1 
        return nd
    
    def smallestValue(self, nd1, nd2): 
        sm_va= 0
        """accepts two model dictionaries and returns the smallest non-zero value in the two dictionarities """
        minnd1=min(nd1.values())
        minnd2=min(nd2.values())
        if minnd1>minnd2:
            sm_va = minnd2
        else:
            sm_va = minnd1
        return sm_va
    
    def compareDictionaries(self,d,nd1,nd2):
        """computer the log progability that dictionary d arose from the data of nd1 and nd2"""
        total_log_prob = 0.0 
        nd1_log_prob = 0.0
        nd2_log_prob  = 0.0 
        epsilon = 0.5 * self.smallestValue(nd1,nd2)
        for k in d: 
            if k in nd1:
                nd1_log_prob+=d[k]*math.log(nd1[k])
            else:
                nd1_log_prob+=d[k]*math.log(epsilon)   
        for k in d:
            if k in nd2:
                nd2_log_prob+=d[k]*math.log(nd2[k])
            else:
                nd2_log_prob+=d[k]*math.log(epsilon)
        List_of_log_probs = [nd1_log_prob, nd2_log_prob]
        return List_of_log_probs
    
    def compareTextWithTwoModels(self,model1,model2):
        """prints comparative results if the log-probabilities for all five dictionaries and determines which is more similar"""
        
        nd1 = model1.normalizeDictionary(model1.words)
        nd2 = model2.normalizeDictionary(model2.words)
        wordfrequency = self.compareDictionaries(self.words, nd1, nd2)

        print( "wordfrequency is", wordfrequency )
        
        nd1A = model1.normalizeDictionary(model1.wordlength)
        nd2A = model2.normalizeDictionary(model2.wordlength)
        wordlen = self.compareDictionaries(self.wordlength, nd1A, nd2A)

        nd1B = model1.normalizeDictionary(model1.makesentencelengths)
        nd2B = model2.normalizeDictionary(model2.makesentencelengths)
        sentlen = self.compareDictionaries(self.makesentencelengths, nd1B, nd2B)

        nd1C = model1.normalizeDictionary(model1.stems1)
        nd2C = model2.normalizeDictionary(model2.stems1)
        stem = self.compareDictionaries(self.stems1, nd1C, nd2C)

        nd1D = model1.normalizeDictionary(model1.punctuation)
        nd2D = model2.normalizeDictionary(model2.punctuation)
        punctuation = self.compareDictionaries(self.punctuation, nd1D, nd2D)
        
        print(f"           name               model 1             model 2")
        print(f"           ----               -------             -------")
        print(f"  wordfrequency       {wordfrequency[0]}   {wordfrequency[1]}   ")
        print(f"    wordlengths       {wordlen[0]}   {wordlen[1]}   ")
        print(f"  sentencelengths     {sentlen[0]}    {sentlen[1]}   ")
        print(f"          stems       {stem[0]}   {stem[1]}")
        print(f"    punctuation       {punctuation[0]}    {punctuation[1]}")
                
        pointm1 = 0
        pointm2 = 0
        
        if wordfrequency[0] > wordfrequency[1]:
            pointm1 += 1
        else: 
            pointm2 += 1

        if wordlen[0] > wordlen[1]:
            pointm1 += 1
        else: 
            pointm2 += 1

        if sentlen[0] > sentlen[1]:
            pointm1 += 1
        else: 
            pointm2 += 1

        if stem[0] > stem[1]:
            pointm1 += 1
        else: 
            pointm2 += 1

        if punctuation[0] > punctuation[1]:
            pointm1 += 1
        else: 
            pointm2 += 1

        print("")
        print("--> Model1 wins on", pointm1, "features")
        print("--> Model2 wins on", pointm2, "features")

        TM1 = [wordfrequency[0],wordlen[0],sentlen[0],stem[0],punctuation[0]]
        TM2 = [wordfrequency[1],wordlen[1],sentlen[1],stem[1],punctuation[1]]
        if sum(TM1) > sum(TM2):
            print("+++++     This story is a better match with Jhumpa Lahiri's The Lowland   +++++")
        elif sum(TM2) > sum(TM1): 
            print("+++++     This story is a better match with John Cleever's Enormous Radio   +++++")
        else:
            print('+++++     Well, the models are tied!     +++++')


print('\n')
print(" +++++++++++ Model1 +++++++++++ ")
TM1 = TextModel()
TM1.readTextFromFile("train1.txt")
TM1.createAllDictionaries()  # provided in hw description
print(TM1)

print(" +++++++++++ Model2 +++++++++++ ")
TM2 = TextModel()
TM2.readTextFromFile("train2.txt")
TM2.createAllDictionaries()  # provided in hw description
print(TM2)


print(" +++++++++++ Unknown text +++++++++++ ")
TM_Unk = TextModel()
TM_Unk.readTextFromFile("unknown.txt")
TM_Unk.createAllDictionaries()  # provided in hw description
print(TM_Unk)

