import pickle
from pathlib import Path
import streamlit_authenticator as stauth

names =  ["Birger", "Adeline Musonera", "Bievenu Murenzi", "HABIMANA Jean de Dieu"]
usernames = ["birger", "amusonera", "mbievenu", "jd"]
# passwords = ["birger@2022", "adelineC4", "MB24", "panini"]
passwords = ["XXX", "XXX", "XXX", "XXX"]

# Hash the password
hashed_passwords = stauth.Hasher(passwords).generate()

# Take the hashed password and store it into pickle file
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)