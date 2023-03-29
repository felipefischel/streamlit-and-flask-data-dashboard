# I use this file to generate a hash for each password. 

import streamlit_authenticator as stauth

hashed_passwords = stauth.Hasher(['Capstone!']).generate()

print(hashed_passwords)
