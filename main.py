import typing
import asyncio
import threading
import tkinter as tk

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
        self.master.title("Краб")
        self.master.geometry("400x150")
        self._create_widgets()

    def _create_widgets(self):
        self.start_button = tk.Button(self.master, text="Стартуємо", command=self._start)
        self.start_button.grid(row=3, column=0, padx=10, pady=10, sticky=tk.E)
    
    def _on_send_logging_callback(self, text: str) -> None: ...

    def _start(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        parser = ParserMock(self._on_send_logging_callback)
        threading.Thread(target=self._sync_to_async_bridge, args=(parser.main_parser_loop,)).start()
        messagebox.showinfo("Інфо", "Парсер запущений успішно!")

    def _sync_to_async_bridge(self, function: typing.Coroutine):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(function())

if __name__ == "__main__":
    root = tk.Tk()
    app = CrabApp(root)
    app.mainloop()
