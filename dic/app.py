import streamlit as st
import pickle
import numpy as np
from explore_analysis import explore_analysis_page
from predict_sales import main_page


page=st.sidebar.selectbox("Explore or Predict",("Predict","Explore"))
model=''
    
if( page=="Predict"):
        main_page(model)
else:
        explore_analysis_page()        
            
 