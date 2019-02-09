import matplotlib.pyplot as pyplot
import matplotlib.animation as animation

fig = pyplot.figure()
ax1 = fig.add_subplot(111)

def refreshGraphData(i):
    print("Refreshing data...")
    graphData = open("input_data.txt", "r").read()
    lines = graphData.split("\n")
    xValues = []
    yValues = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(",")
            xValues.append(int(x))
            yValues.append(int(y))
    ax1.clear()
    ax1.plot(xValues, yValues)
ani = animation.FuncAnimation(fig, refreshGraphData, interval=1000)
pyplot.show()
