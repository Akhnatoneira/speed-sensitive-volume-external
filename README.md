# 🚗 Speed Sensitive Volume Controller (External) 🎵

A modern, external tool for Assetto Corsa that automatically adjusts your music volume based on your car's speed. Developed by **1Developpeur** for an immersive racing experience! 🏁

---

## 📋 Project Description

**Speed Sensitive Volume Controller (External)** is a Windows application designed for Assetto Corsa. It dynamically controls the volume of your favorite music apps (like Spotify, VLC, etc.) according to your in-game speed, making your sim racing sessions more realistic and enjoyable. No more fiddling with the volume knob while racing—let your speed set the mood! 🎶

---

## ✨ Features

- 🎚️ **Automatic Volume Adjustment**: Volume increases with speed, decreases when slowing down
- 🎮 **Assetto Corsa Integration**: Reads real-time speed data from the game
- 🎵 **Supports Popular Music Apps**: Spotify, VLC, Deezer, Tidal, and more
- ⚙️ **Easy Configuration**: Interactive setup for selecting apps and tuning volume/speed ranges
- 🖥️ **External Program**: Runs independently from Assetto Corsa
- 🛠️ **Customizable**: Edit thresholds and preferences anytime

---

# 🚗 Speed Sensitive Volume Controller (External) 🎵
## 🚀 Installation

**Python version required: 3.9.13 or higher**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/1Developpeur/speed-sensitive-volume-external.git
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the program:**
   ```bash
   python main.py
   ```

---

## 🛠️ Configuration & Usage

- On first launch, select which music apps to control.
- Optionally, adjust minimum/maximum volume and speed thresholds.
- The tool will automatically detect your speed in Assetto Corsa and adjust the volume accordingly.
- To change settings later, simply restart the program.

---

## 🎧 Supported Music Apps

- Spotify
- Deezer
- Tidal
- Apple Music
- Amazon Music
- YouTube Music
- Pandora
- SoundCloud
- VLC

---

## ❓ FAQ

**Q: Does this work with other games?**
- No, this version is tailored for Assetto Corsa.

**Q: Can I add more music apps?**
- Yes! Edit the `music_apps` list in `main.py` to add more.

**Q: Is this safe for online racing?**
- Yes, it only reads speed data and controls your local audio sessions.

---

## 🙏 Credits

- Developed by [1Developpeur](https://github.com/1Developpeur)
- Uses [pycaw](https://github.com/AndreMiras/pycaw) for audio control
- Inspired by the Assetto Corsa community

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 🌟 Star this repo if you like it!

Enjoy your immersive Assetto Corsa experience! 🏎️🎶