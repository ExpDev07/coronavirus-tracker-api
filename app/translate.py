from googletrans import Translator, LANGUAGES

class translateIt(listOfLanguages):

    translatorLanguage = Translator()  #
listOfLanguages = ['zh-tw', 'es', 'en', 'hi', 'fr', 'ar', 'pt', 'it', 'ru', 'pa', 'ja']
lang = translatorLanguage.translate(text, dest= listOfLanguages)
