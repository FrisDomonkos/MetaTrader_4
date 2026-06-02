Breakout Spike Trading EA

A MetaTrader 4 Expert Advisor (MQL4) that identifies high-volume bullish breakouts from consolidation zones and manages positions using a trailing stop methodology.

Overview

This Expert Advisor is a long-only breakout strategy designed to capture strong upward price movements following periods of low volatility and market consolidation.

The system combines:

Price breakout detection
Volume confirmation
Consolidation filtering
Upper wick analysis
Dynamic position sizing
Trailing stop management
Trade duration controls
Extensive indicator logging for quantitative analysis

In addition to trade execution, the EA logs dozens of technical indicators at trade entry, making it suitable for machine learning and statistical research.

Features
Entry Filters
Breakout detection based on configurable percentage move
Volume confirmation using historical average volume
Consolidation range analysis
Upper wick rejection filter
Single-position enforcement
Trade Management
Dynamic lot sizing
Trailing stop-loss
Follow-through validation
Maximum trade duration control
Data Collection
Logs all trade entries
Logs all trade exits
Records 30+ technical indicators
Generates datasets suitable for ML pipelines
Strategy Logic
Entry Conditions

A BUY trade is opened only when all conditions below are satisfied.

1. Price Breakout
Current Price - Current Candle Open
>
Current Candle Open × ChangeTrigger

Default:

ChangeTrigger = 0.01

Meaning:

Price must increase at least 1% from the current reference price.
2. Volume Confirmation
Current Volume
>
Average Volume × VolumeMultiplier

Default:

VolumeMultiplier = 2

Meaning:

Current volume must exceed twice the average volume of the previous 20 candles.
3. Consolidation Filter

The EA examines the previous Lookback candles.

Range %
=
((Highest High - Lowest Low) / Lowest Low) × 100

Trading is allowed only when:

Range % ≤ MaxRangePercent

Defaults:

Lookback = 20
MaxRangePercent = 3.0

Purpose:

Identify sideways market conditions before a breakout.
4. Upper Wick Filter

The previous candle is analysed.

Upper Wick %
=
Upper Wick Size / Candle Range × 100

Trading is allowed only when:

Upper Wick % ≤ UpperWickTolerance

Default:

UpperWickTolerance = 20

Purpose:

Avoid candles showing strong rejection from higher prices.
5. No Existing Position

Only one position may be active at any given time.

6. Indicator Filter

Currently disabled.

bool Indicator_Filter(...)
{
    return true;
}

The intended implementation appears to have been:

ADX > 25
ATR < 0.8%
Position Sizing

Position size scales automatically with account balance.

Formula:

(Account Balance / Starting Balance) × Lot Size

Defaults:

StartingBalance = 10000
LotSize = 3

Example:

Balance	Position Size
$5,000	1.5 Lots
$10,000	3 Lots
$20,000	6 Lots
Risk Management
Initial Stop Loss
Entry Price × (1 - TrailingDistance)

Default:

TrailingDistance = 0.01

Meaning:

Initial stop loss is placed 1% below entry.
Trailing Stop

The stop loss is continuously moved upward as price advances.

Characteristics:

Never moves downward
Locks in profits
Allows trends to continue
Follow-Through Validation

After a specified number of candles, the EA checks whether the breakout has continued.

Parameters:

FollowThroughTimeLimit = 3
FollowThroughThreshold = 1.02

Purpose:

Exit weak breakouts early
Retain strong momentum trades
Maximum Trade Duration

The EA can automatically close trades after a specified number of days.

Parameter:

MaxTradeDurationDays

Purpose:

Prevent excessive holding periods
Limit long-term exposure
Technical Indicator Logging

At trade entry, the EA records a large collection of indicators.

Trend Indicators
EMA(10)
EMA(50)
EMA(100)
ADX
Parabolic SAR
Ichimoku
Envelopes
Momentum Indicators
MACD
RSI(7)
RSI(14)
RSI(21)
RSI(28)
RSI(35)
Stochastic
Momentum
CCI
Williams %R
RVI
Volatility Indicators
Bollinger Bands
ATR
Standard Deviation
Volume Indicators
Volume
OBV
Accumulation Distribution
MFI
Hybrid Indicators
Awesome Oscillator
Accelerator Oscillator
DeMarker
Alligator
Output Files
Open Trade Log
open_trades_test.csv

Contains:

Trade information
Entry price
Entry timestamp
Market indicators
Technical indicator values

Purpose:

Machine learning datasets
Backtest analysis
Feature engineering
Closed Trade Log
closed_trades_test.csv

Contains:

Trade ticket
Exit price
Profit/Loss
Exit timestamp
Strategy parameters

Purpose:

Performance analysis
Trade outcome tracking
Workflow
Initialization
│
├── Create CSV logs
├── Calculate average volume
│
└── On Every Tick
     │
     ├── Detect new candle
     ├── Update filters
     │     ├── Volume
     │     ├── Consolidation
     │     └── Upper Wick
     │
     ├── Check active trades
     │
     ├── Manage open positions
     │     ├── Time limit
     │     ├── Follow-through check
     │     └── Trailing stop
     │
     └── Evaluate entry conditions
           │
           ├── Breakout detected?
           ├── Volume confirmed?
           ├── Consolidation valid?
           ├── Upper wick acceptable?
           └── Open BUY order
