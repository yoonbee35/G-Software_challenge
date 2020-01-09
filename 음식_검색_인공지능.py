#!/usr/bin/env python
# coding: utf-8

# In[28]:


from PIL import ImageGrab
import cv2
from selenium import webdriver 
from keras.models import load_model
import os

print("잠시후 캡쳐된 화면에서 찾고자 하는 음식의 왼쪽 위, 오른쪽 아래를 각각 클릭해주세요")


model=load_model('food_classfication_git_ver(31개,58.13%).h5')

#스크린 전체를 캡쳐해서 screenshot.png로 저장
img=ImageGrab.grab()
saveas='screenshot.png'
img.save(saveas)

#캡쳐한 screenshot.png에서 음식이 있는 부분을 클릭을 통하여 ROI로 설정 (왼쪽 위 더블클릭, 오른쪽 아래 더블클릭)
def on_mouse(event, x, y, flags, param):
      if event == cv2.EVENT_LBUTTONUP:
            points.append([x, y])
            

points = list()
img=cv2.imread('screenshot.png')
img=cv2.resize(img,dsize=(1280,720),interpolation=cv2.INTER_AREA)
            
cv2.namedWindow('img')
cv2.setMouseCallback('img', on_mouse)
cv2.imshow("img", img)

#Mouse Event를 사용하여 ROI 설정
while True:
     if len(points) == 2:
        x = points[0][0]
        y = points[0][1]
        ROI = img[y:points[1][1], x:points[1][0]]
        break 
     cv2.waitKey(30)

#설정한 ROI가 맞는지 확인하고 맞다면 ESC를 눌러 창을 종료
cv2.imshow("ROI", ROI)
cv2.waitKey(0)
cv2.destroyAllWindows()


#image classification을 위한 ROI resize및  predict
img=ROI
#img=img.resize(105,500,3)
dst = cv2.resize(img, dsize=(224,224), interpolation=cv2.INTER_AREA)
dst=dst.reshape(1,224,224,3)
predict = model.predict_classes(dst)


# In[29]:


#dataset의 class들을 이름으로 표현하고 predict값과 class의 이름을 동일화

path_dir="images"
file_list=os.listdir(path_dir)

#predict된 class의 이름을 keyword로 지정
keyword=file_list[predict[0]]

print("검색하신 음식은", keyword,"입니다.")


# In[30]:


#selenium을 이용하여 다음 카카오맵에서 자동으로 predict한 class 키워드 검색 -> 주변 음식점 찾기
driver = webdriver.Chrome('chromedriver.exe') 
print("현재위치 주변",keyword,"음식점을 검색하고 있습니다. 잠시만 기다려주세요.")
driver.implicitly_wait(3) 
driver.get('https://map.kakao.com/')
ele1=driver.find_element_by_id("search.keyword.query")
ele1.send_keys(keyword)
ele1.send_keys('\n')


# In[ ]:




