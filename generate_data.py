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

def make_text():
    # generates images of word sequences of variable lengths
    words = np.genfromtxt('words.txt', dtype='U')
    MaxInt = words.size

    for j in range(200):
        string = ''
        for i in range(random.randint(5, 35)):
            if i % 10 == 9:
                string += '\n'
            string += words[random.randint(0, MaxInt)]+' '

        img = Image.new('RGB', (750, 80), color='white')
        d = ImageDraw.Draw(img)
        d.text((10, 10), string, fill=(0, 0, 0))

        x, y = img.size
        new_img = img.resize((int(x*5), int(y*5)))
        new_img.save('./text_data/%i.png' % j)


def generate_pieces(ipath, opath):
    # generates numpy arrays of images of written equations and typed text
    equation_pieces = []
    text_pieces = []

    for path in glob.glob(ipath):
        img = cv2.imread(path)[:, :, 0]
        equation_pieces.append(img)

    for path in glob.glob(opath):
        img = cv2.imread(path)[:, :, 0]
        text_pieces.append(img)

    np.save("equation_pieces", equation_pieces)
    np.save("text_pieces", text_pieces)


def main(train_num, img_size, num_pieces, write=True, plot=False):
    # concatenates images of equations and text into larger images
    equation_pieces = np.load('equation_pieces.npy', allow_pickle=True)
    text_pieces = np.load("text_pieces.npy")

    data = np.ones([train_num, 1, img_size, img_size])*255
    answer = np.ones([train_num, 3, img_size, img_size])*255

    for image_id in tqdm(range(train_num)):
        # np.ones([1, img_size, img_size])*255  # data[image_id]
        image = data[image_id]
        # np.ones([3, img_size, img_size])*255  # answer[image_id]
        image_truth = answer[image_id]

        frequency = np.zeros((img_size, img_size))
        labels, centroids = [], []

        if write:
            f = open("data_processed/%06d.txt" % image_id, 'w')

        for piece_id in range(0, num_pieces):

            # pick the image
            piece_type = np.random.randint(0, 2)
            if piece_type == 0:
                piece = random.choice(text_pieces)
            if piece_type == 1:
                piece = random.choice(equation_pieces)
            #if piece_type == 2: piece = random.choice(image_pieces)
            height, width = np.shape(piece)
            for i in range(height):
                for j in range(width):
                   if piece[i][j] == 255:
                       piece[i][j] -= 1
                       
            # pick the location
            x, y, x_center, y_center = 0, 0, 0, 0

            x, y = random.randint(0, img_size), random.randint(0, img_size)

            # truncating the width and height to fit in the array
            if x+width >= img_size:
                width = img_size-x
            if y+height >= img_size:
                height = img_size-y

            x_center, y_center = x + width/2, y + height/2

            region = image[y:y+height, x:x+width]

            if any(x == 255 for x in itertools.chain(*region)): # prevents overlapping of pieces
                continue
            
            image[0, y:y+height, x:x+width] = piece[:height, :width]
            if piece_type == 0:
                image_truth[0, y:y+height, x:x+width] = 0
            if piece_type == 1:
                image_truth[1, y:y+height, x:x+width] = 1

            if write:
                f.write(' '.join(str(x)
                                 for x in [piece_type, x, y, x+width, y+height]))
                f.write("\n")

        if plot:
            plt.figure()
            plt.imshow(image)

    if write:
        # cv2.imwrite("data_processed/%06d.png" % image_id, image)
        # cv2.imwrite("data_truth/%06d.png" % image_id, image_truth)
        np.save("data_processed.npy", data)
        np.save("data_truth.npy", answer)

plt.close("all")

# make_text()
# generate_pieces("./equation_data/*.png", "./text_data/*.png")
main(train_num=100,
     img_size=500,
     num_pieces=20,
     write=True, plot=False)
