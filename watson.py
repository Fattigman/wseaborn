import seaborn as sns
import subprocess
from matplotlib import pyplot as plt
def get_aggr():
    """
    output: str
    example output:
Tue 07 May 2024 - 00s


Wed 08 May 2024 - 5h 29m 53s
  journal-club - 13m 46s

  mcotm - 5h 16m 07s
        [cnv  5h 16m 07s]


Thu 09 May 2024 - 00s


Fri 10 May 2024 - 1h 07m 54s
  mcotm - 1h 07m 54s
        [cnv  1h 07m 54s]

    """
    data:str  = subprocess.run(['watson', "aggregate"],  stdout=subprocess.PIPE).stdout.decode('utf-8')
    return data

def sum_time(i:int,x: str):
    if i == 1:
        return int(x[:-1])/60
    elif i == 2:
        return int(x[:-1])/3600
    return int(x[:-1])
    
def parse_aggr(data:str):
    weekly_hours :dict = dict()
    for line in data.split("\n"):
        if len(line) == 0:
            continue
        if line[0] in ["M", "T", "W", "F"]:
            day :str = line.split(" ")[0]
            time : str= line.split(" - ")[-1]
            total_time : float = sum([sum_time(i,x) for i, x in enumerate(time.split(" "))])
            weekly_hours[day] = round(total_time, 2)
    # Sort the dictionary by day
    day_order = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    weekly_hours = {k: weekly_hours[k] for k in day_order}
    return weekly_hours

def get_total_time(weekly_hours:dict):
    return sum(weekly_hours.values())

def plot_aggr(data: dict, total_time : float = None):
    # Add a red line at 8 hours
    plt.axhline(y=8, color='r', linestyle='--')
    # Add the total time to the plot if available
    if total_time:
        plt.title(f"Total time: {total_time} hours")
    sns.barplot(x = list(data.keys()), y = list(data.values()))

data = get_aggr()
data = parse_aggr(data)
total_time = get_total_time(data)
plot_aggr(data, total_time)
plt.show()