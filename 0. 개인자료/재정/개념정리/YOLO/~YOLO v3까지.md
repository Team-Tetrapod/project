## Image Detection 개괄

![1571229541260](C:\Users\u37c\Desktop\CNN 변천사)

배경

- 2012년
  - Image Classification은 AlexNet의 등장으로 주목
- 2014년
  - GoogleNet과 VGGNet 등장으로 가속화
- 2015년
  - ResNet의 등장으로 딥러닝이 드디어 인간의 판단능력보다 더 우위에 설 수 있게 됨.
  - 이때 Image Classification에서 특정 class가 Image에 어디에 있는지 예측하는 Localization 문제를 풀고자 노력
  - 이후, 이미지 안에 여러가지의 물체가 어디에 있는지와 그 물체는 어떤 종류의 물체이지를 판단하는 Image Detection에 연구에 관심.



![1571229603614](C:\Users\u37c\AppData\Roaming\Typora\typora-user-images\1571229603614.png)

- One stage method
  - 한 번만에 Image detection을 할 수 있음.
  - YOLO, SSD 등
- two stage method
  - 두 번만에 Image detection을 할 수 있음.
  - R-CNN 계열

Image Detection의 기본 3요소

- Detection
  - 탐지, 검출
- Classification
  - 분류
- Segmentation
  - 추출



### YOLO v1 

![1571229845367](C:\Users\u37c\Desktop\YOLO_Single Neural Network)

- 특징

  - Detection System이다.

- 원리

  - YOLO는 인간의 시각체계와 비슷하게 작동하게끔 모델을 single neural network로 구성
  - bounding box(물체를 싸고 있는)와 그 박스 안에 물체의 종류를 동시에 예측하는 Regression 문제로 Image Detection을 해결
    - 즉, Input 이미지가 있으면, 하나의 신경망을 통과하여 물체의 bounding box와 class를 동시에 예측

- 장점

  - 빠르다

    ![1571230671831](C:\Users\u37c\Desktop\YOLO 빠르다)

  - 다른 알고리즘과 비슷한 정확도를 가진다

    ![1571230861827](C:\Users\u37c\Desktop\비슷한 성능)
    - fast R-CNN과 결합하면 더 좋은 성능을 보임.
      - YOLO는 Background 에러를 줄이는데 사용하고 거기에서 비슷한 바운딩 박스의 RCNN 예측값과 비교해 결과 산출
        - Background란 특정 물체로 오판정하는 경우를 의미.

  - 다른 도메인에서 좋은 성능을 보인다.

    ![1571230944887](C:\Users\u37c\Desktop\YOLO 더 좋은 성능)

- 한계점
  - 각 grid cell은 하나의 클래스만을 예측
    - 즉, object가 겹쳐서 있으면 제대로 예측 X
  - Bouding Box 형태가 training data를 통해서만 학습되므로, 새로운/독특한 형태의 bounding box의 경우 정확히 예측하지 못함.
  - 작은 Boundding box의 loss term이 IOU에 더 민감하게 영향을 줌. localization이 다소 부정확.
    - Localizaion이란 Bounding Box의 위치가 얼마나 정확한가?
- 참고자료
  - <https://taeu.github.io/paper/deeplearning-paper-yolo1-01/>



### SSD: Single Shot Multibox Detector 

![1571231627583](C:\Users\u37c\Desktop\SSD 모델)

- 정의

  - 아웃풋을 만드는 공간을 나눈다.
  - 각 피쳐맵(아웃풋맵)에서 다른 비율과 스케일로 기본 box를 생성하고 모델을 통해 계산된 좌표와 클래스값에 기본 box를 활용해 최종 bounding box를 생성함.

- 원리

  참고자료를 보는게 더 좋을듯.

- 장점

- 한계점

- 참고자료

  <https://taeu.github.io/paper/deeplearning-paper-ssd/>



### YOLO v2

### (YOLO9000: Better Faster, Stronger 분석)

개괄적인 사진

- 원리

  - Better
    - Accuracy, mAP 측면의 개선사항
    - detection dataset에서 k-means 알고리즘을 활용해 하이퍼파라미터들을 설정
  - Faster
    - Darknet. 
      - 많은 Image Detection Model에서 classifier network로 VGG Net을 많이 씀.
      - GoogleNet을 기반으로한 독자적인 arknet을 만들어 30십억의 계산량을 8십억으로 줄임.
    - Training for classification
    - Training for detection
  - Stronger
    - 더 많은, 다양한 클래스 예측
    - training 때 classification과 detection data를 섞어서 씀.
    - data set에서 detection data가 들어오면 원래 loss function을 활용해 계산
    - data set에서 classification data가 들어오면 loss function에서 classification loss만 활용해 계산

- 장점

  - Stronger 즉, 다양한 detection을 하기 위한 새로운 시도가 가능해짐.
    - detection label 데이터가 그만큼 많이 받쳐준다면 학습이 잘 될것임.

- 한계점

  - 부수적이고 작은거 제외하곤 문제 X
    - Real time, 속도를 고려했을 때 trade-off가 발생 한다는 점.

- 참고자료

  <https://taeu.github.io/paper/deeplearning-paper-yolov2/>



### YOLO v3

- 원리

  - Bounding Box Prediction

    ![1571232836150](C:\Users\u37c\Desktop\YOLOv3 Bounding box)

    - YOLO v1과 다르게 각각의 Bounding Box마다 objectness score(그 바운딩박스에 물체가 있는지 없는지)를 예측하고, 이때 prior box(anchor box)와 ground truth box의 IOU가 가장 높은 박스를 1로 두어 매칭(Loss를 prior box와 같은 index, 위치를 가지는 predicted box의 offset만 계산해주겠다는 의미이고 SSD와 다른 알고리즘과는 다르게 Best IOU에 대해서만 1값을 가지게 했다. 나머지는 무시.)

  - Class Prediction

    - multi-label이 있을 수 있으므로 class prediction으로 softmax를 쓰지 않고 independenct logistic classifier를 사용.
    - loss term도 bianry cross-entropy로 바꿈.
    - 이는 좀 더 복잡한 데이터셋을 학습하는데 도움이 됨.

  - Preictions Acrross Scales

    - 3개의 bounding box
    - 3개의 feature map 활용(다른 scale, 각각 2배씩 차이)

  - Feature Extractor

    - Darknet-19 -> Darknet-53으로 변경, 모델과 성능은 아래와 같음.

      ![1571232992675](C:\Users\u37c\Desktop\Darknet53)

      ​	![1571233015595](C:\Users\u37c\Desktop\Darknet53과 비교)

- 특징

  - 욜로 표적 탐지 원리

    - 최종 공지 속도 깊이 연구에 기초하여 실시간으로 타겟 검출 방법

  - YOLO v3 구현 다크 깊은 학습 C 언어 개발, 덜 의존, 휴대 경량의 오픈 소스 프레임워크를 사용하는 것임.

  - 사건을 읽고 우리가 그 구현 원리를 탐구할 수 있는 좋은 코드 역할.

  - 소스

    - C언어로 구성

      - 컴파일한 실행파일에 학습 시킨 cfg 파일과 이미지 파일을 입력하면, 현재 280개 정도의 아이템이 인식

      ![1571233223300](C:\Users\u37c\Desktop\인식 전, 후)

- 장점

  - Image Detection에서 세심한 부분까지 다 건드릴 수 있음.

    ![1571233528938](C:\Users\u37c\Desktop\YOLOv3의 장점)

    

- 한계점

- 참고자료

  <https://taeu.github.io/paper/deeplearning-paper-yolov3/>







https://taeu.github.io/paper/deeplearning-paper-yolo1-01/

(참고 링크)