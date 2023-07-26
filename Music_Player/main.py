from tkinter import * 
import tkinter as tk
from tkinter import filedialog
import pygame
from pygame import mixer
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
 
root = Tk()
root.title('MP3 Music Player')
root.iconbitmap('E:/Internship/Code_Clause/Music_Player/icons/icon.ico')
root.geometry("500x550")
root.configure(bg='#F6F4EB')

# Initialze Pygame Mixer
pygame.mixer.init()

# Change Volume Function
def set_vol(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1

# Create slider function
def slide(x):
    song = song_box.get(ACTIVE)
    song = f'E:/Internship/Code_Clause/Music_Player/Music_Playlist/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(slider.get( )))

# Function to add one song to playlist
def add_song():
    # Open file explorer and select music files
    song = filedialog.askopenfilename(initialdir="Music_Playlist/", title="Select A Song", filetypes=(("mp3 files", "*.mp3"),))
    
    # Strip out directory info and extension
    song = song.replace("E:/Internship/Code_Clause/Music_Player/Music_Playlist/", "")
    song = song.replace(".mp3", "")

    # Add song to list box
    song_box.insert(END, song)

# Function to add multiple songs to playlist
def add_songs():
    songs = filedialog.askopenfilenames(initialdir="Music_Playlist/", title="Select A Song", filetypes=(("mp3 files", "*.mp3"),))

    # Loop through to replace directory and info, extension, etc.
    for song in songs:
        # Strip out directory info and extension
        song = song.replace("E:/Internship/Code_Clause/Music_Player/Music_Playlist/", "")
        song = song.replace(".mp3", "")
 
        # Add song to list box
        song_box.insert(END, song)

# Grab song length time info
def play_time():

    if stopped:
        return

    # Grab current song elapsed time
    current_time = pygame.mixer.music.get_pos() / 1000

    # Convert to time
    converted_time = time.strftime('%M:%S', time.gmtime(current_time))

    # Get current song tuple no.
    current_song_index = song_box.curselection()

    # Grab song title from playlist
    song = song_box.get(ACTIVE)
    song = f'E:/Internship/Code_Clause/Music_Player/Music_Playlist/{song}.mp3'

    # Get Song Length with Mutagen
    song_mut = MP3(song)

    # Load Song Length with Mutagen
    global song_length
    song_length = song_mut.info.length

    # Convert to time format
    converted_length = time.strftime('%M:%S', time.gmtime(song_length))

    # Increase current time by 1 second
    current_time += 1
    global slider_pos

    if int(slider.get()) == int(song_length):
        status_bar.config(text=f'{converted_length}')

    elif paused:
        pass

    elif int(slider.get()) == int(current_time):
        # Update slider position
        
        slider_pos = int(song_length)
        slider.config(to=slider_pos, value=int(current_time))
    else:
        # Update slider position
        slider_pos = int(song_length)
        slider.config(to=slider_pos, value=int(slider.get()))

        converted_time = time.strftime('%M:%S', time.gmtime(slider.get()))
        
        # Output the time to status bar
        status_bar.config(text=f'{converted_time}/{converted_length}')

        next_time = int(slider.get()) + 1
        slider.config(value=next_time)

    # Update the time
    status_bar.after(1000, play_time)

# Function to delete one song
def delete_song():
    stop()
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

# Function to delete all songs
def delete_songs():
    stop()
    song_box.delete(0, END)
    pygame.mixer.music.stop()

# Function to play song
def play():
    global stopped 
    stopped = False

    song = song_box.get(ACTIVE)
    song = f'E:/Internship/Code_Clause/Music_Player/Music_Playlist/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_set(ACTIVE)

    # Call the play_time function
    play_time()

global stopped
stopped = False

# Function to stop song
def stop():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    # Configure status bar and slider
    status_bar.config(text='')
    slider.config(value=0)

    # Stop Variable
    global stopped
    stopped = True

# Create global pause variable
global paused
paused = FALSE 

# Function to Pause and Unpause Song
def pause(is_paused):
    global paused
    paused = is_paused
    # UnPause
    if paused:
         pygame.mixer.music.unpause()
         paused = FALSE
    # Pause
    else:
        pygame.mixer.music.pause()
        paused = True

# Play next song in playlist
def next_song():
    # Configure status bar and slider
    status_bar.config(text='')
    slider.config(to_=slider_pos, value=0)

    # Get current song tuple no.
    current_song_index = song_box.curselection()[0]

    # Calculate next song index
    next_one = (current_song_index + 1) % song_box.size()

    # Grab song title from playlist
    song = song_box.get(next_one)
    song = f'E:/Internship/Code_Clause/Music_Player/Music_Playlist/{song}.mp3'

    # Load and Play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Clear active bar in playlist listbox
    song_box.selection_clear(0, END)

    # Activate new song bar
    song_box.activate(next_one)

    # Set Active bar to next song 
    song_box.selection_set(next_one, last=None)

# Play previous song in playlist
def prev_song():
    # Configure status bar and slider
    status_bar.config(text='')
    slider.config(to_=slider_pos, value=0)

    # Get current song tuple no.
    current_song_index = song_box.curselection()[0]

    # Calculate the previous song index
    prev_song_index = (current_song_index - 1) % song_box.size()

    # Grab song title from playlist
    song = song_box.get(prev_song_index)
    song = f'E:/Internship/Code_Clause/Music_Player/Music_Playlist/{song}.mp3'

    # Load and Play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Clear active bar in playlist listbox
    song_box.selection_clear(0, END)

    # Activate new song bar
    song_box.activate(prev_song_index)

    # Set Active bar to next song 
    song_box.selection_set(prev_song_index, last=None)

# Top layout with title
title_label = tk.Label(root, text="Music Player", font=("Times New Roman", 20, "bold"))
title_label.pack(pady=10)
title_label.configure(bg='#F6F4EB')

# Create Playlist Box
song_box = Listbox(root, bg="grey", fg="white", width=60, selectbackground="white", selectforeground="black")
song_box.pack(pady=10,fill=BOTH)

# Define Player Control Button images
backward_btn_img = PhotoImage(file='E:/Internship/Code_Clause/Music_Player/icons/prev.png')
play_btn_img = PhotoImage(file='E:/Internship/Code_Clause/Music_Player/icons/play.png')
pause_btn_img = PhotoImage(file='E:/Internship/Code_Clause/Music_Player/icons/pause.png')
forward_btn_img = PhotoImage(file='E:/Internship/Code_Clause/Music_Player/icons/next.png')
stop_btn_img = PhotoImage(file='E:/Internship/Code_Clause/Music_Player/icons/stop.png')

# Create Player Control Frame
controls_frame = Frame(root)
controls_frame.pack()
controls_frame.configure(bg='#F6F4EB')

# Create Player Control Buttons
backward_button = Button(controls_frame, image = backward_btn_img, borderwidth=0, command=prev_song)
play_button = Button(controls_frame, image = play_btn_img, borderwidth=0, command=play)
pause_button = Button(controls_frame, image = pause_btn_img, borderwidth=0, command= lambda: pause(paused))
forward_button = Button(controls_frame, image = forward_btn_img, borderwidth=0, command=next_song)
stop_button = Button(controls_frame, image = stop_btn_img, borderwidth=0, command=stop)

backward_button.grid(row = 0, column = 0, padx = 10)
play_button.grid(row = 0, column = 1, padx = 10)
pause_button.grid(row = 0, column = 2, padx = 10)
forward_button.grid(row = 0, column = 3, padx = 10)
stop_button.grid(row = 0, column = 4, padx = 10)

# Create a Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add Song Menu and Function
add_songs_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Add Songs", menu=add_songs_menu)
# Add One Song
add_songs_menu.add_command(label='Add one song to Playlist', command=add_song)
# Add multiple songs
add_songs_menu.add_command(label='Add multiple songs to Playlist', command=add_songs)

# Delete Song Menu and Function
delete_songs_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Delete Songs", menu=delete_songs_menu)
# Delete One Song
delete_songs_menu.add_command(label='Delete one song from Playlist', command=delete_song)
# Delete all songs
delete_songs_menu.add_command(label='Delete all songs from Playlist', command=delete_songs)

# Create music position slider
slider = ttk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, value=0, command=slide, length=360)
slider.pack(pady=8)

# Customize the style of ttk.Scale to change the background color
style = ttk.Style()

# Modify the map for the Horizontal.TScale element
style.map("Horizontal.TScale", background=[('active', '#F6F4EB'), ('!active', '#F6F4EB')])

# Create Status Bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E, bg='#F6F4EB')
status_bar.pack(fill=X, ipady=2)

# Create Volume Control Frame
vol_frame = Frame(root)
vol_frame.pack()
vol_frame.configure(bg='#F6F4EB')

# Create Volume Label
label_vol = Label(vol_frame, text="Drag the slider to set volume", bg='#F6F4EB')
label_vol.pack(pady=10)

# Create Volume Slider
scale = Scale(vol_frame, from_=0, to=100, orient=HORIZONTAL, command=set_vol, length=400, bg='#F6F4EB')
scale.set(70)
scale.pack()

# Create Footer Label
footer_label = Label(root, text='Made by Param Dhingana \n Python Development Intern @ Code Clause', bd=5, relief=GROOVE, bg='#F6F4EB')
footer_label.pack(fill=X, ipady=10, side=BOTTOM)

root.mainloop()