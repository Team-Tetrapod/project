# CUDA 환경 구성

제작년에 keras로 CUDA환경을 구축하려다가 정말 정보의 심각한 부족으로 실패한 적이 있었는데, 이번에는 별 문제 없이 한번에 성공하여서 그 과정을 기록하려고 합니다.



저에게도 의미있는 기록이지만, 다른 분들도 많은 도움이 되셨으면 좋겠네요.





이번에는 keras같은 상위 wrapper 없이 텐서플로 그대로 진행하였습니다.



도움을 많이 받은 문서는

https://www.tensorflow.org/install/gpu

로, 텐서플로 페이지 자체에서 제공해주고 있습니다.



아래는 제 컴이 윈도우즈인 관계로 윈도우즈를 기본으로 합니다.

만약 linux와 같은 운영체제이신 경우 위의 텐서플로 홈페이지에서 리눅스는 어떻게 설치하는지 잘 알려줍니다!



1) 본인의 GPU가 CUDA GPU 환경을 제공하는지를 확인해 봅니다.

기본적으로 CUDA가 엔비디아nVidia사에서 만든 플랫폼이므로 엔비디아의 지포스 제품이면 일단 가능성은 있지 않을까 생각해 볼 수 있을 것 같습니다.

그리고 GTX 붙으면 일단 된다고 보시면 될 것 같습니다.

요기로 가시면 CUDA가 가능한 GPU인지 확인해 보실 수 있습니다. https://developer.nvidia.com/cuda-gpus

저는 GTX 1060이라 묻지도 따지지도 않고  그냥 설치했습니다.



2) 차례대로 NVIDIA® GPU drivers, CUDA® Toolkit, CUPTI, cuDNN을 깔아줍니다.

텐서플로-gpu는 먼저 깔아도 되고 위의 4가지 프로그램을 다 깔고 깔아도 되는 것 같습니다.

CUPTI는 굳이 안깔아도 될 것 같기는 한데, 저번에 한번 CUDA하려다 안되서 작은 가슴에 그냥 깔고 진행했습니다.



2*) gpu환경을 사용하기 위해서는 tensorflow-gpu를 깔아야 합니다. 아나콘다를 사용하시면 아나콘다 프롬프트에서 conda install tensorflow-gpu를, 아니시라면 pip install tensorflow-gpu를 입력하시면 tensorflow-gpu가 깔립니다. tensorflow-gpu가 깔리면, 이전과 같이 import tensorflow하시면 됩니다.



3) 다 깐 뒤에 시스템 PATH를 설정해 주어야 합니다.

여기서는 시스템 PATH를 설정해 주는데, 깔린 위치가 정확해야 합니다.

드라이버와 툴킷을 깔면 설치파일처럼 설치가 되고, CUPTI와 cuDNN은 압축파일로 풀리게 될 것 입니다.

여기서 설치파일은 상관이 없는데, CUPTI과 cuDNN은 압축을 푼 뒤 폴더 이름을 각자 'CUPTI'와 'tools'로 바꾸어 줍니다.

그리고 CUPTI 폴더는 'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\extras'아래에 폴더를 통채로 복사 붙여넣기 해주시고, tools 폴더는 C드라이브 아래 바로 붙여넣어 주세요.



이후 아무 명령 프롬프트나 여시고(예를 들어 실행->cmd)

SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\bin;%PATH%

SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\extras\CUPTI\libx64;%PATH%

SET PATH=C:\tools\cuda\bin;%PATH%

요렇게 세 개를 써주시면 됩니다.



텐서플로에서 9.0만 지원한다고 그래서 찾다가 저는 9.1로 설치하였는데, v10도 텐서플로에서 잘 작동하는 것 같습니다. 만약에 오류가 나시면 v9.1로 시도해 보세요.



4) 제대로 깔려서 gpu에서 사용되는지 확인하기 위해서

파이썬을 켜시고(명령프롬프트에서 python 치셔도 되고, jupyter notebook에서 cell에 입력하셔도 됩니다.)

from tensorflow.python.client import device_lib 

print(device_lib.list_local_devices())

이렇게 입력해서 무언가 주르륵 나온다 하면 설치가 제대로 된 것입니다.

그리고 이후에 tensorflow 소스코드에서



device_name = "/gpu:0"

log_device_placement = True



with tf.device(device_name):

​    x = tf.placeholder(tf.float32, shape=[None, 32, 32, 3])

​    y = tf.placeholder(tf.float32, shape=[None, 10])

​    .

​    .

​    .



with tf.Session(config=tf.ConfigProto(log_device_placement=log_device_placement)) as sess:

​    sess.run(tf.global_variables_initializer())

​    .

​    .

​    .



요런식으로 소스 코드를 수정해주시면 프로그램 실행 중 명령 프롬프트에서 실제로 GPU가 사용되는 현황을 볼 수 있습니다.