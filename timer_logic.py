from music_player import play_random_music, stop_music, play_alarm, resume_music
from resource import resource_path   # ✅ ADD
import os, random

FOCUS_TIME = 50 * 60
BREAK_TIME = 10 * 60

FOCUS_MUSIC_BASE = "assets/focus_music"
BREAK_MUSIC_DIR = "assets/break_music"
ALARM_DIR = "assets/sounds"


state = "IDLE"
remaining_time = 0
previous_state = None
focus_music_type = "lofi_rain"


# ---------------- MUSIC HELPERS ----------------

def play_random_alarm():
    alarm_dir = resource_path(ALARM_DIR)


    if not os.path.exists(ALARM_DIR):
        print("Alarm directory not found:", ALARM_DIR)
        return

    alarms = [
        f for f in os.listdir(ALARM_DIR)
        if f.endswith((".mp3", ".wav"))
    ]

    if not alarms:
        print("No alarm files found")
        return

    alarm = random.choice(alarms)
    play_alarm(os.path.join(ALARM_DIR, alarm))


def play_focus_music():
    file_path = f"{FOCUS_MUSIC_BASE}/{focus_music_type}.mp3"
    play_random_music(file_path)

def play_random_break_music():
    break_dir = resource_path(BREAK_MUSIC_DIR)   
    if not os.path.exists(BREAK_MUSIC_DIR):
        print("Break music directory not found:", BREAK_MUSIC_DIR)
        return

    files = [
        f for f in os.listdir(BREAK_MUSIC_DIR)
        if f.endswith((".mp3", ".wav"))
    ]

    if not files:
        print("No break music files found")
        return

    file_path = os.path.join(BREAK_MUSIC_DIR, random.choice(files))
    play_random_music(file_path)


# ---------------- TIMER CONTROL ----------------

def start_focus():
    global state, remaining_time
    state = "FOCUS"
    remaining_time = FOCUS_TIME
    stop_music()
    play_focus_music()


def start_break():
    global state, remaining_time
    state = "BREAK"
    remaining_time = BREAK_TIME
    stop_music()
    play_random_alarm()
    play_random_break_music()



def pause():
    global state, previous_state
    if state in ("FOCUS", "BREAK"):
        previous_state = state
        state = "PAUSED"
        stop_music()


def resume():
    global state, previous_state
    if state == "PAUSED":
        state = previous_state
        resume_music()
        previous_state = None


def reset():
    global state, remaining_time, previous_state
    state = "IDLE"
    remaining_time = 0
    previous_state = None
    stop_music()


# ---------------- PLAY BUTTON ----------------

def play_button_action():
    if state == "IDLE":
        start_focus()
    elif state == "PAUSED":
        resume()


# ---------------- TICK (CALLED BY TKINTER) ----------------

def tick():
    """
    Decreases timer by 1 second.
    Returns True if time changed, False otherwise.
    """
    global remaining_time

    if state not in ("FOCUS", "BREAK"):
        return False

    remaining_time -= 1

    # Clamp to zero to avoid negatives
    if remaining_time <= 0:
        remaining_time = 0
        if state == "FOCUS":
            start_break()
        else:
            start_focus()

    return True
