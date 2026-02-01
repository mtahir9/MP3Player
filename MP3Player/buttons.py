from enum import Enum
import pygame
import os
import io
from mutagen.mp3 import MP3, MPEGInfo
# from mutagen.id3._frames import APIC
from mutagen.id3 import ID3, APIC

class Button(pygame.sprite.Sprite):
    def __init__(self, surf:str, pos) -> None:
        self.surf = surf
        image = pygame.image.load(os.path.join("images", self.surf)).convert_alpha()
        image = rescale(image, (40,40))
        self.image = image
        self.rect = self.image.get_frect(center=pos)
    # def update(self, dt):
    #     pass

def get_mp3_audio_len(folder, mp3_file_name):
    file_path = os.path.join(folder, mp3_file_name)
    audio_length = MP3(file_path).info
    return audio_length.length

def load_mp3_cover(folder, mp3_file_name) -> pygame.Surface | None:
    file_path = os.path.join(folder, mp3_file_name)

    if not os.path.exists(file_path):
        print(f"File {file_path} not found")
        return None
    audio = ID3(file_path)
    apic_frames = audio.getall("APIC")

    if not apic_frames:
        print(f"No cover found in {file_path}")
        return None
    apic = apic_frames[0]
    image_data = apic.data

    image_file = io.BytesIO(image_data)
    image = pygame.image.load(image_file).convert_alpha()

    image = rescale(image, (300,300))

    if not apic:
        print("No cover metadata")
        return None
    if apic:
        return image

def get_covers_from_folder(folder, mp3_file_name) -> list | None:
    count = len(os.listdir(folder))
    covers_list = []
    for _ in range(count):
        covers_list.append(load_mp3_cover(folder,mp3_file_name))
    if count:
        return covers_list
    return None

class ButtonState(Enum):
    STOPPED = 0
    PLAYING = 1
    PAUSED = 2

def rescale(image, size):
    image = pygame.transform.scale(image, size)
    return image

def play_music(folder, song_name):
    
    file_path = os.path.join(folder, song_name)
    if not os.path.exists(file_path):
        print("File not found")
        return 

    pygame.mixer.music.load(file_path) 
    pygame.mixer.music.play()

    print(f"\nNow playing: {song_name}")

btns = ["back.png", "next.png", "pause.png", "play.png", "forward-arrow.png", "backward-arrow.png"]
