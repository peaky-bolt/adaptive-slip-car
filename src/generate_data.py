import csv
import random
from vehicle import SkidSteerVehicle

random.seed(42)
car = SkidSteerVehicle(track_width= 0.4)
dt = 0.1
num_samples = 2000
fieldnames = ['time','left_command', 'right_command', 'left_grip','right_grip','left_motor_speed','right_motor_speed','left_slip', 'right_slip', 'effective_v_left', 'effective_v_right', 'linear_velocity', 'angular_velocity', 'x', 'y', 'theta']

output_path = 'data/slip_data.csv'
with open(output_path, "w", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(num_samples):
        left_command = random.uniform(0.2,1.0)
        right_command = random.uniform(0.2,1.0)
        left_grip = random.uniform(0.4,1.0)
        right_grip = random.uniform(0.4,1.0)
        left_noise = random.uniform(-0.02,0.02)
        right_noise = random.uniform(-0.02,0.02)
        raw_left_slip = ((1 - left_grip)*(0.3 + 0.4*left_command)) + left_noise
        raw_right_slip = ((1 - right_grip)*(0.3 +0.4*right_command)) + right_noise

        left_slip = max(0.0, min(0.6, raw_left_slip))
        right_slip = max(0.0,min(0.6, raw_right_slip))

        effective_v_left, effective_v_right= car.step_with_commands(left_command= left_command, right_command= right_command
                                                                    , dt= dt, left_slip= left_slip, right_slip= right_slip)
        linear_velocity, angular_velocity = car.calculate_velocities(v_left= effective_v_left, v_right= effective_v_right)

        row= {'time': (i+1)*dt,'left_command': left_command, 'right_command': right_command, 'left_grip': left_grip, 'right_grip': right_grip
              ,'left_motor_speed': car.left_motor.speed, 'right_motor_speed': car.right_motor.speed, 'left_slip': left_slip, 'right_slip': right_slip
              ,'effective_v_left': effective_v_left, 'effective_v_right': effective_v_right, 'linear_velocity': linear_velocity, 'angular_velocity': angular_velocity
              , 'x': car.x, 'y': car.y, 'theta': car.theta}  
        writer.writerow(row)       



