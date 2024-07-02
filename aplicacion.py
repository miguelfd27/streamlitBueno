import streamlit_authenticator as stauth
import streamlit as st
import yaml
from yaml.loader import SafeLoader
import paquetes.modulo as md
import base64

page_element="""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://static.vecteezy.com/system/resources/previews/000/623/004/non_2x/auto-car-logo-template-vector-icon.jpg");
  background-size: 90%;
}
</style>
"""
st.set_page_config(layout="wide")
st.markdown(page_element, unsafe_allow_html=True)


nombre, estado, username, auth = md.login()

if st.session_state["authentication_status"]:
    md.logout(auth)
    md.menu()
    st.title(f'Bienvenido *{st.session_state["name"]}*')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

