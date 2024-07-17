import random
import pygame.sprite
import assets
import configs
from layer import Layer

class Column(pygame.sprite.Sprite):
    def __init__(self, *groups):
        # Khởi tạo đối tượng cột trong game Flappy Bird

        # Thiết lập lớp hiển thị cho sprite là Layer.OBSTACLE để đảm bảo vị trí đúng trong LayeredUpdates
        self._layer = Layer.OBSTACLE

        # Khoảng cách giữa hai cột
        self.gap = 100

        # Tải sprite cho cột dưới từ tệp "pipe-green"
        self.sprite = assets.get_sprite("pipe-green")
        self.sprite_rect = self.sprite.get_rect()

        # Tạo sprite cho cột trên bằng cách lật sprite cột dưới theo chiều dọc
        self.pipe_top = pygame.transform.flip(self.sprite, False, True)

        # Tạo bề mặt hình ảnh cho cột bao gồm cả cột dưới và cột trên
        self.image = pygame.surface.Surface((self.sprite_rect.width, self.sprite_rect.height * 2 + self.gap),
                                            pygame.SRCALPHA)
        self.image.blit(self.sprite, (0, self.sprite_rect.height + self.gap))  # Vẽ cột dưới
        self.image.blit(self.pipe_top, (0, 0))  # Vẽ cột trên

        # Xác định chiều cao của sprite sàn để giới hạn vị trí của cột
        sprite_floor_height = assets.get_sprite("floor").get_rect().height
        min_y = 100  # Vị trí y tối thiểu của cột
        max_y = configs.SCREEN_HEIGHT - sprite_floor_height - 100  # Vị trí y tối đa của cột

        # Đặt vị trí ban đầu của cột ngẫu nhiên theo trục y và cố định trên trục x
        self.rect = self.image.get_rect(midleft=(configs.SCREEN_WIDTH, random.uniform(min_y, max_y)))

        # Tạo mask cho sprite để phát hiện va chạm dựa trên hình dạng
        self.mask = pygame.mask.from_surface(self.image)

        # Biến để kiểm tra xem chim đã vượt qua cột hay chưa
        self.passed = False

        # Gọi constructor của lớp Sprite để thêm sprite vào các nhóm được cung cấp
        super().__init__(*groups)

    def update(self):
        # Cập nhật vị trí của cột khi di chuyển sang trái
        self.rect.x -= 2

        # Nếu cột ra khỏi màn hình bên trái thì loại bỏ cột này khỏi nhóm và khỏi game
        if self.rect.right <= 0:
            self.kill()

    def is_passed(self):
        # Kiểm tra xem cột đã vượt qua chim (vị trí x < 50) và chưa được đếm
        if self.rect.x < 50 and not self.passed:
            self.passed = True
            return True
        return False
