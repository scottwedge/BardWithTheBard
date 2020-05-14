import random
import nltk
import pyttsx3 as tts
import re


punct = ["'",'"', "?", ",", ";", ":", "!", "."]
class WordSearch:

    def __init__(self, sonnet):
        self.original = sonnet
        self.edited = sonnet
        self.sonnet = sonnet.replace("\n", " ")
        self.nouns = self.filter_nouns()
        self.plnouns = self.filter_plnouns()
        self.verbs = self.filter_verb()
        self.verbed = self.filter_verbed()
        self.adverb = self.filter_adverb()
        self.adjectives = self.filter_adjectives()

    def filter_nouns(self):
        nouns = []
        for word, pos in nltk.pos_tag(nltk.word_tokenize(str(self.sonnet))):
            if (pos == 'NN'):
                nouns.append(word)
        return(nouns[1:])

    def filter_plnouns(self):
        plnouns=[]
        for word, pos in nltk.pos_tag(nltk.word_tokenize(str(self.sonnet))):
            if (pos == 'NNS'):
                plnouns.append(word)
        return plnouns

    def filter_verb(self):
        verbs=[]
        for word, pos in nltk.pos_tag(nltk.word_tokenize(str(self.sonnet))):
            if (pos == 'VB'):
                verbs.append(word)
        return verbs

    def filter_verbed(self):
        verbed=[]
        for word, pos in nltk.pos_tag(nltk.word_tokenize(str(self.sonnet))):
            if (pos == 'VBD'):
                verbed.append(word)
        return verbed

    def filter_adverb(self):
        adverbs=[]
        nogo=['not', 'now', 'so', 'too', 'then', 'there', 'as', 'ever', 'very']
        for word, pos in nltk.pos_tag(nltk.word_tokenize(str(self.sonnet))):
            if (pos == 'RB'):
                adverbs.append(word)

            for word in nogo:
                if word in adverbs:
                    adverbs.remove(word)
        return adverbs

    def filter_adjectives(self):
        adjectives=[]
        nogo=["thee","though","thy","thine"]
        for word, pos in nltk.pos_tag(nltk.word_tokenize(str(self.sonnet))):
            if (pos == 'JJ') and word not in nogo:
                adjectives.append(word)

        return adjectives

def sonnetize():
    with open('new_sonnets.txt', 'r') as text:
        sonnets = text.read()
        sonnet=sonnets.split("AAA-")
        return (sonnet[98])
        #return (sonnet[random.randint(1,154)])


def start():
    return WordSearch(sonnetize())

def changes():
    try:
        words_to_change = int(input("How many words would you like to change: (Recommended, 10 - 20, sonnets can be long) "))
        if words_to_change == 0:
            print("That'll just give you the same old sonnet, please enter another number")
            return 0
        elif words_to_change >=20:
            go_on = input("Wow that's quite a few are you sure? Yes or No:")
            if go_on.lower() == "yes" or go_on.lower() == "y":
                return words_to_change
            else:
                print("Let's try again shall we?")
                return 0
        else:
            return words_to_change
    except:
        print("That was not a valid option")
        return 0

def finale():
    answer=(input("\n\nWould you like to see the original sonnet? Yes or No :"))
    if answer.lower() == "yes" or answer.lower() == "y":
        print(madlib.original)
    else:
        print("\nThat wasn't a yes.  \nThank you for playing, have a lovely day")
def selection(x):

    y = random.randint(0,x)
    yield (x, y)

def format_to_change(user_num):
    changee = []
    to_change = 0
    while user_num > 0:
        user_num, to_change = (next(selection(user_num - to_change)))
        if user_num > 2 and user_num != to_change:
            changee.append(to_change)
        elif user_num == to_change:
            changee.append(user_num)
            break
        else:
            changee.append(to_change)
    changee= evenoutlist(changee)
    return (changee)

def evenoutlist(items):
    total=sum(items)
    mydict= {0 : madlib.nouns, 1 : madlib.verbs, 2 : madlib.adverb,
        3 : madlib.adjectives,  4 : madlib.verbed, 5: madlib.plnouns}
    while len(items)<6:
        items.append(0)
    for i in range(0,5):
        if items[i] > len(mydict[i]) and items[i] < total//3:
            items[i + 1] += items[i] - len(mydict[i])
            items[i] = len(mydict[i])

        elif items[i] > total//4:
            items[i+1]+= (items[i])-(total//3)
            items[i]=total//3
        else:
            pass

    if items[5] > total//4:
        items[0]+= items[5]-total//4
        items[5]=total//4
    elif items[5] > len(mydict[5]):
        items[0] += len(mydict[5])- items[5]
        items[5] = len(mydict[5])
    if sum(items)<total:
        items[0]= items[0]+(total-sum(items))

    return(items)

def new_nouns():
    user_nouns = []
    word_change= []
    if len(madlib.nouns) == 0:
        pass
    else:
        for times in range(items[0]):
            new_noun= input("Give me a noun: ")
            user_nouns.append(new_noun)
            x = (random.randint(0, len(madlib.nouns) - 1))
            while x in word_change:
                x = (random.randint(0, len(madlib.nouns) - 1))
            word_change.append(x)
        for index, word in enumerate(user_nouns):
            old = madlib.nouns[word_change[index]]

            madlib.edited = re.sub(rf'\s({old})(:?\S|\W)', f" {word.upper()} "   , madlib.edited, 1)
            #madlib.edited = madlib.edited.replace(madlib.nouns[word_change[index]], + word.upper(), 1)
            print(madlib.nouns[word_change[index]], word)


def new_verbs():
    user_verbs = []
    word_change = []
    if len(madlib.verbs) == 0:
        pass
    else:
        for times in range(items[1]):
            new_verb= input("Give me a verb: ")
            user_verbs.append(new_verb)
            x = (random.randint(0, len(madlib.verbs) - 1))
            while x in word_change:
                x = (random.randint(0, len(madlib.verbs) - 1))
            word_change.append(x)
        for index, word in enumerate(user_verbs):
            madlib.edited = madlib.edited.replace(madlib.verbs[word_change[index]], word.upper(), 1)


def new_adverbs():
    user_adverbs = []
    word_change = []
    if len(madlib.adverb) == 0:
        pass
    else:
        for times in range(items[2]):
            new_adverb= input("Give me an adverb: ")
            user_adverbs.append(new_adverb)
            x = (random.randint(0, len(madlib.adverb) - 1))
            while x in word_change:
                x = (random.randint(0, len(madlib.adverb) - 1))
            word_change.append(x)
        for index, word in enumerate(user_adverbs):
            madlib.edited = madlib.edited.replace(madlib.adverb[word_change[index]], word.upper(), 1)

def new_adjectives():
    user_adjectives = []
    word_change = []
    if len(madlib.adjectives) == 0:
        pass
    else:
        for times in range(items[3]):
            new_adjectives= input("Give me an adjective: ")
            user_adjectives.append(new_adjectives)
            x = (random.randint(0, len(madlib.adjectives) - 1))
            while x in word_change:
                x = (random.randint(0, len(madlib.adjectives) - 1))
            word_change.append(x)
        for index, word in enumerate(user_adjectives):
            madlib.edited = madlib.edited.replace(madlib.adjectives[word_change[index]], word.upper(), 1)

def new_verbed():
    user_verbed = []
    word_change = []
    if len(madlib.verbed) == 0:
        pass
    else:
        for times in range(items[4]):
            new_verbd = input("Give me past tense verb: ")
            user_verbed.append(new_verbd)
            x = (random.randint(0, len(madlib.verbed)-1))
            while x in word_change:
                x = (random.randint(0, len(madlib.verbed)-1))
            word_change.append(x)
        for index, word in enumerate(user_verbed):
            madlib.edited = madlib.edited.replace(madlib.verbed[word_change[index]], word.upper(), 1)

def new_plnouns():
    user_plnouns = []
    word_change= []
    if len(madlib.plnouns) == 0:
        pass
    else:
        for times in range(items[5]):
            new_plnoun= input("Give me a plural noun: ")
            user_plnouns.append(new_plnoun)
            x = (random.randint(0, len(madlib.plnouns)))
            while x in word_change:
                x = (random.randint(0, len(madlib.plnouns)-1))
            word_change.append(x)
        for index, word in enumerate(user_plnouns):
            madlib.edited = madlib.edited.replace(madlib.plnouns[word_change[index]], word.upper(), 1)

def game():

    new_nouns()
    new_verbs()
    new_adverbs()
    new_adjectives()
    new_verbed()
    new_plnouns()
    print(madlib.edited)

def read_it_to_me():
    should_I = input("Do you want this read to you? ")
    if should_I.lower().strip() == "yes" or should_I.lower().strip() == "y":
        engine = tts.init()
        engine.setProperty('voice', u'com.apple.speech.synthesis.voice.tessa')
        engine.setProperty('rate', 160)
        engine.say(madlib.edited)
        engine.runAndWait()
    else:
        pass

madlib = start()
user_num = 0
while user_num == 0:
    user_num = changes()
items = format_to_change(user_num)
new_sonnet= madlib.original
game()
read_it_to_me()
finale()

