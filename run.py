# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/9/18 13:44

import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox


def auto_change_photo_size(w_box, h_box, pil_image):
    # get the size of the image
    # 获取图像的原始大小
    w, h = pil_image.size
    f1 = 1.0 * w_box / w
    f2 = 1.0 * h_box / h
    factor = min([f1, f2])
    # print(f1, f2, factor) # test
    # use best down-sizing filter
    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)


def open_img():
    global tk_image
    global pil_image
    global file_type
    global open_img_flag
    file_path = tk.filedialog.askopenfilename(title='选择文件',
                                              initialdir=(os.path.join(os.path.expanduser('~'), 'Desktop')),
                                              filetypes=[("JPG", ".jpg"), ('PNG', ".png"),
                                                         ("JPEG", '.jpeg'), ("GIF", '.gif'), ("ICO", ".ico")])
    file_type = file_path.split('.')[-1]
    # open as a PIL image object
    # 以一个PIL图像对象打开
    pil_image = Image.open(file_path)
    x_pix.set(pil_image.size[0])
    y_pix.set(pil_image.size[1])
    try:
        x_dpi.set(pil_image.info['dpi'][0])
        y_dpi.set(pil_image.info['dpi'][1])
    except:
        x_dpi.set(None)
        y_dpi.set(None)
    # resize the image so it retains its aspect ration
    # but fits into the specified display box
    # 缩放图像让它保持比例，同时限制在一个矩形框范围内
    pil_image_resized = auto_change_photo_size(w_box, h_box, pil_image)
    # convert PIL image object to Tkinter PhotoImage object
    # 把PIL图像对象转变为Tkinter的PhotoImage对象
    tk_image = ImageTk.PhotoImage(pil_image_resized)
    # put the image on a widget the size of the specified display box
    # Label: 这个小工具，就是个显示框，小窗口，把图像大小显示到指定的显示框
    label = tk.Label(window, image=tk_image, width=w_box, height=h_box)
    # padx,pady是图像与窗口边缘的距离
    label.place(x=0, y=0)
    tk.Label(window, text='当前照片尺寸如下:').place(x=10, y=505)
    info = '宽度: %s        高度: %s        水平分辨率: %s      垂直分辨率: %s' % (str(x_pix.get()), str(y_pix.get()), str(x_dpi.get()), str(y_dpi.get()))
    tk.Label(window, text=info).place(x=50, y=525)


def change_pix():
    def input_infomation():
        global new_image
        x_p = x_pix.get()
        y_p = y_pix.get()
        new_image = pil_image.resize((int(x_p), int(y_p)))
        change_window.destroy()
        tk.messagebox.showinfo(title='成功', message='修改成功！')
        tk.Label(window, text='当前照片尺寸如下:').place(x=10, y=505)
        info = '宽度: %s        高度: %s        水平分辨率: %s      垂直分辨率: %s' % \
               (str(x_pix.get()), str(y_pix.get()),
                str(x_dpi.get()), str(y_dpi.get()))
        tk.Label(window, text=info).place(x=50, y=525)
    change_window = tk.Toplevel(window)
    change_window.geometry('200x166')
    change_window.title('请输入要修改的相关参数')

    tk.Label(change_window, text='宽度(像素): ').place(x=10, y=10)
    entry_x_pix = tk.Entry(change_window, textvariable=x_pix, width=15)
    entry_x_pix.place(x=80, y=10)

    tk.Label(change_window, text='高度(像素): ').place(x=10, y=40)
    entry_y_pix = tk.Entry(change_window, textvariable=y_pix, width=15)
    entry_y_pix.place(x=80, y=40)

    tk.Label(change_window, text='水平分辨率: ').place(x=10, y=70)
    entry_x_dpi = tk.Entry(change_window, textvariable=x_dpi, width=15)
    entry_x_dpi.place(x=80, y=70)

    tk.Label(change_window, text='垂直分辨率: ').place(x=10, y=100)
    entry_y_dpi = tk.Entry(change_window, textvariable=y_dpi, width=15)
    entry_y_dpi.place(x=80, y=100)

    ok_btn = tk.Button(change_window, text='确定', command=input_infomation)
    ok_btn.place(x=155, y=130)


def save_img():
    save_path = tk.filedialog.asksaveasfilename(title=u'保存文件（图片格式与输入图片格式一样）')
    save_path = save_path + '.' + file_type
    x_d = float(x_dpi.get())
    y_d = float(y_dpi.get())
    new_image.save(save_path, dpi=(x_d, y_d))
    tk.messagebox.showinfo(title='成功', message='保存成功！')


def change_img_type():
    def change_info():
        save_path = tk.filedialog.asksaveasfilename(title=u'保存文件')
        save_path = save_path + change_type.get()
        pil_image.save(save_path)
        tk.messagebox.showinfo(title='成功', message='保存成功！')
    change_window = tk.Toplevel(window)
    change_window.geometry('200x200')
    change_window.title('请输入要修改的相关参数')

    tk.Label(change_window, text='宽度(像素): ').place(x=10, y=10)
    entry_x_pix = tk.Entry(change_window, textvariable=x_pix, width=15)
    entry_x_pix.place(x=80, y=10)

    tk.Label(change_window, text='高度(像素): ').place(x=10, y=40)
    entry_y_pix = tk.Entry(change_window, textvariable=y_pix, width=15)
    entry_y_pix.place(x=80, y=40)

    tk.Label(change_window, text='请选择图片类型:').place(x=10, y=70)
    # 插入单选按钮控件；显示一个单选的按钮状态
    radiobutton1 = tk.Radiobutton(change_window,  # 作用与window窗口
                                  text='jpg',  # 按钮显示Option A
                                  variable=change_type,  # 点击按钮后作用于变量change_type
                                  value='.jpg',  # 将value值传给change_type
                                  )  # 点击按钮后执行print_selection操作
    radiobutton1.place(x=40, y=90)

    # 插入单选按钮控件；显示一个单选的按钮状态
    radiobutton2 = tk.Radiobutton(change_window,  # 作用与window窗口
                                  text='png',  # 按钮显示Option A
                                  variable=change_type,  # 点击按钮后作用于变量change_type
                                  value='.png',  # 将value值传给change_type
                                  )  # 点击按钮后执行print_selection操作
    radiobutton2.place(x=110, y=90)

    # 插入单选按钮控件；显示一个单选的按钮状态
    radiobutton3 = tk.Radiobutton(change_window,  # 作用与window窗口
                                  text='ico',  # 按钮显示Option A
                                  variable=change_type,  # 点击按钮后作用于变量change_type
                                  value='.ico',  # 将value值传给change_type
                                  )  # 点击按钮后执行print_selection操作
    radiobutton3.place(x=40, y=115)

    # 插入单选按钮控件；显示一个单选的按钮状态
    radiobutton4 = tk.Radiobutton(change_window,  # 作用与window窗口
                                  text='jpeg',  # 按钮显示Option A
                                  variable=change_type,  # 点击按钮后作用于变量change_type
                                  value='.jpeg',  # 将value值传给change_type
                                  )  # 点击按钮后执行print_selection操作
    radiobutton4.place(x=110, y=115)

    # 插入单选按钮控件；显示一个单选的按钮状态
    radiobutton5 = tk.Radiobutton(change_window,  # 作用与window窗口
                                  text='gif',  # 按钮显示Option A
                                  variable=change_type,  # 点击按钮后作用于变量change_type
                                  value='.gif',  # 将value值传给change_type
                                  )  # 点击按钮后执行print_selection操作
    radiobutton5.place(x=40, y=140)

    ok_btn = tk.Button(change_window, text='确定', command=change_info)
    ok_btn.place(x=155, y=160)


window = tk.Tk()
window.iconbitmap('tb.ico')
window.title('Photo Pixel Modification Software V1.0.0')
# size of image display box you want
# 期望图像显示的大小
w_box = 500
h_box = 500
window.geometry('500x630')  # 窗口尺寸
# 创建一个菜单栏，这里我们可以把他理解成一个容器，在窗口的上方
menubar = tk.Menu(window)
# 定义一个空菜单单元
filemenu = tk.Menu(menubar, tearoff=0)  # tearoff=0表示不用虚线隔开
open_img_flag = False
if not open_img_flag:
    tk.Label(window, text='请先点击open打开图片文件', font=('宋体', 10)).place(x=170, y=200)
    tk.Label(window, text='目前支持的文件格式有:jpg、png、jpeg、gif、ico等', font=('宋体', 10)).place(x=100, y=250)
# 将上面定义的空菜单命名为`Open`，放在菜单栏中，就是装入那个容器中
menubar.add_cascade(label='Open', command=open_img, font=('Arial', 10))
menubar.add_cascade(label='change type', command=change_img_type, font=('Arial', 10))
# 同样的在`File`中加入`Exit`小菜单,此处对应命令为`window.quit`
menubar.add_cascade(label='Exit', command=window.quit, font=('Arial', 10))

x_pix = tk.StringVar()
y_pix = tk.StringVar()
x_dpi = tk.StringVar()
y_dpi = tk.StringVar()
change_type = tk.StringVar()

bt1 = tk.Button(window, text='修改像素', width=15, height=2, command=change_pix, bg='grey')
bt1.place(x=100, y=550)

bt1 = tk.Button(window, text='保存图片', width=15, height=2, command=save_img, bg='grey')
bt1.place(x=250, y=550)

tk.Label(window, text='author: Ming Luo', fg="red").place(x=385, y=575)
window.config(menu=menubar)
window.mainloop()
