import threading
import telethon
import tkinter as tk

from tkinter import messagebox
from src.parser_facade import Parser
from src.parsers import ChatParserIterator
from src.parsers import ChannelCommentsParserIterator
from src.settings import JsonSettings
from src.exporters import CsvExporter

class CrabApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Краб")
        self.master.geometry("400x150")
        self.create_widgets()

    def create_widgets(self):
        self.text_label = tk.Label(self.master, text="Посилання/юзернейм:")
        self.text_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.text_input = tk.Entry(self.master, width=30)
        self.text_input.grid(row=0, column=1, padx=10, pady=5)

        self.channel_label = tk.Label(self.master, text="Це чат?")
        self.channel_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        
        self.channel_var = tk.BooleanVar()
        self.channel_checkbox = tk.Checkbutton(self.master, text="", variable=self.channel_var)
        self.channel_checkbox.grid(row=1, column=1, padx=10, pady=5)

        self.int_label = tk.Label(self.master, text="Ліміт користувачів:")
        self.int_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        
        self.int_input = tk.Entry(self.master, width=10)
        self.int_input.grid(row=2, column=1, padx=10, pady=5)

        self.start_button = tk.Button(self.master, text="Стартуємо", command=self.start)
        self.start_button.grid(row=3, column=0, padx=10, pady=10, sticky=tk.E)

    def start(self):
        entity_to_parse = self.text_input.get()
        is_chat = self.channel_var.get()

        if not entity_to_parse:
            messagebox.showerror("Помилка", "Введіть посилання або юзернейм.")
            return
        
        try:
            user_count_limit = int(self.int_input.get())

        except ValueError:
            messagebox.showerror("Помилка", "Ліміт користувачів це число.")
            return
        
        current_setting = JsonSettings().load()
        current_setting.entity_to_parse = entity_to_parse
        current_setting.entity_type = 'chat' if is_chat else 'channel'
        current_setting.user_count_limit = user_count_limit

        client = telethon.TelegramClient(
            current_setting.account.session_path,
            current_setting.account.api_id,
            current_setting.account.api_hash
        )

        if current_setting.entity_type == 'chat':
            parser_iterator = ChatParserIterator(client, current_setting.entity_to_parse)

        elif current_setting.entity_type == 'channel':
            parser_iterator = ChannelCommentsParserIterator(client, current_setting.entity_to_parse)

        parser = Parser(client, current_setting, CsvExporter(), parser_iterator)

        threading.Thread(target=parser.run).start()
        messagebox.showinfo("Інфо", "Парсер запущений успішно!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CrabApp(root)
    app.mainloop()
