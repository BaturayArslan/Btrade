# Btrade 🤖 

Automation tool for Future Trading.


## Demo

![Demo](https://user-images.githubusercontent.com/33760107/177047357-36615830-e982-4eac-86d7-f220721e0192.gif)


## What You Can Dou With Btrade ? 

You can automize your futures trade via **TradingView** and **Btrade**.Use **Tradingview**
for produce BUY or Sell signal and  **Btrade** will listen that signals then open position on provided
exchange with leverage , profit and loss limit . (currently only support Kucoin but ım planning to add more exchange future.).

## When And Why You Should Use Btrade ?
1-) If your trading stragedy representable as TradingView stragedy.\
2-) You wanna do Future trade\
3-) You dont have much time.


## 🖥️ Installation
        🛠️ Requirements
        * Basic Knowledge of Tradingview and Upgraded Tradingview account.
        * Running and reachable server from internet (preferable Apache on cloud instance)
        * Kucoin future api key 
        * Python 3.7+
  
* Install Btrade with pip:

```bash
  pip install btrade 
```
* You must configure your web server to listen Tradingview signal(webhook) and write that signal to "/var/www/webhook/event.txt" so Btrade can watch changes on that file.\
\
* if you dont have web server yet you can create one with using **Apache** and **Amazon ec2 instance** with  following this briefly described steps:\
  1-) Launch ec2 instance.\
  2-) Install apache and php\
  3-) Create "/var/www/webhook" directory and move script that inside of this repository "./scripts/webhook.php" to this directory.\
  4-) Push "RewriteEngine on" and 'RewriteRule "^/**<path_to_signal_to_be_send>**"  "/var/www/webhook/webhook.php"'\
  5-) Start apache server.



* Produce signal with Tradingview:    


![tradingWiev](https://user-images.githubusercontent.com/33760107/177047341-81c9817a-8855-4137-8c53-dce01d27d04d.png)



## Usage/Examples

```python

btrade.py -p 20 -s 10 -l 20 --pair "XBTUSDTM" -e "kucoin" -f "./configs.ini"

```

-p for profit limit when yor profit ratio hit that value position will be closed.\
-s for loss limit when position lose raiot hit that value position wiil be closed.\
-l for defining position leverage.\
--pair i think its quite self explonitary :) \
-e for exchange btrade only support kucoin exchange for now.\
-f for defining where btrade gonna read your kucoin future api key,passphrase and secret be able to create position.\
file format has to be like this : 

![file](https://user-images.githubusercontent.com/33760107/177047502-a51371d2-586f-4aea-90b3-2e9673edf2fc.png)

## Next Features

- [ ] Embeded server for processing incoming signals.
- [ ] More user friendly way of displaying position status info.
- [ ] Be able to close position via btrade.