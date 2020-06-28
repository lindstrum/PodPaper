from DocumentClasses import Article
from DocumentClasses import TextBlock
from DocumentClasses import Paragraph
from DocumentClasses import Figure
from DocumentClasses import OOLEquation
from DocumentClasses import Element
from DocumentClasses import WorkText

Art = Article("latextext.txt")

for el in range(Art.GetNumElements()):
    print("Element: " + str(el))
    element = Art.GetElement(el)
    type = element.GetType()
    print(type)
    if type == WorkText:
        print("Element is WorkText")
        element.GetElement().PrintSentenceWise()
    if type == Figure:
        print("Element is Figure")
        print(element.GetElement().GetDescription())
    if type == OOLEquation:
        print("Element is OOLEquation")
        print(element.GetElement().GetEnglish())
