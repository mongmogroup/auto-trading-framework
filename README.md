## Deep Reinforcement Learning for Automated Stock Trading
This repository refers to the codes for ICAIF 2020 paper [1]. This project inherits the related work [1] and continues to develop under the issues as follows:
* update the source code with updated versions of ibraries such as stable_baselines3, pytorch, ...
* try to improve this framework with real-time data from the market
* other usecases ...

[1] Hongyang Yang, Xiao-Yang Liu, Shan Zhong, and Anwar Walid. 2020. Deep Reinforcement Learning for Automated Stock Trading: An Ensemble Strategy. In ICAIF ’20: ACM International Conference on AI in Finance, Oct. 15–16, 2020, Manhattan, NY. ACM, New York, NY, USA.


### Prerequisites
1. For [OpenAI Baselines new version](https://stable-baselines3.readthedocs.io/en/master/), you'll need system packages CMake, OpenMPI and zlib. Those can be installed as follows

* Ubuntu
```bash
sudo apt-get update && sudo apt-get install cmake libopenmpi-dev python3-dev zlib1g-dev
```

* Mac OS X
Installation of system packages on Mac requires [Homebrew](https://brew.sh). With Homebrew installed, run the following:
```bash
brew install cmake openmpi
```

    
2. Regarding Python stuffs, there could be some ways for setting up the training environment:
    * (1) Create and Activate Virtual Environment (Optional but highly recommended)
        - cd into this repository
        ```bash
        cd auto-trading-framework
        ```

        - Under folder /auto-trading-framework, create a virtual environment. Virtualenvs are essentially folders that have copies of python executable and all python packages. 
        ```bash
        pip install virtualenv
        ```
        
        - Create a virtualenv **venv** under folder /Deep-Reinforcement-Learning-for-Automated-Stock-Trading-Ensemble-Strategy-ICAIF-2020
        ```bash
        virtualenv -p python3 venv
        ```

        - To activate a virtualenv:
        ```
        source venv/bin/activate
        ```
    * (2) Using anaconda3

## Dependencies

The script has been tested running under **Python3**, with the folowing packages installed:

```shell
pip install -r requirements.txt
```

## How it works
<img src=figs/model-work-flow-diag.png width="500">

### Run the model
```shell
python run_DRL.py
```

### Backtesting
Use Quantopian's [pyfolio package](https://github.com/quantopian/pyfolio) to do the backtesting.
[Backtesting script](backtesting.ipynb)

### Example - Monitoring
``` C
1. Passed preprocessing data
-------------------------------------------------------------
2. Passed adding turbulence
-------------------------------------------------------------
3. Passed unique_trade_data
-------------------------------------------------------------
4. Enter training process
============Start Ensemble Strategy============
============================================
turbulence_threshold:  130.19491825258828
======Model training from:  20090000 to  20151002
======A2C Training========
Training time (A2C):  0.4647514780362447  minutes
======A2C Validation from:  20151002 to  20160104
A2C Sharpe Ratio:  -0.11609424116105528
======PPO Training========
Training time (PPO):  2.264845355351766  minutes
======PPO Validation from:  20151002 to  20160104
PPO Sharpe Ratio:  -0.10733510169634948
======DDPG Training========
Training time (DDPG):  5.358744196097056  minutes
======DDPG Validation from:  20151002 to  20160104
======Trading from:  20160104 to  20160405
Used Model:  <stable_baselines3.ddpg.ddpg.DDPG object at 0x7f567f00bdf0>
previous_total_asset:1000000
end_total_asset:1061363.482010001
total_reward:61363.482010001084
total_cost:  2251.53235
total trades:  880
Sharpe:  0.22554647670927147
============Trading Done============
============================================
turbulence_threshold:  96.08032158358498
======Model training from:  20090000 to  20160104
```

### Data
The stock data we use is pulled from [Compustat database via Wharton Research Data Services](https://wrds-web.wharton.upenn.edu/wrds/ds/compd/fundq).
<img src=figs/data.PNG width="500">

### Ensemble Strategy
Our purpose is to create a highly robust trading strategy. So we use an ensemble method to automatically select the best performing agent among PPO, A2C, and DDPG to trade based on the Sharpe ratio. The ensemble process is described as follows:
* __Step 1__. We use a growing window of 𝑛 months to retrain our three agents concurrently. In this paper we retrain our three agents at every 3 months.
* __Step 2__. We validate all 3 agents by using a 12-month validation- rolling window followed by the growing window we used for train- ing to pick the best performing agent which has the highest Sharpe ratio. We also adjust risk-aversion by using turbulence index in our validation stage.
* __Step 3__. After validation, we only use the best model which has the highest Sharpe ratio to predict and trade for the next quarter.

### Performance
<img src=figs/performance.png>
