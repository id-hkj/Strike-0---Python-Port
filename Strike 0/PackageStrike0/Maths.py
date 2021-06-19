import numpy as np #To make the mathematics faster


def ScreenYMath(ylegnth_for_1080_y_screen, ScreenY):
    y = ylegnth_for_1080_y_screen
    
    return int(np.round_(np.multiply((np.divide(y, 1080)), ScreenY)))

def ScreenXMath(xlegnth_for_1920_x_screen, ScreenX):
    x = xlegnth_for_1920_x_screen
    
    return int(np.round_(np.multiply((np.divide(x, 1920)), ScreenX)))