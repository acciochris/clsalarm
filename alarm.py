import argparse
import re
from datetime import datetime
from playsound import playsound
from time import sleep


times = []
classes = []


def main():
    global times, classes

    # Argument parsing
    parser = argparse.ArgumentParser(description="An alarm clock for classes")
    parser.add_argument(
        "-c",
        "--conf",
        default="timetable.txt",
    )
    conf: str = parser.parse_args().conf

    # Load time table
    with open(conf, "r") as timetable:
        while (classtime := timetable.readline()) != "":
            classtime, *classtable = classtime.split(",")
            classtime = classtime.strip()
            classtable = [c.strip() for c in classtable]
            if classtime[0] == "#":
                continue
            if classtime.startswith("eye:"):
                _, time = classtime.split()
                time.replace("\n", "")
                if time[time.find(":") + 1] == "0":
                    time = time[: time.find(":") + 1] + time[-1]
                times.append("eye")
                times.append(time)
            elif classtime.startswith("gym:"):
                _, time = classtime.split()
                time.replace("\n", "")
                if time[time.find(":") + 1] == "0":
                    time = time[: time.find(":") + 1] + time[-1]
                times.append("gym")
                times.append(time)
            else:
                start, stop = classtime.split("~")
                stop = stop.replace("\n", "")
                if start[start.find(":") + 1] == "0":
                    start = start[: start.find(":") + 1] + start[-1]
                if stop[stop.find(":") + 1] == "0":
                    stop = stop[: stop.find(":") + 1] + stop[-1]
                times.append(start)
                times.append(stop)

            classes.append(classtable)

    classes = list(zip(*classes))
    eye = gym = False
    cur_date = 0

    while True:
        # Wait until next day
        if (datetime.now().day == cur_date) or (datetime.now().weekday in [5, 6]):
            sleep(1)
            continue
        cur_time = datetime.now()
        print(*classes[cur_time.weekday()], sep="\n")
        cur_date = cur_time.day

        # Check time table for one day
        for a in range(len(times)):
            # Skip special time markers
            if times[a] == "eye":
                eye = True
                continue
            if times[a] == "gym":
                gym = True
                continue

            # Skip some time items until now
            time_now = datetime.now()
            h, m = [int(a) for a in times[a].split(":")]
            if h < time_now.hour:
                eye = gym = False
                continue
            elif (h == time_now.hour) and (m < time_now.minute):
                eye = gym = False
                continue

            # Wait until next time item to play sound
            while True:
                sleep(1)
                time_now = datetime.now()
                if eye and (
                    ":".join([str(time_now.hour), str(time_now.minute)]) == times[a]
                ):
                    if classes[time_now.weekday()][(a - 1) / 2] != "None":
                        eye = False
                        print("Next class is eye exercise.")
                        print("{}: eye.mp3".format(times[a]))
                        playsound("eye.mp3")
                        break
                elif gym and (
                    ":".join([str(time_now.hour), str(time_now.minute)]) == times[a]
                ):
                    if classes[time_now.weekday()][(a - 1) / 2] != "None":
                        gym = False
                        print("Next class is gymnastics.")
                        print("{}: gym.mp3".format(times[a]))
                        playsound("gym.mp3")
                        break
                else:
                    if ":".join([str(time_now.hour), str(time_now.minute)]) == times[a]:
                        if classes[time_now.weekday()][(a - 1) / 2] != "None":
                            print(
                                f"Next class is {classes[time_now.weekday()][(a-1)/2]}"
                            )
                            sound = "start.mp3" if a % 2 == 0 else "stop.mp3"
                            print("{}: {}".format(times[a], sound))
                            playsound(sound)
                            break


if __name__ == "__main__":
    main()
