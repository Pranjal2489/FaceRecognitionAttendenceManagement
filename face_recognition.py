from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import cv2.face
import mysql.connector
import cv2
import os
from datetime import datetime
from time import strftime

class Face_Recognitation:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1368x720+0+0")
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root, text="FACE RECOGNITION", font=("times new roman", 35, "bold"), bg="white", fg="green")
        title_lbl.place(x=0, y=0, width=1366, height=45)

        img_top = Image.open(r"C:\Users\hp\Desktop\vFolder\face_recognition_system\images\face.jpg")
        img_top = img_top.resize((550, 650), Image.BILINEAR)  
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_lbl = Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0, y=55, width=550, height=650)

        img_bottom = Image.open(r"C:\Users\hp\Desktop\vFolder\face_recognition_system\images\backimg.jpg")
        img_bottom = img_bottom.resize((850, 700), Image.BILINEAR)
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)

        f_lbl = Label(self.root, image=self.photoimg_bottom)
        f_lbl.place(x=550, y=55, width=850, height=650)

        b1_1 = Button(f_lbl, text="FACE RECOGNITION", cursor="hand2", font=("times new roman", 18, "bold"),
                      bg="dark green", fg="white", command=self.face_recog)
        b1_1.place(x=365, y=570, width=250, height=45)

    # def mark_attendance(self, i, r, n, d):
    #     with open("attendance.csv", "a") as f:
    #         now = datetime.now()
    #         dtString = now.strftime("%H:%M:%S")
    #         d1 = now.strftime("%d/%m/%Y")
    #         f.write(f"\n{i},{r},{n},{d},{dtString},{d1},Present")


# ============attendence=============="r+", newline="\n"


    def mark_attendance(self, i, r, n, d):
        with open(r"C:\Users\hp\Desktop\vFolder\face_recognition_system\pranjal.csv","r+", newline="\n") as f:
            # Read all lines to check existing attendance
            lines = f.readlines()
            name_list = [line.split(",")[0] for line in lines]

            # Check if attendance already exists
            if i not in name_list:
                now = datetime.now()
                
                d1 = now.strftime("%d/%m/%Y")
                dtString = now.strftime("%H:%M:%S")
                # Move the file pointer to the end for writing new entry
                f.seek(0, 2)
                f.write(f"\n{i},{r},{n},{d},{dtString},{d1},Present")


    def face_recog(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbours, color, text, clf):
            # clf = cv2.face.LBPHFaceRecognizer.create()
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features=faceCascade.detectMultiScale(gray_image,1.3,5)
            # features=cv2.CascadeClassifier.detectMultiScale(gray_image,scaleFactor,minNeighbours)
            # features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbours)
            coord=[]
            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
                # id, predict=cv2.face.LBPHFaceRecognizer.predict(gray_image[y:y+h,x:x+w])
                # clf = cv2.face.LBPHFaceRecognizer.create()
                
                id, predict = clf.predict(gray_image[y:y+h,x:x+w])
            
                # id, predict=clf.predict(gray_image[y:y+h,x:x+w])
                # id, predict = clf.predict(gray_image[y:y + h, x:x + w])
                confidence = int((100 * (1 - predict / 300)))

                conn = mysql.connector.connect(host="localhost", username="root", password="Pranjal8924",
                                               database="facial_recognition_sytem")
                my_cursor = conn.cursor()

                my_cursor.execute("select Name from student where Student_id=" + str(id))
                n = my_cursor.fetchone()
                n = "+".join(n) if n is not None else "Pranjal"

                my_cursor.execute("select Roll from student where Student_id=" + str(id))
                r = my_cursor.fetchone()
                r = "+".join(r) if r is not None else "17042100303"

                my_cursor.execute("select Dep from student where Student_id=" + str(id))
                d = my_cursor.fetchone()
                d = "+".join(d) if d is not None else "Electronics"

                my_cursor.execute("select Student_id from student where Student_id=" + str(id))
                i = my_cursor.fetchone()
                i = "+".join(i) if i is not None else "2020010007258"

                if confidence > 77:
                    cv2.putText(img, f"ID: {i}", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Roll: {r}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Name: {n}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Department: {d}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    self.mark_attendance(i, r, n, d)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown face", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                
                
                coord=[x,y,w,y]
            return coord    
        def recognize(img, clf, faceCascade):
            coord = draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 255), "Face", clf)
            return img

        faceCascade = cv2.CascadeClassifier(r"C:\Users\hp\Desktop\vFolder\face_recognition_system\haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer.create()
        clf.read(r"C:\Users\hp\Desktop\vFolder\classifier.xml")

        video_cap = cv2.VideoCapture(0)

        while True:
            ret, img = video_cap.read()
            img = recognize(img, clf, faceCascade)
            cv2.imshow("Welcome to Face Recognition", img)

            if cv2.waitKey(1) == 13:
                break

        video_cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognitation(root)
    root.mainloop()