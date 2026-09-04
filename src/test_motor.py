from motor import Motor
motor = Motor(max_speed = 1.0, tau = 0.5)

for _ in range(10):
    speed = motor.update(command=1.0, dt=0.1)
    print(speed)
    