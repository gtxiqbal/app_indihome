class Modul:

    def FirstUpperCaseWord(sentence):
        words = []
        for firstWord in sentence.split(' '):
            words.append(firstWord.capitalize())

        words = " ".join(words)
        return words.strip()