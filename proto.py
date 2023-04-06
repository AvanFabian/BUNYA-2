class WhiteBall(MainBall):
    def __init__(self, x, y):
        super().__init__((0, 0, 255), x, y, 25, 5)

    def update(self, other_balls):
        super().update(other_balls)

        # Bounce off walls
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = 180 - self.direction
        elif self.rect.right > screenwidth:
            self.rect.right = screenwidth
            self.direction = 180 - self.direction
        if self.rect.top < 0:
            self.rect.top = 0
            self.direction = 360 - self.direction
        elif self.rect.bottom > screenheight:
            self.rect.bottom = screenheight
            self.direction = 360 - self.direction

        # Bounce of white balls
        for ball in other_balls:
            if isinstance(ball, WhiteBall) and ball != self and pygame.sprite.collide_circle(self, ball):
                self.direction = random.randint(0, 360)
        
        # Slow down over time
        if self.speed > 0:
            self.speed -= 0.0009
            print("Current speed:", self.speed)
        # Stop the ball completely
        elif self.speed <=0:
            self.speed = 0

class Kick:
    def __init__(self, character, ball):
        self.character = character
        self.ball = ball

    def do_kick(self):
        if isinstance(self.ball, WhiteBall):
            if self.character.rect.colliderect(self.ball.rect):
                self.ball.speed = 0
        else:
            if self.character.rect.colliderect(self.ball.rect):
                print("Kick successful!")
                self.ball.direction = random.randint(0, 360)


white_ball = WhiteBall(100, 100)
all_balls.add(white_ball)