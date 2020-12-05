from typing import List
from itertools import chain
import numpy as np

def sif_decompression(x_max: int, y_max: int, input: int) -> List:
    input = [int(i) for i in str(input)]
    frames_max = len(input) // (x_max * y_max)
    frames = []
    metadata = {}
    view = 2* np.ones((y_max,x_max))
    for f in range(frames_max):
        frame = []
        null_pixels = 0
        for y in range(y_max):
            line = []
            for x in range(x_max):
                pixel = input[f*x_max*y_max + y*x_max + x]
                line.append(pixel)
                if view[y, x] == 2 and pixel != 2:
                    view[y, x] = pixel
                if pixel == 0:
                    null_pixels += 1
            frame.append(line)
        frames.append(frame)
        metadata[f] = null_pixels
    return frames, metadata, view


def test_sif_decompression_returns_expected():
    pict, meta, view = sif_decompression(3,2,123456789012)
    assert pict == [[[1, 2, 3],
                     [4, 5, 6]],
                    [[7, 8, 9],
                     [0, 1, 2]]]
    assert meta == {0: 0, 1: 1}


def submission():
    with open('day_08_input.txt') as fp:
        raw = fp.read()
    pict, meta, view = sif_decompression(25,6,int(raw))
    min_frame = min(meta.keys(), key=(lambda k: meta[k]))
    validation = list(chain.from_iterable(pict[min_frame]))
    count_1 = sum([1 if v == 1 else 0 for v in validation])
    count_2 = sum([1 if v == 2 else 0 for v in validation])
    return count_1 * count_2, view


def test_submission():
    checksum, view = submission()
    assert checksum == 1360
    print('view\n\n\n',view)

"""
########  ######    ##    ##    ####    ######    
##        ##    ##  ##    ##  ##    ##  ##    ##  
######    ##    ##  ##    ##  ##    ##  ##    ##  
##        ######    ##    ##  ########  ######    
##        ##        ##    ##  ##    ##  ##  ##    
##        ##          ####    ##    ##  ##    ##  
"""