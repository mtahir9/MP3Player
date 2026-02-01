import pygame
import os
from buttons import *

SCREEN_HEIGHT,SCREEN_WIDTH = 500,500
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

def main() ->None:
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("MP3Player")
    clock = pygame.Clock()
    running = True
    folder = "audios"
    mp3_list = []


    if not os.path.isdir(folder):
        print(f'Folder {folder} does not exist')
        return

    count = 0

    mp3_list = [file for file in os.listdir(folder) if file.endswith(".mp3")]
    font = pygame.font.Font(os.path.join("images", "Oxanium-Bold.ttf"), 40)
    audio_length = int(get_mp3_audio_len(folder, mp3_list[count]))
    audio_length_text = font.render(str(audio_length), True, (0,0,0))

    # for i in os.listdir(folder):
    #     if i.endswith(".mp3"):
    #         mp3_list.append(i) 

    back_btn = Button(btns[0], pygame.Vector2(120,300))
    backward_btn = Button(btns[5], pygame.Vector2(185, 300))
    play_pause_btn = Button(btns[3], pygame.Vector2(250,300))
    forward_btn = Button(btns[4], pygame.Vector2(310,300))
    next_btn = Button(btns[1], pygame.Vector2(375,300))
    # pause_btn = Button(btns[2], pygame.Vector2(650,800))

    
    mp3_cover_list = get_covers_from_folder(folder, mp3_list[count])
    mp3_list_len = len(mp3_list)
    # print(mp3_list_len)

    if not mp3_list:
        print("No")
        return
    # print(mp3_list)
    is_playing:bool = False
    play_img = pygame.image.load(os.path.join("images", "play.png")).convert_alpha()
    play_img = pygame.transform.scale(play_img, (40,40))

    pause_img = pygame.image.load(os.path.join("images", "pause.png")).convert_alpha()
    pause_img = pygame.transform.scale(pause_img, (40,40))

    # print(mp3_list)
    first:bool = False
    current_time = 0
    seek_time = 0

    while running:
        dt = clock.tick(60) // 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_btn.rect.collidepoint(event.pos):
                    count = (count + 1) % mp3_list_len
                    play_music(folder, mp3_list[count])
                    mp3_cover_list = get_covers_from_folder(folder, mp3_list[count])
                    audio_length = int(get_mp3_audio_len(folder, mp3_list[count]))
                    is_playing = True
                    play_pause_btn.image = pause_img
                if back_btn.rect.collidepoint(event.pos):
                    count = (count - 1) % mp3_list_len
                    play_music(folder, mp3_list[count])
                    mp3_cover_list = get_covers_from_folder(folder, mp3_list[count])
                    audio_length = int(get_mp3_audio_len(folder, mp3_list[count]))
                    is_playing = True
                    play_pause_btn.image = pause_img
                if backward_btn.rect.collidepoint(event.pos):
                    pass
                if forward_btn.rect.collidepoint(event.pos):
                    pass
                if play_pause_btn.rect.collidepoint(event.pos):
                    if is_playing:
                        pygame.mixer.music.pause()
                        is_playing = False
                        play_pause_btn.image = play_img
                    else:
                        if not first:
                            play_music(folder, mp3_list[count])
                            screen.blit(mp3_cover_list[0], mp3_cover_list[0].get_rect(center=(250,150)))
                            first = True
                        pygame.mixer.music.unpause()
                        play_pause_btn.image = pause_img
                        is_playing = True

        # fill screen
        screen.fill("sky blue")
        for i in range(len(mp3_cover_list)):
            if mp3_cover_list[i]:
                screen.blit(mp3_cover_list[i], mp3_cover_list[i].get_rect(center=(250,150)))
    
        if is_playing:
            current_time = pygame.mixer.music.get_pos() // 1000
        audio_length_text = font.render(f'{current_time//60}:{current_time%60:02d} / {audio_length//60}:{audio_length%60:02d}',
    True,
    (0,0,0))
        screen.blit(audio_length_text,audio_length_text.get_rect(center=(250,400)))


        screen.blit(next_btn.image, next_btn.rect)
        screen.blit(backward_btn.image, backward_btn.rect)
        screen.blit(play_pause_btn.image, play_pause_btn.rect)
        screen.blit(back_btn.image, back_btn.rect)
        screen.blit(forward_btn.image, forward_btn.rect)
    
        # update
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

