import os as os
import re as re
import glob as glob
import datetime as dt
from pytz import timezone


def model_path(model_type):
    """Generate a model name by taking a model_type string (prediction_model, embedding_model, etc) and appending it to the current date and time
    
    Arguments:
        model_type {string} -- prediction_model, embedding_model, bigram
    
    Returns:
        string -- filepath and name
    """
    model_types = os.listdir("../models")
    if model_type in model_types:
        eastern = timezone('US/Eastern')
        now = dt.datetime.now(eastern).strftime('_%y%m%d_%H%M%S')
        #model_name = 'sproutml/models/' + model_type + 'test'+'.pkl'
        model_name = '../models/' + model_type + '/' + model_type + now + '.pkl'
        return model_name
    else:
        print("Error: You need to input a subdirectory of the models folder. Options are " +
              str(model_types) + ".")


def model_version(model_type):
    """Search the directory for all files containing the the string model_type and returns the most recently generated file
    
    Arguments:
        model_type {string} -- prediction_model, embedding_model, bigram
    
    Returns:
        string -- path of latest model version
    """
    model_types = os.listdir("../models")
    if model_type in model_types:  # Could add check to make sure all filenames match regex set out in model_name
        path = "../models/" + model_type + "/*"
        list_of_files = glob.glob(path)
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file
    else:
        print("Errror: You need to input a subdirectory of the models folder. Options are " +
              str(model_types) + ".")
