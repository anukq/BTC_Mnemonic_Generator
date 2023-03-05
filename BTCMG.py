from tkinter import END, Tk, Text, Button, messagebox, LEFT, BOTH
import generator
import os

generated = False


def check_if_generated():
    if not generated:
        display_word_phrase()
    else:
        x = messagebox.askokcancel("Generate new mnemonic", "You are about to generate a new mnemonic! "
                                                            "The current mnemonic will be lost FOREVER!")

        if x:
            display_word_phrase()


def display_word_phrase():
    try:
        global generated

        seed_phrase["state"] = "normal"
        seed_phrase.delete("1.0", END)
        seed_phrase.insert("1.0", str(generator.generate_word_phrase()))
        seed_phrase["state"] = "disabled"
        generated = True
    except Exception as e:
        messagebox.showerror("Error", str(e))


root = Tk()

window_width = 305
window_height = 200

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (window_width / 2)
y = (screen_height / 2) - (window_height / 2)

root.geometry("305x200+" + str(int(x)) + "+" + str(int(y)))
root.resizable(False, False)
if os.path.isfile("icon/icon.ico"):
    root.iconbitmap("icon/icon.ico")
root.title("BTC Mnemonic Generator")

seed_phrase = Text(root, height=9, wrap="word")
seed_phrase.pack(fill=BOTH, padx=5, pady=5)
seed_phrase["state"] = "disabled"

button_generator = Button(root, text="Generate", command=check_if_generated)
button_generator.pack(side=LEFT, padx=5, pady=5)

root.mainloop()
