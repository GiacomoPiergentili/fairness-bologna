import pandas as pd
import numpy as np

import matplotlib
# matplotlib.use('Qt5Agg')  # oppure 'Qt5Agg', 'GTK3Agg' ecc.
import matplotlib.pyplot as plt

path = 'data/varco-n-59-saragozza-direzione-centro.csv'

def plot_stats_intervalli(df_stats, interval_minutes):
    """
    Plotta le statistiche per intervallo (media e std) dei passaggi.

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
        mean_values - std_values,
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

    df = pd.read_csv(path, sep=';')

    stats = get_stats_ts(df)
    plot_stats_intervalli(stats, 15)

