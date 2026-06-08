# Week 02 - OOP Stock Analyzer

This project converts the manual stock analyzer into an object-oriented structure.

The goal is to make the analysis code more reusable by representing each stock as an object with its own ticker, price data, and analysis methods.

## Features

* `Hisse` / `Stock` class
* Ticker and price attributes
* Daily return calculation method
* Simple moving average method
* Basic moving average signal generation method
* Reusable structure for analyzing multiple stocks

## Purpose

In the manual version, functions were called separately with price lists.
In this version, each stock object stores its own data and can run its own analysis methods.

This helps make the code more organized, reusable, and easier to extend later.

## Concepts Practiced

* Object-oriented programming
* Classes
* `__init__`
* `self`
* Instance attributes
* Methods
* `__str__`
* Returning data from methods
* Separating calculation logic from output

## Files

* `oop_analyzer.py`: Object-oriented stock analyzer script

## Example Usage

```python
aapl = Hisse("AAPL", [100, 102, 101, 105, 108])
print(aapl.gunluk_getiri())
print(aapl.hareketli_ortalama(3))
print(aapl.sinyal_uret())
```

## Next Steps

* Connect the OOP analyzer with CSV price data
* Add support for multiple tickers
* Move calculations into Pandas
* Build a basic backtesting engine
