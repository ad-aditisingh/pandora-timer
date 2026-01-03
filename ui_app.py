import tkinter as tk
from PIL import Image, ImageTk
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#Round Boxes
def style_button(btn):
    btn.config(
        relief="flat",
        bd=1,
        highlightthickness=0,
        padx=12,
        pady=6,
        bg="#445DDC",
        activebackground="#5C75F0"
    )

#cat animation
def create_cat_animation(
    parent,
    sprite_path,
    initial_row,
    frame_count=8,
    size=64,
    scale=2.0,
    delay=180
):
    sprite = Image.open(sprite_path)
    scaled_size = int(size * scale)

    label = tk.Label(parent, bg="#6F88FC")
    label.pack(pady=10)

    frames = []
    index = 0

    def load_frames(row):
        nonlocal frames, index
        frames = []
        index = 0

        for i in range(frame_count):
            frame = sprite.crop((
                i * size,
                row * size,
                (i + 1) * size,
                (row + 1) * size
            ))
            frame = frame.resize(
                (scaled_size, scaled_size),
                Image.NEAREST
            )
            frames.append(ImageTk.PhotoImage(frame))

    def animate():
        nonlocal index
        if frames:
            label.config(image=frames[index])
            label.image = frames[index]
            index = (index + 1) % frame_count
        label.after(delay, animate)

    load_frames(initial_row)
    animate()

    # 🔴 expose animation switcher
    label.load_frames = load_frames
    return label


print("UI file started")

root = tk.Tk()

#Heading
root.title("Pandora Timer")
root.geometry("360x420")
root.resizable(False, False)
root.configure(bg="#6F88FC")

#Cat state animations
CAT1_STATE_ROWS = {
    "READY": 36,     # sit and wave r paw
    "FOCUS": 13,     # laying and licking paw
    "BREAK": 39,      # walking
    "PAUSED": 18      #scratching with left paw
}

#global logic
timer_logic = None

def load_logic():
    global timer_logic
    import timer_logic as tl
    timer_logic = tl
    print("Timer logic loaded")

#Frames
welcome_frame = tk.Frame(root, bg="#6F88FC")
main_frame = tk.Frame(root, bg="#6F88FC")

for frame in (welcome_frame, main_frame):
    frame.place(x=0, y=0, width=360, height=420)

#Welcome Screen
title_label = tk.Label(
    welcome_frame,
    text="Pandora Timer",
    fg="white",
    bg="#6F88FC",
    font=("VT323", 24)
)
title_label.pack(pady=(10, 5))

#Welcom screen cat
create_cat_animation(
    parent=welcome_frame,
    sprite_path=resource_path("assets/images/cats/cat2.png"),
    initial_row=12,   #  FIXED
    frame_count=6,
    scale=1.7,
    delay=180
)


#Timer Selection
tk.Label(
    welcome_frame,
    text="Focus Time",
    fg="white",
    bg="#6F88FC",
    font=("VT323", 14)
).pack(pady=(0, 6))

time_buttons_frame = tk.Frame(welcome_frame, bg="#6F88FC")
time_buttons_frame.pack(pady=(0, 16))

selected_time = None
selected_time_button = None

def select_time(btn, value):
    global selected_time, selected_time_button
    if selected_time_button:
        selected_time_button.config(bg="#445DDC")
    btn.config(bg="#5C75F0")
    selected_time_button = btn
    selected_time = value

def create_time_button(text, value):
    btn = tk.Button(
        time_buttons_frame,
        text=text,
        width=8,
        height=1,
        bg="#445DDC",
        fg="white",
        font=("VT323", 12),
        relief="flat",
        command=lambda: select_time(btn, value),
        activebackground="#5C75F0"
    )
    btn.pack(side="left", padx=6)
    return btn

create_time_button("50–10", (50, 10))
create_time_button("60–10", (60, 10))
create_time_button("30–5",  (30, 5))



#Sound selection
tk.Label(
    welcome_frame,
    text="Focus Sound",
    fg="white",
    bg="#6F88FC",
    font=("VT323", 14)
).pack(pady=(0, 6))

sound_buttons_frame = tk.Frame(welcome_frame, bg="#6F88FC")
sound_buttons_frame.pack(pady=(0, 12))

selected_sound = None
selected_sound_button = None

def select_sound(btn, sound):
    global selected_sound, selected_sound_button
    if selected_sound_button:
        selected_sound_button.config(bg="#445DDC")
    btn.config(bg="#5C75F0")
    selected_sound_button = btn
    selected_sound = sound

def create_sound_button(parent, label, value):
    btn = tk.Button(
        parent,
        text=label,
        width=12,
        height=1,
        bg="#445DDC",
        fg="white",
        font=("VT323", 12),
        relief="flat",
        command=lambda: select_sound(btn, value),
        activebackground="#5C75F0"
    )
    return btn

# Row 1
row1 = tk.Frame(sound_buttons_frame, bg="#6F88FC")
row1.pack(pady=2)

create_sound_button(row1, "lofi + rain", "lofi_rain").pack(side="left", padx=4)
create_sound_button(row1, "lofi + chill", "lofi_chill").pack(side="left", padx=4)

# Row 2
row2 = tk.Frame(sound_buttons_frame, bg="#6F88FC")
row2.pack(pady=2)

create_sound_button(row2, "white noise", "white_noise").pack(side="left", padx=4)
create_sound_button(row2, "kpop", "kpop").pack(side="left", padx=4)

# Row 3
row3 = tk.Frame(sound_buttons_frame, bg="#6F88FC")
row3.pack(pady=2)

create_sound_button(row3, "indian", "indian").pack(side="left", padx=4)

#start logic
def start_focus_from_welcome():
    global timer_logic

    if not selected_time or not selected_sound:
        return

    if timer_logic is None:
        import timer_logic as tl
        timer_logic = tl

    timer_logic.reset()

    focus, rest = selected_time
    timer_logic.FOCUS_TIME = focus * 60
    timer_logic.BREAK_TIME = rest * 60
    timer_logic.focus_music_type = selected_sound
    welcome_frame.place_forget()
    main_frame.place(x=0, y=0, width=360, height=420)
    main_frame.tkraise()


    timer_label.config(text=f"{focus:02d}:00")
    state_label.config(text="READY")



#Start button
start_arrow = tk.Button(
    welcome_frame,
    text=">",
    width=1,
    height=1,
    bg="#394FCC",
    fg="white",
    font=("VT323", 16),
    relief="flat",
    command=start_focus_from_welcome
)

#Placement of start button
start_arrow.place(
    x=360 - 50,   # window width - offset
    y=420 - 60    # window height - offset
)
style_button(start_arrow)

#Main frame
title_label = tk.Label(
    main_frame,
    text="Pandora Timer",
    fg="white",
    bg="#6F88FC",
    font=("VT323", 24)
)
title_label.pack(pady=(25, 5))

#Main frame cat
timer_cat = create_cat_animation(
    parent=main_frame,
    sprite_path=resource_path("assets/images/cats/cat1.png"),
    initial_row=CAT1_STATE_ROWS["READY"],
    frame_count=8,
    scale=2.2,
    delay=220
)


timer_cat.pack_configure(pady=(10, 5))


#timer
timer_label = tk.Label(
    main_frame,
    text="00:00",
    fg="white",
    bg="#6F88FC",
    font=("VT323", 36)
)
timer_label.pack(pady=(20, 5))

#State
state_label = tk.Label(
    main_frame,
    text="READY",
    fg="#B8F2C2",
    bg="#6F88FC",
    font=("VT323", 12)
)
state_label.pack()


#Control buttons of main
controls = tk.Frame(main_frame, bg="#6F88FC")
controls.pack(pady=20)

def safe_call(fn):
    if timer_logic:
        fn()

btn_pause = tk.Button(
    controls,
    text="||",
    width=4,
    height=2,
    bg="#445DDC",
    fg="white",
    font=("VT323", 14),
    relief="flat",
    command=lambda: safe_call(timer_logic.pause)
)
btn_pause.pack(side="left", padx=8)
style_button(btn_pause)


btn_play = tk.Button(
    controls,
    text=">",
    width=4,
    height=2,
    bg="#445DDC",
    fg="white",
    font=("VT323", 14),
    relief="flat",
    command=lambda: safe_call(timer_logic.play_button_action)
)
btn_play.pack(side="left", padx=8)
style_button(btn_play)

btn_reset = tk.Button(
    controls,
    text="R",
    width=4,
    height=2,
    bg="#445DDC",
    fg="white",
    font=("VT323", 14),
    relief="flat",
    command=lambda: safe_call(timer_logic.reset)
)
btn_reset.pack(side="left", padx=8)
style_button(btn_reset)



welcome_frame.tkraise()

# IMPORTANT: load logic AFTER UI exists
root.after(50, load_logic)

#timer ui update
last_state = None

def update_timer_ui():
    global last_state

    if timer_logic:
        remaining = timer_logic.remaining_time
        state = timer_logic.state

        state_label.config(text=state)

        if remaining > 0:
            m, s = divmod(remaining, 60)
            timer_label.config(text=f"{m:02d}:{s:02d}")

        #  change cat movement on state change
        if state != last_state:
            row = CAT1_STATE_ROWS.get(state, CAT1_STATE_ROWS["READY"])
            timer_cat.load_frames(row)
            last_state = state

    root.after(300, update_timer_ui)


update_timer_ui()

def tick_loop():
    if timer_logic:
        timer_logic.tick()
    root.after(1000, tick_loop)  # call every 1 second

tick_loop()

print("About to enter mainloop")
root.mainloop()
