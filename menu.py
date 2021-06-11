import tkinter as tk
from tkinter.ttk import Combobox, Style
from buildings import create_buildings
from main import *
from typing import Dict, Union
from buildings import Building, Defence


class Menu:
    def __init__(self):
        self.offset_x: int = 0
        self.offset_y: int = 0
        self.window: tk.Tk = tk.Tk()
        self.canvas: tk.Canvas = tk.Canvas(self.window)
        self.style: Style = Style()
        self.style.configure("TCombobox", fieldbackground='red')
        self.style.theme_use()
        self.background: tk.PhotoImage = tk.PhotoImage(file="res/images/background.png")
        self.ok_btn_image: tk.PhotoImage = tk.PhotoImage(file="res/images/ok_button.png")
        self.quit_btn_image: tk.PhotoImage = tk.PhotoImage(file="res/images/x.png")
        self.choice: Combobox = Combobox(self.window, values=list(range(1, 10)), state="readonly")
        self.quit_btn: tk.Button = tk.Button(self.window,
                                             bg="black",
                                             activebackground="black",
                                             borderwidth=0,
                                             image=self.quit_btn_image,
                                             command=lambda: [self.window.destroy()])

        self.ok_btn: tk.Button = tk.Button(self.window,
                                           bg="black",
                                           activebackground="black",
                                           borderwidth=0,
                                           image=self.ok_btn_image,
                                           command=lambda: [self.start()])
        self.create_menu()

    def drag_window(self, event):
        x: int = self.window.winfo_pointerx() - self.offset_x
        y: int = self.window.winfo_pointery() - self.offset_y
        self.window.geometry(f'+{x}+{y}')

    def click_window(self, event):
        self.offset_x: int = event.x+event.widget.winfo_rootx()-self.window.winfo_rootx()
        self.offset_y: int = event.y+event.widget.winfo_rooty()-self.window.winfo_rooty()

    def create_menu(self):
        self.window.geometry("+500+200")
        self.window.resizable(width=False, height=False)
        self.window.bind('<ButtonPress-1>', self.click_window)
        self.window.bind('<B1-Motion>', self.drag_window)
        self.window.overrideredirect(1)
        self.window.wm_attributes("-topmost", "true")
        self.canvas.config(width=709, height=266, highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_image(354, 133, image=self.background)
        self.choice.current(0)
        self.choice.place(x=380, y=158)
        self.quit_btn.place(x=652, y=27)
        self.ok_btn.place(x=410, y=190)

    def start(self):
        buildings: Dict[str, Union[Building, Defence]] = create_buildings(int(self.choice.get()))
        self.window.destroy()
        MainWindow(buildings)


if __name__ == "__main__":
    menu: Menu = Menu()
    menu.window.mainloop()
