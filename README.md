# Algo
Bot that follows an algorithm in order to be profitable in the foreign exchange market. This strategy uses the CMF, MACD and the ATR and all indicators were built from scratch in the [indicators.py](https://github.com/centgan/Algo/indicators.py) file. This strategy does not belong to me and was not created by me please refernence TradePro at https://www.youtube.com/@tradepro or for the specfic video https://www.youtube.com/watch?v=KLLKVQoC2hY.

## How does it work
This strategy works based off mainly the MACD. The ATR indicator is only used as a guide for your stoploss which you will multiple the current value by 2 and this is the risk you aquire. The CMF is used essentially as a filter where longs are only acquired above the 0 line and shorts are only acquired below the 0 line. Here is where the MACD comes into play, only when the MACD line crosses above the signal line and above the 0 line would you take a buy and only when the signal line crosses above the MACD line and below the 0 line would you take a short.

## Results
This was never put in using real money to trade, only a paper account and the results were poor. Using this strategy had its ups but there were mainly downs. I never really had the intention to use this stategy on a proper account and really used this as an entrance into the world of trading bots.
