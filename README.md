# Breakout Spike Trading EA (MQL4)

## Overview

This Expert Advisor (EA) is a long-only breakout trading system for MetaTrader 4. It detects upward price movements emerging from periods of consolidation and executes trades based on momentum, volume, and price action filters.

The EA also logs detailed market data and technical indicators for each trade, making it suitable for quantitative analysis.

---

## Strategy Type

- Breakout Trading
- Momentum-Based System
- Long Only
- Single Position at a Time

---

## Features

### Entry Logic
- Price breakout detection
- Volume spike confirmation
- Market consolidation filter
- Upper wick rejection filter
- Spike threshold trigger

### Trade Management
- Dynamic lot sizing based on account balance
- Trailing stop-loss system
- Follow-through validation
- Maximum trade duration control

### Data Logging
- Trade entry and exit logging
- 30+ technical indicators recorded per trade
- CSV dataset generation for analysis

---

## Entry Conditions

A BUY trade is opened only when ALL conditions are satisfied:

### 1. Price Breakout

The current price must rise by a configured threshold in a given candle above its lowest price. 

---

### 2. Volume Filter

Increased relative volume further indicates a brakeout event.

---

### 3. Consolidation Filter

The price must be in a tight range. Oscillating prices suggest indecisive market.

---

### 4. Upper Wick Filter

Prevents entries after rejection candles

---

### 5. Single Position Rule

Only one trade is allowed at a time.

---

## Position Sizing

Dynamic lot sizing based on account balance:

---

## Risk Management

### Trailing Stop Loss

- Moves stop loss upward as price increases
- Locks in profit
- Never moves downward

---

### Follow-Through Check

Weak breakouts may be closed early if momentum fails.

---

## Logging System

### Open Trades Log

Stores:
- Entry price and time
- Trade type
- Indicator snapshot
- Strategy configuration ID

---

### Closed Trades Log

Stores:
- Exit price
- Profit/Loss
- Close time
- Trade ticket
- Strategy parameters

---

## Workflow

1. EA initializes
2. Logs are created
3. Average volume is calculated
4. Every tick:
   - Detect new candle
   - Update filters (volume, consolidation, wick)
   - Check open trades
   - Manage trailing stop
   - Evaluate entry conditions
5. Open BUY trade if conditions are met
6. Log trade data
7. Manage trade until exit
