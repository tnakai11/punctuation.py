# coding: utf-8

# @ Takumi Nakai

# This GUI application is for text files written in Japanese.
# What this application can do is as below.
# - Replace "、" and "。" with "，" and "．" 
# - Replace "，" and "．" with "、" and "。" 

# With this application,
# you need little time to switch or standardize the types of punctuations.
# So, you can write Japanese documents
# without worrying too much about which punctuations should be used.

from datetime import datetime
from tkinter import *
from tkinter import filedialog,messagebox, ttk
from pathlib import Path
import re
import shutil

KUTEN_TO_COMMA = 0
COMMA_TO_KUTEN = 1

kutens = ['、','。']
commas = ['，','．']

class Replacer:
    def __init__(self,file,option) -> None:
        self.file_path = Path(file)
        self.option = option
        self.setup_comp()

    def setup_comp(self):
        pattern = {}
        pattern[KUTEN_TO_COMMA] = ".*(" + ")|(".join(kutens) + ").*"
        pattern[COMMA_TO_KUTEN] = ".*(" + ")|(".join(commas) + ").*"
        self.comp = {}
        for key, item in pattern.items():
            self.comp[key] = re.compile(item)

    def can_replace(self) -> None:
        if self.file_path.is_file()==False:
            messagebox.showinfo('Error','Please choose a file.')
            return False
            
        if self.file_path.exists()==False:
            messagebox.showinfo('Error','The file does not exist.')
            return False

    def replace(self) -> None:
        if self.can_replace() == False:
            return
        with open(self.file_path,'r',encoding='utf-8') as f:
            data = f.read()
            if self.comp[self.option].search(data)!=None:
                suffix = self.file_path.suffix
                backup_path = self.file_path.parent / str(self.file_path.stem + '_backup_' + datetime.now().strftime('%Y%m%d_%H%M%S') + suffix)
                shutil.copy(self.file_path,backup_path)
            else:
                messagebox.showinfo('Information','There is nothing to be replaced.')
                return

        if self.option == KUTEN_TO_COMMA:
            for kuten,comma in zip(kutens,commas):
                data = data.replace(kuten,comma)
        elif self.option == COMMA_TO_KUTEN:
            for kuten,comma in zip(kutens,commas):
                data = data.replace(comma,kuten)
        else:
            messagebox.showinfo('Error','Undefined Option')
            return
        
        with open(self.file_path,'w',encoding='utf-8') as f:
            f.write(data)
        messagebox.showinfo('Information','Replacement has been done.')
        return

class Application:
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title('Ku-Tou-Tens to Punctuations')
        self.make_widget()
        self.layout()
        self.root.mainloop()

    def make_widget(self) -> None:
        self.frame = ttk.Frame(self.root,padding=20)
        
        # For File Path
        self.label_frame_file = ttk.LabelFrame(
            self.frame,
            text='File Path',
            padding=(5)
        )
        self.text_file_location = StringVar()
        self.entry_file_location = ttk.Entry(
            self.label_frame_file,
            textvariable=self.text_file_location,
            width=100,
        )
        self.button_choose_file = ttk.Button(
            self.label_frame_file,
            text='Choose File',
            command=self.get_file_location
        )

        # For Options
        self.label_frame_rb = ttk.LabelFrame(self.frame,text='Options',padding=(5))
        self.option = IntVar()
        self.option.set(KUTEN_TO_COMMA)

        self.rb1 = ttk.Radiobutton(
            self.label_frame_rb,
            text = '「、。」 to 「，．」 ',
            value= KUTEN_TO_COMMA,
            variable=self.option
        )
        self.rb2 = ttk.Radiobutton(
            self.label_frame_rb,
            text = '「，．」 to 「、。」 ',
            value= COMMA_TO_KUTEN,
            variable=self.option
        )
        
        # For Starting Replacement
        self.button_replace = ttk.Button(
            self.frame,
            text='Replace',
            command=self.replace
        )

    def layout(self) -> None:
        self.frame.pack()
        self.label_frame_file.grid(row=0,columnspan=2)
        self.button_choose_file.grid(row=0,column=0)
        self.entry_file_location.grid(row=0,column=1)
        self.label_frame_rb.grid(row=1,column=0)
        self.rb1.grid(row=0,column=0)
        self.rb2.grid(row=0,column=1)
        self.button_replace.grid(row=1,column=1)

    def get_file_location(self):
        a = filedialog.askopenfilename()
        self.text_file_location.set(a)
    
    def replace(self):
        r = Replacer(self.text_file_location.get(),self.option.get())
        r.replace()

if __name__ == '__main__':
    app = Application()
