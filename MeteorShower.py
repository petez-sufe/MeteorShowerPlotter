
import matplotlib.pyplot as plt
import os

DATA_PATH = r'/Users/Peter/PycharmProjects/Python for Finance/MeteorShower/'
file_out = 'MeteorShowerPlot.pdf'


def main():
    data = dict()
    file_list = sorted(os.listdir(DATA_PATH))
    for file in file_list:
        if not file.startswith('.'):
            data.update(reader(file, print_flag=True))
    dates, observations, realdates = prepdata(data)
    plotter(dates, observations, file_out, realdates)


def reader(filename, print_flag=True):
    data = dict()
    counter = 0
    file_dir = DATA_PATH+filename
    with open(file_dir, 'r', encoding='utf8') as f_in:
        f_in.readline()
        for line in f_in:
            parts = line.strip('\n').split(';')
            data[parts[0]] = DataClass(parts)
            counter += 1
        if print_flag:
            print(f'In file: {filename}:\n{counter} observations were found.')
    return data


def prepdata(data):
    count = dict()
    day = int(1)
    hour = int(0)
    dates = list()
    while True:
        if day <= 31:
            if hour < 23:
                count[int(f'12{day:0>2d}{hour:0>2d}')] = StatsClass()
                hour += 1
            if hour == 23:
                count[int('12'f'{day:0>2d}'f'{hour:0>2d}')] = StatsClass()
                hour = 0
                dates.append(f'Dec.{day}')
                day += 1
        else:
            break

    for realid in data:
        if data[realid].month == '12':
            if data[realid].MMDDHH not in count:
                count[data[realid].MMDDHH] = StatsClass()
            count[data[realid].MMDDHH].sum += data[realid].observation
            count[data[realid].MMDDHH].count += 1

    group = list()
    numbers = list()
    for hour in sorted(count):
        group.append(hour)
        if count[hour].count == 0:
            numbers.append(int(0))
        else:
            numbers.append(count[hour].sum/count[hour].count)
    return group, numbers, dates


def plotter(dates, observations, file, realdates):
    fig = plt.figure()

    plt.bar(x=range(len(dates)), height=observations)
    plt.xticks(rotation='vertical')
    plt.xticks(range(0, len(dates), 24), realdates)

    plt.tight_layout()
    plt.show()
    fig.savefig(file)


class DataClass:
    def __init__(self, parts):
        self.time = parts[3]
        self.observation = int(parts[12])
        self.month = self.time[6:8]
        self.day = self.time[9:11]
        self.hour = self.time[12:14]
        self.month_day = int(f'{self.month}{self.day}')
        self.MMDDHH = int(f'{self.month_day}{self.hour}')


class StatsClass:
    def __init__(self):
        self.count = 0
        self.sum = 0


main()
