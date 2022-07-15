"""
HSV color space tester for xiaogui robot by OpenCV

"""
import numpy as np
import cv2
from urllib import request

print("hello world")
#this ip is xiaogui robot, please modify it by yourself.
url = "http://192.168.5.34/video?action=photo"


#standard colors BGR
#(H=0~180, S=0~255, V=0~255)
COLOR_BLACK  = [  0,   0,   0]  #黑色
COLOR_GRAY   = [128, 128, 128]  #灰色
COLOR_WHITE  = [255, 255, 255]  #白色
COLOR_RED    = [  0,   0, 255]  #红色
COLOR_ORANGE = [  0, 128, 255]  #橙色
COLOR_YELLOW = [  0, 255, 255]  #黄色
COLOR_GREEN  = [  0, 255,   0]  #绿色
COLOR_CYAN   = [255, 255,   0]  #青色
COLOR_BLUE   = [255,   0,   0]  #蓝色
COLOR_PURPLE = [104,   7,  52]  #紫色

# RANGE_BLACK   = ((  0,   0,   0), (180, 255,  46))
# RANGE_GRAY    = ((  0,   0,  46), (180,  43, 220))
# RANGE_WHITE   = ((  0,   0, 221), (180,  30, 255))
BLACK_VAL_MAX =  46
GRAY_SAT_MAX, GRAY_VAL_MIN, GRAY_VAL_MAX = 43, 46, 220
WHITE_SAT_MAX, WHITE_VAL_MIN = 30, 221

MIN_RED1    =   0
MIN_ORANGE  =  11
MIN_YELLOW  =  26
MIN_GREEN   =  35
MIN_CYAN    =  78
MIN_BLUE    = 100
MIN_PURPLE  = 125
MIN_RED2    = 156



def get_image_robot():
    """ get image from xiaogui robot """
    global url
    with request.urlopen(url) as f:
        data = f.read()
        img1 = np.frombuffer(data, np.uint8)
        img_cv = cv2.imdecode(img1, cv2.IMREAD_ANYCOLOR)
        return img_cv

def get_image_local():
    """ only for test: get image from local file """
    return cv2.imread('colorcard.png', cv2.IMREAD_COLOR)




#----------- CODE FOR COLOR-PANNEL ---------------------
pannel = np.zeros((256,1,3), dtype=np.uint8)
pannel[255] = COLOR_WHITE
pannel[254] = COLOR_GRAY
pannel[253] = COLOR_BLACK

def show_color_pannel():
    """for debug: view pannels value"""
    global pannel
    arr = [(pannel[i,0,0], pannel[i,0,1], pannel[i,0,2]) for i in range(256)]
    print("")
    print(BLACK_VAL_MAX, GRAY_SAT_MAX, GRAY_VAL_MIN, GRAY_VAL_MAX, WHITE_SAT_MAX, WHITE_VAL_MIN)
    print(MIN_RED1, MIN_ORANGE, MIN_YELLOW, MIN_GREEN, MIN_CYAN, MIN_BLUE, MIN_PURPLE, MIN_RED2)
    for i in range(23):
        print(i * 8,
              pannel[i*8+0,0].tolist(), pannel[i*8+1,0].tolist(), pannel[i*8+2,0].tolist(), pannel[i*8+3,0].tolist(), 
              pannel[i*8+4,0].tolist(), pannel[i*8+5,0].tolist(), pannel[i*8+6,0].tolist(), pannel[i*8+7,0].tolist())


def refresh_color_pannel():
    """ refresh color pannel """
    global pannel
    for i in range(181):
        if   i >= MIN_RED2:   pannel[i] = [COLOR_RED]
        elif i >= MIN_PURPLE: pannel[i] = [COLOR_PURPLE]
        elif i >= MIN_BLUE:   pannel[i] = [COLOR_BLUE]
        elif i >= MIN_CYAN:   pannel[i] = [COLOR_CYAN]
        elif i >= MIN_GREEN:  pannel[i] = [COLOR_GREEN]
        elif i >= MIN_YELLOW: pannel[i] = [COLOR_YELLOW]
        elif i >= MIN_ORANGE: pannel[i] = [COLOR_ORANGE]
        elif i >= MIN_RED1:   pannel[i] = [COLOR_RED]

    

def set_color_pannel(name, value):
    """ adjust color threshold value """
    global MIN_RED2, MIN_PURPLE, MIN_BLUE, MIN_CYAN, MIN_GREEN, MIN_YELLOW, MIN_ORANGE, MIN_RED1
    global BLACK_VAL_MAX, GRAY_SAT_MAX, GRAY_VAL_MIN, GRAY_VAL_MAX, WHITE_SAT_MAX, WHITE_VAL_MIN
    if name=="RED2":     MIN_RED2=value
    elif name=="PURPLE": MIN_PURPLE=value
    elif name=="BLUE":   MIN_BLUE=value
    elif name=="CYAN":   MIN_CYAN=value
    elif name=="GREEN":  MIN_GREEN=value
    elif name=="YELLOW": MIN_YELLOW=value
    elif name=="ORANGE": MIN_ORANGE=value
    elif name=="RED1":   MIN_RED1=value

    elif name=="BLACK_VAL_MAX": BLACK_VAL_MAX=value
    elif name=="GRAY_SAT_MAX":  GRAY_SAT_MAX=value
    elif name=="GRAY_VAL_MIN":  GRAY_VAL_MIN=value
    elif name=="GRAY_VAL_MAX":  GRAY_VAL_MAX=value
    elif name=="WHITE_SAT_MAX": WHITE_SAT_MAX=value
    elif name=="WHITE_VAL_MIN": WHITE_VAL_MIN=value

    refresh_color_pannel()
    return None


def color_name(hsv):
    h, s, v = hsv
    if v<=BLACK_VAL_MAX: return "BLACK"
    if s<=GRAY_SAT_MAX and (v>=GRAY_VAL_MIN and v<=GRAY_VAL_MAX): return "GRAY"
    if s<=WHITE_SAT_MAX and v>=WHITE_VAL_MIN: return "WHITE"

    if h>=MIN_RED2: return "RED2"
    if h>=MIN_PURPLE: return "PURPLE"
    if h>=MIN_BLUE: return "BLUE"
    if h>=MIN_CYAN: return "CYAN"
    if h>=MIN_GREEN: return "GREEN"
    if h>=MIN_YELLOW: return "YELLOW"
    if h>=MIN_ORANGE: return "ORGANGE"
    if h>=MIN_RED1: return "RED1"
    return "UNKNOWN"


cv2.namedWindow('pannel')
cv2.resizeWindow('pannel', 400, 650)
cv2.createTrackbar('Black-Vmax','pannel', BLACK_VAL_MAX, 255, lambda x:set_color_pannel("BLACK_VAL_MAX",x))
cv2.createTrackbar('Gray-Smax','pannel', GRAY_SAT_MAX, 255, lambda x:set_color_pannel("GRAY_SAT_MAX",x))
cv2.createTrackbar('Gray-Vmin','pannel', GRAY_VAL_MIN, 255, lambda x:set_color_pannel("GRAY_VAL_MIN",x))
cv2.createTrackbar('Gray-Vmax','pannel', GRAY_VAL_MAX, 255, lambda x:set_color_pannel("GRAY_VAL_MAX",x))
cv2.createTrackbar('White-Smax','pannel', WHITE_SAT_MAX, 255, lambda x:set_color_pannel("WHITE_SAT_MAX",x))
cv2.createTrackbar('White-Vmin','pannel', WHITE_VAL_MIN, 255, lambda x:set_color_pannel("WHITE_VAL_MIN",x))

cv2.createTrackbar('Red2-Hue','pannel', MIN_RED2, 180, lambda x:set_color_pannel("RED2",x))
cv2.createTrackbar('Purple-Hue', 'pannel', MIN_PURPLE, 180, lambda x:set_color_pannel("PURPLE",x))
cv2.createTrackbar('Blue-Hue', 'pannel', MIN_BLUE, 180, lambda x:set_color_pannel("BLUE",x))
cv2.createTrackbar('Cyan-Hue', 'pannel', MIN_CYAN, 180, lambda x:set_color_pannel("CYAN",x))
cv2.createTrackbar('Green-Hue', 'pannel', MIN_GREEN, 180, lambda x:set_color_pannel("GREEN",x))
cv2.createTrackbar('Yellow-Hue', 'pannel', MIN_YELLOW, 180, lambda x:set_color_pannel("YELLOW",x))
cv2.createTrackbar('Oragne-Hue', 'pannel', MIN_ORANGE, 180, lambda x:set_color_pannel("ORANGE",x))
cv2.createTrackbar('Red1-Hue', 'pannel', MIN_RED1, 180, lambda x:set_color_pannel("RED1",x))
refresh_color_pannel()

cv2.namedWindow('org')
cv2.namedWindow('hsv')

#mouse event for show position
def onmouse(event, x, y, flags, param):
    global X, Y
    if event != cv2.EVENT_LBUTTONUP: return
    X, Y = x, y
cv2.setMouseCallback("hsv", onmouse)

X, Y, preX, preY = -1, -1, -1, -1

#start process
while True:
    image = get_image_robot()
    cv2.imshow("org", image)

    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    img_hue = cv2.split(img_hsv)[0]

    #filter no-effect colors, such as black, white, gray
    mask_white = cv2.inRange(img_hsv, (0, 0, WHITE_VAL_MIN), (180, WHITE_SAT_MAX, 255))
    np.place(img_hue, mask_white, 255)
    mask_gray = cv2.inRange(img_hsv, (0, 0, GRAY_VAL_MIN), (180, GRAY_SAT_MAX, GRAY_VAL_MAX))
    np.place(img_hue, mask_gray, 254)  
    mask_black = cv2.inRange(img_hsv, (0, 0, 0), (180, 255, BLACK_VAL_MAX))
    np.place(img_hue, mask_black, 253)

    #standard colors
    rst = cv2.applyColorMap(img_hue, pannel)
    cv2.imshow("hsv", rst)

    if (X!=preX) or (Y!=preY):
        point_org, point_hsv = image[Y, X], img_hsv[Y, X]
        print("POS(x:%d, y:%d) RGB(R:%d, G:%d, B:%d) HSV(H:%d, S:%d, V:%d)"%(X, Y, point_org[2], point_org[1], point_org[0], point_hsv[0], point_hsv[1], point_hsv[2]), 
            color_name(point_hsv))
        preX, preY = X, Y
    if cv2.waitKey(1) & 0xFF == ord('q'): break
   

cv2.destroyAllWindows()


