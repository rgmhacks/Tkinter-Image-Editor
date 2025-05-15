import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox, ttk
from PIL import Image, ImageOps, ImageTk, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import os

root = tk.Tk()
root.state('zoomed')
root.title("Image Editor")
root.config(bg='#c2d5ed')

# To add your own Icon just add the path to the image
# icon = ImageTk.PhotoImage(file="D:\Project\shinchan.jpeg")
# root.iconphoto(False,icon)

pen_size = 5
pen_color = 'black'
file_path = ""
buffer_img = ""
width = 0
height = 0
cache = []
x,y =0,0

def close_window():
    if buffer_img == "":
        root.destroy()
        return
    save = messagebox.askyesnocancel(title="Warning",message="Do you want to save the image?")
    if save == False:
        if os.path.isfile(buffer_img):
            os.remove(buffer_img)
            root.destroy()
        else:
            root.destroy()
    elif save == True:
        save_img()
        root.destroy()
    
def add_image():
    global file_path,width,height,buffer_img,cache
    file_path = filedialog.askopenfilename(
        initialdir="") # Here you can add some base directory so that directory will be opened when we click on Add Image
    image = Image.open(file_path)
    if(file_path[-4]=='.'):
        buffer_img = file_path[:-4]+"tmp"+file_path[-4:]
    else:
        buffer_img = file_path[:-5]+"tmp"+file_path[-5:]
    image.save(buffer_img)
    cache.append(image)
    width, height = int(image.width / 2), int(image.height / 2)
    image = image.resize((width, height))
    canvas.config(width=image.width, height=image.height)
    image = ImageTk.PhotoImage(image)
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

def change_color():
    global pen_color
    pen_color = colorchooser.askcolor(title="Select Text Color")[1]
    text_color.config(bg=pen_color)

def change_colour():
    global pen_color
    pen_color = colorchooser.askcolor(title="Select Text Color")[1]
    pen_colour.config(bg=pen_color)

def draw(event):
    global pen_size
    image_tmp = Image.open(buffer_img)
    image = Image.open(file_path)
    draw = ImageDraw.Draw(image_tmp)
    x1, y1 = (event.x - pen_size), (event.y - pen_size)
    x2, y2 = (event.x + pen_size), (event.y + pen_size)
    if image.width == image_tmp.width and image.height == image_tmp.height:
        draw.ellipse([2*x1, 2*y1, 2*x2, 2*y2], fill=pen_color)
    else:
        draw.ellipse([x1, y1, x2, y2], fill=pen_color)
    image_tmp.save(buffer_img)
    canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline='')

def pen_size_change():
    global pen_size
    pen_size = int(pen_input.get())
    pen_input.delete(0, tk.END)

def clear():
    pen_input.delete(0, tk.END)

def change_brightness(value):
    global buffer_img,width,height,cache
    image_tmp = Image.open(buffer_img)
    image_tmp = ImageEnhance.Brightness(image_tmp).enhance(value)
    image_tmp.save(buffer_img)
    cache.append(image_tmp)
    image_tmp = image_tmp.resize((width,height))
    image_tmp = ImageTk.PhotoImage(image_tmp)
    canvas.image = image_tmp
    canvas.create_image(0, 0, image=image_tmp, anchor="nw")

def change_contrast(value):
    global buffer_img,width,height,cache
    image_tmp = Image.open(buffer_img)
    image_tmp = ImageEnhance.Contrast(image_tmp).enhance(value)
    image_tmp.save(buffer_img)
    cache.append(image_tmp)
    image_tmp = image_tmp.resize((width,height))
    image_tmp = ImageTk.PhotoImage(image_tmp)
    canvas.image = image_tmp
    canvas.create_image(0, 0, image=image_tmp, anchor="nw")

def change_sharpness(value):
    global buffer_img,width,height,cache
    image_tmp = Image.open(buffer_img)
    image_tmp = ImageEnhance.Sharpness(image_tmp).enhance(value)
    image_tmp.save(buffer_img)
    cache.append(image_tmp)
    image_tmp = image_tmp.resize((width,height))
    image_tmp = ImageTk.PhotoImage(image_tmp)
    canvas.image = image_tmp
    canvas.create_image(0, 0, image=image_tmp, anchor="nw")    

def clear_img():
    global width,height
    image = Image.open(file_path)
    image.save(buffer_img)
    image_tmp = Image.open(buffer_img)
    cache.append(image_tmp)
    width, height = int(image.width / 2), int(image.height / 2)
    image_tmp = image_tmp.resize((width, height))
    canvas.config(width=image_tmp.width, height=image_tmp.height)
    image_tmp = ImageTk.PhotoImage(image_tmp)
    canvas.image = image_tmp
    canvas.create_image(0, 0, image=image_tmp, anchor="nw")


def apply_filter(filter):
    global buffer_img,width,height,cache
    image_tmp=Image.open(buffer_img)
    if filter == "Black and White":
        image_tmp = ImageOps.grayscale(image_tmp)
    elif filter == "Blur":
        image_tmp = image_tmp.filter(ImageFilter.BLUR)
    elif filter == "Sharpen":
        image_tmp = image_tmp.filter(ImageFilter.SHARPEN)
    elif filter == "Smooth":
        image_tmp = image_tmp.filter(ImageFilter.SMOOTH)
    elif filter == "Contour":
        image_tmp = image_tmp.filter(ImageFilter.CONTOUR)
    elif filter == "Emboss":
        image_tmp = image_tmp.filter(ImageFilter.EMBOSS)
    image_tmp.save(buffer_img)
    cache.append(image_tmp)
    if width == int(image_tmp.width/2) and height == int(image_tmp.height/2):
        image_tmp = image_tmp.resize((int(image_tmp.width/2),int(image_tmp.height/2)))
    image_tmp = ImageTk.PhotoImage(image_tmp)
    canvas.image = image_tmp
    canvas.create_image(0, 0, image=image_tmp, anchor="nw")
    return

def resize_img():
    global width,height,buffer_img,resize,cache
    resize = True
    width = int(wid_val.get())
    height = int(height_val.get())
    wid_val.delete(0,tk.END)
    height_val.delete(0,tk.END)
    image_tmp = Image.open(buffer_img)
    image_tmp = image_tmp.resize((width,height))
    image_tmp.save(buffer_img)
    cache.append(image_tmp)
    canvas.config(width=image_tmp.width, height=image_tmp.height)
    image_tmp = ImageTk.PhotoImage(image_tmp)
    canvas.image = image_tmp
    canvas.create_image(0, 0, image=image_tmp, anchor="nw")

def rotate_img():
    global cache
    degree = int(deg_val.get())
    deg_val.delete(0,tk.END)
    image_tmp = Image.open(buffer_img)
    image_tmp = image_tmp.rotate(degree)
    image_tmp.save(buffer_img)
    cache.append(image_tmp)
    image_tmp = image_tmp.resize((width,height))
    image_tmp = ImageTk.PhotoImage(image_tmp)
    canvas.image = image_tmp
    canvas.create_image(0, 0, image=image_tmp, anchor="nw")

def add_text():
    global x,y,cache
    image_tmp = Image.open(buffer_img)
    draw = ImageDraw.Draw(image_tmp)
    txt = text_input.get()
    text_input.delete(0,tk.END)
    font = ImageFont.truetype("arial.ttf", int(text_size_input.get()), encoding="unic")
    text_size_input.delete(0,tk.END)
    if width == int(image_tmp.width/2) and height == int(image_tmp.height/2):
        draw.text((2*x,2*y),txt,pen_color,font=font)
    else:
        draw.text((x,y),txt,pen_color,font=font)
    image_tmp.save(buffer_img)
    cache.append(image_tmp)
    image_tmp = image_tmp.resize((width,height))
    image_tmp = ImageTk.PhotoImage(image_tmp)
    canvas.image = image_tmp
    canvas.create_image(0, 0, image=image_tmp, anchor="nw")

def message(event):
    message_box = messagebox.showinfo(title = "Please Note", message = 
                                      "Please double click at the place where you want to add the text before clicking on Add text button!!!")

def getco_ordinarate(event):
    global x,y
    x,y = event.x,event.y
    print(x,y)

def crop_img():
    global width,height
    image_tmp = Image.open(buffer_img)
    image = Image.open(file_path)
    if image.width == image_tmp.width and image.height == image_tmp.height:
        image_tmp = image_tmp.crop((int(left_input.get())*2,int(top_input.get())*2,
                                int(right_input.get())*2,int(bottom_input.get())*2))
    else:
        image_tmp = image_tmp.crop((int(left_input.get()),int(top_input.get()),
                                int(right_input.get()),int(bottom_input.get())))
    image_tmp.save(buffer_img)
    width, height = image_tmp.width, image_tmp.height
    cache.append(image_tmp)
    left_input.delete(0, tk.END)
    right_input.delete(0, tk.END)
    top_input.delete(0, tk.END)
    bottom_input.delete(0, tk.END)
    canvas.config(width=image_tmp.width, height=image_tmp.height)
    image_tmp = ImageTk.PhotoImage(image_tmp)
    canvas.image = image_tmp
    canvas.create_image(0, 0, image=image_tmp, anchor = "nw")

def helper_l(event):
    left_input.delete(0,tk.END)
    left_input.insert(0,str(x))

def helper_r(event):
    right_input.delete(0,tk.END)
    right_input.insert(0,str(x))

def helper_t(event):
    top_input.delete(0,tk.END)
    top_input.insert(0,str(y))

def helper_b(event):
    bottom_input.delete(0,tk.END)
    bottom_input.insert(0,str(y))

def flip():
    image_tmp = Image.open(buffer_img)
    image_tmp = image_tmp.transpose(Image.FLIP_LEFT_RIGHT)
    image_tmp.save(buffer_img)
    cache.append(image_tmp)
    if width == int(image_tmp.width/2) and height == int(image_tmp.height/2):
        image_tmp = image_tmp.resize((int(image_tmp.width/2),int(image_tmp.height/2)))
    image_tmp = ImageTk.PhotoImage(image_tmp)
    canvas.image = image_tmp
    canvas.create_image(0, 0, image=image_tmp, anchor = "nw")

def detect_edge():
    image_tmp = Image.open(buffer_img)
    image = Image.open(file_path)
    image_tmp = image_tmp.convert("L")
    image_tmp = image_tmp.filter(ImageFilter.FIND_EDGES)
    image_tmp.save(buffer_img)
    cache.append(image_tmp)
    if image_tmp.width == image.width and image_tmp.height == image.height:
        image_tmp = image_tmp.resize((int(image_tmp.width/2),int(image_tmp.height/2)))
    image_tmp = ImageTk.PhotoImage(image_tmp)
    canvas.image = image_tmp
    canvas.create_image(0, 0, image=image_tmp, anchor = "nw")

def undo_img():
    image_tmp = cache.pop()
    image_tmp.save(buffer_img)
    image = Image.open(file_path)
    if image.width == image_tmp.width and image.height == image_tmp.height:
        image_tmp = image_tmp.resize((int(image_tmp.width/2),int(image_tmp.height/2)))
    canvas.config(width=image_tmp.width, height=image_tmp.height)
    image_tmp = ImageTk.PhotoImage(image_tmp)
    canvas.image = image_tmp
    canvas.create_image(0, 0, image=image_tmp, anchor="nw")

def save_img():
    save_path = filedialog.asksaveasfilename(initialdir="D:\Engineering\sem 3\python\Miniproject\Picture",
                                             defaultextension=".jpg")
    image_tmp = Image.open(buffer_img)
    image_tmp.save(save_path)
    os.remove(buffer_img)

left_frame = tk.Frame(root, width=200, height=800, bg='#c2d5ed')
left_frame.pack(side="left", fill="y",padx=20)

canvas = tk.Canvas(root, width=1250, height=800)
canvas.pack()
canvas.bind("<B1-Motion>", draw)

image_button = tk.Button(left_frame, text="Add Image",
                         command=add_image, bg='#e9f0e9')
image_button.pack(pady=10)

annotate_frame = tk.LabelFrame(left_frame, text = "Annotations", bg='#c2d5ed')
annotate_frame.pack()

pen = tk.Label(annotate_frame, text = "Pen Size: ", bg = '#c2d5ed')
pen.pack(side = "left")

pen_input = tk.Entry(annotate_frame, width = 5)
pen_input.pack(side = "left")

pen_size_set = tk.Button(annotate_frame, text = "Set", bg='#e9f0e9', command = pen_size_change)
pen_size_set.pack(side = "left", padx = 5)

pen_colour = tk.Button(annotate_frame,width=2,bg = pen_color,command = change_colour)
pen_colour.pack(side="left",padx = 5, pady = 1)

brightness_frame = tk.LabelFrame(left_frame, bg='#c2d5ed', text="Brightness")
brightness_frame.pack(pady=5,padx=3)

brightness_1 = tk.Radiobutton(
    brightness_frame, text="Decrease", value=1, command=lambda: change_brightness(0.75), bg='#c2d5ed')
brightness_1.pack(side="left")

brightness_2 = tk.Radiobutton(
    brightness_frame, text="Increase", value=2, command=lambda: change_brightness(1.25), bg='#c2d5ed')
brightness_2.pack(side="left")
brightness_2.select()

contrast = tk.LabelFrame(left_frame, text = "Contrast", bg = '#c2d5ed')
contrast.pack(pady=5, padx=3)

contrast_1 = tk.Radiobutton(
    contrast, text="Decrease", value=4, command=lambda: change_contrast(0.75), bg='#c2d5ed')
contrast_1.pack(side="left")

contrast_2 = tk.Radiobutton(
    contrast, text="Increase", value=5, command=lambda: change_contrast(1.25), bg='#c2d5ed')
contrast_2.pack(side="left")
contrast_2.select()

sharpness_frame = tk.LabelFrame(left_frame, text = "Sharpness", bg = '#c2d5ed')
sharpness_frame.pack(pady=5, padx=3)

sharpness_1 = tk.Radiobutton(
    sharpness_frame, text="Decrease", value=7, command=lambda: change_sharpness(0.75), bg='#c2d5ed')
sharpness_1.pack(side="left")

sharpness_2 = tk.Radiobutton(
    sharpness_frame, text="Increase", value=8, command=lambda: change_sharpness(1.25), bg='#c2d5ed')
sharpness_2.pack(side="left")
sharpness_2.select()

filter_frame = tk.LabelFrame(left_frame, bg = '#c2d5ed', text="Filter")
filter_frame.pack()

filter_combobox = ttk.Combobox(filter_frame, values=["Original", "Black and White", "Blur", "Contour",
                                             "Emboss", "Sharpen", "Smooth"])
filter_combobox.pack(padx = 2, pady = 2)
filter_combobox.current(0)

filter_combobox.bind("<<ComboboxSelected>>",
                     lambda event: apply_filter(filter_combobox.get()))

resize_frame = tk.LabelFrame(left_frame, bg='#c2d5ed', text="Resize")
resize_frame.pack(pady=5,padx=3)

width_frame = tk.Frame(resize_frame, bg='#c2d5ed')
width_frame.pack()

wid = tk.Label(width_frame, text = "Width: ", bg = '#c2d5ed')
wid.pack(side = "left" )
wid_val = tk.Entry(width_frame)
wid_val.pack(side = "left", padx = 1, pady = 1)

height_frame = tk.Frame(resize_frame, bg='#c2d5ed')
height_frame.pack()

height = tk.Label(height_frame, text = "Height: ", bg = '#c2d5ed')
height.pack(side = "left")
height_val = tk.Entry(height_frame)
height_val.pack(side = "left", padx = 1, pady = 1)

resize = tk.Button(resize_frame, text="Resize", bg = '#e9f0e9', command = resize_img)
resize.pack(padx = 1, pady = 1)

rotate = tk.LabelFrame(left_frame,text = "Rotate", bg='#c2d5ed')
rotate.pack(pady=5,padx=3)

rot = tk.Frame(rotate,bg = '#c2d5ed')
rot.pack()

degree = tk.Label(rot, text = "Degree: ", bg = '#c2d5ed')
degree.pack(side="left")

deg_val = tk.Entry(rot)
deg_val.pack(side="left", padx = 1, pady = 1)

rotate_button = tk.Button(rotate,text = "Rotate", bg = '#e9f0e9', command = rotate_img)
rotate_button.pack(padx = 1, pady = 1)

watermark_frame = tk.LabelFrame(left_frame, text = "Add Text", bg = '#c2d5ed')
watermark_frame.pack(pady=5,padx=3)

text_input = tk.Entry(watermark_frame,width = 30, bg = 'white')
text_input.pack()
text_input.bind("<Button-1>", message)

text_button = tk.Frame(watermark_frame,bg = '#c2d5ed')
text_button.pack()

text_size = tk.Label(text_button, text = "Size: ", bg = '#c2d5ed')
text_size.pack(side = "left",padx = 1,pady = 1)
text_size_input = tk.Entry(text_button, bg = 'white')
text_size_input.pack(side = "left",padx = 1,pady = 1)

text_color = tk.Button(text_button,width=2,bg = pen_color,command = change_color)
text_color.pack(side="left",padx = 2, pady = 1)

add_text_button = tk.Button(watermark_frame, text = "Add Text", bg = '#e9f0e9', command = add_text)
add_text_button.pack(padx = 1, pady = 1)
canvas.bind("<Double 1>",getco_ordinarate)

crop_frame = tk.LabelFrame(left_frame, text = "Crop", bg = '#c2d5ed')
crop_frame.pack()

horiontal = tk.Frame(crop_frame, bg = '#c2d5ed')
horiontal.pack()

left = tk.Label(horiontal, text = "Left: ",bg = '#c2d5ed')
left.pack(side = "left")

left_input = tk.Entry(horiontal, bg = 'white', width = 5)
left_input.pack(side = "left")
left_input.bind('<Button-1>',helper_l)

right = tk.Label(horiontal, text = "Right: ",bg = '#c2d5ed')
right.pack(side = "left", padx = 1, pady = 1)

right_input = tk.Entry(horiontal, bg = 'white', width = 5)
right_input.pack(side = "left")
right_input.bind('<Button-1>',helper_r)

vertical = tk.Frame(crop_frame, bg = '#c2d5ed')
vertical.pack()

top = tk.Label(vertical, text = "Top: ",bg = '#c2d5ed')
top.pack(side = "left")

top_input = tk.Entry(vertical, bg = 'white', width = 5)
top_input.pack(side = "left")
top_input.bind('<Button-1>',helper_t)

bottom = tk.Label(vertical, text = "Bottom: ",bg = '#c2d5ed')
bottom.pack(side = "left", padx = 1, pady = 1)

bottom_input = tk.Entry(vertical, bg = 'white', width = 5)
bottom_input.pack(side = "left")
bottom_input.bind('<Button-1>',helper_b)

crop = tk.Button(crop_frame, text = "Crop", bg = '#e9f0e9', command = crop_img)
crop.pack()

features_frame = tk.Frame(left_frame, bg = '#c2d5ed')
features_frame.pack()

mirror = tk.Button(features_frame,text = "Mirror", bg = '#e9f0e9', command = flip)
mirror.pack(side = "left",padx=5,pady=5)

edge_detection = tk.Button(features_frame, text = "Detect Edges", bg = '#e9f0e9', command = detect_edge)
edge_detection.pack(side = "left",padx=5,pady=5)

image_reverse_button = tk.Frame(left_frame,bg='#c2d5ed')
image_reverse_button.pack()

undo = tk.Button(image_reverse_button,text="Undo",command=undo_img,bg='#e9f0e9')
undo.pack(side = "left",padx=5,pady=5)

clear_button = tk.Button(image_reverse_button, text="Clear All Effects",
                         command=clear_img, bg="#FF9797")
clear_button.pack(side = "left",padx=5,pady=5)

save = tk.Button(left_frame, text = "Save", bg = '#e9f0e9', command = save_img)
save.pack(padx=5,pady=5)

root.protocol("WM_DELETE_WINDOW", close_window)
root.mainloop()
