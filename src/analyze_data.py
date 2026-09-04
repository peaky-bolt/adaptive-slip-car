import csv
import matplotlib.pyplot as plt

left_grip_values = []
left_slip_values = []
with open('data/slip_data.csv', 'r', newline="") as csv_file:
    reader = csv.DictReader(csv_file)

    for row in reader:
        left_grip = float(row['left_grip'])
        left_slip = float(row['left_slip'])
        left_grip_values.append(left_grip)
        left_slip_values.append(left_slip)

plt.scatter(x= left_grip_values, y= left_slip_values, s=8, alpha=0.4)
plt.title('Left Grip vs Left Slip')
plt.xlabel('Left Grip')
plt.ylabel('Left slip')
plt.grid()
plt.show()        

