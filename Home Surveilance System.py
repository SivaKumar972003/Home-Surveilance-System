import cv2, time
from datetime  import datetime
import argparse
import os

import urllib.request
import io
import tkinter as tk
from PIL import Image, ImageTk

def button_click():
    print("start capturing")


window = tk.Tk()
window.title("Home Surveillance System")


image_url = "https://th.bing.com/th/id/OIP.WmwB18efAKvkYjkiaC73UwHaHa?pid=ImgDet&w=1024&h=1024&rs=1"
image_data = urllib.request.urlopen(image_url).read()
image = Image.open(io.BytesIO(image_data))


photo = ImageTk.PhotoImage(image)


image_label = tk.Label(window, image=photo)
image_label.pack()

text1= tk.Label(window, text="Home Surveillance System", font=("Algerian", 36),fg='red')
text1.pack()
text1.place(x=250,y=150)


button = tk.Button(window, text="CAPTURE IMAGES", command=window.destroy,width=50,height=5,fg='green')
button.place(x=400, y=310)  


button = tk.Button(window, text="CAPTURE IMAGES AND VIDEO", command=window.destroy,width=50,height=5,fg='green')
button.place(x=400, y=410)  

button = tk.Button(window, text="CANCEL", command=window.destroy,width=50,height=5,fg='BLUE')
button.place(x=400, y=510)  

window.mainloop()

face_casacde=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


video = cv2.VideoCapture(0)

while True:
    check,frame=video.read()
    if frame is not None:
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_casacde.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=10)
        for x,y,w,h in faces:
            img=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
            exact_time=datetime.now().strftime('%H-%S')
            cv2.imwrite("face detected"+str(exact_time)+".jpg",img)
#%Y-%b-%d-%H-%S-%f

        cv2.imshow("home surv",frame)
        key=cv2.waitKey(1)

        if key==ord('q'):
            ap=argparse.ArgumentParser()
            ap.add_argument("-ext","--extension",required=False,default='jpg')
            ap.add_argument("-o","--output",required=False,default='output.mp4')
            args=vars(ap.parse_args())


            dir_path='.'
            ext=args['extension']
            output=args['output']


            images=[]

            for f in os.listdir(dir_path):
                if f.endswith(ext):
                    images.append(f)



            image_path=os.path.join(dir_path,images[0])
            frame=cv2.imread(image_path)
            height,width,channels=frame.shape


            forcc=cv2.VideoWriter_fourcc(*'mp4v')
            out=cv2.VideoWriter(output,forcc,5.0,(width,height))


            for image in images:
                image_path=os.path.join(dir_path,image)
                frame=cv2.imread(image_path)
                out.write(frame)

            break


video.release()
cv2.destroyAllWindows
