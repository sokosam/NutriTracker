import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import pytesseract as pyt 
from pytesseract import Output
import cv2 
from helper import *
import os
from PIL import Image
import numpy as np
import FloatSpinbox

workDir = os.getcwd()   
pyt.pytesseract.tesseract_cmd = workDir + "/tes/tesseract.exe"

class menu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1250x1000")
        self.title("NutriTracker")
        self.imgpath = ""
        self.foundImg = False
        self.img = None
        self.lab = None
        self.vals = {"Carbohydrates": 0, "Fats": 0, "Protein": 0, "Calcium": 0, "Fiber": 0, "Iron": 0, "Calories": 0, "Sugars": 0}
        self.target = [400, 44, 80, 250, 30, 50, 3000, 30]
        self.progress = []
        self.progressLabels = []
        

        frame = ctk.CTkFrame(master=self)
        frame.pack(pady=20,padx=20, fill="both", expand = True)

        for q,i in enumerate(self.vals):
            x = ctk.CTkProgressBar(master=frame)
            x.place(x=100,y=20 + q*20)
            x.set(value = 0)
            t = i + " 0/" +str(self.target[q])
            y = ctk.CTkLabel(master =frame, text = t )
            y.place(x=325, y = 8+q*20)
            self.progress.append(x)
            self.progressLabels.append(y)
        
        def setProgress():
            z = 0
            try:
                for i in self.vals:
                    self.progress[z].set(value= self.vals[i]/self.target[z])
                    t = i +" " + str(self.vals[i]) + "/" + str(self.target[z])
                    self.progressLabels[z].configure(text = t)
                    if self.vals[i]/self.target[z] > 1:
                        self.progress[z].configure(progress_color = 'red')
                    else:
                        self.progress[z].configure(progress_color = ["#3a7ebf", "#1f538d"])
                    z+=1
            except IndexError:
                for i in self.progress:
                    i.set(value = 0)
                    t = i +" 0/" + str(self.target[z]) 
                    self.progressLabels[z].configure(text = t)
                    z+=1

        def targetBox():
            box = ctk.CTkToplevel()
            box.title("Define your nutritional targets")
            box.geometry("1200x200")
            box.after(10,box.focus)
            box.grab_set()
            box.resizable(0,0)

            framebox = ctk.CTkFrame(master = box)
            framebox.pack(pady= 20, padx=20, fill = "both", expand = False)

            spinBox = []
            labels = []
            keys = list(self.vals.keys())
            for i,t in enumerate(self.target):
                x = FloatSpinbox.FloatSpinbox(box, width=100, step_size= 25)
                x.place(x= 65 + i*137.5, y =50)
                x.set(t)

                y = ctk.CTkLabel(master = framebox, text = keys[i])
                y.place(x=50 + i* 137.5, y = 75)
                labels.append(y)
                spinBox.append(x)
            
            def setTargets():
                for i,b in enumerate(spinBox):
                    self.target[i] = b.get()
                setProgress()
                box.destroy()

            but=  ctk.CTkButton(master= framebox, text= "Set", command= setTargets)
            but.place(x= 500,y = 125)

        def displayImg() -> None:
            newWind = ctk.CTkToplevel()
            newWind.geometry("500x600")
            newWind.after(10,newWind.focus)
            newWind.grab_set()
            newWind.title("Find your image")
            newWind.resizable(0,0)

            frame1 = ctk.CTkFrame(master = newWind)
            frame1.pack(pady=20,padx=20, fill ='both', expand= True)

            def upload() -> None:
                filename = filedialog.askopenfilename(title="Open File")
                self.imgpath = filename
                newWind.after(10,newWind.lift)
                if filename:
                    try:
                        if not self.lab:
                            self.img = ctk.CTkImage(light_image=Image.open(os.path.abspath(filename)), size =(450,500))
                            self.lab = ctk.CTkLabel(master = frame1, image=self.img, text= "")
                            self.lab.pack(pady=10,padx=10)
                        else:
                            self.lab.destroy()
                            self.img = ctk.CTkImage(light_image=Image.open(os.path.abspath(filename)), size =(450,500))
                            self.lab = ctk.CTkLabel(master = frame1, image=self.img, text= "")
                            self.lab.pack(pady=10,padx=10)
                        self.foundImg = True
                    except Exception as e:
                        self.lab = ctk.CTkLabel(master=frame1, text=f"Not a valid picture file (Error: {e})")
                        self.lab.pack(pady=10,padx=10)
                        self.foundImg = False


            def confirmFile():
                if self.foundImg:
                    newWind.destroy()
                    self.after(10, self.focus)
                    self.foundImg = False
                    self.img = cv2.imread(self.imgpath)
                    sharpen_kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])  
                    self.img = cv2.filter2D(self.img,-1,sharpen_kernel)
                    self.results = pyt.image_to_data(self.img, lang ="eng", config="--psm 4",output_type=Output.DICT)
                    x = process(self.results)
                    for i in x:
                        if self.vals[i] == 0:
                            self.vals[i] = x[i]
                        else:
                            self.vals[i] += x[i]
                    setProgress()
                    print(self.vals)


                else:
                    if self.lab== None:
                        self.lab = ctk.CTkLabel(master=frame1, text="No Picture Selected!")
                        self.lab.pack(pady=10,padx=10)
                    else:
                        self.lab.pack(pady=10,padx=10)
                        self.lab.configure(text="No Picture Selected!")
                  

            getImg = ctk.CTkButton(master= frame1, text= "Find Image", command=upload)
            getImg.place(relx = 0.33, y = 530, anchor = ctk.CENTER)

            confirm = ctk.CTkButton(master= frame1, text= "Confirm Image", command=confirmFile)
            confirm.place(relx = 0.66, y = 530, anchor = ctk.CENTER)
    
            newWind.mainloop()
        self.label1 = ctk.CTkLabel(master= frame, text="Upload your image", font=("Roboto",16))
        self.label1.pack(pady=10,padx=10)

        self.button1 = ctk.CTkButton(master=frame, text="Upload Nutritional Values", command = displayImg)
        self.button1.pack(pady= 10, padx= 10)

        self.label2 = ctk.CTkLabel(master= frame, text=  "Set your targets")
        self.label2.pack(pady=10, padx= 10)
        
        self.button2 = ctk.CTkButton(master = frame, text= "Click to set nutritional targets", command = targetBox)
        self.button2.pack(pady=10,padx=10)
        
        self.mainloop()



