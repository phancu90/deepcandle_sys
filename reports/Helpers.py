import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

some_df = pd.DataFrame()


def calc_range_candle(open_price, close_price):
    if open_price > close_price:
        return open_price - close_price
    else:
        return close_price - open_price


def calc_time_candle(date_time):
    DATETIME = date_time.split(':')[0] + ':00:00'
    return pd.to_datetime(DATETIME, format='%Y.%m.%d %H:%M:%S')  # 2000.01.01 00:00:00


def time_convert(time='00:00:00'):
    return time.split(':')[0] + ':00:00'


class Helper:

    def load_csv(self, path):
        df = pd.read_csv(path)
        # df['HOUR'] = np.vectorize(calc_time_candle)(df['DATETIME'])
        # df['DATETIME'] = pd.to_datetime(df['DATETIME'], format='%Y.%m.%d %H:%M:%S')  # 2000.01.01 00:00:00
        df['BODY'] = np.vectorize(calc_range_candle)(df['PRICE_OPEN'], df['PRICE_CLOSE'])
        df['HL'] = df['PRICE_HIGH'] - df['PRICE_LOW']
        # df['row_id'] = df.index
        return df

    def filter_time(self, min_time, max_time, df=some_df):
        min_time = datetime.datetime.strptime(min_time, '%Y.%m.%d %H:%M:%S')
        max_time = datetime.datetime.strptime(max_time, '%Y.%m.%d %H:%M:%S')
        mask = (df['DATETIME'] > min_time) & (df['DATETIME'] <= max_time)
        return df[mask]

    def get_candles_by_range(self, min, max, df=some_df, type='hl'):
        if type == 'hl':
            return df[((df.PRICE_HIGH - df.PRICE_LOW) >= min) & ((df.PRICE_HIGH - df.PRICE_LOW) <= max)]
        else:
            return df[(df.BODY >= min) & (df.BODY <= max)]

    def get_candles_at_time(self, df, date_time, buffer):
        date_time = datetime.datetime.strptime(date_time, '%Y.%m.%d %H:%M:%S')
        index_candle_by_time = df.index[df['DATETIME'] == date_time].values[0]
        start_index = index_candle_by_time - buffer if index_candle_by_time - buffer > 0 else 0
        end_index = index_candle_by_time + buffer if index_candle_by_time + buffer < len(df) else len(df)
        return df.loc[start_index: end_index, :]

    def show_chart_pie(sefl, title_chart, c_follow, c_break, c_sideway, file_name, total, path_save):

        labels = [
            'Follow  (' + str(c_follow) + ') ' + str(format((c_follow / total) * 100, '.2f')) + '%',
            'Break  (' + str(c_break) + ') ' + str(format((c_break / total) * 100, '.2f')) + '%',
            'Sideway  (' + str(c_sideway) + ') ' + str(format((c_sideway / total) * 100, '.2f')) + '%'
        ]
        fig, ax = plt.subplots()
        fig.suptitle(title_chart)
        colors = ['#62bd7a', '#ec5555', '#efe683']
        patches, texts = ax.pie([c_follow, c_break, c_sideway], colors=colors, startangle=90)
        ax.legend(patches, labels, loc="best")
        f = plt.gcf()
        f.set_size_inches(11.69, 8.27)
        plt.savefig(path_save + '/' + file_name + '.jpg')
        plt.clf()
        plt.close()

    def total_chart_bars_hours(self, path_save, candles, range_pip, percent='', name='', color='r', range_time=''):
        df_u = pd.value_counts(candles['time']).sort_index().rename_axis('unique_values').reset_index(name='counts')
        index = ['00:00:00', '01:00:00', '02:00:00', '03:00:00', '04:00:00', '05:00:00', '06:00:00', '07:00:00', '08:00:00', '09:00:00', '10:00:00', '11:00:00', '12:00:00', '13:00:00',
                 '14:00:00', '15:00:00', '16:00:00', '17:00:00', '18:00:00', '19:00:00', '20:00:00', '21:00:00', '22:00:00', '23:00:00']
        count_candle = []
        for idx, time in enumerate(index):
            time_check = df_u['unique_values'] == time
            val = (df_u[time_check])
            if val.empty is False:
                x = val['counts'].iloc[0]
                count_candle.append(x)
            else:
                count_candle.append(0)
        index = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13',
                 '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
        df = pd.DataFrame({'Candle Up': count_candle}, index=index)
        plt.grid(b=True, which='major', color='#eaeaea', linestyle='-')
        ax = df.plot.bar(rot=0, color=tuple([color]))
        if percent != '':
            plt.title(str(len(candles)) + ' Candles ' + name + '  Range ' + range_pip + ' | ' + percent + '%|  ' + range_time)
        else:
            plt.title(str(len(candles)) + ' Candles ' + name + '  Range ' + range_pip + ' | ' + range_time)
        plt.ylabel('Total Candles')
        plt.xlabel('Hour')
        f = plt.gcf()  # f = figure(n) if you know the figure number
        f.set_size_inches(11.69, 8.27)
        plt.savefig(path_save + '/pb_' + name + '.jpg')
        plt.clf()
        plt.close()
