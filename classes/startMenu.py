import customtkinter as ctk
import log
import menu

class startMenu(ctk.CTk):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")        
    def __init__(self):
        super().__init__()
        self.geometry("500x300")
        self.title("NutriTracker")

        frame = ctk.CTkFrame(master= self)
        frame.pack(pady=20,padx=60,fill='both',expand=True)

        labelStart = ctk.CTkLabel(master=frame, text= "NutriTracker", font=("Roboto", 24))
        labelStart.pack(pady=20,padx=12)

        def start():
            self.destroy()
            a = menu.menu()

        startButton = ctk.CTkButton(master=frame, text= "Start", font=("Roboto", 16), command=start)
        startButton.pack(pady=20,padx=10)       
        
        def openLogs():
            gui2 = log.log(self)

        changeLog = ctk.CTkButton(master = frame, text= "Change Log", font=("Roboto", 16), command=openLogs )
        changeLog.pack(pady=5, padx=10)

        self.mainloop()


if __name__ == "__main__":
    start = startMenu()



