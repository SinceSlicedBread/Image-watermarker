import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFont, ImageDraw

FONTS = ["Arial", "Comic Sans", "DK Hand", "Helvetica", "Times New Roman"]
COLOURS = {
    "White": (255, 255, 255),
    "Black": (0, 0, 0),
    "Red": (255, 0, 0),
    "Blue": (0, 0, 255),
    "Green": (0, 255, 0),
    "Yellow": (255, 255, 0),
    "Orange": (255, 165, 0),
    "Purple": (128, 0, 128)
}
POSITIONS = ["Top Left", "Top Right", "Centre", "Bottom Left", "Bottom Right"]
FONT_FILES = {
    "Arial": "fonts/ARIAL.TTF",
    "Times New Roman": "fonts/times.ttf",
    "DK Hand": "fonts/DkHandRegular-orna.ttf",
    "Helvetica": "fonts/Helvetica-Bold.ttf",
    "Comic Sans": "fonts/comic.ttf"
}
original_image = None
edited_image = None

## Create window and main frame
window = Tk()
window.title("Watermark Your Images")
window.config(background='blue', width=1000, height=500)

main_frame = ttk.Frame(window, padding=20)
main_frame.grid()


## Create methods for button functionality
# Open find file dialog box and update file path widget with string (ready for load button)
def find_file():
    file_name = filedialog.askopenfilename(
        title="Select a photo file",
        filetypes=[('Image files', '*.jpg *.jpeg *.png *.gif *.bmp'),
                   ('JPEG files', '*.jpg *.jpeg'),
                   ('PNG files', '*.png'),
                   ('All files', '*.*')
                   ])
    load_image_entry.delete(0, END)
    load_image_entry.insert(0, file_name)


## Method to update the Before canvas widget with the selected image
def show_image():
    global original_image

    original_image = Image.open(load_image_entry.get()).convert("RGBA")
    display = original_image.copy()
    display.thumbnail((300, 300), Image.Resampling.LANCZOS)

    tk_image = ImageTk.PhotoImage(display)

    before_image.configure(image=tk_image,
                           height=tk_image.height(),
                           width=tk_image.width())
    before_image.image = tk_image

    after_image.configure(image=tk_image,
                          height=tk_image.height(),
                          width=tk_image.width())
    after_image.image = tk_image


## Method to apply text to After image
def draw_text():
    global after_image, edited_image

    base = Image.open(load_image_entry.get()).convert("RGBA")

    watermark_text = text_options_text_entry.get()
    watermark_text_size = int(text_options_size_spinbox.get())

    txt = Image.new("RGBA",
                    base.size,
                    (255, 255, 255, 0)
                    )

    fnt = ImageFont.truetype(FONT_FILES[text_options_font_combo.get()],
                             size=watermark_text_size)

    position = text_options_position_combo.get()

    rgb = COLOURS[text_options_colour_combo.get()]
    fill = (*rgb, 100)

    d = ImageDraw.Draw(txt)

    bbox = d.textbbox((0, 0),
                      watermark_text,
                      font=fnt
                      )
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    if position == "Top Left":
        x, y = 10, 10
    elif position == "Top Right":
        x = base.width - text_width - 10
        y = 10
    elif position == "Centre":
        x = (base.width - text_width) // 2
        y = (base.height - text_height) // 2
    elif position == "Bottom Left":
        x = 10
        y = base.height - text_height - 10
    elif position == "Bottom Right":
        x = base.width - text_width - 10
        y = base.height - text_height - 10

    d.text((x, y),
           text=watermark_text,
           font=fnt,
           fill=fill
           )
    out = Image.alpha_composite(base, txt)
    out.thumbnail((300, 300), Image.Resampling.LANCZOS)
    tk_image = ImageTk.PhotoImage(out)

    after_image.configure(image=tk_image,
                          width=tk_image.width(),
                          height=tk_image.height()
                          )
    after_image.image = tk_image
    edited_image = out


def apply_watermark():
    global edited_image

    save_path = filedialog.asksaveasfilename(
        title="Save Your Watermarked Image",
        defaultextension=".png",
        filetypes=[
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg"),
            ("All Files", "*.*")
        ]
    )
    if not save_path:
        return

    image_to_save = edited_image

    if save_path.lower().endswith((".jpg", ".jpeg")):
        image_to_save = edited_image.convert("RGB")

    image_to_save.save(save_path)

    tkinter.messagebox.showinfo(
        "Success!",
        "Image saved successfully!"
    )


## Configure Section 1 GUI - image view

image_frame = ttk.Frame(main_frame)
image_frame.grid(column=0, columnspan=2, row=0)
image_frame_label = ttk.Label(image_frame, text="Image Preview")
image_frame_label.grid(column=0, row=0, sticky="w")

before_label = ttk.Label(image_frame, text="Before")
before_label.grid(column=0, row=2)
after_label = ttk.Label(image_frame, text="After")
after_label.grid(column=1, row=2)

before_image = Label(image_frame, width=20, height=20, bg="yellow")
after_image = Label(image_frame, width=20, height=20, bg="orange")
before_image.grid(column=0, row=1)
after_image.grid(column=1, row=1)

## Configure Section 2 GUI - load image

load_image_frame = ttk.Frame(main_frame)
load_image_frame.grid(column=0, row=1, sticky="wn")
load_image_label = ttk.Label(load_image_frame, text="Load Image")
load_image_label.grid(column=0, row=0, sticky="w")

load_image_entry_label = ttk.Label(load_image_frame, text="File Path")
load_image_entry_label.grid(column=0, row=2, sticky="w")
load_image_entry = ttk.Entry(load_image_frame)
load_image_entry.grid(column=1, row=2)

load_image_btn = ttk.Button(load_image_frame, text="Load", command=show_image)
load_image_btn.grid(column=1, row=3, sticky="w")
find_image_btn = ttk.Button(load_image_frame, text="Find File", command=find_file)
find_image_btn.grid(column=1, row=0, sticky="w")

## Configure Section 3 GUI - watermarking options

text_options_frame = ttk.Frame(main_frame)
text_options_frame.grid(column=1, row=1)

text_options_text_label = ttk.Label(text_options_frame, text="Watermark text")
text_options_text_entry = ttk.Entry(text_options_frame)
text_options_text_label.grid(column=0, row=0, sticky="w")
text_options_text_entry.grid(column=1, row=0, sticky="w")

text_options_font_label = ttk.Label(text_options_frame, text="Font Family")
text_options_font_combo = ttk.Combobox(text_options_frame, values=FONTS)
text_options_font_label.grid(column=0, row=1, sticky="w")
text_options_font_combo.grid(column=1, row=1)

text_options_size_label = ttk.Label(text_options_frame, text="Size")
text_options_size_spinbox = ttk.Spinbox(text_options_frame, from_=8, to=54)
text_options_size_label.grid(column=0, row=2, sticky="w")
text_options_size_spinbox.grid(column=1, row=2, sticky="w")

text_options_colour_label = ttk.Label(text_options_frame, text="Colour")
text_options_colour_combo = ttk.Combobox(text_options_frame, values=list(COLOURS.keys()))
text_options_colour_label.grid(column=0, row=3, sticky="w")
text_options_colour_combo.grid(column=1, row=3)

text_options_position_label = ttk.Label(text_options_frame, text="Text Position")
text_options_position_combo = ttk.Combobox(text_options_frame, values=POSITIONS)
text_options_position_label.grid(column=0, row=4, sticky="w")
text_options_position_combo.grid(column=1, row=4)

text_options_preview = ttk.Button(text_options_frame, text="Preview", command=draw_text)
text_options_apply = ttk.Button(text_options_frame, text="Apply Watermark", command=apply_watermark)
text_options_preview.grid(column=2, row=3)
text_options_apply.grid(column=2, row=4)

## Configure Section 4 GUI - extra options and Go button

other_options_frame = ttk.Frame(main_frame)
other_options_frame.grid(column=0, columnspan=2, row=2, sticky="w")
other_options_label = ttk.Label(other_options_frame, text="Other Options")
other_options_label.grid(column=0, row=0, sticky="w")

other_options_batch_checkbox = ttk.Checkbutton(other_options_frame, text="Batch Process Folder?")
other_options_batch_checkbox.grid(column=0, row=1, sticky="w")

other_options_path_label = ttk.Label(other_options_frame, text="Folder Path")
other_options_path_entry = ttk.Entry(other_options_frame)
other_options_path_label.grid(column=0, row=2, sticky="w")
other_options_path_entry.grid(column=1, row=2)

other_options_btn = ttk.Button(other_options_frame, text="Batch Process Folder")
other_options_btn.grid(column=1, row=3, sticky="w")

window.mainloop()
