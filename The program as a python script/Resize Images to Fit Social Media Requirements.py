import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk
import os
import sys

selected_size = None
original_image_path = None
chosen_color = None

def choose_image():
    global original_image_path
    original_image_path = filedialog.askopenfilename(
        title="Choose Image to Process",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
    )
    if original_image_path:
        print(f"Selected image: {original_image_path}")
        choose_color()

def choose_color():
    global chosen_color
    color = colorchooser.askcolor(title="Choose Color of Pixels to Add")
    if color[1] is not None:
        chosen_color = tuple(int(x) for x in color[0])
        print(f"Selected color: {chosen_color}")
        choose_size()


def choose_size():
    global selected_size

    size_window = tk.Toplevel(root)
    size_window.title("Select Image Size")

    # Set the size_window dimensions to 800x800 (1:1 ratio)
    size_window.geometry("650x650")

    size_label = tk.Label(size_window, text="Choose size of image to create")
    size_label.pack(pady=10)

    listbox = tk.Listbox(size_window)
    listbox.pack(fill=tk.BOTH, expand=True)

    all_sizes = [
        "Instagram: Profile Photo: 320 x 320 px",
        "Instagram: Landscape: 1080 x 566 px",
        "Instagram: Portrait: 1080 x 1350 px",
        "Instagram: Square: 1080 x 1080 px",
        "Instagram: Stories and Reels: 1080 x 1920 px",
        "Facebook: Profile Photo: 170 x 170 px",
        "Facebook: Landscape: 1200 x 630 px",
        "Facebook: Portrait: 630 x 1200 px",
        "Facebook: Square: 1200 x 1200 px",
        "Facebook: Stories and Reels: 1080 x 1920 px",
        "Facebook: Cover Photo: 851 x 315 px",
        "X (aka Twitter): Profile Photo: 400 x 400 px",
        "X (aka Twitter): Landscape: 1600 x 900 px",
        "X (aka Twitter): Portrait: 1080 x 1350 px",
        "X (aka Twitter): Square: 1080 x 1080 px",
        "X (aka Twitter): Cover Photo: 1500 x 1500 px",
        "LinkedIn: Profile Photo: 400 x 400 px",
        "LinkedIn: Landscape: 1200 x 627 px",
        "LinkedIn: Portrait: 627 x 1200 px",
        "LinkedIn: Square: 1080 x 1080 px",
        "LinkedIn: Cover photo: 1128 x 191 px"

        # Add more sizes here with their corresponding dimensions
    ]

    for size in all_sizes:
        listbox.insert(tk.END, size)

    select_button = tk.Button(size_window, text="Select Size", command=lambda: close_and_set_size(size_window, listbox))
    select_button.pack(pady=15)



    # Add the following line before select_button.pack()
    contact_info_label = tk.Label(size_window, text="Programmer's Contact Info", fg="blue", cursor="hand2", anchor="se")
    contact_info_label.config(font=("Arial", 16, "bold underline"))
    contact_info_label.pack(side="bottom", padx=20, pady=20)
    contact_info_label.bind("<Button-1>", show_info_form)  # Bind the click event to show_info_form function


def show_info_form(event=None):  # Added 'event=None' to handle click event
    info_window = tk.Toplevel(root)
    info_window.title("Information")
    info_text = "Name: David Franciamone\nPhone Number: (442) 370-5470\nEmail: David.Franciamone@gmail.com"
    
    info_text_widget = tk.Text(info_window, height=5, width=40)
    info_text_widget.insert(tk.END, info_text)
    info_text_widget.configure(state="disabled")  # Disable text widget for read-only
    info_text_widget.pack()


def close_and_set_size(window, listbox):
    global selected_size
    selected_index = listbox.curselection()
    
    if not selected_index:
        # If no item is selected, select the first item
        listbox.select_set(0)
        selected_index = (0,)
    
    selected_size = listbox.get(selected_index[0])
    window.destroy()
    display_colored_image()


def upscale_image(input_image_path, output_image_path):
    with Image.open(input_image_path) as img:
        width, height = img.size
        img = img.resize((width*2, height*2), Image.LANCZOS)
        img.save(output_image_path)





def display_colored_image():
    global selected_size, original_image_path, chosen_color

    if selected_size is None or original_image_path is None or chosen_color is None:
        return
    

    # Map size names to dimensions
    size_dimensions = {
        "Instagram: Profile Photo: 320 x 320 px": (320, 320),
        "Instagram: Landscape: 1080 x 566 px": (1080, 566),
        "Instagram: Portrait: 1080 x 1350 px": (1080, 1350),
        "Instagram: Square: 1080 x 1080 px": (1080, 1080),
        "Instagram: Stories and Reels: 1080 x 1920 px": (1080, 1920),
        "Facebook: Profile Photo: 170 x 170 px": (170, 170),
        "Facebook: Landscape: 1200 x 630 px": (1200, 630),
        "Facebook: Portrait: 630 x 1200 px": (630, 1200),
        "Facebook: Square: 1200 x 1200 px": (1200, 1200),
        "Facebook: Stories and Reels: 1080 x 1920 px": (1080, 1920),
        "Facebook: Cover Photo: 851 x 315 px": (851, 315),
        "X (aka Twitter): Profile Photo: 400 x 400 px": (400, 400),
        "X (aka Twitter): Landscape: 1600 x 900 px": (1600, 900),
        "X (aka Twitter): Portrait: 1080 x 1350 px": (1080, 1350),
        "X (aka Twitter): Square: 1080 x 1080 px": (1080, 1080),
        "X (aka Twitter): Cover Photo: 1500 x 1500 px": (1500, 1500),
        "LinkedIn: Profile Photo: 400 x 400 px": (400, 400),
        "LinkedIn: Landscape: 1200 x 627 px": (1200, 627),
        "LinkedIn: Portrait: 627 x 1200 px": (627, 1200),
        "LinkedIn: Square: 1080 x 1080 px": (1080, 1080),
        "LinkedIn: Cover photo: 1128 x 191 px": (1128, 191)
        # Add more sizes here with their corresponding dimensions
    }


    original_image = Image.open(original_image_path)

    if selected_size in size_dimensions:
        width, height = size_dimensions[selected_size]

        # Check if both dimensions are larger than the original image
        if width > original_image.width and height > original_image.height:
            upscale_factor = max(width / original_image.width, height / original_image.height)
            new_width = round(original_image.width * upscale_factor)
            new_height = round(original_image.height * upscale_factor)
            original_image = original_image.resize((new_width, new_height), Image.LANCZOS)

        # Check if the original image is larger than the selected size
        if original_image.width > width or original_image.height > height:
            original_image.thumbnail((width, height))
        colored_canvas = Image.new('RGBA', (width, height), chosen_color)
        paste_x = (width - original_image.width) // 2
        paste_y = (height - original_image.height) // 2
        colored_canvas.paste(original_image, (paste_x, paste_y))

        original_dir, original_filename = os.path.split(original_image_path)
        processed_filename = os.path.splitext(original_filename)[0] + " - processed.png"
        processed_path = os.path.join(original_dir, processed_filename)

        # Save the PNG image with a lower compression level (0 means no compression)
        colored_canvas.save(processed_path, compression=0)
        colored_canvas.show()
        
        root.quit()  # Close the program after displaying the image


        
root = tk.Tk()
root.title("Image Processor")

choose_image()

root.mainloop()
