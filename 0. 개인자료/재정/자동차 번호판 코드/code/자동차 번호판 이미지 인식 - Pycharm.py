from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import math
import os
import os.path
import pymysql
import numpy as np
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt    # 결과물 시각화
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract"


def malloc(h, w, initValue=0) :
    retMemory= []
    for _ in range(h) :
        tmpList = []
        for _ in range(w) :
            tmpList.append(initValue)
        retMemory.append(tmpList)
    return retMemory

# 파일을 메모리로 로딩하는 함수
def loadImageColor(fnameOrCvData) :  # 파일명 or OpenCV 개체
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo,cvPhoto
    inImage = []

    ##################################
    ## PIL 개체 --> OpenCV 개체로 복사.
    if type(fnameOrCvData) == str:
        cvData = cv2.imread(fnameOrCvData)  # 파일 --> cvData개체로 읽어옴.
    else:
        cvData = fnameOrCvData
    cvPhoto = cv2.cvtColor(cvData, cv2.COLOR_BGR2RGB) # 중요! CV개체.
    photo = Image.fromarray(cvPhoto)  # 중요! PIL(pillow) 객체
    inW = photo.width;
    inH = photo.height  # 불러오는 사진의 크기
    ##################################

    ## 메모리 확보
    for _ in range(3) :  # 3면 확보
        inImage.append(malloc(inH, inW))
    photoRGB = photo.convert('RGB')   # RGB색을 만들기 위함.
    print(photoRGB)
    for i in range(inH) :
        for k in range(inW) :
            r, g, b = photoRGB.getpixel((k,i))   # (163, 58, 73) 형태로 나옴. jpg이기 때문에 기존 raw와는 다르다.
            inImage[R][i][k] = r
            inImage[G][i][k] = g
            inImage[B][i][k] = b



def openImageColor() :
    global window, canvas, paper, filename, inImage, outImage,inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                filetypes=(("칼라 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename == '' or filename == None :
        return
    loadImageColor(filename)  # load를 하면, 불러온 사진에서 inImage의 픽셀 값이 저장됨.
    equalImageColor()


def displayImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if canvas != None : # 예전에 실행한 적이 있다.
        canvas.destroy()
    global VIEW_X, VIEW_Y
    #가로/세로 비율 계산
    ratio = outH / outW
    ## 고정된 화면 크기
    if outH <= VIEW_Y or outW <= VIEW_X:
        VIEW_X = outW
        VIEW_Y = outH
        step = 1
    else:
        VIEW_X = 512
        VIEW_Y = 512
        step = outW / VIEW_X

    window.geometry(str(int(VIEW_X*1.2)) + 'x' + str(int(VIEW_Y*1.2)))  # 벽
    canvas = Canvas(window, height=VIEW_Y, width=VIEW_X)
    paper = PhotoImage(height=VIEW_Y, width=VIEW_X)
    canvas.create_image((VIEW_X // 2, VIEW_Y // 2), image=paper, state='normal')

    import numpy
    rgbStr = '' # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0,outH, step) :
        tmpStr = ''
        for k in numpy.arange(0,outW, step) :
            i = int(i); k = int(k)
            r , g, b = outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]
            tmpStr += ' #%02x%02x%02x' % (r,g,b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)
    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))


import numpy as np
# JGG 파일이 임시 저장소에 저장. (AppData) -> 참고로, RAW와 jpg 저장 방식은 다르다.(내가 여기서 고민 많이 함.)
def saveImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if outImage == None :
        return
    outArray = []
    for i in range(outH):
        tmpList = []
        for k in range(outW):
            tup = tuple([outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]])
            tmpList.append(tup)
        outArray.append(tmpList)

    outArray = np.array(outArray)
    savePhoto = Image.fromarray(outArray.astype(np.uint8), 'RGB')
    saveFp = asksaveasfile(parent=window, mode='wb',
                           defaultextension='.', filetypes=(("그림 파일", "*.png;*.jpg;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return

    savePhoto.save(saveFp.name)
    print('Save~')

###############################################
##### 컴퓨터 비전(영상처리) 알고리즘 함수 모음 #####
###############################################
# 동일영상 알고리즘
def equalImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ## 메모리 확보
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ############################
    ### 진짜 컴퓨터 비전 알고리즘 ###
    for RGB in range(3) :  # RGB가 0면, 1면, 2면으로 값이 저장됨.
        for i in range(inH) :
            for k in range(inW) :
                outImage[RGB][i][k] = inImage[RGB][i][k]
    #############################
    displayImageColor()


    # 진짜 번호판일 것 같은 boundingRect를 추려내기. -> 순차적으로 정리 되어 있는 것들을 확인한다.
    # 규칙 정하기 - 노트 참고1
    MAX_DIAG_MULTIPLYER = 5  # diag의 중심점끼리의 거리가 diag length의 __ 배 안쪽으로 있어야 함.
    MAX_ANGLE_DIFF = 12.0  # contour와 contour와의 각도 최댓값
    MAX_AREA_DIFF = 0.5  # contour와 contour 면적 차이가 ___이하(비율로 계산할 것임)
    MAX_WIDTH_DIFF = 0.8  # contour와 contour의 너비 차이가 ____ 이하(비율로 계산할 것임)
    MAX_HEIGHT_DIFF = 0.2  # contour와 contour의 높이 차이가 ____ 이하(비율로 계산할 것임)
    MIN_N_MATCHED = 7  # 위 다섯 개의 변수를 만족하는 네모가 적어도 7개 이상이어야 함.

# 재귀적 방식으로 번호판 후보군을 찾을 것임.
def find_chars(contour_list):
    global MAX_DIAG_MULTIPLYER, MAX_ANGLE_DIFF, MAX_AREA_DIFF, MAX_WIDTH_DIFF, MAX_HEIGHT_DIFF, MIN_N_MATCHED
    global possible_contours

    matched_result_idx = []  # 최종적을 남는 index 값들을 저장.

    #  이중 for문을 돎으로써, contour간에 계산 비교하기 - 노트 참고
    for d1 in contour_list:
        matched_contours_idx = []
        for d2 in contour_list:
            if d1['idx'] == d2['idx']:  # contour가 같으면 넘어감.
                continue

            # 노트참고2 - 위 변수 중 MAX_DIAG_MULTIPLYER와 값을 비교하기 위함.
            dx = abs(d1['cx'] - d2['cx'])  # 대각선 길이 구하기 위한 dx
            dy = abs(d1['cy'] - d2['cy'])  # 대각선 길이 구하기 위한 dy

            diagonal_length1 = np.sqrt(d1['w'] ** 2 + d1['h'] ** 2)  # contour1의 대각선 길이

            distance = np.linalg.norm(np.array([d1['cx'], d1['cy']]) - np.array([d2['cx'], d2['cy']]))
            ## np.linalg.norm(a-b)  => 벡터 a와 벡터 b 사이의 거리를 구한다.

            # 노트참고3 - 위 변수 중 MAX_ANGLE_DIFF와 값을 비교하기 위함.=> dx, dy 계산이 있어야함.
            if dx == 0:  # dx = 0이면 contour1과 contour2간의 관계가 각도가 90도로 이루어짐.
                angle_diff = 90
            else:
                angle_diff = np.degrees(np.arctan(dy / dx))  # arctan을 통해 각도를 계산한다.
            area_diff = abs(d1['w'] * d1['h'] - d2['w'] * d2['h']) / (d1['w'] * d1['h'])  # 면적의 비율
            width_diff = abs(d1['w'] - d2['w']) / d1['w']  # 너비의 비율
            height_diff = abs(d1['h'] - d2['h']) / d1['h']  # 높이의 비율

            # 위 파라미터 기준에 맞는 친구들만 matched_contours_idx에 집어넣는다.
            if distance < diagonal_length1 * MAX_DIAG_MULTIPLYER \
                    and angle_diff < MAX_ANGLE_DIFF and area_diff < MAX_AREA_DIFF \
                    and width_diff < MAX_WIDTH_DIFF and height_diff < MAX_HEIGHT_DIFF:
                matched_contours_idx.append(d2['idx'])  # 노트참고4 - d1과 함께하는 d2들 중 조건에 만족하면 모두 추가하기.

        matched_contours_idx.append(d1['idx'])  # d2와 비교했던 d1추가.

        # 번호판 갯수 확인 -> 윤곽선 갯수가 3보다 작으면 번호판일 확률이 낮다. 왜냐하면 한국 번호판은 총 7자리이기 때문.
        if len(matched_contours_idx) < MIN_N_MATCHED:  # if 조건을 만족하면 번호판이 아님. 따라서 continue 진행.
            continue

        matched_result_idx.append(matched_contours_idx)  # 통과했으면 최종 후보군에 넣을 것임.

        # 최종 후보군이 아닌 애들을 한 번 더 비교해볼 것임.
        unmatched_contour_idx = []
        for d4 in contour_list:
            if d4['idx'] not in matched_contours_idx:  # mathced_contours_idx에 값이 없으면,
                unmatched_contour_idx.append(d4['idx'])  # unmatched_contour_idx에 값을 대입하자.

        unmatched_contour = np.take(possible_contours,
                                    unmatched_contour_idx)  # 전체 contour와 unmatched contour의 교집합을 찾자!!!
        ## np.take(a, idx) => a에서 idx와 같은 인덱스의 값만 추출.

        # ★★★재귀 진행★★★ -> 후보군인 것들을 제거하면서 후보군이 아닌 값들 중 후보일 것으로 예상 되는 값을 찾기 위함.
        recursive_contour_list = find_chars(unmatched_contour)

        # 살아남은 것을 matched_result_idx에 저장.
        for idx in recursive_contour_list:
            matched_result_idx.append(idx)
        break

    return matched_result_idx


def carNumberOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    global MAX_DIAG_MULTIPLYER, MAX_ANGLE_DIFF, MAX_AREA_DIFF, MAX_WIDTH_DIFF, MAX_HEIGHT_DIFF, MIN_N_MATCHED
    global possible_contours
    if inImage == None:
        return
    img_car = cvPhoto
    # 높이, 너비, 크기 채널 조절
    height, width, channel = img_car.shape
    # 이미지를 GrayScale로 전환
    gray = cv2.cvtColor(img_car, cv2.COLOR_BGR2GRAY)
    # 가우시안 blur + Threshold 진행.
    img_blurred = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0)
    img_blur_thresh = cv2.adaptiveThreshold(
        img_blurred,
        maxValue=255.0,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY_INV,
        blockSize=19,
        C=9
    )
    # 윤곽선 그리기(컨투어 과정)
    contours2, _ = cv2.findContours(
        img_blur_thresh,
        mode=cv2.RETR_LIST,  # 모든 컨투어 라인을 찾지만, 상하구조 관계를 구성하지않음.
        method=cv2.CHAIN_APPROX_SIMPLE  # 컨투어인을 그릴 수 있는 포인트만 반환
    )
    # height, width, channel 크기에 맞게, 0으로 초기화
    temp_result2 = np.zeros((height, width, channel), dtype=np.uint8)

    cv2.drawContours(temp_result2, contours=contours2, contourIdx=-1, color=(255, 255, 255))
    ## findContours에서 있던 것을 drawContours를 통해 그림을 그릴 수 있음.

    # 윤곽선을 직사각형으로 만들기.
    contours_dict = []
    for contour in contours2:
        x, y, w, h = cv2.boundingRect(contour)  # cv2.boundingRect() 윤곽선을 감싸는 사각형을 구한다. => 사각형 범위 찾기
        cv2.rectangle(temp_result2, pt1=(x, y), pt2=(x + w, y + h), color=(255, 255, 255),
                      thickness=2)  # 이미지에 사각형을 그린다.
        # dict에 데이터 삽입
        contours_dict.append({  # boundingRect에 해당하는 값들을 저장.
            'contour': contour,
            'x': x,
            'y': y,
            'w': w,
            'h': h,
            'cx': x + (w / 2),  # (cx,cy)는 중심 좌표.
            'cy': y + (h / 2)
        })
    # 위에서 네모를 다음 구간으로 추릴 것임.
    MIN_AREA = 80  # boundingRect의 최소 넓이는 80
    MIN_WIDTH, MIN_HEIGHT = 2, 8  # boundingRect의 최소 너비와 높이는 2, 8로 지정.
    MIN_RATIO, MAX_RATIO = 0.25, 1.0  # boundingRect의 가로, 세로 비율의 최소와 최대

      # 가능한 boundingRect를 다 저장할 것임.

    cnt = 0
    for d in contours_dict:
        area = d['w'] * d['h']  # 넓이 = 가로 * 세로
        ratio = d['w'] / d['h']  # 비율 = 가로 / 세로

        # 위 조건들을 확인하며, 번호판 확률이 높은 친구들을 possible_contours에 저장하자.
        if area > MIN_AREA and d['w'] > MIN_WIDTH and d['h'] > MIN_HEIGHT \
                and MIN_RATIO < ratio < MAX_RATIO:
            d['idx'] = cnt
            cnt += 1
            ## 각 윤곽선의 idx 값을 매겨 놓고, 나중에 조건에 맞는 윤곽선들의 idx만 따로 빼내기 위해 idx 값 지정.
            possible_contours.append(d)

    # 9. 조건에 맞는 boundingRect를 추려보기
    temp_result2 = np.zeros((height, width, channel), dtype=np.uint8)  # 값을 초기화 시키기.

    for d in possible_contours:
        cv2.rectangle(temp_result2, pt1=(d['x'], d['y']), pt2=(d['x'] + d['y'], d['y'] + d['h']), color=(255, 255, 255),
                      thickness=2)

    result_idx = find_chars(possible_contours)

    matched_result = []
    for idx_list in result_idx:
        matched_result.append(np.take(possible_contours, idx_list))  # 전체와 부분을 비교해본다.

    # 10. matched_result 시각화 진행 => 최종적으로 번호판 위치를 확인하기 위함.
    temp_result2 = np.zeros((height, width, channel), dtype=np.uint8)

    for r in matched_result:
        for d in r:
            cv2.rectangle(temp_result2, pt1=(d['x'], d['y']), pt2=(d['x'] + d['w'], d['y'] + d['h']),
                          color=(255, 255, 255), thickness=2)

    # 비틀어진 이미지 바로 만들기.
    # Affine Transform 활용 -> 비틀어진 이미지를 바로 만들기.
    PLATE_WIDTH_PADDING = 1.3
    PLATE_HEIGHT_PADDING = 1.5
    MIN_PLATE_RATIO = 3
    MAX_PLATE_RATIO = 10
    # triangle_height = 1
    # triangle_hypotenus = 1
    # plate_cx = 1
    # plate_cy = 1
    # plate_width = 1
    # plate_height = 1



    for i, matched_chars in enumerate(
            matched_result):  # enumerate => (인덱스, 컬렉션의 원소) 형태로 추출 -> 참고 사이트 : https://wikidocs.net/16045
        sorted_chars = sorted(matched_chars, key=lambda x: x['cx'])  # x 방향으로 순차적으로 정렬 해주기.

        #  노트참고5
        # plate의 cx, cy, width, height를 계산함. => plate_x, plate_y, plate_width, plate_height가 변수임.
        plate_cx = (sorted_chars[0]['cx'] + sorted_chars[-1]['cx']) / 2  # center x => (처음 + 마지막) / 2 => central x
        plate_cy = (sorted_chars[0]['cy'] + sorted_chars[-1]['cy']) / 2  # center y => (처음 + 마지막) / 2 => central y

        plate_width = (sorted_chars[-1]['x'] + sorted_chars[-1]['w'] - sorted_chars[0]['x']) * PLATE_WIDTH_PADDING

        sum_height = 0
        for d in sorted_chars:
            sum_height += d['h']

        plate_height = int(sum_height / len(sorted_chars) * PLATE_HEIGHT_PADDING)

        # 수평선을 기준으로 비틀어진 각도를 바로 잡기 위함.
        # 각도를 계산하기 위해 arcsin 사용.
        triangle_height = sorted_chars[-1]['cy'] - sorted_chars[0]['cy']  # 컨투어끼리에서 높이 계산
        triangle_hypotenus = np.linalg.norm(  # contour간의 대각선 길이 계산
            np.array([sorted_chars[0]['cx'], sorted_chars[0]['cy']]) - np.array([sorted_chars[-1]['cx'], sorted_chars[-1]['cy']])
        )
    # '라디안' -> '도'로 전환
    angle = np.degrees(np.arcsin(triangle_height / triangle_hypotenus))

    # RotationMatrix를 구하기.
    rotation_matrix = cv2.getRotationMatrix2D(center=(plate_cx, plate_cy), angle=angle, scale=1.0)

    # 비틀어진 이미지를 바로 잡기. => warpAffine() 활용. ---> getRotationMatrix2D가 전제.
    img_rotated = cv2.warpAffine(img_blur_thresh, M=rotation_matrix, dsize=(width, height))

    # 목표1. 번호판 위치 찾기 완료.
    # 바로잡은 사진에서 원하는 부분만 사진으로 추출. => getRectSubPix() 함수 사용.
    img_cropped = cv2.getRectSubPix(
        img_rotated,
        patchSize=(int(plate_width), int(plate_height)),
        center=(int(plate_cx), int(plate_cy))
    )

    resize_plate = cv2.resize(img_cropped, None, fx=1.8, fy=1.8,
                              interpolation=cv2.INTER_CUBIC + cv2.INTER_LINEAR)
    _, th_plate = cv2.threshold(resize_plate, 150, 255, cv2.THRESH_BINARY)

    # 파일을 쓸 것임. => 저장을 해야 좀 더 진하게 읽어올 수 있음. => 따라서 임시 사진인, temp.jpg 생성.
    cv2.imwrite('C:/programming/myPyCode/BigData/Final_Prjoect/image/temp.jpg', th_plate)

    # 파일 읽어들일 것. => 훨씬 구분을 잘함.
    from PIL import Image
    Image = Image.open('C:/programming/myPyCode/BigData/Final_Prjoect/image/temp.jpg')

    chars = pytesseract.image_to_string(Image)  # 이미지에서 string을 뽑아내라.

    print(chars)
    plt.imshow(Image, cmap='gray')
    plt.show()

####################
#### 전역변수 선언부 ####
####################
R, G, B = 0, 1, 2
inImage, outImage = [], []  # 3차원 리스트(배열)
inH, inW, outH, outW = [0] * 4
window, canvas, paper = None, None, None
filename = ""
VIEW_X, VIEW_Y = 512, 512 # 화면에 보일 크기 (출력용)
MAX_DIAG_MULTIPLYER = 5  # diag의 중심점끼리의 거리가 diag length의 __ 배 안쪽으로 있어야 함.
MAX_ANGLE_DIFF = 12.0  # contour와 contour와의 각도 최댓값
MAX_AREA_DIFF = 0.5  # contour와 contour 면적 차이가 ___이하(비율로 계산할 것임)
MAX_WIDTH_DIFF = 0.8  # contour와 contour의 너비 차이가 ____ 이하(비율로 계산할 것임)
MAX_HEIGHT_DIFF = 0.2  # contour와 contour의 높이 차이가 ____ 이하(비율로 계산할 것임)
MIN_N_MATCHED = 7
possible_contours = []

####################
#### 메인 코드부 ####
####################
window = Tk()
window.geometry("500x500")
window.title("컴퓨터 비전(딥러닝-칼라) ver 0.1")

status = Label(window, text='이미지 정보:', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=openImageColor)
fileMenu.add_separator()
fileMenu.add_command(label="파일 저장", command=saveImageColor)

openCVMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="이미지 인식", menu=openCVMenu1)
openCVMenu1.add_command(label="자동차 번호판 인식", command=carNumberOpenCV)

window.mainloop()