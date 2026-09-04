import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from vehicle import SkidSteerVehicle


model = nn.Sequential(
    nn.Linear(6, 16),nn.ReLU(),nn.Linear(16, 16),nn.ReLU(),nn.Linear(16, 2)
)

saved_weights = torch.load(
    "models/slip_predictor.pth",
    weights_only=True
)

model.load_state_dict(saved_weights)
model.eval()

car_no_control = SkidSteerVehicle(track_width= 0.4)
car_adaptive = SkidSteerVehicle(track_width= 0.4)
x_no =[car_no_control.x]
y_no =[car_no_control.y]
x_ad =[car_adaptive.x]
y_ad =[car_adaptive.y]
dt = 0.1
steps = 150
desired_speed = 0.6
left_command = desired_speed
right_command = desired_speed
desired_y = 0.0
desired_theta = 0.0
k_y = 0.4
k_theta = 1.2

for step in range(steps):
    if 30<= step <90:
        left_slip = 0.3
    else: 
        left_slip = 0.0
    right_slip = 0.0
    car_no_control.step_with_commands(left_command=desired_speed, right_command=desired_speed
                                      ,dt= dt, left_slip= left_slip, right_slip= right_slip)
    x_no.append(car_no_control.x)
    y_no.append(car_no_control.y)

    effective_v_left, effective_v_right= car_adaptive.step_with_commands(left_command= left_command,
                                                                         right_command= right_command, dt= dt,
                                                                         left_slip= left_slip, right_slip= right_slip,)
    x_ad.append(car_adaptive.x)
    y_ad.append(car_adaptive.y)

    linear_velocity = (effective_v_right + effective_v_left)/2.0
    angular_velocity = (effective_v_right - effective_v_left)/ 0.4

    model_input =torch.tensor([[left_command, right_command, car_adaptive.left_motor.speed,
                                car_adaptive.right_motor.speed, linear_velocity, angular_velocity]],
                                dtype=torch.float32)
    with torch.no_grad():
        predicted_slip = model(model_input)
        bounded_slip = torch.clamp(predicted_slip, min=0.0, max=0.6)
        predicted_left_slip = bounded_slip[0,0].item()
        predicted_right_slip = bounded_slip[0,1].item()

    y_error = desired_y - car_adaptive.y
    theta_error = desired_theta - car_adaptive.theta
    desired_angular_velocity = (k_y * y_error) + (k_theta * theta_error)

    desired_v_left = desired_speed - ((desired_angular_velocity * 0.4)/ 2)
    desired_v_right = desired_speed + ((desired_angular_velocity * 0.4)/2)

    left_command = desired_v_left / (1 - predicted_left_slip)
    left_command = max(0.0, min(1.0, left_command))
    right_command = desired_v_right / (1 - predicted_right_slip)
    right_command = max(0.0, min(1.0, right_command))

max_error_no_control = max(abs(value) for value in y_no)
max_error_adaptive = max(abs(value) for value in y_ad)

final_error_no_control = abs(y_no[-1])
final_error_adaptive = abs(y_ad[-1])

print("Maximum error without control:", max_error_no_control)
print("Maximum error with adaptive control:", max_error_adaptive)
print("Final error without control:", final_error_no_control)
print("Final error with adaptive control:", final_error_adaptive)

plt.plot(x_no, y_no, label = 'Without control')
plt.plot(x_ad, y_ad, label = 'Adaptive control')

plt.title('Path comparison')
plt.xlabel('X position (m)')
plt.ylabel('Y position (m)')
plt.axhline(
    y=0.0,
    color="black",
    linestyle="--",
    label="Desired path"
)
plt.legend()
plt.axis('equal')
plt.grid()
plt.savefig("results/path_comparison.png", dpi=300, bbox_inches="tight")
plt.show()



