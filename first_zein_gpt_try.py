import tkinter as tk
from tkinter import messagebox
import json
import os

# Define a function to perform arithmetic operations
def calculate(expression):
    try:
        return eval(expression)
    except Exception as e:
        return str(e)

# Save history to file
def save_history(history):
    with open('history.json', 'w') as file:
        json.dump(history, file)

# Load history from file
def load_history():
    if os.path.exists('history.json'):
        with open('history.json', 'r') as file:
            return json.load(file)
    return []

# Sort history alphabetically
def sort_history(history):
    return sorted(history, key=lambda x: x['expression'])

# Search history for an expression
def search_history(history, query):
    return [item for item in history if query in item['expression']]

# Define the GUI application class
class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.expression = ""
        self.history = load_history()
        
        self.input_text = tk.StringVar()
        
        self.create_widgets()

    def create_widgets(self):
        input_frame = tk.Frame(self.root)
        input_frame.pack()

        input_field = tk.Entry(input_frame, textvariable=self.input_text, font=('arial', 18, 'bold'), bd=10, insertwidth=4, width=14, borderwidth=4)
        input_field.grid(row=0, column=0)

        button_frame = tk.Frame(self.root)
        button_frame.pack()

        buttons = [
            '7', '8', '9', '/', 'C',
            '4', '5', '6', '*', 'H',
            '1', '2', '3', '-', 'S',
            '0', '.', '=', '+', 'Q'
        ]

        row_val = 0
        col_val = 0

        for button in buttons:
            if col_val > 4:
                col_val = 0
                row_val += 1

            button = tk.Button(button_frame, text=button, font=('arial', 18, 'bold'), bd=1, padx=20, pady=20, command=lambda x=button: self.on_button_click(x))
            button.grid(row=row_val, column=col_val)
            col_val += 1

    def on_button_click(self, button):
        if button == "C":
            self.expression = ""
        elif button == "=":
            result = calculate(self.expression)
            self.history.append({'expression': self.expression, 'result': result})
            self.expression = str(result)
        elif button == "H":
            self.show_history()
        elif button == "S":
            self.sort_and_show_history()
        elif button == "Q":
            save_history(self.history)
            self.root.quit()
        else:
            self.expression += button
        self.input_text.set(self.expression)

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("History")
        history_text = tk.Text(history_window, font=('arial', 12))
        history_text.pack()

        for item in self.history:
            history_text.insert(tk.END, f"{item['expression']} = {item['result']}\n")

    def sort_and_show_history(self):
        sorted_history = sort_history(self.history)
        history_window = tk.Toplevel(self.root)
        history_window.title("Sorted History")
        history_text = tk.Text(history_window, font=('arial', 12))
        history_text.pack()

        for item in sorted_history:
            history_text.insert(tk.END, f"{item['expression']} = {item['result']}\n")

# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
