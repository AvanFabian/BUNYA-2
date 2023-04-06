class Kick:
    def __init__(self, character, ball):
        self.character = character
        self.ball = ball

    def do_kick(self):
        #check if this is whiteball
        if isinstance(self.ball, WhiteBall):
            if self.character.rect.colliderect(self.ball.rect):
                print("Kick successful!")
                self.ball.direction = random.randint(0, 360)
                self.ball.speed += 5   # Increase the speed of ball by 5
        #pass if is not
        else:
            if self.character.rect.colliderect(self.ball.rect):
                pass