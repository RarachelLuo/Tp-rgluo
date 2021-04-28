# All the text files for the bible are copied and pasted from
#http://stewartonbibleschool.org/bible/text/index.html∫

def genesis():
    with open ("genesis.txt", "r") as myfile:
        book = myfile.read().splitlines()
    return book

def exodus():
    with open ("exodus.txt", "r") as myfile:
        book = myfile.read().splitlines()
    return book

def leviticus():
    with open ("leviticus.txt", "r") as myfile:
        book = myfile.read().splitlines()
    return book

def numbers():
    with open ("numbers.txt", "r") as myfile:
        book = myfile.read().splitlines()
    return book

def deuteronomy():
    with open ("deuteronomy.txt", "r") as myfile:
        book = myfile.read().splitlines()
    return book

def joshua():
    with open ("joshua.txt", "r") as myfile:
        book = myfile.read().splitlines()
    return book

def judges():
    with open ("judges.txt", "r") as myfile:
        book = myfile.read().splitlines()
    return book

def ruth():
    with open ("ruth.txt", "r") as myfile:
        book = myfile.read().splitlines()
    return book

def firstSamuel():
    with open ("firstSamuel.txt", "r") as myfile:
        book = myfile.read().splitlines()
    return book

def secondSamuel():
    with open ("secondSamuel.txt", "r") as myfile:
        book = myfile.read().splitlines()
    return book

def firstKings():
    with open ("firstKings.txt", "r") as myfile:
        book = myfile.read().splitlines()
    return book

def secondKings():
    with open ("secondKings.txt", "r") as myfile:
        book = myfile.read().splitlines()
    return book

def firstChronicles():
    with open ("firstChronicles.txt", "r") as myfile:
        book = myfile.read().splitlines()
    return book

def secondChronicles():
    with open ("secondChronicles.txt", "r") as myfile:
        book = myfile.read().splitlines()
    return book

def chooseBook(num):
    books=[genesis(),exodus(),leviticus(), numbers(), deuteronomy(),joshua(),
            judges(),ruth(),firstSamuel(),secondSamuel(),firstKings(),
            secondKings(),firstChronicles(),secondChronicles()]
    return books[num]
    
#print(chooseBook(12))
