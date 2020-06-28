try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

image_names_list = []


def main(input_text_file, output_text_file):
    #complies all image file names and converts images to latex
    read_thru_file(input_text_file)
    write_to_textfile(output_text_file)

def read_thru_file( file_name ): 
    #complies name of all image files
    f = open('Image to Latex\\' + file_name, "r")
    for image in f:
        image_name = image
        new_image_name = image_name.replace('\n','')
        image_names_list.append('Image to Latex\\Example Images\\' + new_image_name)
    f.close()
    return

def write_to_textfile( file_name ): 
    #converts images to latex and writes to text file named file_name (string)
    f = open('Image to Latex\\' + file_name,"w")
    paragraph_end = False
    for image in image_names_list:
        if 'Text' in image:
            if paragraph_end: 
                f.write('\paragraph{}')
                paragraph_end = False
            else:
                f.write(' ')
            text = image_to_text(image)
            f.write(text)
            if text.endswith('.') or text.endswith('. '): paragraph_end = True
        elif 'Math' in image:
            math = image_to_math("Nothing here yet.")
            f.write(math)
        else:
            f.write("\\begin{figure}\n\centering\n\includegraphics[scale = 0.4]{"+image+"}")
    f.close()
    return





def image_to_text( image_name ):
    #return image text as string
    text_string = pytesseract.image_to_string(Image.open(image_name))
    text_string = text_format(text_string)
    return text_string

def image_to_math( image_name):
    #return image math as string. Method not complete
    #supposed to be function that converts image to latex math
    math = 'x' #filler latex math that would be outputed
    math_string = ' $' + math + '$'
    return math_string

def text_format( text_string ):
    #changes formating of text given in text_string to be compatible with latex. 
    #Note text with special characters {, }, \ cannot be completely formatted
    if 'figure' in text_string[0:6].lower():
        text_string = '\caption{' + text_string  
        text_string = text_string.replace('\n\n','}\n\end{figure}\paragraph{}',1) 
    else:
        text_string = text_string.replace('\n\n','\n\end{figure}\paragraph{}',1) 
    text_string = text_string.replace('\n\n \n\n','\paragraph{}')
    text_string = text_string.replace('\n\n‘','\paragraph{}')
    text_string = text_string.replace('\n\n','\paragraph{}')
    text_string = text_string.replace('-\n','')
    text_string = text_string.replace('\n‘',' ')
    text_string = text_string.replace('\n',' ')
    text_string = text_string.replace("&","\&")
    text_string = text_string.replace('%','\%')
    text_string = text_string.replace('$','\$')
    text_string = text_string.replace('#','\#')
    text_string = text_string.replace('_','\_')
    text_string = text_string.replace('^','\^')
    text_string = text_string.replace('~','\~')        
    return text_string




main('ExampleImage.txt', 'latextext.txt')


#read_thru_file('Image.txt')
#print(image_names_list)
#write_to_textfile('latextext.txt')