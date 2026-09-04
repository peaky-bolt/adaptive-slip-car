import matplotlib.pyplot as plt
from vehicle import SkidSteerVehicle
 

def simulate_path(left_slip, right_slip, steps = 50):
    car = SkidSteerVehicle(track_width= 0.4)
    x_history = [car.x]
    y_history = [car.y] 

    for _ in range(steps):
        car.step_with_commands(left_command= 1.0, right_command= 1.0, dt= 0.1,left_slip= left_slip, right_slip= right_slip)
        x_history.append(car.x)
        y_history.append(car.y)

    return x_history, y_history
x_no_slip, y_no_slip = simulate_path(left_slip=0.0, right_slip=0.0)
x_equal_slip, y_equal_slip = simulate_path(left_slip=0.2, right_slip=0.2)
x_left_slip , y_left_slip = simulate_path(left_slip=0.2, right_slip=0.0)

plt.plot(x_no_slip, y_no_slip, label='No slip')
plt.plot(x_equal_slip, y_equal_slip, label='Equal slip')
plt.plot(x_left_slip, y_left_slip, label='Left slip only')

plt.title('Slip comparison')
plt.xlabel('X position (m)')
plt.ylabel('Y position (m)')
plt.legend()
plt.show()