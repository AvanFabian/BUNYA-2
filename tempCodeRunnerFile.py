# Define a step size factor for the ball movement
STEP_FACTOR = 10
# Create the balls
black_balls = [
    # Add the track points to the black ball objects
    BlackBall(50, 50), 
    BlackBall(display_width - 50, 50), 
    BlackBall(50, display_height - 50), 
    BlackBall(display_width - 50, display_height - 50)]
# Add more track points to the black ball objects
black_balls[0].track_points.extend([(100, 100), (100, 200), (200, 200), (200, 100)])

white_balls = [
    # Add the track points to the white ball objects
    WhiteBall(100, 100),
    WhiteBall(display_width - 100, 100), 
    WhiteBall(100, display_height - 100), 
    WhiteBall(display_width - 100, display_height - 100)]

# Add the balls to sprite groups
all_balls = pygame.sprite.Group()
all_balls.add(black_balls)
all_balls.add(white_balls)


# Set up the game loop
game_running = True
while game_running:
    # Handle events
    for event in pygame.event.get():
        #event when quit pressed
        if event.type == pygame.QUIT:
            game_running = False
        #event when button pressed 
        elif event:
            character.handle_event(event) 
    
    # Update the balls
    all_balls.update(all_balls)

    # Update the balls
    for ball in black_balls:
        current_pos = ball.rect.center
        if len(ball.track_points) > 1:
            next_pos = ball.track_points[0]
            # Calculate the distance between current and next point
            delta_x = next_pos[0] - current_pos[0]
            delta_y = next_pos[1] - current_pos[1]
            distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
            # Calculate the step size based on STEP_FACTOR and distance
            step_size = min(distance / STEP_FACTOR, distance)
            # Normalize the delta values to get unit vector
            unit_x = delta_x / distance
            unit_y = delta_y / distance
            # Move the ball toward the next point by step_size
            new_pos_x = current_pos[0] + unit_x * step_size
            new_pos_y = current_pos[1] + unit_y * step_size
            ball.rect.center = (new_pos_x, new_pos_y)
            # If the ball has reached the next point, remove it from the list
            if distance <= step_size:
                ball.track_points.pop(0)