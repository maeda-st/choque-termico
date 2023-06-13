import keyboard
from tkinter import Tk, Entry, Button

class KeyboardApp:
    def __init__(self):
        self.root = Tk()
        self.entry = Entry(self.root)
        self.entry.pack()
        
        self.create_keyboard()

    def create_keyboard(self):
        keyboard_frame = Tk()
        
        # Layout do teclado
        buttons = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm']
        ]
        
        for row in buttons:
            for key in row:
                button = Button(keyboard_frame, text=key, width=5, height=2)
                button.bind("<Button-1>", self.button_click)
                button.grid(row=buttons.index(row), column=row.index(key))

        keyboard_frame.mainloop()

    def button_click(self, event):
        button = event.widget
        key = button['text']
        self.entry.insert('end', key)

if __name__ == "__main__":
    app = KeyboardApp()
    app.root.mainloop()
