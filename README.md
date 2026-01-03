#  Pandora Timer

Pandora Timer is a **cute, distraction-free focus timer desktop app** inspired by the Pomodoro technique — with animated pixel cats, background music, and a clean UI.

It is designed to make long focus sessions feel calm, enjoyable, and less tiring.

---

##  Features

-  Focus timer presets: **50–10**, **60–10**, **30–5**
-  Focus music options:
  - Lofi + Rain
  - Lofi + Chill
  - White Noise
  - K-Pop
  - Indian
-  Animated pixel cats (different animations for focus, break, pause)
-  Single play button for **Start / Resume**
-  Pause and  Reset controls
-  Random alarm sound on session switch
-  Works as:
  - Python desktop app
  - Windows executable (planned)

---

##  Tech Stack

- **Python 3.12**
- **Tkinter** – UI
- **Pygame** – Audio playback
- **Pillow (PIL)** – Sprite animation handling

---

##  Project Structure

pandora_timer/
│
├── ui_app.py # Main UI application
├── timer_logic.py # Timer state machine & logic
├── music_player.py # Audio handling
├── requirements.txt
│
├── assets/
│ ├── images/
│ │ └── cats/ # Pixel cat sprites
│ ├── focus_music/ # Focus music files (.mp3)
│ ├── break_music/ # Break music files
│ └── sounds/ # Alarm sounds
│
└── README.md


---

##  How to Run (Local)

###  Clone the repository
```bash
git clone https://github.com/ad-aditisingh/pandora-timer.git
cd pandora-timer
