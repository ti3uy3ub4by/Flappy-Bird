import os
import pygame
import assets
import configs
from objects.background import Background
from objects.bird import Bird
from objects.column import Column
from objects.floor import Floor
from objects.gameover_message import GameOverMessage
from objects.gamestart_message import GameStartMessage
from objects.score import Score

# Khởi tạo Pygame
pygame.init()

# Thiết lập màn hình hiển thị với kích thước lấy từ tệp cấu hình configs
screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
pygame.display.set_caption("by Pham Thanh Tung")

# Đặt icon cho chương trình
icon_path = os.path.join('assets', 'icons', 'red_bird.png')
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)

# Tạo đối tượng đồng hồ để quản lý thời gian và tốc độ khung hình
clock = pygame.time.Clock()

# Định nghĩa sự kiện tạo cột
COLUMN_CREATE_EVENT = pygame.USEREVENT

# Biến trạng thái trò chơi
running = True
gameover = False
gamestarted = False

# Tải âm thanh và sprite từ tệp assets
assets.load_audios()
assets.load_sprites()

# Tạo nhóm các sprite để quản lý và vẽ chúng
sprites = pygame.sprite.LayeredUpdates()

def create_sprites():
    """
    Hàm tạo các sprite cần thiết cho trò chơi.
    Trả về đối tượng chim, thông báo bắt đầu trò chơi, và điểm số.
    """
    Background(0, sprites)
    Background(1, sprites)
    Floor(0, sprites)
    Floor(1, sprites)
    return Bird(sprites), GameStartMessage(sprites), Score(sprites)

# Khởi tạo các đối tượng chính trong trò chơi
bird, game_start_message, score = create_sprites()

# Vòng lặp chính của trò chơi
while running:
    # Xử lý các sự kiện
    for event in pygame.event.get():
        # Nếu sự kiện là thoát (đóng cửa sổ), dừng vòng lặp
        if event.type == pygame.QUIT:
            running = False
        # Xử lý sự kiện tạo cột
        if event.type == COLUMN_CREATE_EVENT:
            Column(sprites)
        # Xử lý sự kiện nhấn phím
        if event.type == pygame.KEYDOWN:
            # Bắt đầu trò chơi khi nhấn phím cách lần đầu
            if event.key == pygame.K_SPACE and not gamestarted and not gameover:
                gamestarted = True
                game_start_message.kill()
                pygame.time.set_timer(COLUMN_CREATE_EVENT, 1500)
            # Khởi động lại trò chơi khi trò chơi kết thúc và nhấn phím cách
            elif event.key == pygame.K_SPACE and gameover:
                gameover = False
                gamestarted = False
                sprites.empty()
                bird, game_start_message, score = create_sprites()

        # Xử lý sự kiện của con chim
        bird.handle_event(event)

    # Tô màu nền màn hình là màu đen
    screen.fill(0)

    # Vẽ tất cả các sprite lên màn hình
    sprites.draw(screen)

    # Cập nhật sprite khi trò chơi đang chạy và chưa kết thúc
    if gamestarted and not gameover:
        sprites.update()

    # Kiểm tra va chạm của con chim, kết thúc trò chơi nếu va chạm
    if bird.check_collision(sprites) and not gameover:
        gameover = True
        gamestarted = False
        GameOverMessage(sprites)
        pygame.time.set_timer(COLUMN_CREATE_EVENT, 0)
        assets.play_audio("hit")

    # Kiểm tra nếu cột đã được vượt qua, tăng điểm và phát âm thanh
    for sprite in sprites:
        if isinstance(sprite, Column) and sprite.is_passed():
            score.value += 1
            assets.play_audio("point")

    # Cập nhật màn hình hiển thị
    pygame.display.flip()

    # Giới hạn tốc độ khung hình theo giá trị trong tệp cấu hình configs
    clock.tick(configs.FPS)

# Thoát Pygame
pygame.quit()
