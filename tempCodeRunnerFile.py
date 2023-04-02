# Create the balls
black_balls = [BlackBall(50, 50), BlackBall(display_width - 50, 50), BlackBall(50, display_height - 50), BlackBall(display_width - 50, display_height - 50)]
white_balls = [WhiteBall(100, 100), WhiteBall(display_width - 100, 100), WhiteBall(100, display_height - 100), WhiteBall(display_width - 100, display_height - 100)]

# Add the balls to sprite groups
all_balls = pygame.sprite.Group()
all_balls.add(black_balls)
all_balls.add(white_balls)