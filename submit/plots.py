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
        # backtracks = f.readlines()[0]
        # backtracks = [int(backtrack) for backtrack in backtracks]

        backtracks = f.readlines()[1:500]
        backtracks = [int(backtrack[0]) for backtrack in backtracks]


    # plot the histogram bins = max(backtracks bc there are only integers and we want a bar for each integer)
    plt.hist(backtracks, bins=max(backtracks), align='left', color='g')
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
            # backtracks = f.readlines()[0]
            # backtracks = [int(backtrack) for backtrack in backtracks]

            backtracks = f.readlines()[1:501]
            all_strategies.append(backtracks)

    # plot the boxplot
    fig, ax = plt.subplots() 

    my_pal = ['tab:blue', 'tab:green']     

    sns.boxplot(all_strategies, palette=my_pal)
    plt.title(title, pad=20, font='arial', fontsize=13)
    plt.ylabel("Number of backtracks per Sudoku", font='arial', fontsize=12, labelpad=10)
    plt.xlabel("Heuristic", font='arial', fontsize=12, labelpad=10)

    # CHANGE THIS WHEN DOING THREE HEURISTICS
    ax.set_xticklabels(['None', 'Human'])
    plt.savefig(f"figs/boxplots/{output_file}")
    plt.show()

if __name__ == "__main__":

    type = sys.argv[1]

    if type == "histogram":
        histogram('results/top870_first500_S3.txt', 
                title='Histogram of of backtracks per sudoku \nfor 500 hard 9x9 sudokus with human heuristic',
                output_file='500_S3_hist.png')
        
    elif type == 'boxplot':
        boxplot(['results/500_S1.txt', 'results/500_S3.txt'],
                title='Boxplot of backtracks per sudoku for 500 hard 9x9 Sudokus',
                output_file='500_v4.png')