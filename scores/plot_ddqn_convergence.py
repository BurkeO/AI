import pandas as pd 
import matplotlib.pyplot as plt

score_file_names = {
    "WIN_SIZE_300" : "ddqn_avg_scores_300_SIZE_12_2021_04_22_14_51_46.csv",
    "WIN_SIZE_400" : "ddqn_avg_scores_400_SIZE_16_2021_04_23_10_16_07.csv",
    "WIN_SIZE_500" : "ddqn_avg_scores_500_SIZE_20_2021_04_23_13_36_49.csv",
    "WIN_SIZE_600" : "ddqn_avg_scores_600_SIZE_24_2021_04_23_17_05_59.csv"
}

def normalize_x_axis(dfs):
    max_steps = 400000

    for df in dfs:
        df_max_runs = df.iloc[-1][0]
        norm_multip = float(max_steps)/float(df_max_runs)
        for run_index in range(int(df.size/2)):
            df.iloc[run_index,0] = df.iloc[run_index,0] * norm_multip

    return dfs

def plot_graphs():
    df_300 = pd.read_csv(score_file_names["WIN_SIZE_300"])
    df_400 = pd.read_csv(score_file_names["WIN_SIZE_400"])
    df_500 = pd.read_csv(score_file_names["WIN_SIZE_500"])
    df_600 = pd.read_csv(score_file_names["WIN_SIZE_600"])

    dfs = [df_300,df_400,df_500,df_600]

    normalized_dfs = normalize_x_axis(dfs)

    ax = normalized_dfs[0].plot(x="Steps",y="Score",label="N=300")
    for i in range(1,len(normalized_dfs)):
        n = (i+3) * 100
        label = "N=" + str(n)
        normalized_dfs[i].plot(ax=ax,x="Steps",y="Score", label=label)

    ax.set_ylabel("Average Score (500 Runs)")
    plt.show()


if __name__ == "__main__":
    plot_graphs()