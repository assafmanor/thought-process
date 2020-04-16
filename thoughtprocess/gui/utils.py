from datetime import datetime, timedelta, timezone
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import requests
from statistics import mean
import time


def format_timestamp(data_dict, key):
    ts = data_dict[key]
    data_dict[key] = datetime.fromtimestamp(
        ts, timezone(timedelta(hours=3)))


def calc_average(snapshot_url, snapshots):
    translation_lst = []
    rotation_lst = []
    feelings_lst = []
    for cur in snapshots:
        snapshot_id = cur['snapshot_id']
        req = requests.get(snapshot_url.format(id=snapshot_id))
        snapshot = req.json()
        translation_lst.append(snapshot['pose']['translation'])
        rotation_lst.append(snapshot['pose']['rotation'])
        feelings_lst.append(snapshot['feelings'])
    avg_translation = [mean([item[i] for item in translation_lst]) for i in range(3)]
    avg_rotation = [mean([item[i] for item in rotation_lst]) for i in range(4)]
    avg_feelings = [mean([item[i] for item in feelings_lst]) for i in range(4)]
    avg_snapshot = {}
    avg_snapshot['pose'] = {}
    avg_snapshot['pose']['translation'] = avg_translation
    avg_snapshot['pose']['rotation'] = avg_rotation
    avg_snapshot['feelings'] = avg_feelings
    return avg_snapshot


def get_arranged_feelings(snapshot_url, snapshots):
    feelings_lst = []
    for cur in snapshots:
        snapshot_id = cur['snapshot_id']
        req = requests.get(snapshot_url.format(id=snapshot_id))
        snapshot = req.json()
        feelings_lst.append(snapshot['feelings'])
    return [[item[i] for item in feelings_lst] for i in range(4)]


def create_figure(data, title, ylabel):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title(title)
    axis.set_ylabel(ylabel)
    xs = [i+1 for i in range(len(data))]
    ys = data
    axis.plot(xs, ys)
    return fig