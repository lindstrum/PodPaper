import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image
from PIL import Image, ImageDraw
import cv2
import random
import itertools
import glob
from tqdm import tqdm

def dist(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def main(train_num, img_size, num_pieces, write=True, plot=False):
    equation_pieces = np.load('equation_pieces.npy', allow_pickle=True)
    text_pieces = np.load("text_pieces.npy")
    
    for image_id in tqdm(range(train_num)):
        image = np.ones((img_size, img_size))*255
        image_truth = np.ones((img_size, img_size, 3))*255
        
        frequency = np.zeros((img_size, img_size))
        labels, centroids = [], []
        
        if write:
            f = open("data_processed/%06d.txt" % image_id, 'w')
        
        # TODO: variable colonies per image
        for piece_id in range(0, num_pieces):
            
            # pick the image
            piece_type = np.random.randint(0, 2)
            if piece_type == 0: piece = random.choice(text_pieces)
            if piece_type == 1: piece = random.choice(equation_pieces)
            #if piece_type == 2: piece = random.choice(image_pieces)   
            height, width = np.shape(piece)
           
    
            # pick the location
            x, y, x_center, y_center = 0, 0, 0, 0
            
            x, y = random.randint(0, img_size), random.randint(0, img_size)
            
            #truncating the width and height to fit in the array
            if x+width >=img_size:
                width = img_size-x-1
            if y+height >=img_size:
                height = img_size-y-1
    
            x_center, y_center = x + width/2, y + height/2
            
            #good = True
            
            #region = image[y:y+height, x:x+width]
            #if (all(x == 255 for x in itertools.chain(*region))):
            #    good = False
            #for l in centroids:
            #    if dist(l, (x_center, y_center)) < 200:
            #        good = False

            #if not good: break
            #centroids.append((x_center, y_center))
            
            image[y:y+height, x:x+width] =  piece[:height,:width]
            if piece_type == 0:
                image_truth[y:y+height, x:x+width, 0]  = 0
            if piece_type == 1:
                image_truth[y:y+height, x:x+width, 1]  = 1
            
            if write:
                f.write(' '.join(str(x) for x in [piece_type, x, y, x+width, y+height]))
                f.write("\n")
        
        # image = cv2.GaussianBlur(image, (0,0), 2)
        if plot:
            plt.figure()
            plt.imshow(image)
            #plt.imshow(image_truth)
    
        if write:
            cv2.imwrite("data_processed/%06d.png" % image_id, image)
            cv2.imwrite("data_truth/%06d.png" % image_id, image_truth)

def make_text():
    words = np.genfromtxt('words.txt', dtype='U')
    MaxInt = words.size
    
    for j in range(200):
        string = ''
        for i in range(random.randint(5,35)):
            if i % 10 == 9:
                string += '\n'
            string += words[random.randint(0, MaxInt)]+' '
        
        img = Image.new('RGB', (750, 80), color='white')
        d = ImageDraw.Draw(img)
        d.text((10, 10), string, fill=(0,0,0))
        
        x, y = img.size
        new_img = img.resize((int(x*5), int(y*5)))
        new_img.save('./text_data/%i.png' % j)

def generate_pieces(ipath, opath):
    equation_pieces = []
    text_pieces = []
    
    for path in glob.glob(ipath):
            print(path)
            img = cv2.imread(path)[:,:,0]
            print(img)
            equation_pieces.append(img)
            
    
    for path in glob.glob(opath):
            print(path)
            img = cv2.imread(path)[:,:,0]
            print(img)
            text_pieces.append(img)
    
    np.save("equation_pieces", equation_pieces)
    np.save("text_pieces", text_pieces)

plt.close("all")

make_text()
generate_pieces("./equation_data/*.png", "./text_data/*.png")
main(train_num=50,
     img_size=3000,
     num_pieces=20,
     write=True, plot=True)
