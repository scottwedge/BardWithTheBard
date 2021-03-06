import random
import nltk
import pyttsx3 as tts
import re
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logging.disable(logging.DEBUG)
class WordSearch:
    """ Initializes a sonnet into word parts, keeps an original and makes a duplicate to edit so you can compare at
the end of all of it if you'd like"""

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
        """
        Skips the first noun due to sometimes mistakenly tokenizing the Roman numeral.
        :return: nouns
        """
        nouns = []
        for word, pos in nltk.pos_tag(nltk.word_tokenize(str(self.sonnet))):
            if (pos == 'NN'):
                nouns.append(word)
        return(nouns[1:])

    def filter_plnouns(self):
        """

        :return: Plural nouns
        """
        plnouns=[]
        for word, pos in nltk.pos_tag(nltk.word_tokenize(str(self.sonnet))):
            if (pos == 'NNS'):
                plnouns.append(word)
        return plnouns

    def filter_verb(self):
        """
        :return: List of verbs
        """
        verbs=[]
        for word, pos in nltk.pos_tag(nltk.word_tokenize(str(self.sonnet))):
            if (pos == 'VB'):
                verbs.append(word)
        return verbs

    def filter_verbed(self):
        """
        :return: list of past tense verbs
        """
        verbed=[]
        for word, pos in nltk.pos_tag(nltk.word_tokenize(str(self.sonnet))):
            if (pos == 'VBD'):
                verbed.append(word)
        return verbed

    def filter_adverb(self):
        """
        Took out some adverbs that made some of the sonnets too wonky
        :return: adverbs
        """
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
        """

        :return: adjectives
        """
        adjectives=[]
        nogo=["thee","though","thy","thine"]
        for word, pos in nltk.pos_tag(nltk.word_tokenize(str(self.sonnet))):
            if (pos == 'JJ') and word not in nogo:
                adjectives.append(word)

        return adjectives

def sonnetize():
    """
    Splits on AAA-, after doing that I realized I could also split based on multiple \n's
    for future adlib files I may change it
    :return: random sonnet from an edited text file
    """
    with open('new_sonnets.txt', 'r') as text:
        sonnets = text.read()
        sonnet=sonnets.split("AAA-")

        return (sonnet[random.randint(1,154)])


def start():
    """

    :return: random sonnet initialized into word types
    """
    return WordSearch(sonnetize())

def changes():
    """

    :return: Number of words to madlib in the sonnet
    """
    try:
        words_to_change = int(input("How many words would you like to change: (Recommended, 10 - 20, sonnets can be long) "))
        if words_to_change == 0:
            print("That'll just give you the same old sonnet, please enter another number")
            return 0
        elif words_to_change >20:
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
    """
    End of the game
    :return: original sonnet or end
    """
    answer=(input("\n\nWould you like to see the original sonnet? Yes or No :"))
    if answer.lower() == "yes" or answer.lower() == "y":
        print(madlib.original)
    else:
        print("\nThat wasn't a yes.  \nThank you for playing, have a lovely day")

def selection(x):
    """
    Randomizes amount of words in each category will be assigned
    :param x: user number
    :return:
    """
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
    changee= evenoutlist(changee) # just ensuring that no list exceeds numbers of word type
    return (changee)

def evenoutlist(items):
    """ Evens out the distribution of tasks.  Also makes sure you are not asked to fill out more than each of the
    available word types"""
    total=sum(items)
    mydict= {0 : madlib.nouns, 1 : madlib.verbs, 2 : madlib.adverb,
        3 : madlib.adjectives,  4 : madlib.verbed, 5: madlib.plnouns}
    while len(items)<6:
        items.append(0)
    for i in range(0,5):
        if items[i] > len(mydict[i]) and items[i] < total//3:
            items[i + 1] += items[i] - len(mydict[i])
            items[i] = len(mydict[i])
        elif items[i] > len(mydict[i]):
            items[i + 1] += items[i] - len(mydict[i])
            items[i] = len(mydict[i])
        elif items[i] > total//3:
            items[i+1]+= (items[i])-(total//3)
            items[i]=total//3
        else:
            pass
    # Bookending plural nouns to go back to the nouns since sometimes there are very few of them.
    if items[5] > total//3:
        items[0]+= items[5]-total//3
        items[5]=total//4
    elif items[5] > len(mydict[5]):
        items[0] += len(mydict[5])- items[5]
        items[5] = len(mydict[5])
    if sum(items)<total:
        items[0]= items[0]+(total-sum(items))
    logging.debug(f"Your evened out list {items}")
    return(items)

def new_nouns():
    """

    :return: madlib updated with new nouns
    """
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
            madlib.edited = re.sub(rf'(\s){(old)}(\W)', rf"\g<1>{word.upper()}\g<2>", madlib.edited, 1)
            logging.debug(f"{old}: original noun, {word.upper()}, new noun")

def new_verbs():
    """

    :return: madlib update with new verbs
    """
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
            old = madlib.verbs[word_change[index]]
            madlib.edited = re.sub(rf'(\s){(old)}(\W)', rf"\g<1>{word.upper()}\g<2>", madlib.edited, 1)
            logging.debug(f"{old}: original verb, {word.upper()}, new verb")


def new_adverbs():
    """

    :return: madlib updated with user adverbs
    """
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
            old = madlib.adverb[word_change[index]]
            madlib.edited = re.sub(rf'(\s){(old)}(\W)', rf"\g<1>{word.upper()}\g<2>", madlib.edited, 1)
            logging.debug(f"{old}: original adverb, {word.upper()}, new adverb")

def new_adjectives():
    """

    :return: madlib updated with new adjectives
    """
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
            old = madlib.adjectives[word_change[index]]
            madlib.edited = re.sub(rf'(\s){(old)}(\W)', rf"\g<1>{word.upper()}\g<2>", madlib.edited, 1)
            logging.debug(f"{old}: original adjective, {word.upper()}, new adjective")

def new_verbed():
    """

    :return: madlib updated with new past tense verbs
    """
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
            old = madlib.verbed[word_change[index]]
            madlib.edited = re.sub(rf'(\s){(old)}(\W)', rf"\g<1>{word.upper()}\g<2>", madlib.edited, 1)
            logging.debug(f"{old}: original past tense verb, {word.upper()}, new past tense verb")

def new_plnouns():
    """

    :return: madlib updated with new plural nouns
    """
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
            old = madlib.plnouns[word_change[index]]
            madlib.edited = re.sub(rf'(\s){(old)}(\W)', rf"\g<1>{word.upper()}\g<2>", madlib.edited, 1)
            logging.debug(f"{old}: original plural noun, {word.upper()}, new plural noun")

def game():

    new_nouns()
    new_verbs()
    new_adverbs()
    new_adjectives()
    new_verbed()
    new_plnouns()
    print(madlib.edited)

def read_it_to_me():
    """

    :return: spoken text
    """
    should_I = input("Do you want this read to you? ")
    if should_I.lower().strip() == "yes" or should_I.lower().strip() == "y":
        engine = tts.init()
        engine.setProperty('voice', u'com.apple.speech.synthesis.voice.tessa')
        engine.setProperty('rate', 155)
        engine.say(madlib.edited)
        engine.runAndWait()
    else:
        pass

if __name__ == "__main__":
    madlib = start()
    user_num = 0
    while user_num == 0:
        user_num = changes()
    items = format_to_change(user_num)
    new_sonnet= madlib.original
    game()
    read_it_to_me()
    finale()

