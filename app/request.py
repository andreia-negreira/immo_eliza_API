import requests

# For the request, it gets a disctionary as initial input
data = {
    "locality": "Borgerhout",
    "Type_property": "APARTMENT",
    "subtype_property": "APARTMENT",
    "n_rooms": 2.0,
    "living_area": 106.0,
    "equipped_kitchen": 1.0,
    "furnished": 0.0,
    "fireplace": 1.0,
    "terrace": 1.0,
    "garden": 0.0,
    "land_surface": 0.0,
    "swimming_pool": 0.0,
    "state_building": "JUST_RENOVATED"
}

# It makes the request passing the dictionary as argument in json type
prediction_response = requests.post("http://127.0.0.1:8000/prediction/", json=data)

print(prediction_response.text)
