#import libraries
import numpy as np
import os
import matplotlib.pyplot as plt
from PIL import Image

dirPath = "C:\\Users\\ahmed\\Documents\\klinisches_anwendungs_projekt\\resources\\narvis-data"

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def vertical_flip_textures():
    models = os.listdir(dirPath)
    nModels = len(models)
    for i,model in enumerate(models):
        texturePath = os.path.join(dirPath,model,"Data\\Model\\Model_0.jpg")
        #read image (set image as m)
        m = Image.open(texturePath)
        #change image to array (set array as np_array)
        np_array = np.array(m)
        new_np_array = np.copy(np_array)
        #define the width(w) and height(h) of the image
        h, w, c = np_array.shape
        #make the image upside down
        for i in range(0,h):
            for j in range(0,w):
                new_np_array[i,j] = np_array[h-1-i,j]
        #change array back to image (set processed image as pil_image)
        pil_image = Image.fromarray(new_np_array)
        #save the processed image
        pil_image.save(os.path.join(dirPath,model,"Data\\Model\\Texture.jpg"))
        printProgressBar(i + 1, nModels, prefix = 'Progress:', suffix = 'Complete', length = 50)

if __name__ == '__main__':
    vertical_flip_textures()
