from utils import read_blocks, get_block_value, get_block_timediff, get_block_size, get_block_tx, \
    generate_block_report, generate_time_report, plot_block_features, plot_time_features

if __name__ == "__main__":

    # Load blocks datasets
    df_blocks = read_blocks('data/blocks.json')

    # Execute subprocess to obtain features of blocks
    block_value = get_block_value('data/txs.json')
    block_timediff = get_block_timediff(df_blocks)
    block_avgsize = get_block_size(df_blocks)
    block_tx = get_block_tx(df_blocks)

    # Generate output CSV with results
    df_output = generate_block_report(df_blocks, block_value, block_timediff)
    df_output_t = generate_time_report(block_avgsize, block_tx)
    print("\nOutput files generated (blocks_info.csv, blocks_t_info.csv).\n")

    # Plot results
    plot_block_features(df_output)
    plot_time_features(df_output_t)
