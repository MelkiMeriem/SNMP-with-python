import matplotlib
matplotlib.use('Qt5Agg')  # Keep Qt5 backend
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

def animate(i):
    try:
        with open("debit.txt", "r") as f:
            lines = f.readlines()

        # Parse data with error handling
        xar = []
        yar = []
        for line in lines[-50:]:  # Show last 50 points
            if ',' not in line:
                continue
            try:
                timestamp, value = line.strip().split(',')
                dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                xar.append(dt)
                yar.append(float(value))
            except (ValueError, TypeError) as e:
                print(f"Skipping invalid line: {line.strip()} | Error: {e}")
                continue

        if xar and yar:
            ax1.clear()
            ax1.plot(xar, yar, marker='o', linestyle='-')
            ax1.set_title("Real-Time Network Bandwidth")
            ax1.set_ylabel("Bandwidth Value")
            ax1.set_xlabel("Timestamp")
            plt.xticks(rotation=45)
            fig.tight_layout()

    except FileNotFoundError:
        print("debit.txt not found")
    except Exception as e:
        print(f"Unexpected error: {e}")

ani = animation.FuncAnimation(fig, animate, interval=1000, cache_frame_data=False)
plt.show()