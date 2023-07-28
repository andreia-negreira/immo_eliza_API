import pickle
import pandas as pd
import os

# In this file, the prediction function was initially created without using FastAPI
# It takes a dictionary as parameter
data = {
    "locality": "Borgerhout",
    "type_property": "APARTMENT",
    "subtype_property": "APARTMENT",
    "n_rooms": 2.0,
    "living_area": 106.0,
    "equipped_kitchen": 1.0,
    "furnished": 0.0,
    "fireplace": 1.0,
    "terrace": 1.0,
    "garden": 0.0,
    "land_surface": 3.0,
    "swimming_pool": 0.0,
    "state_building": "JUST_RENOVATED"
}

def prediction(**args):
    # The values from the dictionary are stored in a list of a dictionary
    data_list = [{'locality': args['locality'], 
                'Type_property': args['type_property'], 
                'subtype_property': args['subtype_property'], 
                'n_rooms': args['n_rooms'], 
                'living_area': args['living_area'], 
                'equipped_kitchen': args['equipped_kitchen'], 
                'furnished': args['furnished'], 
                'fireplace': args['fireplace'], 
                'terrace': args['terrace'], 
                'garden': args['garden'], 
                'land_surface': args['land_surface'], 
                'swimming_pool': args['swimming_pool'], 
                'state_building': args['state_building']}]
    # This list is transformed in a pandas dataframe
    df = pd.DataFrame(data_list)
    # The model is loaded
    filename = os.path.abspath("immo_prediction_model.pickle ")
    loaded_model = pickle.load(open(filename, "rb")) 
    # A prediction is made
    prediction = loaded_model.predict(df)
    prediction_model = {"prediction": prediction[0]}
    return prediction_model

# Calling the function
final_prediction = prediction(**data)
# Printing the outcome
print(final_prediction)

