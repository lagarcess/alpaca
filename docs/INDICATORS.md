# Supported Technical Indicators

This document lists all technical indicators supported by the engine.

## Syntax Guide

For indicators that support a **Time Period** (e.g. SMA, RSI), you can specify the period using an underscore:
- Format: `INDICATOR_PERIOD`
- Example: `SMA_50` (50-period Simple Moving Average)
- Example: `RSI_14` (14-period Relative Strength Index)

For others, simply use the indicator name (e.g., `OBV`).

## Cycle Indicators

| Indicator | Full Name | Syntax Example |
| :--- | :--- | :--- |
| **HT_DCPERIOD** | Hilbert Transform - Dominant Cycle Period | `HT_DCPERIOD` |
| **HT_DCPHASE** | Hilbert Transform - Dominant Cycle Phase | `HT_DCPHASE` |
| **HT_PHASOR** | Hilbert Transform - Phasor Components | `HT_PHASOR` |
| **HT_SINE** | Hilbert Transform - SineWave | `HT_SINE` |
| **HT_TRENDMODE** | Hilbert Transform - Trend vs Cycle Mode | `HT_TRENDMODE` |

## Math Operators

| Indicator | Full Name | Syntax Example |
| :--- | :--- | :--- |
| **ADD** | Vector Arithmetic Add | `ADD` |
| **DIV** | Vector Arithmetic Div | `DIV` |
| **MAX** | Highest value over a specified period | `MAX_14` or `MAX` |
| **MAXINDEX** | Index of highest value over a specified period | `MAXINDEX_14` or `MAXINDEX` |
| **MIN** | Lowest value over a specified period | `MIN_14` or `MIN` |
| **MININDEX** | Index of lowest value over a specified period | `MININDEX_14` or `MININDEX` |
| **MINMAX** | Lowest and highest values over a specified period | `MINMAX_14` or `MINMAX` |
| **MINMAXINDEX** | Indexes of lowest and highest values over a specified period | `MINMAXINDEX_14` or `MINMAXINDEX` |
| **MULT** | Vector Arithmetic Mult | `MULT` |
| **SUB** | Vector Arithmetic Subtraction | `SUB` |
| **SUM** | Summation | `SUM_14` or `SUM` |

## Math Transform

| Indicator | Full Name | Syntax Example |
| :--- | :--- | :--- |
| **ACOS** | Vector Trigonometric ACos | `ACOS` |
| **ASIN** | Vector Trigonometric ASin | `ASIN` |
| **ATAN** | Vector Trigonometric ATan | `ATAN` |
| **CEIL** | Vector Ceil | `CEIL` |
| **COS** | Vector Trigonometric Cos | `COS` |
| **COSH** | Vector Trigonometric Cosh | `COSH` |
| **EXP** | Vector Arithmetic Exp | `EXP` |
| **FLOOR** | Vector Floor | `FLOOR` |
| **LN** | Vector Log Natural | `LN` |
| **LOG10** | Vector Log10 | `LOG10` |
| **SIN** | Vector Trigonometric Sin | `SIN` |
| **SINH** | Vector Trigonometric Sinh | `SINH` |
| **SQRT** | Vector Square Root | `SQRT` |
| **TAN** | Vector Trigonometric Tan | `TAN` |
| **TANH** | Vector Trigonometric Tanh | `TANH` |

## Momentum Indicators

| Indicator | Full Name | Syntax Example |
| :--- | :--- | :--- |
| **ADX** | Average Directional Movement Index | `ADX_14` or `ADX` |
| **ADXR** | Average Directional Movement Index Rating | `ADXR_14` or `ADXR` |
| **APO** | Absolute Price Oscillator | `APO` |
| **AROON** | Aroon | `AROON_14` or `AROON` |
| **AROONOSC** | Aroon Oscillator | `AROONOSC_14` or `AROONOSC` |
| **BOP** | Balance Of Power | `BOP` |
| **CCI** | Commodity Channel Index | `CCI_14` or `CCI` |
| **CMO** | Chande Momentum Oscillator | `CMO_14` or `CMO` |
| **DX** | Directional Movement Index | `DX_14` or `DX` |
| **MACD** | Moving Average Convergence/Divergence | `MACD` |
| **MACDEXT** | MACD with controllable MA type | `MACDEXT` |
| **MACDFIX** | Moving Average Convergence/Divergence Fix 12/26 | `MACDFIX` |
| **MFI** | Money Flow Index | `MFI_14` or `MFI` |
| **MINUS_DI** | Minus Directional Indicator | `MINUS_DI_14` or `MINUS_DI` |
| **MINUS_DM** | Minus Directional Movement | `MINUS_DM_14` or `MINUS_DM` |
| **MOM** | Momentum | `MOM_14` or `MOM` |
| **PLUS_DI** | Plus Directional Indicator | `PLUS_DI_14` or `PLUS_DI` |
| **PLUS_DM** | Plus Directional Movement | `PLUS_DM_14` or `PLUS_DM` |
| **PPO** | Percentage Price Oscillator | `PPO` |
| **ROC** | Rate of change : ((price/prevPrice)-1)*100 | `ROC_14` or `ROC` |
| **ROCP** | Rate of change Percentage: (price-prevPrice)/prevPrice | `ROCP_14` or `ROCP` |
| **ROCR** | Rate of change ratio: (price/prevPrice) | `ROCR_14` or `ROCR` |
| **ROCR100** | Rate of change ratio 100 scale: (price/prevPrice)*100 | `ROCR100_14` or `ROCR100` |
| **RSI** | Relative Strength Index | `RSI_14` or `RSI` |
| **STOCH** | Stochastic | `STOCH` |
| **STOCHF** | Stochastic Fast | `STOCHF` |
| **STOCHRSI** | Stochastic Relative Strength Index | `STOCHRSI_14` or `STOCHRSI` |
| **TRIX** | 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA | `TRIX_14` or `TRIX` |
| **ULTOSC** | Ultimate Oscillator | `ULTOSC` |
| **WILLR** | Williams' %R | `WILLR_14` or `WILLR` |

## Overlap Studies

| Indicator | Full Name | Syntax Example |
| :--- | :--- | :--- |
| **BBANDS** | Bollinger Bands | `BBANDS_14` or `BBANDS` |
| **DEMA** | Double Exponential Moving Average | `DEMA_14` or `DEMA` |
| **EMA** | Exponential Moving Average | `EMA_14` or `EMA` |
| **HT_TRENDLINE** | Hilbert Transform - Instantaneous Trendline | `HT_TRENDLINE` |
| **KAMA** | Kaufman Adaptive Moving Average | `KAMA_14` or `KAMA` |
| **MA** | Moving average | `MA_14` or `MA` |
| **MAMA** | MESA Adaptive Moving Average | `MAMA` |
| **MAVP** | Moving average with variable period | `MAVP` |
| **MIDPOINT** | MidPoint over period | `MIDPOINT_14` or `MIDPOINT` |
| **MIDPRICE** | Midpoint Price over period | `MIDPRICE_14` or `MIDPRICE` |
| **SAR** | Parabolic SAR | `SAR` |
| **SAREXT** | Parabolic SAR - Extended | `SAREXT` |
| **SMA** | Simple Moving Average | `SMA_14` or `SMA` |
| **T3** | Triple Exponential Moving Average (T3) | `T3_14` or `T3` |
| **TEMA** | Triple Exponential Moving Average | `TEMA_14` or `TEMA` |
| **TRIMA** | Triangular Moving Average | `TRIMA_14` or `TRIMA` |
| **WMA** | Weighted Moving Average | `WMA_14` or `WMA` |

## Pattern Recognition

| Indicator | Full Name | Syntax Example |
| :--- | :--- | :--- |
| **CDL2CROWS** | Two Crows | `CDL2CROWS` |
| **CDL3BLACKCROWS** | Three Black Crows | `CDL3BLACKCROWS` |
| **CDL3INSIDE** | Three Inside Up/Down | `CDL3INSIDE` |
| **CDL3LINESTRIKE** | Three-Line Strike  | `CDL3LINESTRIKE` |
| **CDL3OUTSIDE** | Three Outside Up/Down | `CDL3OUTSIDE` |
| **CDL3STARSINSOUTH** | Three Stars In The South | `CDL3STARSINSOUTH` |
| **CDL3WHITESOLDIERS** | Three Advancing White Soldiers | `CDL3WHITESOLDIERS` |
| **CDLABANDONEDBABY** | Abandoned Baby | `CDLABANDONEDBABY` |
| **CDLADVANCEBLOCK** | Advance Block | `CDLADVANCEBLOCK` |
| **CDLBELTHOLD** | Belt-hold | `CDLBELTHOLD` |
| **CDLBREAKAWAY** | Breakaway | `CDLBREAKAWAY` |
| **CDLCLOSINGMARUBOZU** | Closing Marubozu | `CDLCLOSINGMARUBOZU` |
| **CDLCONCEALBABYSWALL** | Concealing Baby Swallow | `CDLCONCEALBABYSWALL` |
| **CDLCOUNTERATTACK** | Counterattack | `CDLCOUNTERATTACK` |
| **CDLDARKCLOUDCOVER** | Dark Cloud Cover | `CDLDARKCLOUDCOVER` |
| **CDLDOJI** | Doji | `CDLDOJI` |
| **CDLDOJISTAR** | Doji Star | `CDLDOJISTAR` |
| **CDLDRAGONFLYDOJI** | Dragonfly Doji | `CDLDRAGONFLYDOJI` |
| **CDLENGULFING** | Engulfing Pattern | `CDLENGULFING` |
| **CDLEVENINGDOJISTAR** | Evening Doji Star | `CDLEVENINGDOJISTAR` |
| **CDLEVENINGSTAR** | Evening Star | `CDLEVENINGSTAR` |
| **CDLGAPSIDESIDEWHITE** | Up/Down-gap side-by-side white lines | `CDLGAPSIDESIDEWHITE` |
| **CDLGRAVESTONEDOJI** | Gravestone Doji | `CDLGRAVESTONEDOJI` |
| **CDLHAMMER** | Hammer | `CDLHAMMER` |
| **CDLHANGINGMAN** | Hanging Man | `CDLHANGINGMAN` |
| **CDLHARAMI** | Harami Pattern | `CDLHARAMI` |
| **CDLHARAMICROSS** | Harami Cross Pattern | `CDLHARAMICROSS` |
| **CDLHIGHWAVE** | High-Wave Candle | `CDLHIGHWAVE` |
| **CDLHIKKAKE** | Hikkake Pattern | `CDLHIKKAKE` |
| **CDLHIKKAKEMOD** | Modified Hikkake Pattern | `CDLHIKKAKEMOD` |
| **CDLHOMINGPIGEON** | Homing Pigeon | `CDLHOMINGPIGEON` |
| **CDLIDENTICAL3CROWS** | Identical Three Crows | `CDLIDENTICAL3CROWS` |
| **CDLINNECK** | In-Neck Pattern | `CDLINNECK` |
| **CDLINVERTEDHAMMER** | Inverted Hammer | `CDLINVERTEDHAMMER` |
| **CDLKICKING** | Kicking | `CDLKICKING` |
| **CDLKICKINGBYLENGTH** | Kicking - bull/bear determined by the longer marubozu | `CDLKICKINGBYLENGTH` |
| **CDLLADDERBOTTOM** | Ladder Bottom | `CDLLADDERBOTTOM` |
| **CDLLONGLEGGEDDOJI** | Long Legged Doji | `CDLLONGLEGGEDDOJI` |
| **CDLLONGLINE** | Long Line Candle | `CDLLONGLINE` |
| **CDLMARUBOZU** | Marubozu | `CDLMARUBOZU` |
| **CDLMATCHINGLOW** | Matching Low | `CDLMATCHINGLOW` |
| **CDLMATHOLD** | Mat Hold | `CDLMATHOLD` |
| **CDLMORNINGDOJISTAR** | Morning Doji Star | `CDLMORNINGDOJISTAR` |
| **CDLMORNINGSTAR** | Morning Star | `CDLMORNINGSTAR` |
| **CDLONNECK** | On-Neck Pattern | `CDLONNECK` |
| **CDLPIERCING** | Piercing Pattern | `CDLPIERCING` |
| **CDLRICKSHAWMAN** | Rickshaw Man | `CDLRICKSHAWMAN` |
| **CDLRISEFALL3METHODS** | Rising/Falling Three Methods | `CDLRISEFALL3METHODS` |
| **CDLSEPARATINGLINES** | Separating Lines | `CDLSEPARATINGLINES` |
| **CDLSHOOTINGSTAR** | Shooting Star | `CDLSHOOTINGSTAR` |
| **CDLSHORTLINE** | Short Line Candle | `CDLSHORTLINE` |
| **CDLSPINNINGTOP** | Spinning Top | `CDLSPINNINGTOP` |
| **CDLSTALLEDPATTERN** | Stalled Pattern | `CDLSTALLEDPATTERN` |
| **CDLSTICKSANDWICH** | Stick Sandwich | `CDLSTICKSANDWICH` |
| **CDLTAKURI** | Takuri (Dragonfly Doji with very long lower shadow) | `CDLTAKURI` |
| **CDLTASUKIGAP** | Tasuki Gap | `CDLTASUKIGAP` |
| **CDLTHRUSTING** | Thrusting Pattern | `CDLTHRUSTING` |
| **CDLTRISTAR** | Tristar Pattern | `CDLTRISTAR` |
| **CDLUNIQUE3RIVER** | Unique 3 River | `CDLUNIQUE3RIVER` |
| **CDLUPSIDEGAP2CROWS** | Upside Gap Two Crows | `CDLUPSIDEGAP2CROWS` |
| **CDLXSIDEGAP3METHODS** | Upside/Downside Gap Three Methods | `CDLXSIDEGAP3METHODS` |

## Price Transform

| Indicator | Full Name | Syntax Example |
| :--- | :--- | :--- |
| **AVGPRICE** | Average Price | `AVGPRICE` |
| **MEDPRICE** | Median Price | `MEDPRICE` |
| **TYPPRICE** | Typical Price | `TYPPRICE` |
| **WCLPRICE** | Weighted Close Price | `WCLPRICE` |

## Statistic Functions

| Indicator | Full Name | Syntax Example |
| :--- | :--- | :--- |
| **BETA** | Beta | `BETA_14` or `BETA` |
| **CORREL** | Pearson's Correlation Coefficient (r) | `CORREL_14` or `CORREL` |
| **LINEARREG** | Linear Regression | `LINEARREG_14` or `LINEARREG` |
| **LINEARREG_ANGLE** | Linear Regression Angle | `LINEARREG_ANGLE_14` or `LINEARREG_ANGLE` |
| **LINEARREG_INTERCEPT** | Linear Regression Intercept | `LINEARREG_INTERCEPT_14` or `LINEARREG_INTERCEPT` |
| **LINEARREG_SLOPE** | Linear Regression Slope | `LINEARREG_SLOPE_14` or `LINEARREG_SLOPE` |
| **STDDEV** | Standard Deviation | `STDDEV_14` or `STDDEV` |
| **TSF** | Time Series Forecast | `TSF_14` or `TSF` |
| **VAR** | Variance | `VAR_14` or `VAR` |

## Volatility Indicators

| Indicator | Full Name | Syntax Example |
| :--- | :--- | :--- |
| **ATR** | Average True Range | `ATR_14` or `ATR` |
| **NATR** | Normalized Average True Range | `NATR_14` or `NATR` |
| **TRANGE** | True Range | `TRANGE` |

## Volume Indicators

| Indicator | Full Name | Syntax Example |
| :--- | :--- | :--- |
| **AD** | Chaikin A/D Line | `AD` |
| **ADOSC** | Chaikin A/D Oscillator | `ADOSC` |
| **OBV** | On Balance Volume | `OBV` |

