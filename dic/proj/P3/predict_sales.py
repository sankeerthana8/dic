import streamlit as st
import pickle
import numpy as np
from PIL import Image
import datetime

model=pickle.load(open('saved_file.pkl','rb'))
  
def validate(a,b):
        if(b=="Item_Weight"):
                try:
                        a=float(a)
                except ValueError:        
                        st.error(f"please fill {b} in range 0-100")
                        return False
        elif(b=="Total_Items"):
                if not a.isnumeric():
                        st.error(f"please fill {b} with numerical values")
                        return False
        elif(b=="Item_Quantity"):
                
                if not a.isnumeric():
                        st.error(f"please fill {b} with numerical values")
                        return False
                                                
        elif(b=="Item_MRP"):
                if not a.isnumeric():
                        st.error(f"please fill {b} with numerical values")
                        return False
        elif(b=="Outlet_Establishment_Year"):
                if not a.isnumeric():
                        st.error(f"please fill {b} from 1950-{present_year.year()}")
                        return False
                if a.isnumeric():
                        present_year = datetime.datetime.now()
                        d=int(a)
                        if(d<1950 or d>present_year.year):
                                st.error(f"please fill {b} from 1950-{present_year.year}")
                                return False
                                
        return True       
                                               
                                      
def predict_sales(Item_Weight,Item_Quantity,Total_Items,Item_Type,Item_MRP,Outlet_Establishment_Year,Outlet_Type,outlet_location,Outlet_Size,model1):
    
    HouseHold_items=['Dairy','Baking Goods','Meat' ,'Breads','Starchy Foods','Breakfast','Fruits and Vegetables','Household','Seafood']
    Snack_Items=['Frozen Foods' , 'Canned','Snack Foods']
    Other_Items=['Soft Drinks' , 'Hard Drinks','Health and Hygiene','Others']

    dic_items={'HouseHold_items':0,'Snack_Items':1,'Other_Items':2}
    dic_loc_tpes={"Tier 1":0,"Tier 2":1,"Tier 3":2}
    dic_outlet_type={"Large-Sized-SuperMarket":0,"Small-Sized-SuperMarket":1,"Medium-Sized-SuperMarket":2,"Grocery-Store":3}

    Item_Weight=float(Item_Weight)
    Item_Quantity=float(Item_Quantity)
    Total_Items=float(Total_Items)
    Item_MRP=float(Item_MRP)
    Outlet_Establishment_Year = float(Outlet_Establishment_Year)
    Item_Visibility= Item_Quantity/Total_Items
    Item_type_encoded=0
    Outlet_type_small=0
    Outlet_type_Medium=0
    Outlet_type_Large=0
    Outlet_Establishment_Year=2022-Outlet_Establishment_Year
    
    
    if Item_Type in HouseHold_items:
            Item_type_encoded=dic_items['HouseHold_items']
    elif Item_Type in Snack_Items:
            Item_type_encoded=dic_items['Snack_Items']
    elif Item_Type in Other_Items:
            Item_type_encoded=dic_items['Other_Items'] 
            
    outlet_type_encoded=dic_outlet_type[Outlet_Type]
    outlet_location_encoded=dic_loc_tpes[outlet_location]  
             
    if(Outlet_Size=="Large"):
            Outlet_type_small=0
            Outlet_type_Medium=0
            Outlet_type_Large=1

    if(Outlet_Size=="Small"):
            Outlet_type_small=1
            Outlet_type_Medium=0
            Outlet_type_Large=0
            
    if(Outlet_Size=="Medium"):
            Outlet_type_small=0
            Outlet_type_Medium=1
            Outlet_type_Large=0
                                     
    input=np.array([[Item_Weight,Item_Visibility,Item_type_encoded,Item_MRP,Outlet_Establishment_Year,outlet_location_encoded,outlet_type_encoded,Outlet_type_Large,Outlet_type_Medium,Outlet_type_small]]).astype(np.float64)
    prediction=0
    if(len(model1)!=0):
        #     st.write("hurray new one")
            prediction=model1.predict(input)
    else:
        #     st.write("yupp using old one")
            prediction=model.predict(input)
                    
            
    pred='{0:.{1}f}'.format(prediction[0],2)
    return float(pred)

                    
def main_page(model):            
    html_temp = """
    <div style="background-color:#025246 ;padding:10px">
    <h2 style="color:white;text-align:center;">Sales Prediction App </h2>
    </div>
    """
    if(len(model)==0):
            st.markdown(html_temp, unsafe_allow_html=True)
            st.markdown('#')
            image = Image.open('Logo.jpg')
            col1, col2, col3 = st.columns([1,6,1])
            with col1:
              st.write("")
            with col2:
                     st.image(image)

            with col3:
                    st.write("")
       
            
    Item_types=("Dairy","Baking Goods","Meat" ,"Breads",
                "Starchy Foods","Breakfast","Fruits and Vegetables",
                "Household","Seafood" , "Frozen Foods" , "Canned",
                "Snack Foods","Soft Drinks" , "Hard Drinks",
                "Health and Hygiene","Others")
    
    outlet_size_options=("Large","Small", "Medium")
    outlet_type_options=("Large-Sized-SuperMarket","Small-Sized-SuperMarket","Medium-Sized-SuperMarket","Grocery-Store")
    
    outlet_location_options=("Tier 1","Tier 2","Tier 3")
    
    Item_Weight = st.text_input("Item_Weight",key="item_weight")
    if(Item_Weight):
            validate(Item_Weight,"Item_Weight")
    Total_Items = st.text_input("Total Items in the Store",key="item_total")
    if(Total_Items):
            validate(Total_Items,"Total_Items")        
    Item_Quantity=st.text_input("Items Quantites in the Store",key="item_quantity")
    if(Item_Quantity):
            validate(Total_Items,"Item_Quantity")  
    Item_Type =  st.selectbox("Item_Type",Item_types,index=1) 
    Item_MRP= st.text_input("Item_MRP",key="item_mrp")
    if(Item_MRP):
            validate(Item_MRP,"Item_MRP")
    Outlet_Establishment_Year=st.text_input("Outlet_Establishment_year",key="year")
    if(Outlet_Establishment_Year):
            validate(Outlet_Establishment_Year,"Outlet_Establishment_Year") 
    Outlet_Type = st.selectbox("Outlet_Type",outlet_type_options)
    outlet_location=st.selectbox("Outlet_Location",outlet_location_options)
    Outlet_Size= st.selectbox("Outlet_Size",outlet_size_options)
    
    button_click=st.button("Predict") 
      
    if button_click:
        if(validate(Item_Weight,"item weight") and validate(Total_Items,"Total_Items") and validate(Total_Items,"Item_Quantity") and  validate(Item_MRP,"Item_MRP") and validate(Outlet_Establishment_Year,"Outlet_Establishment_Year")):
                    output=predict_sales(Item_Weight,Item_Quantity,Total_Items,Item_Type,Item_MRP,Outlet_Establishment_Year,Outlet_Type,outlet_location,Outlet_Size,model)
                    st.success('The Expected number of sales are {}'.format(output))
        