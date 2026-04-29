from customtkinter import *
from PIL import Image
import os

class MainWindow(CTk):
    def __init__(self):
        super().__init__()

        self.title("fshop")
        self.geometry("500x400")
        
        self.font = CTkFont(family="Arial", size=24)
        self.font2 = CTkFont(family="Arial", size=48, weight="bold")

        self.grid_columnconfigure(0, weight=7, uniform="a")
        self.grid_columnconfigure(1, weight=3, uniform="a")
        self.grid_rowconfigure(0, weight=1)

        self.left_frame = CTkFrame(self, corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        
        self.right_frame = CTkFrame(self, corner_radius=0)
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=1)

        # Image setup
        self.img_path = "img.png"
        if os.path.exists(self.img_path):
            self.original = Image.open(self.img_path)
            self.bgimg = CTkImage(light_image=self.original, dark_image=self.original, size=(500, 400))
            self.background = CTkLabel(self.left_frame, image=self.bgimg, text="")
            self.background.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.left_frame.bind("<Configure>", self.resize_handler)
        
        self.resize_timer = None

        self.app_name_display = CTkLabel(self.left_frame, text="fshop!", font=self.font2, text_color="white", fg_color="transparent")
        self.app_name_display.place(relx=0.5, rely=0.5, anchor="center")

        self.center_frame = CTkFrame(self.right_frame, fg_color="transparent")
        self.center_frame.grid(row=0, column=0, sticky="nsew")
        self.center_frame.grid_columnconfigure(0, weight=1)
        self.center_frame.grid_rowconfigure((0, 5), weight=1)

        self.login_entry = CTkEntry(self.center_frame, placeholder_text="Имя:", height=35)
        self.login_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.pass_frame = CTkFrame(self.center_frame, fg_color="transparent")
        self.pass_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.pass_frame.grid_columnconfigure(0, weight=1)

        self.show_password = False
        self.pass_entry = CTkEntry(self.pass_frame, placeholder_text="пароль:", show="*", height=35)
        self.pass_entry.grid(row=0, column=0, sticky="ew")

        self.eye_btn = CTkButton(self.pass_frame, text="👁️", width=35, height=35, fg_color="gray30", command=self.toggle_password)
        self.eye_btn.grid(row=0, column=1, padx=(5, 0))

        self.login_btn = CTkButton(self.center_frame, text="Login", font=self.font, command=self.check_acc)
        self.login_btn.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.reg_btn = CTkButton(self.center_frame, text="Register", font=self.font, command=self.save_acc)
        self.reg_btn.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

    def resize_handler(self, event):
        if self.resize_timer:
            self.after_cancel(self.resize_timer)
        self.resize_timer = self.after(100, lambda: self.bgimg.configure(size=(event.width, event.height)))

    def toggle_password(self):
        self.show_password = not self.show_password
        self.pass_entry.configure(show="" if self.show_password else "*")
        self.eye_btn.configure(text="🙈" if self.show_password else "👁️")

    def save_acc(self):
        login, pas = self.login_entry.get(), self.pass_entry.get()
        if login and pas:
            with open("accs.txt", "a") as f:
                f.write(f"{login}:{pas}\n")

    def check_acc(self):
        login, pas = self.login_entry.get(), self.pass_entry.get()
        if not os.path.exists("accs.txt"): return
        with open("accs.txt", "r") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) == 2 and login == parts[0] and pas == parts[1]:
                    print("SUCCESS")
                    return
        print("FAILED")

if __name__ == "__main__":
    MainWindow().mainloop()