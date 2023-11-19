import streamlit as st
import pickle
import numpy as np
from explore_analysis import explore_analysis_page
from predict_sales import main_page

 
page=st.sidebar.selectbox("Analyse Data & Predict or Predict Sales",("Predict Sales","Analyse Data & Predict"))
model=''
   
if( page=="Predict Sales"):
        main_page(model)
else:
        explore_analysis_page()        
            
 