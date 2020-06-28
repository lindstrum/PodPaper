#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Jun 27

@author: JeremieLePageBourbonnais
"""
import nltk
import TexToEnglish

class Article:
    #Object for the full file.Contains textblocks, figures, and equations

    title = None
    intpuPath = None
    textBlocks = None
    workTexts = None
    paragraphs = None
    figures = None
    oolEquations = None
    curElement = None
    numElements = None

    def __init__(self, inputPath):
        self.title = ''
        self.inputPath = inputPath
        self.textBlocks = []
        self.workTexts = []
        self.paragraphs = []
        self.figures = []
        self.oolEquations = []
        self.ParseTex()
        self.CombineParagraphs()
        self.numElements = len(self.workTexts) + len(self.figures) + len(self.oolEquations)
        self.curElement = 0

    def ParseTex(self):
        #Create list of line by line version of Tex file
        file = open(self.inputPath, "r")
        rawString = ''
        for line in file:
            rawString += line.lstrip(" ")
        rawString = rawString.replace("\\paragraph", "\n\\paragraph")
        rawString = rawString.replace("\\begin{", "\n\\begin{")
        rawString = rawString.replace("\\include", "\n\\include")
        rawString = rawString.replace("\\caption", "\n\\caption")
        rawString = rawString.replace("\\end", "\n\\end")
        document = rawString.split("\n")
        #Search for the commands (i.e. \paragraph{}, \begin{equation}. \begin{figure})
        order = -1
        paragraphsToAdd = []
        inFigure = False
        figurePath = None
        figureDescription = None
        inEquation = False
        for line in document:
            if "\\paragraph{}" in line:
                parLength = len(self.paragraphs)
                if parLength > 0:
                    if self.paragraphs[parLength-1].GetOrder() == order:
                        order -= 1
                order += 1
                self.paragraphs.append(Paragraph(order, line[line.find("{}")+2 : len(line)]))
                thisLineIs = -1

            elif inFigure or "\\begin{figure}" in line or "\\begin{tabular}" in line:
                inFigure = True
                if "\\includegraphics" in line:
                    figurePath = line[line.find("{")+1 : len(line)-1]
                if "\\caption{" in line:
                    figureDescription = line[line.find("{")+1 : len(line)-1]

                if "\\end{figure}" in line or "\\end{tabular}" in line or (figurePath != None and figureDescription != None):
                    order += 1
                    self.figures.append(Figure(order, -1, "PlaceHolder", figureDescription, figurePath))
                    figurePath = None
                    figureDescription = None
                    inFigure = False

            elif inEquation or "\\begin{equation}" in line:
                inEquation = True
                if "\\begin{equation}" not in line:
                    order += 1
                    self.oolEquations.append(OOLEquation(order, -1, line))
                    inEquation = False
        return order+1

    def CombineParagraphs(self):
        prevParOrder = -1
        tmpW = None
        for par in self.paragraphs:
            if par.GetOrder() != prevParOrder:
                tmpW = WorkText(par.GetOrder())
                self.workTexts.append(tmpW)
            self.workTexts[len(self.workTexts)-1].AddParagraph(par)
            prevParOrder = par.GetOrder()

    def GetNumElements(self):
        return self.numElements

    def GetElement(self, order):
        type, index = self.FindElementAt(order)
        if type == -1 or index == -1:
            print("Error: document element could not be found")
            return None
        self.curElement = order
        if type == 0:
            return Element(self.workTexts[index])
        if type == 1:
            return Element(self.figures[index])
        if type == 2:
            return Element(self.oolEquations[index])

    def GetCurElement(self):
        type, index = self.FindElementAt(self.curElement)
        if type == -1 or index == -1:
            print("Error: document element could not be found")
            return None
        if type == 0:
            return Element(self.workTexts[index])
        if type == 1:
            return Element(self.figures[index])
        if type == 2:
            return Element(self.oolEquations[index])

    def GetNextElement(self):
        type, index = self.FindElementAt(self.curElement+1)
        if self.curElement+1 >= self.numElements:
            print("Error: Tried to access element out of bounds (order > numElements)")
            return None
        if type == -1 or index == -1:
            print("Error: document element could not be found")
            return None
        if type == 0:
            self.curElement += 1
            return Element(self.workTexts[index])
        if type == 1:
            self.curElement += 1
            return Element(self.figures[index])
        if type == 2:
            self.curElement += 1
            return Element(self.oolEquations[index])

    def GetPreviousElement(self):
        type, index = self.FindElementAt(self.curElement+1)
        if self.curElement <= 0:
            print("Error: Tried to access element out of bounds (order < 0)")
            return None
        if type == -1 or index == -1:
            print("Error: document element could not be found")
            return None
        if type == 0:
            self.curElement -= 1
            return Element(self.workTexts[index])
        if type == 1:
            self.curElement -= 1
            return Element(self.figures[index])
        if type == 2:
            self.curElement -= 1
            return Element(self.oolEquations[index])


    def GetListOfTextBlocks(self):
        return self.textBlocks

    def GetListOfWorkTexts(self):
        return self.workTexts

    def GetListOfFigures(self):
        return self.figures

    def GetListOfOOLEquations(self):
        return self.oolEquations

    def SetTitle(self, title):
        self.title = title

    def GetTitle(self, title):
        return self.title

    def FindElementAt(self, order):
        type = -1 #0: textbox, 1 figure, 2 equation
        index = -1
        for text in self.workTexts:
            index +=1
            if text.GetOrder() == order:
                return 0, index
            elif text.GetOrder() > order:
                break
        index = -1
        for fig in  self.figures:
            index +=1
            if fig.GetOrder() == order:
                return 1, index
            elif fig.GetOrder() > order:
                break
        index = -1
        for equ in self.oolEquations:
            index +=1
            if equ.GetOrder() == order:
                return 2, index
            elif equ.GetOrder() > order:
                break
        return type, index

class Element:
    type = None
    element = None
    def __init__(self, element):
        self.element = element
        self.type = type(element)

    def GetType(self):
        return self.type

    def GetElement(self):
        return self.element


class TextBlock:
    order = -1
    numParagraphs = -1
    currentParagraph = -1
    paragraphs = []

    def __init__(self, order=-1):
        self.order = order
        self.currentParagraph = 0
        self.numParagraphs = 0

    def GetFullContent(self):
        output = ''
        for par in self.paragraphs:
            output += par.GetFullContent()
        return output

    def AddParagraph(self, paragraph):
        if type(paragraph) is not Paragraph:
            print("Tried to add non-paragraph object")
            return -1

        self.numParagraphs += 1
        self.paragraphs.append(paragraph)

    def GetNumParagraphs(self):
        return self.numParagraphs

    def GetOrder(self):
        return self.order

    def GetCurrentParagraph(self):
        return self.paragraphs[self.currentParagraph]

    def GetNextParagraph(self):
        if (self.currentParagraph + 1 >= self.numParagraphs):
            self.currentParagraph = self.numParagraphs -1
            return None
        self.paragraph += 1
        return self.paragraphs[self.currentParagraph]

    def GetPreviousParagraph(self):
        if (self.currentParagraph - 1 < 0):
            self.currentParagraph = 0
            return None
        self.paragraph -= 1
        return self.paragraphs[self.currentParagraph]

    def GetParagraph(self, paragraph, curParagraph=None):
        if curParagraph == None:
            curParagraph = paragraph
        if paragraph < 0 or paragraph >= self.numParagraphs:
            return None
        self.currentParagraph = curParagraph
        return self.paragraphs[paragraph]

    def PrintParagraphWise(self):
        for par in range(self.numParagraphs):
            self.paragraphs[par].PrintParagraph()
            print("\n")

    def PrintSentenceWise(self):
        for par in range(self.numParagraphs):
            self.paragraphs[par].PrintSentenceWise()
            print("\n")

class Paragraph:
    order = -1
    content = ''
    sentences = None
    numSentences = -1
    currentLine = -1;

    def __init__(self, order=-1, content=''):
        self.order = order
        self.content = content
        self.currentLine = 0
        self.SeparateSentences()
        self.ConvertInLineEquations()
        self.numSentences = len(self.sentences)

    def SeparateSentences(self):
        #Switch to using nltk
        self.sentences = nltk.sent_tokenize(self.content)

    def ConvertInLineEquations(self):
        CleanedSentences = []
        for line in self.sentences:
            cleanSentence = line
            firstPos = cleanSentence.find("$")
            lastPos = cleanSentence.find("$", firstPos+1, len(cleanSentence))
            if firstPos == -1 or lastPos == -1:
                CleanedSentences.append(cleanSentence)
                continue
            rawEquation = cleanSentence[firstPos+1:lastPos]
            print(rawEquation)
            cleanEquation = TexToEnglish.getEnglish(rawEquation)
#            cleanEquation = rawEquation
            cleanSentence = cleanSentence.replace(rawEquation, cleanEquation)
            cleanSentence = cleanSentence.replace("$", "")
            CleanedSentences.append(cleanSentence)
        self.sentences = CleanedSentences

    def GetOrder(self):
        return self.order

    def GetFullContent(self):
        return self.content

    def GetNumSentences(self):
        return self.numSentences

    def GetCurSentence(self):
        return self.sentences[self.currentLine]

    def GetNextSentence(self):
        if (self.currentLine + 1 >= self.numSentences):
            return None
        self.currentLine += 1
        return self.sentences[self.currentLine]

    def GetPreviousSentence(self):
        if (self.currentLine <= 0):
            self.currentLine = 0
            return None
        self.currentLine -= 1
        return self.sentences[self.currentLine]

    def GetSentence(self, sentence, curSentence = None):
        if curSentence == None:
            curSentence = sentence
        if sentence < 0 or sentence >= self.numSentences:
            return None
        self.currentLine = curSentence
        return self.sentences[sentence]

    def PrintParagraph(self):
        print(self.content)

    def PrintSentenceWise(self):
        for sentence in range(self.numSentences):
            print(self.GetSentence(sentence))

class OOLEquation:
    #OOLEquation: Out-Of-Line Equation
    order = -1
    latex = ''
    english = ''
    refNumber = -1

    def __init__(self, order = -1, refNumber = -1, latex = ''):
        self.order = order
        self.refNumber = refNumber
        self.latex = latex
        self.english = TexToEnglish.getEnglish(latex)
        self.english = latex + 'temp'

    def SetOrder(self, order):
        self.order = order

    def SetRefNumber(self, refNumber):
        self.refNumber = refNumber

    def SetLatex(self, latex):
        self.latex = latex

    def SetEnglish(self, english):
        self.english = english

    def GetOrder(self):
        return self.order

    def GetRefNumber(self):
        return self.refNumber

    def GetLatex(self):
        return self.latex

    def GetEnglish(self):
        return self.english

class Figure:
        refNumber = -1
        order = -1
        path = ''
        type = None
        description = None

        def __init__(self, order = -1, refNumber = -1, type = None, description = None, path = None):
            self.order = order
            self.refNumber = refNumber
            self.path = path
            self.description = description
            self.type = type

        def SetType(self, type):
            self.type = type

        def SetDescription(self, par):
            if (type(par) != Paragraph):
                print("Error: Trying to add non-paragraph description. For text description use Figure::SetDescriptionText")
                return -1
            self.description = par

        def SetDescriptionText(self, text):
            if (type(text) != str):
                print("Error: Trying to add non-text description. To set paragraph use Figure::SetDescription")
                return -1
            self.description = Paragraph(0, text)

        def SetRefNumber(self, refNumber):
            self.refNumber = refNumber

        def SetOrder(self, order):
            self.order = order

        def SetPath(self, path):
            self.path = path

        def GetType(self):
            return self.type

        def GetDescription(self):
            return self.description

        def GetRefNumber(self):
            return self.refNumber

        def GetOrder(self):
            return self.order

        def GetPath(self):
            return self.path

class WorkText:
    paragraphs = []
    order = -1
    def __init__(self, iorder):
        self.paragraphs = []
        self.order = iorder

    def AddParagraph(self, par):
        self.paragraphs.append(par)

    def GetOrder(self):
        return self.order

    def PrintSentenceWise(self):
        for par in range(len(self.paragraphs)):
            self.paragraphs[par].PrintSentenceWise()
            print("\n")

    def GetFullContent(self):
        output = ''
        for par in self.paragraphs:
            output += par.GetFullContent()
        return output
