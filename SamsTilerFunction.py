from skimage.io import imread_collection
import numpy as np
from tifffile import imsave

def SamsTilingFunction(path_to_image, target_tile_height, target_tile_width):
    
    folder = np.array(imread_collection(path_to_image), dtype = object)
    
    heights = []
    widths = []
    for i in range(len(folder)):
        heights.append(folder[i].shape[0])
        widths.append(folder[i].shape[1])
    max_rows = sorted(heights, reverse = True)[0]
    max_columns = sorted(widths, reverse = True)[0]
    
    ydiv = np.ceil(max_rows / target_tile_height)
    xdiv = np.ceil(max_columns / target_tile_width)
    
    target_full_rows = ydiv * target_tile_height
    target_full_columns = xdiv * target_tile_width
    
    rowdiff = []
    columndiff = []
    for i in range(len(heights)):
        rowdiff.append(target_full_rows - heights[i])
        columndiff.append(target_full_columns - widths[i])
    rowdiff = [int(i) for i in rowdiff]
    columndiff = [int(i) for i in columndiff]
    
    imgs = folder.copy()
    for i in range(len(folder)):
        imgs[i] = np.pad(folder[i], ((0, rowdiff[i]), (0, columndiff[i])))
        
    for i in range(len(imgs)):
        if imgs[i].shape[0] != target_full_rows:
            print("Target rows doesn't match actual rows")
        elif imgs[i].shape[1] != target_full_columns:
                print("Target columns doesn't match actual columns")
        else:
            continue
        
    intsplit = []
    for i in range(len(imgs)):
        intsplit.append(np.array_split(imgs[i], ydiv, axis = 0))
    intsplit = np.array(intsplit)
    tiled_imgs = []
    for i in range(len(intsplit)):
        tiled_imgs.append(np.array_split(intsplit[i], xdiv, axis = 2))
    tiled_imgs = np.array(tiled_imgs)
    
    for i in range(len(tiled_imgs)):
        for j in range(int(xdiv)):
            for k in range(int(ydiv)):
                imsave("img{}tile{},{}.tiff".format(i, j, k), tiled_imgs[i][j][k])
    
    intermediate1 = []
    intermediate2 = []
    stitched_imgs = np.array([])
    for j in range(len(folder)):
        for i in range(int(xdiv)):
            intermediate1.append(np.vstack((tiled_imgs[j][i][0], tiled_imgs[j][i][1])))
        intermediate2  = np.hstack(([i for i in intermediate1]))
    stitched_imgs = np.asarray(np.hsplit(intermediate2, len(imgs)))
    
    return [xdiv, ydiv, target_tile_height, target_tile_width]
