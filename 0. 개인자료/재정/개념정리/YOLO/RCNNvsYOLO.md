## RCNN

- Two State Detector
  - Object Proposal
  - Object Classification  & Bounding Box Regression
  - 과정
    - 이미지 하나로부터 수천개에 이르는 proposal을 만듬 -> 각각에 대해 분류기(classifier)를 돌려 물체를 검출
  - 문제점
    - 1장을 처리하는데 너무 많은 연산양을 필요
    - RCNN의 경우 수 초의 시간이 필요
    - background noise를 물체로 오인식하는 경우가 많음
      - (우리가 RCNN으로 했을 때 잘 인식하지 못했던 이유 같음.)

## YOLO

- Single Stage Detector

  - 

- 기본방식

  1. 예측하고자 하는 이미지를 SxS Grid cells로 나누고 각 cell마다 하나의 객체를 예측.

     ![1571228386740](C:\Users\u37c\Desktop\YOLO cell 구분)

     - 그리고 미리 설정된 개수의 boundary boxes를 통해 객체의 위치와 크기를 파악.

     - 각 cell마다 하나의 객체만을 예측할 수 있기 때문에 여러 객체가 겹쳐 있으면 몇몇몇의 객체는 탐지를 못할 수 있음.

     각 cell은 다음 조건 하에 예측

     - B개의 boudnary boxes를 예측하고 각 box는 box confidence score를 가지고 있음.
     - 예측된 box 수에 관계없이 단 하나의 객체만 탐지
     - C개의 conditional class probabilities를 예측

     ![1571228566932](C:\Users\u37c\AppData\Roaming\Typora\typora-user-images\1571228566932.png)

<https://wdprogrammer.tistory.com/50>

(YOLO 모델의 원리) - 더 정리 해야 함 













- 종류

  - YOLO
  - YOLOv2

  - YOLOv3

  

  <https://wdprogrammer.tistory.com/50>

  (YOLO 원리)

  

  - 참고
    - YOLOv3
      - 다크 넷(dark net)
        - 정의
          - 특정 프로그램을 사용하는 컴퓨터들끼리 서로 연결된 네트워크
          - 비표준적인 통신 규약과 포트를 사용하는 특정 소프트웨어, 설정, 또는 허가가 있어야 접속할 수 있는 오버레이 네트워크
          - 이러한 네트웍에 접속하는 사용자의 신원과 장소(IP 주소)는 Layered Encryption System을 사용하고 있기 땜ㄴ에, 익명성이 보장되고 추적하기 어려운 특징을 가짐.
        - 개발 목적
          - 정부와 같은 통제기관의 감시와 통제를 피하면서 인터넷을 자유롭게 사용하기 위함.
      - 다크 웹(dark web)
        - 네트워크 상에 존재하는 웹 사이트







## RCNN vs YOLO

![1571226912935](C:\Users\u37c\Desktop\RCNN ~ YOLO')

![1571226978186](C:\Users\u37c\Desktop\1571226978186.png)

- 왼쪽 차트
  - Background란 특정 물체로 오판정하는 경우
  - YOLO가 잘못 Dectect하는 비율
  - Fast RCNN에 비해 월등히 우수
- 오른쪽 차트
  - Bounding Box의 위치가 얼마나 정확한가?
  - Single Stage Detector의 초기 버전이다보니 아무래도 Box의 정확도 면에서 다소 떨어짐.







기타자료

<http://openresearch.ai/t/yolo-you-only-look-once-unifed-real-time-object-detection/67>

(You Only Look Once: Unifed, Real-Time Object Detection)

