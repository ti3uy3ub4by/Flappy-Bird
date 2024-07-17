import os
import pygame

# Tạo một từ điển để lưu trữ các sprite
sprites = {}
audios = {}


def load_sprites():
    # Định nghĩa đường dẫn tới thư mục chứa các sprite
    path = os.path.join("assets", "sprites")

    # Duyệt qua tất cả các tệp trong thư mục sprite
    for file in os.listdir(path):
        # Tải mỗi tệp hình ảnh và lưu trữ vào từ điển sprites với khóa là tên tệp (không có phần mở rộng)
        sprites[file.split('.')[0]] = pygame.image.load(os.path.join(path, file))


def get_sprite(name):
    # Trả về sprite theo tên từ từ điển sprites
    return sprites[name]


def load_audios():
    path = os.path.join("assets", 'audios')
    for file in os.listdir(path):
        audios[file.split('.')[0]] = pygame.mixer.Sound(os.path.join(path, file))


def play_audio(name):
    audios[name].play()

