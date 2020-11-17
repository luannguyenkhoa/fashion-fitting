# Fashion Fitting

Building and training deep learning models using Keras.

# Installation

1. python3 -m venv env
2. source env/bin/activate
3. pip install -r requirements/dev.txt

**Python3 interpreter**
From Vscode, cmd + shift + P, type *Select Interpreter*, scroll down to find the python ver: *python 3.8.1* at path `env/bin/python`

# Getting Started
Build and train deep learning models with checkpoints and tensorboard visualization.

Steps to produce a run:
1. Define a data loader class.
2. Define a model class that inherits from BaseModel.
3. Define a trainer class that inherits.
4. Define a configuration file with the parameters needed in an experiment.
5. Run the model using:
```shell
python main.py -c [path to configuration file]
```

# Run The Project
To run the project:
1. Start the training using:
```shell
python main.py -c configs/conv_mnist_config.json
```
2. Start Tensorboard visualization using:
```shell
tensorboard --logdir=experiments/conv_mnist/logs
```

<div align="center">

<img align="center" width="600" src="https://github.com/Ahmkel/Keras-Project-Template/blob/master/figures/Tensorboard_demo.PNG?raw=true">

</div>

# Comet.ml Integration
This template also supports reporting to Comet.ml which allows you to see all your hyper-params, metrics, graphs, dependencies and more including real-time metric.

Add your API key [in the configuration file](configs/conv_mnist_config.json#L15):


Replace the corresponding api_key to the pair:  `"comet_api_key": "your key here"`

Here's how it looks after you start training:
<div align="center">

<img align="center" width="800" src="https://comet-ml.nyc3.digitaloceanspaces.com/CometDemo.gif">

</div>

You can also link your Github repository to your comet.ml project for full version control.


# Template Details

## Project Architecture

<div align="center">

<img align="center" width="600" src="https://github.com/Ahmkel/Keras-Project-Template/blob/master/figures/ProjectArchitecture.jpg?raw=true">

</div>


## Folder Structure

```
├── main.py             - here's an example of main that is responsible for the whole pipeline.
│
│
├── base                - this folder contains the abstract classes of the project components
│   ├── base_data_loader.py   - this file contains the abstract class of the data loader.
│   ├── base_model.py   - this file contains the abstract class of the model.
│   └── base_train.py   - this file contains the abstract class of the trainer.
│
│
├── model               - this folder contains the models of your project.
│   └── conv_mnist_model.py
│
│
├── trainer             - this folder contains the trainers of your project.
│   └── conv_mnist_trainer.py
│
|
├── data_loader         - this folder contains the data loaders of your project.
│   └── conv_mnist_data_loader.py
│
│
├── configs             - this folder contains the experiment and model configs of your project.
│   └── conv_mnist_config.json
│
│
├── datasets            - this folder might contain the datasets of your project.
│
│
└── utils               - this folder contains any utils you need.
     ├── config.py      - util functions for parsing the config files.
     ├── dirs.py        - util functions for creating directories.
     └── utils.py       - util functions for parsing arguments.
```


## Main Components

### Models
You need to:
1. Create a model class that inherits from **BaseModel**.
2. Override the ***build_model*** function which defines your model.
3. Call ***build_model*** function from the constructor.


### Trainers
You need to:
1. Create a trainer class that inherits from **BaseTrainer**.
2. Override the ***train*** function which defines the training logic.

**Note:** To add functionalities after each training epoch such as saving checkpoints or logs for tensorboard using Keras callbacks:
1. Declare a callbacks array in your constructor.
2. Define an ***init_callbacks*** function to populate your callbacks array and call it in your constructor.
3. Pass the callbacks array to the ***fit*** function on the model object.

**Note:** You can use ***fit_generator*** instead of ***fit*** to support generating new batches of data instead of loading the whole dataset at one time.

### Data Loaders
You need to:
1. Create a data loader class that inherits from **BaseDataLoader**.
2. Override the ***get_train_data()*** and the ***get_test_data()*** functions to return your train and test dataset splits.

**Note:** You can also define a different logic where the data loader class has a function ***get_next_batch*** if you want the data reader to read batches from your dataset each time.

### Configs
You need to define a .json file that contains your experiment and model configurations such as the experiment name, the batch size, and the number of epochs.


### Main
Responsible for building the pipeline.
1. Parse the config file
2. Create an instance of your data loader class.
3. Create an instance of your model class.
4. Create an instance of your trainer class.
5. Train your model using ".Train()" function on the trainer object.

### From Config
We can now load models without having to explicitly create an instance of each class. Look at:
1. from_config.py: this can load any config file set up to point to the right modules/classes to import
2. Look at configs/conv_mnist_from_config.json to get an idea of how this works from the config. Run it with:
```shell
python from_config.py -c configs/conv_mnist_from_config.json
```
3. See conv_mnist_from_config.json (and the additional data_loader/model) to see how easy it is to run a different experiment with just a different config file:
```shell
python from_config.py -c configs/conv_mnist_from_config.json
```

### Issue fixing:

Error: `ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1108)` <br>
Solution: add the following block code to the file at path: `env/lib/python3.8/site-packages/tensorflow/python/keras/utils/data_utils.py` before the line: `if sys.version_info[0] == 2:`
```
import requests
requests.packages.urllib3.disable_warnings()
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
```