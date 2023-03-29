# I use this file to generate a hash for the streamlit login password.
import os

import streamlit_authenticator as stauth

hashed_passwords = stauth.Hasher(os.environ['STREAMLIT_PASSWORD']).generate()

print(hashed_passwords)
