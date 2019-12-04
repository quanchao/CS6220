# import the necessary packages
import os

pre_path = '/content/drive/My Drive/6220_project/'
# initialize the path to the *original* input directory of images
ORIG_INPUT_DATASET = pre_path + 'cleanedDatasets'

# initialize the base path to the *new* directory that will contain
# our images after computing the training and testing split
BASE_PATH = pre_path + "dataset"

# define the names of the training, testing, and validation
# directories
TRAIN = "trainData"
TEST = "testData"
VAL = "validData"

# initialize the list of class label names
CLASSES = ["cheesecake", "pancake","sashimi", "steak", "ice_cream", 
"pizza", "other_sandwich", "wings", "burrito", "dumpling", "fried_chicken", 
"pasta", "benedict", "curry", "fried_rice", "sushi", "waffle", "omelette", 
"spring_rolls", "ramen"]

# set the batch size when fine-tuning
BATCH_SIZE = 32

# initialize the label encoder file path and the output directory to
# where the extracted features (in CSV file format) will be stored
LE_PATH = os.path.sep.join([pre_path + "output", "le.cpickle"])
BASE_CSV_PATH = pre_path + "output"

# set the path to the serialized model after training
MODEL_PATH = os.path.sep.join([pre_path + "output", "food.model"])

# define the path to the output training history plots
UNFROZEN_PLOT_PATH_acc = os.path.sep.join([pre_path + "output", "unfrozen_acc.png"])
WARMUP_PLOT_PATH_acc = os.path.sep.join([pre_path + "output", "warmup_acc.png"])

UNFROZEN_PLOT_PATH_loss = os.path.sep.join([pre_path + "output", "unfrozen_loss.png"])
WARMUP_PLOT_PATH_loss = os.path.sep.join([pre_path + "output", "warmup_loss.png"])