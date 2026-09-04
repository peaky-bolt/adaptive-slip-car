import math
from motor import Motor

class SkidSteerVehicle:
    def __init__(self, track_width=0.3):
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.track_width = track_width
        self.left_motor = Motor()
        self.right_motor = Motor()

    def calculate_velocities(self, v_left, v_right):
        linear_velocity = (v_right + v_left) / 2.0
        angular_velocity = (v_right - v_left) / self.track_width

        return linear_velocity, angular_velocity
    def step_with_commands(self, left_command, right_command, dt, left_slip = 0.0, right_slip = 0.0):
        v_left = self.left_motor.update(left_command, dt)
        v_right = self.right_motor.update(right_command, dt)
        effective_v_left = (1.0 - left_slip)* v_left
        effective_v_right = (1.0 - right_slip)* v_right
        self.step(v_left=effective_v_left, v_right=effective_v_right, dt=dt)
       
        return effective_v_left, effective_v_right
    


    def step(self, v_left, v_right, dt):
        linear_velocity, angular_velocity = self.calculate_velocities(
            v_left,
            v_right)
        self.x += linear_velocity * math.cos(self.theta) * dt
        self.y += linear_velocity * math.sin(self.theta) * dt
        self.theta += angular_velocity * dt