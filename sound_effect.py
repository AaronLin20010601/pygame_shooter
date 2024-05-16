import pygame

class Sound_effect():
    def __init__(self):
        #starting set
        self.volume = pygame.mixer.music.set_volume(0.3)
        self.jump_sound = pygame.mixer.Sound("audio/jump.wav")
        self.shot_sound = pygame.mixer.Sound("audio/shot.wav")
        self.grenade_sound = pygame.mixer.Sound("audio/grenade.wav")

        self.jump_sound.set_volume(0.5)
        self.shot_sound.set_volume(0.5)
        self.grenade_sound.set_volume(0.5)

    #play background music
    def play_music(self):
        pygame.mixer.music.load("audio/music2.mp3")
        pygame.mixer.music.play(-1,0.0,5000)

    #jump sound effect
    def jump_effect(self):
        self.jump_sound.play()

    #shot sound effect
    def shot_effect(self):
        self.shot_sound.play()

    #grenade sound effect
    def grenade_effect(self):
        self.grenade_sound.play()