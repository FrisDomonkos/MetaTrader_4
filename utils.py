import pandas as pd

def days_hours_minutes(td):
    return td.days, td.seconds//3600, (td.seconds//60)%60

def Preprocessing(raw_df,
                  date_format="%Y.%m.%d %H:%M:%S"):
    
    processed_df = raw_df.copy()
    
    processed_df["OpenTime"] = pd.to_datetime(processed_df["OpenTime"], format=date_format)
    processed_df["CloseTime"] = pd.to_datetime(processed_df["CloseTime"], format=date_format)
    processed_df['TradeDuration'] =(processed_df["CloseTime"] - processed_df["OpenTime"]).apply(lambda x: x.seconds)
    
    processed_df["TradeResult"] = processed_df["Profit"].apply(lambda x: 1 if x >= 0 else -1) 

    processed_df["WaitTime"] = (processed_df["OpenTime"] - processed_df["CloseTime"].shift(1)).apply(lambda x: x.seconds)
    processed_df["WaitTime"] = processed_df["WaitTime"].fillna(0)

    return processed_df

def Extract_Profit_Data(df):
    profit = df['Profit'].sum()
    
    positive_profit_df = df[df['TradeResult'] == 1]
    positive_profit = positive_profit_df['Profit'].sum()

    negative_profit_df = df[df['TradeResult'] == -1]
    negative_profit = negative_profit_df['Profit'].sum()
    
    '''
    print(f'Net Profit: {profit}')
    print('')
    print(f'Number of wins: {len(positive_profit_df)}')
    print(f'Profit: {positive_profit}')
    print('')
    print(f'Number of losses: {len(negative_profit_df)}')
    print(f'Loss: {negative_profit}')
    '''
    return profit, len(positive_profit_df), positive_profit, len(negative_profit_df), negative_profit

def Extract_Time_Data(df):

    win_df = df[df['TradeResult'] == 1]
    loss_df = df[df['TradeResult'] == -1]
    fig, axes = plt.subplots(2, 3, figsize=(15, 4))

    # All durations
    df['TradeDuration'].plot(kind='hist', bins=10, ax=axes[0][0])
    axes[0][0].set_title('All Trade Durations')
    axes[0][0].set_xlabel('Bars')
    axes[0][0].set_ylabel('Amount')
    
    # Win durations
    win_df['TradeDuration'].plot(kind='hist', bins=10, ax=axes[0][1])
    axes[0][1].set_title('Win Trade Durations')
    axes[0][1].set_xlabel('Bars')
    axes[0][1].set_ylabel('Amount')
    
    # Loss durations
    loss_df['TradeDuration'].plot(kind='hist', bins=10, ax=axes[0][2])
    axes[0][2].set_title('Loss Trade Durations')
    axes[0][2].set_xlabel('Bars')
    axes[0][2].set_ylabel('Amount')

    # All durations
    df['WaitTime'].plot(kind='hist', bins=10, ax=axes[1][0])
    axes[1][0].set_title('All Wait Durations')
    axes[1][0].set_xlabel('Bars')
    axes[1][0].set_ylabel('Amount')
    
    # Win durations
    win_df['WaitTime'].plot(kind='hist', bins=10, ax=axes[1][1])
    axes[1][1].set_title('Win Wait Durations')
    axes[1][1].set_xlabel('Bars')
    axes[1][1].set_ylabel('Amount')
    
    # Loss durations
    loss_df['WaitTime'].plot(kind='hist', bins=10, ax=axes[1][2])
    axes[1][2].set_title('Loss Wait Durations')
    axes[1][2].set_xlabel('Bars')
    axes[1][2].set_ylabel('Amount')
    
    plt.tight_layout()
    plt.show()