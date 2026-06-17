import pandas as pd

def merge_open_close(open_df : pd.DataFrame,
                     close_df: pd.DataFrame
                    ) -> pd.DataFrame:
    '''
    Description:
    - Merges the open and close transaction data on Test_ID
    - Devides with the open price for indicators where its relevant
    
    Inputs: 
    - open_df: pandas dataframe containing transaction data related to the time of open
    - close_df: pandas dataframe containing transaction data related to the time of closure
    
    Outputs:
    - df: pandas dataframe merge of open_df and close_df
    '''
    df = pd.merge(
        open_df,
        close_df,
        on=["Test_ID", "Ticket"],
        how="right",
        suffixes=("_open", "_close")
    )

    # List of Indicators to normalise
    Normalise_with_price = ['fast_MA','fast_MA_prev','fast_EMA_diff','MA','slow_MA','SAR','ENVELOPES','AD','Alligator','ATR']
    
    for param in Normalise_with_price:
        df[param] = df[param] / df['OpenPrice']

    df = df.drop('Type_close',axis=1).rename(columns={"Type_open": "Type"})
    return df


def prepare_data(df: pd.DataFrame
                ) -> pd.DataFrame:

    '''
    Description:
    - Drop irrelevant columns
    - Create target columns
    
    Inputs: 
    - df: pandas dataframe 
    
    Outputs:
    - df: modified pandas dataframe
    '''
    
    
    df = df.drop(['Symbol_open','OpenTime','OpenTime',
                  'Symbol_close','ClosePrice', 'CloseTime',],
                 axis=1)
    
    df['Target'] = (df["Profit"] > 0).astype(int)


    df = df.drop('OpenPrice',axis=1)
    return df

def assign_candle_id(
    df: pd.DataFrame,
    time_col: str="OpenTime",
    candle_size: str="15min",
    id_col: str="candle_id"
) -> pd.DataFrame:
    '''
    Description:
    - Create candle_id column based on OpenTime
    - Create target columns
    
    Inputs: 
    - df: pandas dataframe 
    - time_col: column containing the date
    - candle_size: candle size to base the assigment on
    - id_col: name of the new col
    
    Outputs:
    - result: input df + the new col
    '''
    result = df.copy()

    ts = pd.to_datetime(result[time_col])

    # Convert candle size to nanoseconds
    candle_ns = pd.Timedelta(candle_size).value

    # Unix timestamp in nanoseconds
    result[id_col] = ts.astype("int64") // candle_ns

    return result