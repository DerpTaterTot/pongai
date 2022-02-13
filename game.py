import math
import pygame
import random

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# window setup
WIDTH, HEIGHT = 1280, 720
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Pong AI")

# paddle setup
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100

# ball setup
BALL_WIDTH = 20
BALL_HEIGHT = 20

# fps
FPS = 60

# velocity
VEL = 5
BALL_VEL = 11

# font 
pygame.font.init()
font = pygame.font.SysFont('JetBrainsMono Nerd Font', 30)

class Game:
# functions
    def __init__(self) -> None:
        self.score = 0
        
    def draw_window(self, paddle, ball):
        WINDOW.fill(WHITE) 

        pygame.draw.rect(WINDOW, BLACK, ball)
        
        pygame.draw.rect(WINDOW, BLACK, paddle)
        
        scoreinfo = font.render(f"Score: {self.score}", False, BLACK)
        
        WINDOW.blit(scoreinfo, (WIDTH/2 - 60, 10))
        
        pygame.display.update()

    def paddle_handle_movement(self, keys_pressed, paddle):
        if keys_pressed[pygame.K_UP] and paddle.y - VEL > 0:
            paddle.y -= VEL
        if keys_pressed[pygame.K_DOWN] and paddle.y + VEL < HEIGHT - PADDLE_HEIGHT:
            paddle.y += VEL

    def ball_handle_movement(self, paddle, ball, ballXVel, ballYVel):
        if ball.x + ballXVel < WIDTH - 20: 
            ball.x += ballXVel
        else:
            ballXVel *= -1
            
        if ball.y < paddle.y + 100 and ball.y > paddle.y and ball.x + ballXVel < 60: # see if ball collides with paddle
            self.score += 10 # hit ball, 10 points
            ballXVel *= -1
            
        if ball.x + ballXVel < 20: # see if ball collides with the wall behind the paddle
            self.score -= 10 # lose game, lose 10 points
            self.reset()
            
        if ball.y + ballYVel < HEIGHT - 20 and ball.y + ballYVel > 20:
            ball.y += ballYVel
        else:
            ballYVel *= -1
            
        if ball.x < paddle.x + 20 and ball.x > paddle.x and ball.y + ballYVel > paddle.y and ball.y + ballYVel < paddle.y + 100:
            ballYVel *= -1 
                
        return ballXVel, ballYVel

    def reset(self):
        self.paddle = pygame.Rect(40, 310, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = pygame.Rect(WIDTH / 2 - 10, HEIGHT / 2 - 10, BALL_WIDTH, BALL_HEIGHT)
        
        self.ballXVel = random.random() * 3 + 3
        self.ballXVel *= -1 # reverse direction
        
        self.ballYVel = math.sqrt(BALL_VEL ** 2 - self.ballXVel ** 2) # meth
    
    def mainloop(self):
        self.reset()
        
        clock = pygame.time.Clock()
        
        run = True
        
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            keys_pressed = pygame.key.get_pressed()
            self.paddle_handle_movement(keys_pressed, self.paddle)
            self.ballXVel, self.ballYVel = self.ball_handle_movement(self.paddle, self.ball, self.ballXVel, self.ballYVel)
            
            self.draw_window(self.paddle, self.ball)

    def main(self):
        self.mainloop()
        pygame.quit()
    
if __name__ == "__main__":
    game = Game()
    game.main()