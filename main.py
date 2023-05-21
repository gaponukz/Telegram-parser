import time
import asyncio
import threading
import tkinter as tk

from tkinter import messagebox

from src import utils
from src.parser_facade import Parser
from src.settings import ISetting, JsonSettings
from src.exporters import IExporter, CsvExporter

class CrabApp(tk.Frame):
    def __init__(self, master: tk.Tk, setting: ISetting, exporter: IExporter):
        super().__init__(master)
        self.master = master
        self.setting = setting.load()
        self.exporter = exporter

        self.master.title("Crab 1.0.0")
        self.master.resizable(0, 0)
        self.master.iconbitmap("logo.ico")
        self._create_widgets()

    def _create_widgets(self):
        tk.Label(self.master, text="Посилання на telegram-канал: ",
              font=('Segoe UI', 11), relief=tk.RIDGE).grid(row=0, column=0, padx=5,
                                                        pady=5)

        self.link_input = tk.Entry(self.master, font=('arial', 10), width=50)
        self.link_input.grid(row=0, column=1, sticky=tk.EW)

        self.button_start = tk.Button(self.master, text="Старт",
                                   command=self._button_pressed,
                                   font=('Segoe UI', 10), relief=tk.RAISED,
                                   fg='black', bg='#ffffff', width=8, height=1)
        self.button_start.grid(row=0, column=2, sticky=tk.E, padx=10)

        # Frame, containing output data
        self.output_frame = tk.Frame(self.master)
        self.output_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky=tk.EW)

        self.text = tk.Text(self.output_frame, font=('Cascadia Code', 10, "bold"), bg='#000000', fg='#149414',
                         insertbackground='#149414', height=15)
        self.text.grid(row=0, column=0, sticky=tk.EW)
        self.text.configure(state=tk.DISABLED)

        scrollbar_text = tk.Scrollbar(self.output_frame, orient=tk.VERTICAL, command=self.text.yview, )
        self.text.configure(yscrollcommand=scrollbar_text.set)
        scrollbar_text.place(relx=1, rely=0, relheight=1, anchor=tk.NE)

    def _button_pressed(self):
        """Actions performed after click of a button"""
        if not self.link_input.get():
            messagebox.showinfo("Помилка", "Поле пусте")
            return

        link = self.link_input.get()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        client = utils.build_client_from_settings(self.setting)

        parser_iterator = utils.sync_to_async_bridge(
            utils.get_parser_iterator_due_to_link(client, link)
        )

        parser = Parser(client, self.exporter, parser_iterator, self._on_send_logging_callback)

        threading.Thread(target=client.loop.run_until_complete, args=(parser.main_parser_loop(),)).start()
        messagebox.showinfo("Інфо", "Парсер запущений успішно!")
    
    def _on_send_logging_callback(self, text: str) -> None:
        """Displays string" in a Text widget"""
        self.text.configure(state=tk.NORMAL)
        self.text.insert('end',  time.strftime('%H:%M:%S', time.localtime(time.time())) + ' ' + text + '\n')
        self.text.configure(state=tk.DISABLED)
       

if __name__ == "__main__":
    root = tk.Tk()
    app = CrabApp(root, JsonSettings(), CsvExporter())
    app.mainloop()
