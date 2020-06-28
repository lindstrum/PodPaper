#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 11:56:12 2020

@author: yanli
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 22:04:39 2020

@author: yanli
"""

import pyttsx3
import sys
import copy
from datetime import datetime 

from DocumentClasses import Article
from DocumentClasses import TextBlock
from DocumentClasses import Figure
from DocumentClasses import OOLEquation

# readerConfiguration = {}
class Reader:
    def SetReaderConfiguration(self, readerConfiguration):
        Q1 = input("Would you like to read without interruption? y/n?")
        Q2 = input("Would you like to read the fiugre discription? y/n?")
        readerConfiguration['interruption'] = True if Q1 == 'y' else False
        readerConfiguration['figureDisc'] = True if Q2 == 'y' else False


    def IsContinueReading(self):
        engine = pyttsx3.init()
        engine.say("Would you like to continue to next paragraph?")
        engine.runAndWait()
        engine.stop()
        answer = input("Would you like to continue to next paragraph? y/n?")
        if answer == 'n':
            sys.exit('exit as you wish')
        if answer == 'y':
            return True
                    

    def GetcontentFromElement(self, element):
        elementType = element.type
        if elementType == TextBlock:
            return element.GetFullContent()
        elif elementType == Figure:
            return element.GetDescription().GetFullContent()
        elif elementType == OOLEquation:
            return element.GetEnglish()
        else:
            print('Invalid type!')

        
    def TextReader(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        
    def SaveAudio(self, article):
        articleText = ''
        while article.GetNextElement():
            articleText += str(self.GetcontentFromElement(article.GetNextElement())).replace('. ', ',, ')
        print(articleText, "yanyanyan")
        engine = pyttsx3.init()
#        engine.say(articleText)
#        engine.runAndWait()
        engine.save_to_file(articleText, 'article' + str(datetime.now()) + '.mp3')
        engine.runAndWait()
        engine.stop()




    def ReadArticle(self, article: Article):
        """
        Read the given Article and output a pdf file with all the figures and mp3
        file. 
        """
        print('yanyanyan')
        # we'll save the article to the audio file regardless the config of user

        copyOfArticle = copy.deepcopy(article)
        self.SaveAudio(copyOfArticle)
        print("yanyanyan")
        # read and set the reading configuration
        readerConfiguration = {}
        self.SetReaderConfiguration(readerConfiguration)
        isInterruption = readerConfiguration['interruption']
        isFigureDisc = readerConfiguration['figureDisc']
        

        # reading the article based on user's configuration and interaction
        currentReadingText = ''    
        while article.GetNextElement():
            currentElement = article.GetNextElement()
            currentElementType = currentElement.type
            currentReadingText = self.GetcontentFromElement(currentElement)
            if isInterruption and isFigureDisc:
                if self.IsContinueReading():
                    currentReadingText = currentReadingText
            if isInterruption and not isFigureDisc:
                if self.IsContinueReading():
                    currentReadingText = ",," if currentElementType == 'Figure' else currentReadingText
            if not isInterruption and isFigureDisc:
                currentReadingText = currentReadingText
            if not isInterruption and not isFigureDisc:
                currentReadingText = ",," if currentElementType == 'Figure' else currentReadingText
            self.TextReader(currentReadingText)
        sys.exit()

        
