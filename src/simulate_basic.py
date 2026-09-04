import numpy as np
import matplotlib.pyplot as plt
from vehicle import SkidSteerVehicle

car = SkidSteerVehicle(track_width=0.4)

x_history = [car.x]
y_history = [car.y]

for _ in range(50):
    car.step_with_commands(left_command= 1.0, right_command= 1.0, dt=0.1, left_slip= 0.2, right_slip= 0.2)
    x_history.append(car.x)
    y_history.append(car.y)

plt.plot(x_history, y_history)
plt.title("Skid-Steer Vehicle Path")
plt.show()


