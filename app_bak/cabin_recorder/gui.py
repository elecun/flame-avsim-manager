
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/developer/dev/gui_designer/build/assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("2161x1021")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 1021,
    width = 2161,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=1875.0,
    y=963.0,
    width=114.0,
    height=35.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=1477.0,
    y=610.0,
    width=114.0,
    height=35.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=762.0,
    y=862.0,
    width=114.0,
    height=35.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=884.0,
    y=862.0,
    width=114.0,
    height=35.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=2009.0,
    y=60.0,
    width=114.0,
    height=35.0
)

canvas.create_text(
    38.0,
    18.0,
    anchor="nw",
    text="In-Cabin Camera Monitoring",
    fill="#000000",
    font=("Inter", 15 * -1)
)

canvas.create_text(
    1007.0,
    18.0,
    anchor="nw",
    text="Eye Tracker Monitoring",
    fill="#000000",
    font=("Inter", 15 * -1)
)

canvas.create_text(
    1602.0,
    18.0,
    anchor="nw",
    text="Simulation Scenario",
    fill="#000000",
    font=("Inter", 15 * -1)
)

canvas.create_rectangle(
    1007.0,
    52.0,
    1591.0,
    610.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    38.0,
    52.0,
    518.0,
    322.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    518.0,
    52.0,
    998.0,
    322.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    38.0,
    322.0,
    518.0,
    592.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    518.0,
    322.0,
    998.0,
    592.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    38.0,
    592.0,
    518.0,
    862.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    518.0,
    592.0,
    998.0,
    862.0,
    fill="#000000",
    outline="")

canvas.create_text(
    1602.0,
    71.0,
    anchor="nw",
    text="Scenario File : ",
    fill="#000000",
    font=("Inter", 15 * -1)
)

canvas.create_rectangle(
    1713.0,
    60.0,
    2000.0,
    95.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    1600.0,
    105.0,
    2123.0,
    922.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    37.0,
    945.0,
    2123.0,
    946.0,
    fill="#000000",
    outline="")

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat"
)
button_6.place(
    x=2005.0,
    y=964.0,
    width=114.0,
    height=35.0
)
window.resizable(False, False)
window.mainloop()