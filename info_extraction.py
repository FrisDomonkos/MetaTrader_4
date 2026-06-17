import pandas as pd
import matplotlib.pyplot as plt

def calc_profit(close_df: pd.DataFrame,
                TOP_N: int = 15,
                Mask: pd.DataFrame = None
               ) -> pd.DataFrame:
    """
    Calculates profit statistics for each test run.

    Outputs:
    - Profit: total profit
    - Trade_Count: number of trades
    - Lowest_Balance: worst cumulative profit state reached
    - Winning_Profit: sum of profitable trades
    - Winning_Count: number of profitable trades
    - Losing_Profit: sum of losing trades
    - Losing_Count: number of losing trades
    """
    def max_drawdown_metrics(profits, initial_balance=10000):
        equity = initial_balance + profits.cumsum()

        peak = equity.cummax()

        drawdown = peak - equity
        drawdown_pct = drawdown / peak  # relative to peak

        return pd.Series({
            "Max_Drawdown": drawdown.max(),
            "Max_Drawdown_Pct": drawdown_pct.max()
        })

    df = close_df.copy()

    # Running account balance (profit) within each test
    df["Running_Balance"] = df.groupby(["Test_ID", "Type"])["Profit"].cumsum()

    profit_df = df.groupby(["Test_ID", "Type"], as_index=False).agg(
        Profit=("Profit", "sum"),
        Max_Drawdown=("Profit", lambda x: max_drawdown_metrics(x, 10000)["Max_Drawdown"]),
        Max_Drawdown_Pct=("Profit", lambda x: max_drawdown_metrics(x, 10000)["Max_Drawdown_Pct"] *100),
        Trade_Count=("Profit", "size"),

        Winning_Profit=("Profit", lambda x: x[x > 0].sum()),
        Winning_Count=("Profit", lambda x: (x > 0).sum()),

        Losing_Profit=("Profit", lambda x: x[x < 0].sum()),
        Losing_Count=("Profit", lambda x: (x < 0).sum()),


    )

    return (
        profit_df
        .sort_values(by="Profit", ascending=False)
        .head(TOP_N)
    )

def calc_profit_with_condition(df: pd.DataFrame,
                               filter_mask: tuple,
                               sort_column: str = 'Profit',
                               TOP_N: int = 15
                              ) -> pd.DataFrame:
    
    '''
    Description:
    - Goal is to apply the results of a decision tree classification model
    - Use a filter mask to achive the classification
    - Calculates the profit for each filtered test run and sorts them based on it

    Inputs: 
    - df: pandas dataframe containing transaction data
    - filter_mask: filter equivalent with the classification
    - sort_column: basis of the sorting
    - TOP_N: How many rows to display
    
    Outputs:
    - out_df: pandas dataframe containing the sum of wins, losses and the total profit for each test run
    with and without the filtering
    '''
    
    # Filter mask example
    # filter_variable_values = ["slow_MA","SAR","fast_MA_prev"]
    # example_mask = (
    #     (df["slow_MA"] > filter_variable_values[0])
    #     &
    #     (
    #         (df["SAR"] <= filter_variable_values[1])
    #         |
    #         (df["fast_MA_prev"] > filter_variable_values[2])
    #     )
    # )
    
    # Total winning profit
    profit_df = (
        df[df['Profit'] > 0]
        .groupby(["Test_ID", "Type"], as_index=False)["Profit"]
        .sum()
        .rename(columns={"Profit": "Win"})
    )

    # Total losing profit
    loss_df = (
        df[df['Profit'] <= 0]
        .groupby(["Test_ID", "Type"], as_index=False)["Profit"]
        .sum()
        .rename(columns={"Profit": "Loss"})
    )

    # Merge total results
    out_df = (
        profit_df.merge(
            loss_df,
            on=["Test_ID", "Type"],
            how="outer"
        )
        .fillna(0)
    )

    # Total net profit
    out_df['Profit'] = out_df['Win'] + out_df['Loss']

    # Filtered wins
    #filter_win_df = (
     #   df[filter_mask]
      #  .groupby(["Test_ID", "Type"], as_index=False)["Profit"]
       # .sum()
        #.rename(columns={"Profit": "Class_1"})
    #)
    filter_win_df = (
        df[filter_mask]
        .groupby(["Test_ID", "Type"], as_index=False)
        .agg(
            Class_1_Profit=("Profit", "sum"),
            Class_1_Wins=("Profit", lambda x: x[x > 0].sum()),
            Class_1_Losses=("Profit", lambda x: x[x < 0].sum()),
        )
    )
    # Filtered losses
    #filter_loss_df = (
     #   df[~filter_mask]
      #  .groupby(["Test_ID", "Type"], as_index=False)["Profit"]
       # .sum()
        #.rename(columns={"Profit": "Class_0"})
    #)
    filter_loss_df = (
        df[~filter_mask]
        .groupby(["Test_ID", "Type"], as_index=False)
        .agg(
            Class_0_Profit=("Profit", "sum"),
            Class_0_Wins=("Profit", lambda x: x[x > 0].sum()),
            Class_0_Losses=("Profit", lambda x: x[x < 0].sum()),
        )
    )
    # Merge results safely
    out_df = (
        out_df
        .merge(filter_win_df, on=["Test_ID", "Type"], how="left")
        .merge(filter_loss_df, on=["Test_ID", "Type"], how="left")
        .fillna(0)
    )

    return (
        out_df
        .sort_values(by=sort_column, ascending=False)
        .round(0)
        .head(TOP_N)
    )


def plot_corr_with_highlight(df, target_col, columns=None, scale=1.1):
    # Filter columns if provided
    if columns is not None:
        missing = set(columns) - set(df.columns)
        if missing:
            raise ValueError(f"Columns not found in dataframe: {missing}")
        df = df[columns]

    # Compute correlation matrix
    corr = df.corr()

    if target_col not in corr.columns:
        raise ValueError(f"{target_col} not found in selected columns")

    n = len(corr.columns)

    # Dynamically scale figure size
    fig_size = max(6, n * scale)
    fig, ax = plt.subplots(figsize=(fig_size, fig_size))

    cax = ax.matshow(corr)
    plt.colorbar(cax)

    # Highlight mask
    highlight_mask = np.zeros_like(corr, dtype=bool)
    target_idx = corr.columns.get_loc(target_col)
    highlight_mask[target_idx, :] = True
    highlight_mask[:, target_idx] = True

    # Adjust font size dynamically
    font_size = max(10, min(12, 20 / n))

    # Add values
    for i in range(n):
        for j in range(n):
            value = corr.iloc[i, j]
            ax.text(j, i, f"{value:.2f}",
                    va='center', ha='center',
                    fontsize=font_size,
                    color='white' if abs(value) > 0.5 else 'black')

    # Draw highlight boxes
    for i in range(n):
        for j in range(n):
            if highlight_mask[i, j]:
                ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1,
                                           fill=False, edgecolor='red', linewidth=2))

    # Labels
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(corr.columns, rotation=90, fontsize=font_size)
    ax.set_yticklabels(corr.columns, fontsize=font_size)

    plt.title(f"Correlation Matrix (highlight: {target_col})", fontsize=font_size + 2)
    plt.tight_layout()
    plt.show()

    return corr