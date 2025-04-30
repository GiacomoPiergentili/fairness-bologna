import pandas as pd
import numpy as np
import matplotlib
# matplotlib.use('Qt5Agg')  # oppure 'Qt5Agg', 'GTK3Agg' ecc.
import matplotlib.pyplot as plt
from utils import *

"""
this file contains the code used to create the dataframe representing the
amount of people crossing the door at each time of the day.
"""
door = 'saragozza'

def plot_stats_intervalli(df_stats, interval_minutes):
    """
    Plots the time series statistics (mean and standard deviation) computed over fixed time intervals.

    Parameters:
    - df_stats: DataFrame returned by `get_stats_ts()`, which must include:
        - 'timeStr': formatted time labels (HH:MM)
        - 'mean': average values per interval
        - 'std': standard deviation per interval
    - interval_minutes: the width of each time interval in minutes (used for labeling and x-axis ticks)

    Note:
    - The function assumes the input DataFrame is already sorted by time.
    """
    plt.figure(figsize=(15, 7)) # Aumentiamo un po' la dimensione per i più punti

    x_values = df_stats['timeStr']
    mean_values = df_stats['mean']
    std_values = df_stats['std']

    # Plot della media
    plt.plot(x_values, mean_values, label='Media passaggi', marker='.', linestyle='-', markersize=4) # Marker più piccolo

    # Area intorno alla media ± std
    plt.fill_between(
        x_values,
        np.maximum(mean_values - std_values, 0),
        mean_values + std_values,
        color='lightblue',
        alpha=0.4,
        label='±1 Deviazione standard'
    )

    # Decorazioni
    plt.title(f'Media passaggi per intervalli di {interval_minutes} minuti (con deviazione standard)')
    plt.xlabel('Ora del giorno (HH:MM)')
    plt.ylabel('Totale passaggi')

    # Gestione dei tick sull'asse X (cioè ogni 60/interval_minutes intervalli)
    tick_frequency = 60 // interval_minutes
    plt.xticks(ticks=np.arange(0, len(x_values), tick_frequency),
               labels=x_values[::tick_frequency],
               rotation=90, ha='right') # Ruota le etichette per leggibilità

    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    # plt.savefig(f'stats_{interval_minutes}min.png')
    plt.show()
    plt.close()

def compute_intervals_ts(df,
                    time_index=0,
                    interval_minutes=15):
    """
    Converts a datetime column in the input DataFrame into hour-based intervals 
    and groups the data accordingly.

    Parameters:
    - df: pandas DataFrame containing time series data.
    - time_index: index or name of the column containing datetime values (default is column 0).
    - interval_minutes: size of each time interval in minutes (default is 15).

    Returns:
    - A grouped DataFrame indexed by 'hour' and 'minute_interval'.
    """
    cols = df.columns
    try:
        # Prova a parsare direttamente con l'offset (funziona con pandas recenti)
        df[cols[time_index]] = pd.to_datetime(df[cols[time_index]], format='ISO8601', utc=True)
    except ValueError:
        # Fallback se il formato non è esattamente ISO8601 o per versioni pandas meno recenti
        df[cols[time_index]] = pd.to_datetime(df[cols[time_index]])

    df['hour'] = df[cols[time_index]].dt.hour
    df['minute'] = df[cols[time_index]].dt.minute
    # eg: 10:00 -> 0, 10:14 -> 0, 10:15 -> 15, 10:29 -> 15, 10:30 -> 30
    df['minute_interval'] = (df['minute'] // interval_minutes) * interval_minutes

    return df.groupby(['hour', 'minute_interval'])

def get_stats_ts(df,
                time_index=0,
                interval_minutes=15,
                row_to_colletc = 'Totale passaggi'):
    """
    Computes statistical summaries (mean and standard deviation) of a selected column 
    from a time series DataFrame, grouped into regular time intervals.

    Parameters:
    - df: pandas DataFrame containing the time series data.
    - time_index: index or column used as the datetime reference (default is column 0).
    - interval_minutes: size of each time interval in minutes (default is 15).
    - row_to_colletc: name of the column for which statistics are calculated.

    Returns:
    - A new DataFrame with columns for interval time, mean, standard deviation, and time label.
    """
    grouped_df = compute_intervals_ts(df,time_index,interval_minutes)
    stats = grouped_df[row_to_colletc].agg(['mean', 'std']).reset_index()
    stats['std'] = stats['std'].fillna(0)   # if there is only one sample in that interval then std = 0
    stats['timeStr'] = stats.apply(
        lambda row: f"{int(row['hour']):02d}:{int(row['minute_interval']):02d}",
        axis=1
    )
    stats = stats.sort_values(['hour', 'minute_interval'])
    return stats.reset_index(drop=True)

if __name__ == '__main__':
    """
    used to plot the current TS
    """
    path = get_path(door)
    df = pd.read_csv(path, sep=';')

    stats = get_stats_ts(df)
    plot_stats_intervalli(stats, 15)

