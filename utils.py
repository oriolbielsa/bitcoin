import json
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict


def read_blocks(blocks_file):
    """
    Read the relevant content of the Block file (hash, size, number of tx, time)
        and returns the info formatted in a DataFrame structure
    """
    blocks = {}
    # Reading the file line by line
    with open(blocks_file) as f_blocks:
        for block in f_blocks:
            in_blocks = json.loads(block)
            # Store info for each blockhash
            blocks[in_blocks["hash"]] = {"size": in_blocks["size"], "num_tx": len(in_blocks["tx"]),
                                         "time": dt.datetime.utcfromtimestamp(in_blocks["time"])}
        # Create and format the DataFrame
        df_blocks = pd.DataFrame.from_dict(blocks, orient='index')
        df_blocks.reset_index(inplace=True)
        df_blocks.rename(columns={'index': 'hash'}, inplace=True)
    return df_blocks


def get_block_value(txs):
    """
    Read the relevant information of TXS file(sum of total value, blockhash)
        and returns the info formatted as DataFrame.
    """
    value_blocks = defaultdict(int)
    # Reading the file line by line
    with open(txs) as f_txs:
        for txs in f_txs:
            in_txs = json.loads(txs)
            # Sum the value for each tx
            value = sum([d["value"] for d in in_txs["vout"]])
            # Store info for each blockhash
            value_blocks[in_txs["blockhash"]] += value
        # Create and format the DataFrame
        df_value = pd.DataFrame(value_blocks.items(), columns=['hash', 'value'])
    return df_value


def get_block_timediff(df_blocks):
    """
    Calculate the time difference in seconds between consecutive blocks
        in input DataFrame, and return the info formatted as DataFrame.
    """
    # Create DataFrame with time difference
    df_timediff = pd.DataFrame(df_blocks['time'].shift() - df_blocks['time'])
    df_timediff.rename(columns={'time': 'timediff'}, inplace=True)
    # Create column with time difference in sec
    df_timediff['timediff_sec'] = [v.total_seconds() for v in list(df_timediff['timediff'])]
    # Add column with block hash and reorder
    df_timediff['hash'] = df_blocks['hash']
    df_timediff = pd.DataFrame(df_timediff, columns=['hash', 'timediff', 'timediff_sec'])
    return df_timediff


def get_block_size(df_blocks):
    """
    Return a DataFrame with the average size per distinct
        date-hour for each block in input DataFrame.
    """
    # Create DataFrame with date-hour grouping and mean of size
    df_avgsize = pd.DataFrame(df_blocks.groupby([pd.to_datetime(df_blocks['time']).dt.hour,
                              pd.to_datetime(df_blocks['time']).dt.date])['size'].mean())
    # We apply DataFrame output pre-processing
    df_avgsize = df_proc_avg(df_avgsize)
    return df_avgsize


def get_block_tx(df_blocks):
    """
    Return a DataFrame with the number of transactions
        per distinct date-hour for each block in input DataFrame.
    """
    # Create DataFrame with date-hour grouping and sum of txs
    df_avgsize = pd.DataFrame(df_blocks.groupby([pd.to_datetime(df_blocks['time']).dt.hour,
                                pd.to_datetime(df_blocks['time']).dt.date])['num_tx'].sum())
    # We apply DataFrame output pre-processing
    df_avgsize = df_proc_avg(df_avgsize)
    return df_avgsize


def df_proc_avg(df):
    """
    Receive DataFrame with hour and date multiindex.
        Returns time-ordered DataFrame with date-hour unique column.
    """
    df.rename_axis(index=["hour", "date"], inplace=True)
    df.reset_index(inplace=True)
    df.sort_values(["date", "hour"], ascending=True, inplace=True)
    df['date_hour'] = df['date'].astype(str) + '_' + df['hour'].astype(str) + 'H'
    df.drop(['date', 'hour'], axis=1, inplace=True)
    return df


def generate_block_report(df_blocks, block_value, block_timediff):
    """
    Receive DataFrames with the features analyzed related to blocks.
        Return result dataframe, and creates file with the information: blocks_info.csv.
    """
    # Merge values based on block has
    df_output = pd.merge(df_blocks, block_value, on=['hash'])
    df_output = pd.merge(df_output, block_timediff, on=['hash'])
    # Generate CSV files
    df_output.to_csv('data/blocks_info.csv', index = False, header=True, sep=';')
    return df_output


def generate_time_report(block_avgsize, block_tx):
    """
    Receive DataFrames with the features analyzed related to date/time.
        Return result dataframe, and creates file with the information: blocks_t_info.csv.
    """
    # Merge values based on date/time
    df_output_t = pd.merge(block_avgsize, block_tx, on=['date_hour'])
    # Reorder and rename columns
    df_output_t = df_output_t[['date_hour', 'size', 'num_tx']]
    df_output_t.rename(columns={'size': 'avg_size', 'num_tx': 'sum_tx'}, inplace=True)
    # Generate CSV files
    df_output_t.to_csv('data/blocks_t_info.csv', index = False, header=True, sep=';')
    return df_output_t


def plot_block_features(df_output):
    """
    Receive DataFrames with blocks features analyzed, and plot the information.
    """
    # Plot - Number of transactions per block
    fig = plt.figure("Bitcoin Block Analysis")
    plt.subplot(3, 1, 1)

    # Plotting bar graph
    ys = df_output['num_tx']
    xs = range(len(ys))
    plt.bar(xs, ys, color='tab:blue')
    # Config of axis
    plt.ylabel('#Transactions')
    plt.title('Transactions per block')

    # Plot - Total value of all transactions per block
    plt.subplot(3, 1, 2)
    # Plotting bar graph
    ys = df_output['value']
    xs = range(len(ys))
    plt.bar(xs, ys, color='tab:green')
    # Config of axis
    plt.ylabel('Total Value')
    plt.title('Total value per block')

    # Plot - Total value of all transactions per block
    plt.subplot(3, 1, 3)
    # Plotting bar graph
    ys = df_output['timediff_sec']
    xs = range(len(ys))
    plt.bar(xs, ys, color='tab:cyan')
    # Config of axis
    plt.xlabel('Block')
    plt.ylabel('TimeDiff (sec)')
    plt.title('Time difference between blocks')

    # Plot and save graph
    fig.tight_layout(pad=1.0)
    fig.savefig('./data/block_analysis.png')
    plt.show()


def plot_time_features(df_output_t):
    """
    Receive DataFrames with blocks time/date features analyzed, and plot the information.
    """
    # Plot - Average block size per hour
    fig = plt.figure("Bitcoin Block Time Analysis")
    plt.subplot(2, 1, 1)

    # Plotting graph
    ys = df_output_t['avg_size']
    xs = df_output_t['date_hour']
    plt.xticks(rotation=90, fontsize=5)
    plt.plot(xs, ys, color='tab:blue')
    # Config of axis
    plt.ylabel('Avg Block Size')
    plt.title('Average block size per hour')

    # Plot - Total value of all transactions per block
    plt.subplot(2, 1, 2)
    # Plotting graph
    ys = df_output_t['sum_tx']
    xs = df_output_t['date_hour']
    plt.xticks(rotation=90, fontsize=5)
    plt.plot(xs, ys, color='tab:green')
    # Config of axis
    plt.xlabel('Date/Hour')
    plt.ylabel('#Transactions')
    plt.title('Block transactions per hour')

    # Plot and save graph
    fig.tight_layout(pad=1.0)
    fig.savefig('./data/block_t_analysis.png')
    plt.show()
