import pytesseract
from PIL import Image
import matplotlib.pyplot as plt

Image = Image.open('C:/images/exercise/car3.png')
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract"
result = pytesseract.image_to_string(Image)

with open('C:/images/exercise/picture.txt', mode = 'w') as file:
    file.write(result)
    print("finsh!!!")

print(result)

plt.imshow(Image, cmap= 'gray')
plt.show()