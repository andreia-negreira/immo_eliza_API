from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Union
from fastapi.responses import PlainTextResponse
import pandas as pd
import pickle
from enum import Enum

# Here the classes accepting Enum types were created in order to validate and controls the input by the user
# Each class will be further used in the BaseModel class in the appropriate object
# The content of each Enum class is what is only accepted as input
class Type_property_val(str, Enum):
    APARTMENT =  'APARTMENT'
    HOUSE = 'HOUSE'

class subtype_property_val(str, Enum):
    CASTLE = "CASTLE"
    EXCEPTIONAL_PROPERTY = "EXCEPTIONAL_PROPERTY"
    MANSION = "MANSION"
    VILLA = "VILLA"
    MANOR_HOUSE = "MANOR_HOUSE"
    OTHER_PROPERTY = "OTHER_PROPERTY"
    APARTMENT_BLOCK = "APARTMENT_BLOCK"
    PENTHOUSE = "PENTHOUSE"
    FARMHOUSE = "FARMHOUSE"
    MIXED_USE_BUILDING = "MIXED_USE_BUILDING"
    TRIPLEX = "TRIPLEX"
    LOFT = "LOFT"
    DUPLEX = "DUPLEX"
    COUNTRY_COTTAGE = "COUNTRY_COTTAGE"
    HOUSE = "HOUSE"
    TOWN_HOUSE = "TOWN_HOUSE"
    APARTMENT = "APARTMENT"
    GROUND_FLOOR = "GROUND_FLOOR"
    CHALET = "CHALET"
    BUNGALOW = "BUNGALOW"
    SERVICE_FLAT = "SERVICE_FLAT"
    FLAT_STUDIO = "FLAT_STUDIO"
    KOT = "KOT"

class state_building_val(str, Enum): 
    AS_NEW = "AS_NEW"
    JUST_RENOVATED = "JUST_RENOVATED"
    GOOD = "GOOD"
    TO_BE_DONE_UP = "TO_BE_DONE_UP"
    TO_RENOVATE = "TO_RENOVATE"
    TO_RESTORE = "TO_RESTORE"

# The BaseModel class accepts the objects used to create the model
# Different dtypes are accepted to avoid that the default error message will be raised
# In this way, the validation will be done inside the function prediction    
class Data(BaseModel):
    locality: Union[float, str] = None
    Type_property: Type_property_val = None
    subtype_property: subtype_property_val = None
    n_rooms: Union[float, str] = None
    living_area: Union[float, str] = None
    equipped_kitchen: Union[float, str] = None
    furnished: Union[float, str] = None
    fireplace: Union[float, str] = None
    terrace: Union[float, str] = None
    garden: Union[float, str] = None
    land_surface: Union[float, str] = None
    swimming_pool: Union[float, str] = None
    state_building: state_building_val = None
    class Config:
        use_enum_values = True
    
# The FastAPI is instantiated in the object app
app = FastAPI()

# The route get has the instruction for the post route
# It was used the parameter response_class to change the view mode of the text 
# It will be displayed with break lines, in a more readable way
@app.get('/', response_class=PlainTextResponse)
def root():
    return '''Hi there, if you are here, you probably want to make some prediction on the price of a property for sale in Belgium.\n

Here is how the route POST works and what you need to do:\n

1. It is expected from you that you enter all the data correctly, respecting the types;\n
2. For the features bellow, you have to enter the following options:\n
type_property: "APARTMENT" or "HOUSE"\n
subtype_property: "CASTLE", "EXCEPTIONAL_PROPERTY", "MANSION", "VILLA", "MANOR_HOUSE", "OTHER_PROPERTY", "APARTMENT_BLOCK",\n
                  "PENTHOUSE", "FARMHOUSE", "MIXED_USE_BUILDING", "TRIPLEX", "LOFT", "DUPLEX", "COUNTRY_COTTAGE", "HOUSE",\n
                  "TOWN_HOUSE", "APARTMENT", "GROUND_FLOOR", "CHALET", "BUNGALOW", "SERVICE_FLAT", "FLAT_STUDIO", "KOT"\n
state_building: "AS_NEW", "JUST_RENOVATED", "GOOD", "TO_BE_DONE_UP", "TO_RENOVATE", "TO_RESTORE"\n
3. For the location, the first letter has to be capitalized;\n
4. For the other features, please enter 0 for no and 1 for yes.\n

And that is it!\n

Now, please, grab your coffee and enjoy receiving a prediction by the click of your mouse! ;)'''

#The route post makes the prediction of the worth of the property
# It takes as parameter the objects of the BaseModel class
@app.post('/prediction/')
def prediction(item_preprocessing: Data):
    # It fist checks if any required field was missed during the request
    required_fields = {'locality', 'Type_property', 'subtype_property', 'n_rooms', 'living_area', 'equipped_kitchen',
                       'furnished', 'fireplace', 'terrace', 'garden', 'land_surface', 'swimming_pool', 'state_building'}
    missing_fields = required_fields - item_preprocessing.model_dump(exclude_none=True).keys()
    if missing_fields:
        # If the missing_fields variable is True, it will raise an error
        # It will indicate which key value was forgot
        raise HTTPException(status_code=400, detail= f"All required fields were expected. You forgot: {', '.join(missing_fields)}.")     
    # Transforming the Pydantic BaseModel list into a pandas dataframe
    df = pd.DataFrame([item_preprocessing.model_dump()])
    # Importing the model that was saved in a pickle file
    filename = "src/immo_prediction_model.pickle"
    # Opening the model and storing it in the object loaded_model
    loaded_model = pickle.load(open(filename, "rb"))
    # Making a prediction with the loaded_model using the new data
    prediction = loaded_model.predict(df)
    # As it was a succesful request, it will return the status code 200
    # At the same time, it returns the prediction        
    return {"Prediction €": prediction[0], "status_code": 200}
    