from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageGrab, UnidentifiedImageError
import datetime as dt


def check_size(img, max_size):
    """check size of uploaded images and resize if needed"""
    original_size = img.size
    original_width = original_size[0]
    original_height = original_size[1]
    if original_width > max_size:
        res_width = int(original_width * (max_size / original_width))
        res_height = int(original_height * (max_size / original_width))
    if original_height > max_size:
        res_width = int(original_width * (max_size / original_height))
        res_height = int(original_height * (max_size / original_height))
    else:
        res_width = original_width
        res_height = original_height
    res_size = (res_width, res_height)
    res_image = img.resize(res_size)
    return res_image


def open_image():
    """upload image"""
    path = filedialog.askopenfilename()
    try:
        pil_image = Image.open(path)
    except UnidentifiedImageError:
        messagebox.showerror("FileFormatError",
                             "Only files with the following extensions are allowed:"
                             ".PNG, .JPEG, .PPM, .GIF, .TIFF, .BMP")
    else:
        return pil_image


def photo_editor():
    """upload photo; add logo; save new image"""

    def restart():
        """clear the previous canvas; restart"""
        root.state("normal")
        canvas.destroy()
        restart_button.destroy()
        logo_button.destroy()

    def add_logo():
        """let user choose image for logo; add logo in the upper left corner
        of the photo; add save_image button"""

        def save_image():
            """save new image with logo as JPG file"""
            # build unique name for new file with logo using current date and time
            date = str(dt.datetime.now())
            saved_file_name = (date.replace("-", "").replace(":", "").
                               replace(".", "").replace(" ", "_") + ".jpg")

            # grab_image
            x = root.winfo_rootx() + canvas.winfo_x()
            y = root.winfo_rooty() + canvas.winfo_y()
            x1 = x + canvas.winfo_width()
            y1 = y + canvas.winfo_height()
            ImageGrab.grab().crop((x, y, x1, y1)).save(saved_file_name)
            restart()
            save_button.destroy()

        # add logo
        try:
            resized_logo = check_size(open_image(), 60)
        except AttributeError:
            pass
        else:
            logo = ImageTk.PhotoImage(resized_logo)
            canvas.create_image(50, 50, image=logo)
            canvas.image = logo
            canvas.tag_raise(photo)
            canvas.grid(column=1, row=1)

            save_button = Button(text="Save Image", command=save_image)
            save_button.grid(column=2, row=0)

            root.state('zoomed')

    # add photo
    try:
        resized_image = check_size(open_image(), 600)
    except AttributeError:
        pass
    else:
        resized_width = resized_image.size[0]
        resized_height = resized_image.size[1]
        canvas = Canvas(width=resized_width, height=resized_height, bg="#C0C0C0", highlightthickness=0)
        photo = ImageTk.PhotoImage(resized_image)
        canvas.create_image(resized_width / 2, resized_height / 2, image=photo)
        canvas.image = photo
        canvas.grid(column=1, row=1)

        # Buttons
        restart_button = Button(text="Restart", command=restart)
        restart_button.grid(column=3, row=0)
        logo_button = Button(text="Add Logo", command=add_logo)
        logo_button.grid(column=1, row=0)


root = Tk()
root.title("Watermark/Logo Editor")
root.minsize(width=300, height=300)
root.config(bg="#C0C0C0", padx=35, pady=20)

# upload button
upload_button = Button(text="Add Photo", command=photo_editor)
upload_button.grid(column=0, row=0)

root.mainloop()
