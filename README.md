# Cocktails

Cocktails was a 1-month project to write a trading strategy trainer. It can train, backtest, experiment and execute a trained model live. The primary model used is a set of stochastic indicators that are weighted using a neural network, to produce a buy or sell decision of a set volume. The trainer then optimises the network using a genetic algorithm that reinforces well performing models against worse performing ones.

### Install

1. Install [Python3](https://www.python.org/downloads/)
2. Install [Pip](https://pip.pypa.io/en/stable/installation/)
3. Install pip dependencies:

```commandline
pip install backtrader
pip install git+https://github.com/happydasch/btoandav20
```

4. Create `config.json` file in same directory as this README file
5. Create practice account on [Oanda](https://trade.oanda.com/)
6. Add Oanda API keys to `config.json` in this format:
```json
{
  "oanda": {
    "account": "ACCOUNT_ID",
    "token": "ACCOUNT_TOKEN"
  }
}
```

### Training

The first model listed in the [experiments file](src/model/ExperimentSet.py) is selected for training. The model is optimised using a genetic algorithm for 1000 generations at a 1 month, minute interval backtest. This halts after 20 generations if fitness doesn't improve, and caches the best model of each generation. The trainer can be executed with this command:

```commandline
python3 -u main.py train
```

Once training is complete, the model is outputted to the `./train` directory.

### Backtesting

The backtest command is used by the trainer to determine the fitness of a model. The backtest command triggers a backtest of the model in the `/train` directory and outputs the models return of investment

```commandline
python3 -u main.py backtest
```

### Experiments

The experiment command can be used to compare models or hyper parameter configurations listed in the [experiments file](src/model/ExperimentSet.py). It executes training on 5 set seeds for each experiment and compares their maximum fitness averages. The one with the best average is declared the winning configuration. Each experiment result is cached in the `/train` directory.

```commandline
python3 -u main.py experiment
```

### Live Trading

The live trader will run the model saved in the `/train` on live data. This executes real trades on the Oanda account found in `config.json`. This is built to run on a linux server where `install.sh` and `start_live.sh` are helper scripts that deploy this package onto the server.

```commandline
python3 -u main.py live
```



