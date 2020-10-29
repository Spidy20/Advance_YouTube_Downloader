from PIL import ImageTk
import PIL.Image
from tkinter import *
from tkinter import ttk
import tkinter as tk
import pafy
import io
from urllib.request import urlopen

windo = Tk()
windo.configure(background='white')
windo.title("YouTube Video Downloader")

windo.geometry('1120x520')
windo.iconbitmap('./meta/yt.ico')
windo.resizable(0, 0)


def get_info():
    global video,lc,im5
    link_vid = txt2.get()
    try:
        video = pafy.new(link_vid)
    except Exception as e:
        error = tk.Label(windo, text="Something went wrong!! Please check URL", width=35, height=2, fg="white", bg="red",
                        font=('times', 18, ' bold '))
        error.place(x=274, y=370)
        windo.after(5000, destroy_widget, error)
        print(e)

    ## Set Video Title
    v_name = video.title
    video_title.config(text="Name: "+ v_name,width=80)
    video_title.place(x=50, y=300)

    ## Set Duration
    dura = video.duration
    video_dur.config(text="Time: " +dura,width=17)
    video_dur.place(x=50, y=330)

    ## Get the Thumbnail of Video
    thumb = video.bigthumb
    print(thumb)
    u = urlopen(thumb)
    raw_data = u.read()
    im5 = PIL.Image.open(io.BytesIO(raw_data))
    im5_resized = im5.resize((240, 150), PIL.Image.ANTIALIAS)

    image = ImageTk.PhotoImage(im5_resized)
    panel50 = Label(windo, image=image, borderwidth=0)
    panel50.image = image
    panel50.pack()
    panel50.place(x=881, y=90)

    ## Download button of Thumbnail
    im7 = PIL.Image.open('./meta/download.png')
    im7 = im7.resize((40, 40), PIL.Image.ANTIALIAS)
    sp_img7 = ImageTk.PhotoImage(im7)
    panel8 = Button(windo, borderwidth=0,command = download_video_thumbnail, image=sp_img7, bg='white')
    panel8.image = sp_img7
    panel8.pack()
    panel8.place(x=985, y=245)

    dow_list = ["Choose Format", "Video with Sound","Video(No Sound)", "Audio Only"]
    lc = ttk.Combobox(windo, width=16, state="readonly")
    lc.pack()
    lc['values'] = dow_list
    lc.current(0)
    lc.place(x=280, y=234)

    lc.bind("<<ComboboxSelected>>", quality_choose)

def destroy_widget(widget):
    widget.destroy()

def download_video_thumbnail():
    try:
        vid_id = video.videoid
        im5.save(vid_id+'.jpg')
        msg = tk.Label(windo, text='Thumbnail Downloaded', width=25, height=2, fg="white", bg="midnightblue",
                        font=('times', 18, ' bold '))
        msg.place(x=274, y=370)
        windo.after(5000, destroy_widget, msg)
    except Exception as e:
        print(e)

def quality_choose(event):
    global lc1,best,down_qual
    cho = lc.get()
    if cho == "Video with Sound":
        down_qual = video.streams
        best = list(video.streams)
        best.insert(0, '--Select Quality--')
        for i, s in enumerate(best):
            best[i] = str(s).replace('normal:', '')
        lc1 = ttk.Combobox(windo, width=18, state="readonly")
        lc1.pack()
        lc1['values'] = best
        lc1.current(0)
        lc1.place(x=430, y=234)

    if cho == "Video(No Sound)":
        down_qual = video.videostreams
        best = list(video.videostreams)
        best.insert(0,'Select Video Quality')
        for i, s in enumerate(best):
            best[i] = str(s).replace('video:','')

        lc1 = ttk.Combobox(windo, width=18, state="readonly")
        lc1.pack()
        lc1['values'] = best
        lc1.current(0)
        lc1.place(x=430, y=234)

    if cho == "Audio Only":
        down_qual = video.audiostreams
        best = list(video.audiostreams)
        best.insert(0, 'Select Audio Quality')
        for i, s in enumerate(best):
            best[i] = str(s).replace('audio:','')
        lc1 = ttk.Combobox(windo, width=18, state="readonly")
        lc1.pack()
        lc1['values'] = best
        lc1.current(0)
        lc1.place(x=430, y=234)

    lc1.bind("<<ComboboxSelected>>", download_button)

def download_button(event):
    im7 = PIL.Image.open('./meta/down.png')
    im7 = im7.resize((140,43), PIL.Image.ANTIALIAS)
    sp_img7 = ImageTk.PhotoImage(im7)
    panel8 = Button(windo,command = download_vid, borderwidth=0, image=sp_img7, bg='white')
    panel8.image = sp_img7
    panel8.pack()
    panel8.place(x=580, y=223)

def download_vid():
    try:
        choice_qual = lc1.get()
        ind = int(best.index(choice_qual))
        new_ind = ind-1
        selected_qual = down_qual[new_ind]
        selected_qual.download()
        msg = tk.Label(windo, text='Stream Downloaded', width=25, height=2, fg="white", bg="midnightblue",
                       font=('times', 18, ' bold '))
        msg.place(x=274, y=370)
        windo.after(4000, destroy_widget, msg)

    except Exception as e:
        error = tk.Label(windo, text="Something went wrong!!", width=27, height=2, fg="white", bg="red",
                        font=('times', 18, ' bold '))
        error.place(x=274, y=370)
        windo.after(5000, destroy_widget, error)
        print(e)

def clear():
    txt2.delete(first=0,last=100)

im = PIL.Image.open('./meta/ylogo.png')
im = im.resize((200, 200), PIL.Image.ANTIALIAS)
wp_img = ImageTk.PhotoImage(im)
panel4 = Label(windo, image=wp_img, bg='white')
panel4.pack()
panel4.place(x=50, y=70)

im1 = PIL.Image.open('./meta/search.png')
im1 = im1.resize((40, 40), PIL.Image.ANTIALIAS)
sp_img = ImageTk.PhotoImage(im1)
panel5 = Button(windo, borderwidth=0,command = get_info, image=sp_img, bg='white')
panel5.pack()
panel5.place(x=750, y=175)

im2 = PIL.Image.open('./meta/eraser.png')
im2 = im2.resize((40, 40), PIL.Image.ANTIALIAS)
sp_img1 = ImageTk.PhotoImage(im2)
panel6 = Button(windo, borderwidth=0,command=clear, image=sp_img1, bg='white')
panel6.pack()
panel6.place(x=810, y=175)


pred = tk.Label(windo, text="YouTube Video Downloader", width=30, height=2, fg="white", bg="maroon2",
                font=('times', 25, ' bold '))
pred.place(x=274, y=10)

lab = tk.Label(windo, text="Enter your URL", width=18, height=1, fg="white", bg="blue2",
               font=('times', 16, ' bold '))
lab.place(x=394, y=120)

txt2 = tk.Entry(windo, borderwidth=7, width=43, bg="white", fg="black", font=('times', 15, ' bold '))
txt2.place(x=280, y=170)
# txt2.insert(tk.END, 'https://www.youtube.com/watch?v=p_dtI2bLWhY&list=RDMMgkCKTuR-ECI&index=7')

video_title = tk.Label(windo, width=10, height=1, fg="black", bg="spring green",
                           font=('times', 15, ' bold '))

video_dur = tk.Label(windo, width=10, height=1, fg="white", bg="dark violet",
                       font=('times', 15, ' bold '))

windo.mainloop()