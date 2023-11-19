import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import seaborn as sns

model1=pickle.load(open('saved_file.pkl','rb'))



def encode_data(df):
    df['Item_Type']=df['Item_Type'].replace(to_replace =['Dairy','Baking Goods','Meat' ,'Breads',
                                                     'Starchy Foods','Breakfast','Fruits and Vegetables','Household'] ,
                                        value = 'Household_Items')

    df['Item_Type']=df['Item_Type'].replace(to_replace =['Seafood' , 'Frozen Foods' , 'Canned','Snack Foods'] ,
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

@st.cache       
def train_data(df):
    
       
    
    
#     data = df.groupby(["Item_Outlet_Sales"])["Outlet_Location_Type"]
#     st.bar_chart(data)
    data = df['Item_Type'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.write("""ALL ITEMS OF FOOD""")

    st.pyplot(fig1)
    
    
    data = df['Outlet_Location_Type'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.write("""ALL LOCATIONS""")

    st.pyplot(fig1)
    
    
    df=encode_data(df)
    X=df.drop(['Item_Outlet_Sales'],axis=1)
    Y=df['Item_Outlet_Sales']
    X = np.array(X)
    Y = np.array(Y)
    X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,random_state=2)
    model1.fit(X_train,Y_train)
    
   
#     data = df["Item_Weight"].values
#     st.write("this is item weight ")
#     st.write(data)
#     columns=[data,df['Item_Weight']]
    fig=plt.figure()
    df["Item_Weight"].value_counts().plot(kind="area")
    st.pyplot(fig)
    
    # fig=plt.figure()
    # sns.countplot(df["Item_Outlet_Sales"])
    # st.pyplot(fig)
    # .value_counts().plot(kind="kde")
    # st.bar_chart(df['Item_Outlet_Sales'],width=30)
    sns.displot(df['Item_MRP'], color='g',kde=True)
    st.write("You can now Predict with your dataset",model1)
   
#     fig1, ax1 = plt.subplots()
#     ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
#     ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
#     st.write("""#### Number of Data from different countries""")
#     st.pyplot(fig1)
    # st.area_chart(columns)
    
    



# train_df = df[df['source'] == 'train']
# test_df = df[df['source'] == 'test']

# print(X.head())


#     model.fit()
    
    
    





def explore_analysis_page():
    st.title("Exploration of Sales")
    html_temp = """
    <div style="background-color:#025246 ;padding:10px">
    <h2 style="color:white;text-align:center;">Exploration of Sales </h2>
    </div>
    """
    spectra = st.file_uploader("upload file", type={"csv", "txt"})
    if spectra is not None:
            spectra_df = pd.read_csv(spectra)
            train_data(spectra_df) 
            st.write(spectra_df)
            
    else:
            st.error("Please upload valid csv files")        
            
        