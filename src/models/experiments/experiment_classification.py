from data_preparation import get_gen
from keras import backend, metrics
from model import get_model
from training import train
from testing import test, test_w_classification
from keras.optimizers import Adam, SGD
from keras.preprocessing.image import ImageDataGenerator
import global_hyperparams as hp

# Hyperparameters
NUM_EPOCHS = hp.NUM_EPOCHS
LEARNING_RATE = 0.001
BATCH_SIZE_TRAIN = 16
BATCH_SIZE_VAL = 16
LOSS = 'mae'
OPTIMIZER = Adam()
NUM_TRAINABLE_LAYERS = 10
IMG_SIZE = (299, 299)
PRETRAINED = 'imagenet'


def execute():
    """
    Experiment difference if performing regression or classification on age
    :return:
    """
    train_idg = ImageDataGenerator(rotation_range=20, width_shift_range=0.2, height_shift_range=0.2,
                                   zoom_range=0.2, horizontal_flip=True)

    val_idg = ImageDataGenerator(width_shift_range=0.25, height_shift_range=0.25, horizontal_flip=True)

    train_gen_boneage, val_gen_boneage, steps_per_epoch_boneage, validation_steps_boneage = get_gen(train_idg, val_idg,
                                                                                                    IMG_SIZE,
                                                                                                    BATCH_SIZE_TRAIN,
                                                                                                    BATCH_SIZE_VAL,
                                                                                                    'boneage',
                                                                                                    disease_enabled=False,
                                                                                                    classification=CLASSIFICATION)

    model = get_model(model='winner', gender_input_enabled=False, age_output_enabled=True,
                      disease_enabled=False, pretrained=PRETRAINED, classification=CLASSIFICATION)

    OPTIMIZER = Adam(lr=1e-3)

    history = train(train_gen_boneage, val_gen_boneage, steps_per_epoch_boneage, validation_steps_boneage, model,
                    OPTIMIZER, LOSS, LEARNING_RATE, NUM_EPOCHS, finetuning=False,
                    num_trainable_layers=NUM_TRAINABLE_LAYERS, metrics=METRICS)

    print('Boneage dataset (final) history:', history.history)

    if CLASSIFICATION:
        test_w_classification(model)
    else:
        test(model)

    backend.clear_session()


if __name__ == '__main__':
    CLASSIFICATION = True
    METRICS = hp.METRIC_CLASSIFICATION
    LOSS = hp.LOSS_CLASSIFICATION
    execute()
    CLASSIFICATION = False
    METRICS = hp.METRIC
    LOSS = hp.LOSS_DEFAULT
    execute()
