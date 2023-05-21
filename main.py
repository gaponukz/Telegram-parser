import time
import typing
import asyncio
import threading
import tkinter as tk

from tkinter import *
from tkinter import messagebox

class ParserMock:
    def __init__(self, logger_writer: typing.Callable[[str], None]):
        self.logger_writer = logger_writer

    async def main_parser_loop(self):
        for i in range(10):
            await asyncio.sleep(1)
            self.logger_writer(f'{i} iteration')

class CrabApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Crab 1.0.0")
        self.master.resizable(0, 0)
        self.master.iconbitmap("logo.ico")
        self._create_widgets()

    def _create_widgets(self):
        Label(self.master, text="Посилання на telegram-канал: ",
              font=('Segoe UI', 11), relief=RIDGE).grid(row=0, column=0, padx=5,
                                                        pady=5)

        self.link_input = Entry(self.master, font=('arial', 10), width=50)
        self.link_input.grid(row=0, column=1, sticky=EW)

        self.button_start = Button(self.master, text="Старт",
                                   command=self._button_pressed,
                                   font=('Segoe UI', 10), relief=RAISED,
                                   fg='black', bg='#ffffff', width=8, height=1)
        self.button_start.grid(row=0, column=2, sticky=E, padx=10)

        # Frame, containing output data
        self.output_frame = Frame(self.master)
        self.output_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky=EW)

        self.text = Text(self.output_frame, font=('Cascadia Code', 10, "bold"), bg='#000000', fg='#149414',
                         insertbackground='#149414', height=15)
        self.text.grid(row=0, column=0, sticky=EW)
        self.text.configure(state=DISABLED)

        scrollbar_text = Scrollbar(self.output_frame, orient=VERTICAL, command=self.text.yview, )
        self.text.configure(yscrollcommand=scrollbar_text.set)
        scrollbar_text.place(relx=1, rely=0, relheight=1, anchor=NE)

    def _button_pressed(self):
        """Actions performed after click of a button"""
        if not self.link_input.get():
            messagebox.showinfo("", "Wrong time input. Try Again")
            return

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        parser = ParserMock(self._on_send_logging_callback)
        threading.Thread(target=self._sync_to_async_bridge, args=(parser.main_parser_loop,)).start()
        messagebox.showinfo("Інфо", "Парсер запущений успішно!")
    
    def _on_send_logging_callback(self, text: str) -> None:
        """Displays string" in a Text widget"""
        self.text.configure(state=NORMAL)
        self.text.insert('end',  time.strftime('%H:%M:%S', time.localtime(time.time())) + ' ' + text + '\n')
        self.text.configure(state=DISABLED)
       
    def _sync_to_async_bridge(self, function: typing.Coroutine):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(function())

if __name__ == "__main__":
    root = tk.Tk()
    app = CrabApp(root)
    app.mainloop()
