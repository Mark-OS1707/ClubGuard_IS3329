import json # Bringing in python's tool for reading JSON files
from pathlib import Path # Finding file locations

Profile_Directory_it_is_in = Path(__file__).parent

Profile_files = { "westeros-rfc": "westeros_rfc.json"} # Brings the club ID to the club profile in where the prototype has one club  which is the synthetic data

class ClubNotFoundError(Exception): # Given when no profile for the club ID matches it
    pass

def get_profile(club_id): # Getting the club profile
    if club_id in Profile_files:   # if statement
        filename = Profile_files[club_id]
        with open(Profile_Directory_it_is_in / filename, encoding="utf-8") as f:
            return json.load(f)          # if the club_id matches the club profile then the json data of it is returned of the synthetic data
    else:
        raise ClubNotFoundError(f"No club profile found for '{club_id}'.")  # else raises an error from the class  above when club id isn't found

def update_profile(club_id, changes): # Would update the club profile
        raise NotImplementedError("Editing the club profile is deferred in the prototype, that is for the target architecture.")
