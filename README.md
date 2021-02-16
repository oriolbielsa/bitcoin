# Bitcoin Analyzer

## Table of contents
* [General info](#general-info)
* [Setup](#setup)
* [Usage example](#usage-example)
* [Graph details](#graph-details)
* [Release history](#release-history)

## General info
The purpose of this project is provide a tool for a basic and easy analysis of bitcoin blocks and transactions.

The studied features are: **(1) #Transactions per block**, **(2) Total value per block**, **(3) Time between blocks**, 
**(4) Average size of block per hour** and **(5) Total transactions per hour**.
	
## Setup
To run this project, copy it locally, and then execute:

```
$ cd ../bitcoin
$ python3 bitcoin.py
```

The input JSON files should be named: blocks.json and txs.json; and should be located in ./data path.
The reference files -which should be used for the unittest execution- can be downloaded in this [link](https://drive.google.com/file/d/1xLO-BISgwKRqNpDefF8I240HNh7xfU5A/view?usp=sharing).

## Usage example

1. Put desired blocks.json and txs.json files to be analyzed in ./data path
2. Execute bitcoin.py
3. Get [console information](./img/screen1.jpg) regarding finished analysis and output files created
4. Get graph plots of those [block features](./img/screen2_1.jpg), and [time features](./img/screen2_2.jpg)
5. Finally, in ./data folder you will have two outputs generated:

    5.1 **Output csv files** with all features: [blocks_info.csv](./img/screen3.jpg) and [blocks_t_info.csv](./img/screen4.jpg). 
	Those file include block hash details, so that they can be used for futher analysis or processing.
    
    5.2 **Output png graphs** as shown in execution (block_analysis.png and block_t_analysis.png)

## Graph details

* Transactions per block
    * x-axis: Blocks ordered by item (hash detail in csv output)
    * y-axis: Number of transactions contained in each block

* Total value per block
    * x-axis: Blocks ordered by item (hash detail in csv output)
    * y-axis: Sum of value of all transactions contained in each block

* Time difference between blocks
    * x-axis: Blocks ordered by item (hash detail in csv output)
    * y-axis: Time difference in seconds between block x and x-1. 
      (P.eg. the first registrer will always be NaN vale.)

* Average block size per hour
    * x-axis: Unique hour stamp
    * y-axis: Average block size in that hour 

* Block transactions per hour
    * x-axis: Unique hour stamp
    * y-axis: Sum of block transactions in that hour

## Release History

* 0.1.0
    * First full release