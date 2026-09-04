import torch
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(6,16), nn.ReLU(), nn.Linear(16,16), nn.ReLU(), nn.Linear(16,2)
)

saved_weights = torch.load(
    'models/slip_predictor.pth',
    weights_only= True
)
model.load_state_dict(saved_weights)
model.eval()
sample_input = torch.tensor(
    [[0.8, 0.8, 0.8, 0.8, 0.68, 0.6]],
    dtype=torch.float32
)

with torch.no_grad():
    predicted_slip = model(sample_input)
    bounded_slip = torch.clamp(predicted_slip, min=0.0, max=0.6)
    print(bounded_slip)
    predicted_left_slip = bounded_slip[0,0].item()
    predicted_right_slip = bounded_slip[0,1].item()

desired_speed = 0.6
corrected_left_command = desired_speed / (1 - predicted_left_slip)
corrected_left_command = max(0.0, min(1.0, corrected_left_command))
corrected_right_command = desired_speed / (1 - predicted_right_slip)
corrected_right_command = max(0.0, min(1.0, corrected_right_command))

print(corrected_left_command)
print(corrected_right_command)