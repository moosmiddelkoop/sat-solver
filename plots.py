import matplotlib.pyplot as plt
import sys
import seaborn as sns
import pandas as pd

# def create_dataframe()

def histogram(backtrack_path, title="Histogram of Backtracks", output_file="histogram.png"):
    '''
    function to plot histogram of backtracks
    '''

    # read the backtracks from the file
    with open(backtrack_path, 'r') as f:
        backtracks = f.readlines()[0]
        backtracks = [int(backtrack) for backtrack in backtracks]

    # plot the histogram bins = max(backtracks bc there are only integers and we want a bar for each integer)
    plt.hist(backtracks, bins=max(backtracks), align='left')
    plt.title(title, pad=15, fontweight='bold')
    plt.savefig(f"figs/histograms/{output_file}")
    plt.show()

def boxplot(backtrack_paths, title="Boxplot of Backtracks", output_file="boxplot.png"):
    '''
    function to plot boxplot of backtracks
    '''

    all_strategies = []

    for path in backtrack_paths:

        # read the backtracks from the file
        with open(path, 'r') as f:
            backtracks = f.readlines()[0]
            backtracks = [int(backtrack) for backtrack in backtracks]
        
            all_strategies.append(backtracks)

    # plot the boxplot
    fig, ax = plt.subplots()      

    sns.boxplot(all_strategies)
    plt.title(title, pad=20, font='arial', fontsize=14, fontweight='bold')
    plt.ylabel("Number of backtracks per sudoku", font='arial', fontsize=12, labelpad=10)
    plt.xlabel("Heuristic", font='arial', fontsize=12, labelpad=10)
    ax.set_xticklabels(['None', 'DLCS', 'Human'], fontweight='bold')
    plt.savefig(f"figs/boxplots/{output_file}")
    plt.show()

if __name__ == "__main__":

    type = sys.argv[1]

    if type == "histogram":
        histogram('results/backtracks-damnhard-S3.txt', 
                title='Histogram of backtracks per sudoku for damnhard.sdk.txt with heuristic: human',
                output_file='damnhard_S3.png')
        
    elif type == 'boxplot':
        boxplot(['results/backtracks.txt', 'results/backtracks-S2.txt', 'results/backtracks-S3.txt'],
                title='Boxplot of backtracks per sudoku for 1000_sudokus.txt',
                output_file='1000_sudokus_boxplot.png')