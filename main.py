from pycaw.pycaw import AudioUtilities, IAudioSessionManager2, IAudioSessionControl
from pycaw.constants import AudioSessionState
from InquirerPy.validator import EmptyInputValidator
from ac_interface import AssettoCorsaData
import configparser, time, psutil, math, subprocess, socket
from InquirerPy import inquirer
from typing import Union
from threading import Thread

class Config:
    def __init__(self) -> None:
        self.configPath = r"config.ini"
        self.config = configparser.ConfigParser()
        self.config.read(self.configPath)
    
    def get(self, section="SpeedSensitiveVolume", option=""):
        return self.config.getint(section, option)
    
    def set(self, section="SpeedSensitiveVolume", option="", value=None):
        self.config.set(section, option, str(value))
        self.config.write(open(self.configPath, 'w'))

class SpeedSensitiveVolume:
    def __init__(self) -> None:
        self.assettoReader = AssettoCorsaData()
        self.assettoReader.start()
        self.config = Config()
        
        self.scan_delay : Union[int, float] = self.config.get(option='scan_delay') / 1000
        self.min_volume : int = self.config.get(option='min_volume')
        self.max_volume : int = self.config.get(option='max_volume')
        self.min_speed  : int = self.config.get(option='min_speed')
        self.max_speed  : int = self.config.get(option='max_speed')
        
        self.running_apps: list = []
        self.music_apps: list = [
            "spotify", "deezer", "tidal", "applemusic",
            "amazon music", "youTube music", "pandora",
            "soundcloud", "vlc"
        ]
        self.last_time: int = self.get_time()
        self.last_volume: int = 0
        self.debug: bool = False
        self.controlled_apps: list = []
        self.volume_change_threshold: int = 1
        
        self.volume: int = 0
        self.speed : int = 0
        self.ingame_stat: bool = False

    def wait_for_connection(self):
        while True:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect(('localhost', 13370))
                print("+ Connected to in-game stat server")
                return
            except:
                pass

    def send_volume(self):
        while True:
            try:
                self.client_socket.send(f"{self.volume}|{self.speed}".encode())
            except:
                self.wait_for_connection()
            time.sleep(self.scan_delay)

    def get_time(self):
        return round(time.time()*1000)

    def get_audio_sessions(self):
        sessions = AudioUtilities.GetAllSessions()
        audio_sessions = []

        for session in sessions:
            if session.State == AudioSessionState.Active:
                audio_sessions.append(session)
        
        return audio_sessions

    def set_volume(self, volume: int, speed: int):
        for session in self.sessions:
            try:
                pid = session.ProcessId
                process = psutil.Process(pid)
                if any(app.lower() in process.name().lower() for app in self.controlled_apps):
                    session.SimpleAudioVolume.SetMasterVolume(volume / 100.0, None)
                    print(f"Set volume for {process.name()} to {volume}% at speed {speed} km/h      ", end="\r")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def scan_processes(self):
        try:
            self.running_apps.clear()
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.name().lower().split('.exe')[0] in self.music_apps:
                    self.running_apps.append((proc.name(), proc.pid))
        except Exception as err:
            print(f"Error: {err}")
    
    def getSpeed(self) -> int:
        return round(self.assettoReader.getData()['speed'])

    def calculate_volume(self, speed):
        if speed <= self.min_speed:
            return self.min_volume
        if speed >= self.max_speed:
            return self.max_volume

        volume_range = float(self.max_volume - self.min_volume)
        
        # Exponential scaling for volume adjustment
        volume_expo = int(self.min_volume + ((speed ** 2) / (self.max_speed ** 2)) * volume_range)
        
        volume = volume_expo
        
        if self.debug:
            ac.log(f"Volume will be set to: {volume} | for speed: {speed}")
        
        return volume

    def setup(self):
        self.scan_processes()
        
        app_names = []
        if self.running_apps:
            for app in self.running_apps:
                if not app[0] in app_names:
                    app_names.append(app[0])
        
        self.sessions = self.get_audio_sessions()
        if app_names:
            self.controlled_apps = inquirer.rawlist(
                message="Select music apps to be controlled:",
                choices=app_names,
                default=1,
                multiselect=True,
                transformer=lambda result: ", ".join(result),
                validate=lambda result: len(result) > 0,
                invalid_message="Minimum 1 selections",
            ).execute()

            proceed = inquirer.confirm(message="Would you like to edit config?", default=True).execute()
            if proceed:
                self.min_volume = inquirer.number(
                    message="Minimum volume (0, 100):",
                    min_allowed=0,
                    max_allowed=100,
                    default=self.min_volume,
                    validate=EmptyInputValidator(),
                ).execute()
                self.max_volume = inquirer.number(
                    message="Maximum volume (1, 100):",
                    min_allowed=1,
                    max_allowed=100,
                    default=self.max_volume,
                    validate=EmptyInputValidator(),
                ).execute()
                self.min_speed = inquirer.number(
                    message="Minimum speed (0, 400):",
                    min_allowed=0,
                    max_allowed=400,
                    default=self.min_speed,
                    validate=EmptyInputValidator(),
                ).execute()
                self.max_speed = inquirer.number(
                    message="Maximum speed (1, 400):",
                    min_allowed=1,
                    max_allowed=400,
                    default=self.max_speed,
                    validate=EmptyInputValidator(),
                ).execute()

                self.config.set(option="min_volume", value=self.min_volume)
                self.config.set(option="max_volume", value=self.max_volume)
                self.config.set(option="min_speed", value=self.min_speed)
                self.config.set(option="max_speed", value=self.max_speed)
                print('+ New config has been successfully saved.')
            else:
                print('+ No changes have been made.')
        else:
            print('- No music apps have been found!')
            exit()  

    def run(self):
        self.setup()
        if self.ingame_stat:
            self.wait_for_connection()
            Thread(target=self.send_volume, daemon=True).start()
        
        while True:
            if (self.get_time() - self.last_time) >= self.scan_delay:
                self.last_time = self.get_time()
                current_speed = self.getSpeed()
                volume = self.calculate_volume(current_speed)
                if volume != self.last_volume:# and abs(volume - self.last_volume) > self.volume_change_threshold:
                    self.last_volume = volume
                    self.set_volume(volume, current_speed)
                    self.volume = volume
                    self.speed = current_speed
            
            time.sleep(self.scan_delay)

# Running the system
ssv = SpeedSensitiveVolume()
ssv.run()
