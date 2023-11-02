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
        self.vals = {"carbohydrate": 0, "fat": 0, "protein": 0, "calcium": 0, "fiber": 0, "iron": 0, "calories": 0, "sugars": 0}
        self.target = [400, 44, 80, 250, 30, 50, 3000, 30]
        self.progress = []

        frame = ctk.CTkFrame(master=self)
        frame.pack(pady=20,padx=20, fill="both", expand = True)

        for i in self.vals:
            x = ctk.CTkProgressBar(master=frame)
            x.pack(pady=10,padx=10)
            self.progress.append(x)
        
        def setProgress():
            z = 0
            for i in self.vals:
                self.progress[z].set(value= self.vals[i]/self.target[z])
                if self.vals[i]/self.target[z] > 1:
                    self.progress[z].configure(progress_color = 'red')
                z+=1


        def displayImg() -> None:
            newWind = ctk.CTkToplevel()
            newWind.geometry("500x600")
            newWind.after(10,newWind.focus)
            newWind.grab_set()

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
        self.label1.pack(side=ctk.LEFT)

        self.button1 = ctk.CTkButton(master=frame, text="Upload Nutritional Values", command = displayImg)
        self.button1.pack(pady= 10, padx= 10)

 
        # self.progressBar = ctk.CTkProgressBar(master=frame)
        # self.progressBar.pack(pady=10,padx=10)
        # self.progressBar.set(value=0.1)

        
        self.mainloop()



