import warnings

warnings.simplefilter("ignore")
# common library

# preprocessor
# config
# model
from model.models import *
from preprocessing.preprocessors import *


def run_model() -> None:
    """Train the model."""

    # read and preprocess data
    data = preprocess_data()
    print("1. Passed preprocessing data")
    # print(data)
    print("-------------------------------------------------------------")

    data = add_turbulence(data)
    print("2. Passed adding turbulence")
    # print(data)
    print("-------------------------------------------------------------")

    # 2015/10/01 is the date that validation starts
    # 2016/01/01 is the date that real trading starts
    # unique_trade_date needs to start from 2015/10/01 for validation purpose
    unique_trade_date = data[(data.datadate > 20151001) & (data.datadate <= 20200707)].datadate.unique()
    print("3. Passed unique_trade_data")
    # print(unique_trade_date)
    print("-------------------------------------------------------------")

    # rebalance_window is the number of months to retrain the model
    # validation_window is the numebr of months to validation the model and select for trading
    rebalance_window = 63
    validation_window = 63

    ## Ensemble Strategy
    print("4. Enter training process")
    run_ensemble_strategy(df=data,
                          unique_trade_date=unique_trade_date,
                          rebalance_window=rebalance_window,
                          validation_window=validation_window)

    # _logger.info(f"saving model version: {_version}")


if __name__ == "__main__":
    run_model()
