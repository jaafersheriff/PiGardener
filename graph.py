import matplotlib.pyplot as plt
import csv

itemcount=500

x = []
y = []

print "Finding sum"
with open('sensor.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    rc = sum(1 for row in plots)

print "Appending"
with open('sensor.csv', 'r') as csvfile:
    plots = list(csv.reader(csvfile, delimiter=','))
    for i in range(rc-itemcount, rc):
        x.append(plots[i][0])
        y.append(plots[i][1])

print "Plotting"
plt.plot(x, y, label="Moisture")
# plt.axis("off")
plt.xlabel('Date')
plt.ylabel('Moisture')
plt.title('Moisture')

print "Showing"
plt.show()
