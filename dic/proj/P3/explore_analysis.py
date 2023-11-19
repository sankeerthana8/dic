import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import seaborn as sns
from io import StringIO
from predict_sales import main_page


model1=pickle.load(open('saved_file.pkl','rb'))



def encode_data(df):
    
    bool_val=0
    list1=['Item_Weight','Item_Visibility', 'Item_Type', 'Item_MRP',
       'Outlet_Establishment_Year', 'Outlet_Location_Type', 'Outlet_Type',
       'Outlet_Size','Item_Outlet_Sales']
    
    list_of_columns=df.columns
    
    for i in list_of_columns:
        if i not in list1:
            st.error(f"Please choose correct csv file with the correct columns {list1}")
            bool_val=1
            no_data = np.zeros(shape=(0,0))
            d = pd.DataFrame(no_data)
            return d
            
    if(bool_val==0):
        df['Item_Type']=df['Item_Type'].replace(to_replace =['Dairy','Baking Goods','Meat' ,'Breads','Seafood',
                                                     'Starchy Foods','Breakfast','Fruits and Vegetables','Household'] ,
                                        value = 'Household_Items')

        df['Item_Type']=df['Item_Type'].replace(to_replace =['Frozen Foods' , 'Canned','Snack Foods'] ,
                                        value = 'Snack_Items')

        df['Item_Type']=df['Item_Type'].replace(to_replace =['Soft Drinks' , 'Hard Drinks','Health and Hygiene','Others'] ,
                                        value = 'Other_Items')
    
        change_lists = df.columns[df.dtypes == "object"].tolist()
    
        for i in change_lists:
            df[i] = df[i].astype("category")
        enc=OneHotEncoder()
        columns = df.select_dtypes(['category']).columns
        df[columns] = df[columns].apply(lambda x: x.cat.codes)
    
        onehot1=pd.DataFrame(enc.fit_transform(df[['Outlet_Size']]).toarray())
        df['Outlet_Large']=onehot1[0]
        df['Outlet_Medium']=onehot1[1]
        df['Outlet_Small']=onehot1[2]
        df['Outlet_Establishment_Year'] = 2022 - df['Outlet_Establishment_Year']
       
        df=df.drop(['Outlet_Size'],axis=1)

        return df


def graphs(df):
   
   bool_val=0
   list1=['Item_Weight','Item_Visibility', 'Item_Type', 'Item_MRP',
       'Outlet_Establishment_Year', 'Outlet_Location_Type', 'Outlet_Type',
       'Outlet_Size','Item_Outlet_Sales']
   list_of_columns=df.columns
    
   for i in list1:
        
        if (i not in list_of_columns) or (len(list_of_columns)!=len(list1)):
            st.error(f"Please choose correct csv file with the correct columns {list1}")
            bool_val=1
            break
                 
   if(bool_val==0): 
       data = df.groupby(["Item_Outlet_Sales"])["Outlet_Location_Type"]
#     st.bar_chart(data)
       data = df['Item_Type'].value_counts()
       fig1, ax1 = plt.subplots()
       ax1.pie(data,labels=data.index, autopct="%1.0f%%", startangle=70)
       ax1.axis("equal") 
       st.subheader("ALL ITEMS OF FOOD")
       st.pyplot(fig1)
    
    
       data = df['Outlet_Location_Type'].value_counts()
       fig2, ax1 = plt.subplots()
       ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
       ax1.axis("equal")  
       st.subheader("ALL LOCATIONS")
       st.pyplot(fig2)
    
       fig=plt.figure(figsize=(4, 2))
       df['Item_Weight'].value_counts().plot(kind="area")
       st.subheader("ALL ITEMS WEIGHT") 
       st.pyplot(fig)
    
       data = df.groupby(["Outlet_Location_Type"])["Item_Outlet_Sales"].mean().sort_values(ascending=True)
       st.subheader("Outlet Location Types vs Sales")
       st.bar_chart(data)
    
       data = df.groupby(["Item_Type"])["Item_Outlet_Sales"].mean().sort_values(ascending=True)
       st.subheader("Item Types vs Sales")
       st.bar_chart(data)
    
       data = df.groupby(["Outlet_Size"])["Item_Outlet_Sales"].mean().sort_values(ascending=True)
       st.subheader("Outlet Size vs Sales")
       st.bar_chart(data)
    
       data = df.groupby(["Outlet_Type"])["Item_Outlet_Sales"].mean().sort_values(ascending=True)
       st.subheader("Outlet Types vs Sales")
       st.bar_chart(data)
    
  
def train_data(df,bool_val):
    df=encode_data(df)
    bool_val1=0
    if(df.shape[0]==0):
        bool_val1=1
    if(bool_val1==0):       
        X=df.drop(['Item_Outlet_Sales'],axis=1)
        Y=df['Item_Outlet_Sales']
        X = np.array(X)
        Y = np.array(Y)
        X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,random_state=2)
        model1.fit(X_train,Y_train)
        if(bool_val):
            main_page(model1)
            st.write("You can now Predict with your dataset")

    
def explore_analysis_page():
    st.title("Analyse Data and Prediction")
    html_temp = """
    <div style="background-color:#025246 ;padding:10px">
    <h2 style="color:white;text-align:center;">Exploration of Sales </h2>
    </div>
    """
    spectra = st.file_uploader("upload file", type="csv")
    # if st.button('clear uploaded_file'):
    #     state = st.get_session_state()
        # state.widget_key = str(randint(1000, 100000000))
    if spectra is not None:
            st.session_state["spectra"] = spectra.getvalue().decode("utf-8")
            
    if "spectra" in st.session_state:
                k=pd.read_csv(StringIO(st.session_state["spectra"]))
                options=("Show Visualization","Predict Sales")
                p1=st.selectbox("Choose",options)
                if(p1=="Show Visualization"):
                    graphs(k)
                    st.write(k) 
                elif(p1=="Predict Sales"):
                    train_data(k,True)      
                      
            
    # if spectra is None:
    #         st.error("Please upload valid csv files")        
            
        