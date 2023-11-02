import customtkinter as ctk

class log(ctk.CTkToplevel):
    def __init__(self, top):
        super().__init__(top)
        self.geometry("800x550")
        self.version = "p.0.1.3"
        self.title("Change Log " + self.version)
        self.after(10,self.focus)
        self.grab_set()

        frame = ctk.CTkFrame(master = self)
        frame.pack(pady=20,padx=20,expand=True, fill="both")

        label = ctk.CTkLabel(master= frame, text= "Change Log", font= ("Roboto",36))
        label.pack(pady=20,padx=20)


        textbox = ctk.CTkTextbox(master =frame, height=600, width=600 )
        textbox.pack(pady=20,padx=20)
        text = """
                Update %s - 11/1/2023
                    - Nutrition targets added
                    - Nutrition target setter added
                    - Updated where the color of the progress bar turns red when the target is overmet
                    - Updated where the color will change back to normal if the target is updated
                      and current nutrition is less than target

                Update p.0.1.2 - 10/22/2023
                    - Nutritions extracted and saved 

                Update p.0.1.1 - 10/12/2023
                    - Can now change uploaded image
                    - Upload box focused when opened

                Update p.0.1.0 - 10/11/2023
                    - Change Log added
                    - Start Menu added
                    - Main menu added
                    - Picture upload added
                """ % self.version
        textbox.insert("0.0", text)

        self.mainloop()



