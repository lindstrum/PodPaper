try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

image_total = 6 #filler
image_names_list = []
test_image = 'Image to Latex\\Images\\Text 7.png'

def read_thru_file( file_name ): 
    #reads through textfile named file_name(string)
    #this should probably be redone to be nicer
    f = open('Image to Latex\\' + file_name, "r")
    for image in f:
        image_name = image
        new_image_name = image_name.replace('\n','')
        image_names_list.append('Image to Latex\\Images\\' + new_image_name)
    f.close()
    return

def write_to_textfile( file_name ): 
    #writes to text file named file_name(string)
    f = open('Image to Latex\\' + file_name,"w")
    
    for image in image_names_list:
        if 'Text' in image:
            text = image_to_text(image)
            f.write(' ' + text)
        elif 'Math' in image:
            math = image_to_math("Nothing here yet.")
            f.write(math)
        else:
            f.write(" Gonna probably include something about and image.")
    f.close()
    return




# print(pytesseract.image_to_string(Image.open('HELLO\\test.PNG')))

def image_to_text( image_name ):
    #return image text as string
    text_string = pytesseract.image_to_string(Image.open(image_name))
    return text_string

def image_to_math( image_name):
    #return image math as string
    return " Insert math here."

read_thru_file('Image.txt')
print(image_names_list)
write_to_textfile('latextext.txt')