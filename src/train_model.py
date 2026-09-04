import csv
import torch
import torch.nn as nn
inputs = []
targets = []
with open("data/slip_data.csv", "r", newline="") as csv_file:
    reader = csv.DictReader(csv_file)

    for row in reader:
        input_row = [float(row['left_command']), float(row['right_command'])
                     , float(row['left_motor_speed']), float(row['right_motor_speed'])
                     , float(row['linear_velocity']), float(row['angular_velocity'])]
        target_row = [float(row['left_slip']), float(row['right_slip'])]

        inputs.append(input_row)
        targets.append(target_row)

input_tensor = torch.tensor(inputs, dtype= torch.float32)
target_tensor = torch.tensor(targets, dtype= torch.float32) 

torch.manual_seed(42)
indices = torch.randperm(len(input_tensor))

train_size = int(0.8 * len(input_tensor))
train_indices = indices[:train_size]
test_indices = indices[train_size:]

x_train = input_tensor[train_indices]
y_train = target_tensor[train_indices]
x_test = input_tensor[test_indices]
y_test = target_tensor[test_indices]

model = nn.Sequential(
    nn.Linear(6,16), nn.ReLU(), nn.Linear(16,16), nn.ReLU(), nn.Linear(16,2)
    )

loss_function = nn.MSELoss()
optimizer = torch.optim.Adam(
    model.parameters(),
    lr= 0.01
)
for epoch in range(1000):
    predictions = model(x_train)
    loss = loss_function(predictions, y_train)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if (epoch + 1) % 50 ==0:
        print('Epoch', epoch +1, 'Error', loss.item())

model.eval()
with torch.no_grad():
    test_predictions = model(x_test)
    test_loss = loss_function(test_predictions, y_test)
    test_loss_value = test_loss.item()
    print('Test MSE', test_loss_value)

    difference = test_predictions - y_test
    test_mae = torch.mean(torch.abs(difference))
    print('Test MAE', test_mae.item())

torch.save(
    model.state_dict(), 'models/slip_predictor.pth'
) 



  