from data_loader.conv_mnist_data_loader import ConvMnistDataLoader
from models.conv_mnist_model import ConvMnistModel
from trainers.conv_mnist_trainer import ConvMnistModelTrainer
from utils.config import process_config
from utils.dirs import create_dirs
from utils.utils import get_args

def main():
    # capture the config path from the run arguments
    # then process the json configuration file
    try:
        args = get_args()
        config = process_config(args.config)
    except:
        print("missing or invalid arguments")
        exit(0)

    # create the experiments dirs
    create_dirs([config.callbacks.tensorboard_log_dir, config.callbacks.checkpoint_dir])

    print('Create the data generator.')
    data_loader = ConvMnistDataLoader(config)

    print('Create the model.')
    model = ConvMnistModel(config)

    print('Create the trainer')
    trainer = ConvMnistModelTrainer(model.model, data_loader.get_train_data(), config)

    print('Start training the model.')
    trainer.train()


if __name__ == '__main__':
    main()
