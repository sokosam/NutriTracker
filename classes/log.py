import customtkinter as ctk

class log(ctk.CTkToplevel):
    def __init__(self, top):
        super().__init__(top)
        self.geometry("800x550")
        self.version = "p.0.1.2"
        self.title("Change Log " + self.version)

        frame = ctk.CTkFrame(master = self)
        frame.pack(pady=20,padx=20,expand=True, fill="both")

        label = ctk.CTkLabel(master= frame, text= "Change Log", font= ("Roboto",36))
        label.pack(pady=20,padx=20)


        textbox = ctk.CTkTextbox(master =frame, height=600, width=600 )
        textbox.pack(pady=20,padx=20)
        text = """
                Update %s - 10/22/2023
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



