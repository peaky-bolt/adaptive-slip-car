
class Motor:
    def __init__(self, max_speed=1.0, tau=0.5):
        self.max_speed = max_speed
        self.tau = tau
        self.speed = 0.0

    def update(self, command, dt):
        target_speed = command * self.max_speed    
        self.speed = self.speed + (target_speed - self.speed) / self.tau * dt
        return self.speed