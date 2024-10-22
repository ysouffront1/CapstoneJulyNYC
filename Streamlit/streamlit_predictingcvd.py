### import libraries

import pandas as pd
import streamlit as st
import joblib
import seaborn as sns 
import matplotlib.pyplot as plt 

[theme]
base="light"


# Initialize session state for page control
if 'page' not in st.session_state:
    st.session_state.page = 'intro'  # Default page is the introduction

# Function to navigate to assessment page
def go_to_assessment():
    st.session_state.page = 'assessment'  # Set the page to 'assessment'
    st.rerun() # rerun app immediately after page change


# function navigating back to intro page
def go_back_to_intro():
    st.session_state.page = 'intro'
    st.rerun() # rerun app to go to intro page


# Introduction page
def introduction_page():
    st.markdown("<h1 style='text-align: center; color:white;'> Welcome to the Cardiovascular Disease Risk Assessment</h1>",unsafe_allow_html=True)
    st.write("")
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image("https://cdn3.poz.com/40191_heart-stethoscope-is-000008477896.jpg_1201786e-eb3e-4db0-bc6b-d600b742cd12_x2.jpeg")
        st.write('')  

    #creating side by side layout

   # col1, col2 = st.columns(2)

    # Creating Intro container
    with st.container():
        st.markdown("<h2 style='text-align: center; color: white;'>Introduction </h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center, color: white;'>Cardiovascular disease (CVD) is one of the leading causes of death worldwide. This application aims to assess your risk for cardiovascular disease by asking a few questions related to demographic information and brief medical history. </h3>", unsafe_allow_html=True)


    # Creating directions container 

    with st.container():
        st.markdown("<h2 style='text-align: center; color: white;'>How Do I Use This? </h2>",unsafe_allow_html=True)
        st.write("""
        1. Click the "Begin Assessment" button below.
        2. Answer a few questions about your health, including age, height, weight, symptoms, and family history.
        3. After completing the assessment, the tool will display your estimated risk of cardiovascular disease.
        4. This result is for informational purposes only; consult a medical professional for further evaluation.
        
        Note: Individuals 19 and under are unable to participant in this assessment.
        """)

    # Create a "Begin Assessment" button in the center of the screen
    
    st.write('')  
    st.write('')  # Create some space

    col1, col2, col3 , col4, col5 = st.columns(5)

    with col1:
        pass

    with col2:
        pass
    with col4:
        pass
    with col5:
        pass
    with col3 :
        if st.button("Begin Assessment", key="begin"):
            go_to_assessment() 



# Risk assessment page
def assessment_page():

    # Title of the app
    st.title("Cardiovascular Disease Risk Assessment")

    # Quick description
    st.write('##### Below is a quick assessment that will determine whether or not you are at risk for cardiovascular disease.')

    st.write('')  
    # Add a "Back" button to return to the introduction page
    if st.button("Back to Introduction", key="back"):
        go_back_to_intro()  # Switch back to intro page
    st.write('')  


    #### Loading Models
    # Load saved models 

    rf_smoteenn_tuned = joblib.load('Streamlit/rf_smoteenn_tuned.pkl')
    #xgb_model_smoteenn_tuned = joblib.load('xgb_model_smoteenn_tuned.pkl')
    #xgb_model_adasyn_tuned = joblib.load('xgb_model_adasyn_tuned.pkl')


    # Check if model file is present before loading
    try:
        rf_smoteenn_tuned = joblib.load('Streamlit/rf_smoteenn_tuned.pkl')
    except FileNotFoundError:
        st.error("Model file not found. Make sure 'rf_smoteenn_tuned.pkl' is in the correct directory.")
        return  # Don't proceed if model is not found



    # Load the blending function
    def blended_model_predict(X):
        y_prob_rf = rf_smoteenn_tuned.predict_proba(X)[:, 1]
    # y_prob_xgb_smoteenn = xgb_model_smoteenn_tuned.predict_proba(X)[:, 1]
    # y_prob_xgb_adasyn = xgb_model_adasyn_tuned.predict_proba(X)[:, 1]

        # Average probabilities
        #y_prob_blended = (y_prob_rf + y_prob_xgb_smoteenn + y_prob_xgb_adasyn) / 3
        #return y_prob_blended
        return y_prob_rf

    def predict_risk(input_data):
        input_df = pd.DataFrame([input_data])
        model_columns = [
            'sex', 'age_bins_20-25', 'age_bins_26-30', 'age_bins_31-35',
            'age_bins_36-40', 'age_bins_41-45', 'age_bins_46-50', 'age_bins_51-55',
            'age_bins_56-60', 'age_bins_61-65', 'age_bins_66-70', 'age_bins_71-75',
            'age_bins_76-80', 'age_bins_81+', 'height_cm', 'weight_kg',
            'Education_College graduate or above',
            'Education_High school graduate/GED or equivalent',
            'Education_Less than 9th grade', 'Education_Some college or AA degree',
            'has_angina', 'has_family_history'
        ]
        input_df = input_df.reindex(columns=model_columns)
        y_prob_rf = blended_model_predict(input_df)
        return y_prob_rf


    # Function to get feature importances
    def get_feature_importances(model):
    # Assuming model is a RandomForest model
        importances = model.feature_importances_
        feature_names = model.feature_names_in_
        return pd.DataFrame({'Feature': feature_names, 'Importance': importances})


    # Function to display the feature importances
    def plot_feature_importances(image_path):
        # Display the image in Streamlit 
        st.image(image_path, use_column_width=True)



    def personalized_feedback(user_input,feature_importances):
        st.write("Here are the factors driving your cardiovascular risk:")

        # Compare the user's age input with the age bins
        age_bins = ['age_bins_20-25', 'age_bins_26-30', 'age_bins_31-35', 
                    'age_bins_36-40', 'age_bins_41-45', 'age_bins_46-50', 
                    'age_bins_51-55', 'age_bins_56-60', 'age_bins_61-65', 
                    'age_bins_66-70', 'age_bins_71-75', 'age_bins_76-80', 
                    'age_bins_81+']
        
    
             # Compare the user's age input with the age bins
        if user_input['age_bins_20-25'] == 1:
            st.write("- **Age**: You fall into the '20-25' age bin, which is considered a lower risk group.")
        elif user_input['age_bins_26-30'] == 1:
            st.write("- **Age**: You fall into the '26-30' age bin, which is considered a lower risk group.")
        elif user_input['age_bins_31-35'] == 1:
            st.write("- **Age**: You fall into the '31-35' age bin, which is considered a moderate risk group.")
        elif user_input['age_bins_36-40'] == 1:
            st.write("- **Age**: You fall into the '36-40' age bin, which is considered a moderate risk group.")
        elif user_input['age_bins_41-45'] == 1:
            st.write("- **Age**: You fall into the '41-45' age bin, which is considered a moderate risk group.")
        elif user_input['age_bins_46-50'] == 1:
            st.write("- **Age**: You fall into the '46-50' age bin, which is considered a moderate risk group.")
        elif user_input['age_bins_51-55'] == 1:
            st.write("- **Age**: You fall into the '51-55' age bin, which is considered a moderate risk group.")
        elif user_input['age_bins_56-60'] == 1:
            st.write("- **Age**: You fall into the '56-60' age bin, which is considered a **high** risk group.")
        elif user_input['age_bins_61-65'] == 1:
            st.write("- **Age**: You fall into the '61-65' age bin, which is considered a **high** risk group.")
        elif user_input['age_bins_66-70'] == 1:
            st.write("- **Age**: You fall into the '66-70' age bin, which is considered a **high** risk group.")
        elif user_input['age_bins_71-75'] == 1:
            st.write("- **Age**: You fall into the '71-75' age bin, which is considered a **high** risk group.")
        elif user_input['age_bins_76-80'] == 1:
            st.write("- **Age**: You fall into the '76-80' age bin, which is considered a **high** risk group.")
        elif user_input['age_bins_81+'] == 1:
            st.write("- **Age**: You fall into the '81+' age bin, which is considered a **high** risk group.")



        # Compare height and weight to general ranges (you can customize these further)
        if user_input['height_cm'] < 160:
            st.write("- **Height**: Your height is below average, which does not significantly impact your risk.")
        else:
            st.write("- **Height**: Your height is average or above, which does not significantly impact your risk.")

        if user_input['weight_kg'] > 80:
            st.write("- **Weight**: Your weight is above 80kg, which may contribute to a higher risk.")
        else:
            st.write("- **Weight**: Your weight is below 80kg, contributing to a lower risk.")

        # Compare the education level
        if user_input['Education_College graduate or above'] == 1:
            st.write("- **Education**: Your education level (College graduate or above) is associated with lower risk.")
        elif user_input['Education_High school graduate/GED or equivalent'] == 1:
            st.write("- **Education**: High school education is associated with moderate risk.")
        elif user_input['Education_Less than 9th grade'] == 1:
            st.write("- **Education**: Your less than 9th grade education is associated with moderate risk.")
        elif user_input['Education_Some college or AA degree'] == 1:
            st.write("- **Education**: Your some college or AA degree education is associated with moderate risk.")



        # Provide feedback on other important factors
        if user_input['has_angina'] == 1:
            st.write("- **Angina**: You reported experiencing frequent chest pain (angina), which is a significant risk factor.")
        
        if user_input['has_family_history'] == 1:
            st.write("- **Family History**: A family history of cardiovascular disease increases your risk.")

        # Display the sorted feature importances
        st.write("### Top 3 Most Important Features:")
        top_features = feature_importances.sort_values(by='Importance', ascending=False).head(3)
        st.write(top_features)


       

    # Threshold Slider
   # threshold = st.slider(
   #     'Select Probability Threshold:',
   #     min_value=0.1,
   #     max_value=0.8,
    #    value=0.3,  # Default value
    #    step=0.05
    #)

    # add drop down menu, "What's this?, show visual of precision recall graph"
    # add description of recall graph
 #   with st.expander("**What's This?**"):
 #       st.write("In this context, a higher threshold will increase precision but will decrease recall. Conversely, a lower threshold may improve recall at the cost of precision.")
 #       st.image('images/precision_recall_graph.png', caption='Precision and Recall Graph', use_column_width=True)
 #       st.write("""
 #    This graph illustrates the relationship between precision and recall at different threshold values. 
 #   - **Precision**: Precision is the proportion of true positive results out of all positive predictions made by the model. It answers the question, "Of all the cases the model predicted as positive, how many were actually positive?"
 #   - **Recall** (also known as Sensitivity): Recall is the proportion of actual positives correctly identified by the model. It answers the question, "Of all the actual positive cases, how many did the model correctly predict as positive?"

    
    ### Precision and Recall in Healthcare

   # In healthcare, especially when predicting cardiovascular disease, recall is often more important than precision. Here's why:
    
   # - **Early Disease Identification**: In cardiovascular disease detection, missing a potential positive case (i.e., a false negative) can lead to serious consequences, as individuals might not receive the early intervention or monitoring they need. High recall helps ensure that fewer cases of the disease are missed.
    
   # - **Early Disease Prevention**: The goal in healthcare is often to catch as many true positive cases as possible, even if it means casting a wider net and possibly including some false positives. With early prevention strategies in place, false positives can be further evaluated through additional testing, whereas a false negative could result in undiagnosed disease progression.
    
   # In this context, optimizing recall is critical because identifying those at risk of cardiovascular disease early can lead to preventive measures, which could save lives.
   # """)


    # Questionnaire for user input
    st.write('### Please fill out the following questions:')

    # Question 1: Sex
    sex = st.selectbox(
        'Sex:',
        ['Male', 'Female']
    )

    # Question 2: Age
    age_bin = st.selectbox('Select your age range (20+ Only):',
        ['20-25', '26-30', '31-35', '36-40', '41-45', '46-50', '51-55', '56-60', '61-65', '66-70', '71-75', '76-80', '81+'])


    # Convert age bins to binary features
    age_bins = {
        'age_bins_20-25': 1 if age_bin == '20-25' else 0,
        'age_bins_26-30': 1 if age_bin == '26-30' else 0,
        'age_bins_31-35': 1 if age_bin == '31-35' else 0,
        'age_bins_36-40': 1 if age_bin == '36-40' else 0,
        'age_bins_41-45': 1 if age_bin == '41-45' else 0,
        'age_bins_46-50': 1 if age_bin == '46-50' else 0,
        'age_bins_51-55': 1 if age_bin == '51-55' else 0,
        'age_bins_56-60': 1 if age_bin == '56-60' else 0,
        'age_bins_61-65': 1 if age_bin == '61-65' else 0,
        'age_bins_66-70': 1 if age_bin == '66-70' else 0,
        'age_bins_71-75': 1 if age_bin == '71-75' else 0,
        'age_bins_76-80': 1 if age_bin == '76-80' else 0,
        'age_bins_81+': 1 if age_bin == '81+' else 0,
    }


    #inserting function converting height from feet and inches to cm

    def convert_height_to_cm(feet, inches):
        return (feet * 30.48) + (inches * 2.54)

    # Function to convert weight from pounds to kg
    def convert_weight_to_kg(pounds):
        return pounds / 2.20462

    # Question 3: Height (cm)
   # height = st.number_input('Height (cm):', min_value=0, value=170)
    feet = st.number_input('Height (feet):', min_value=0, value=5)
    inches = st.number_input('Height (inches):', min_value=0, value=7)
    height_cm = convert_height_to_cm(feet, inches)


    # Question 4: Weight (kg)
   # weight = st.number_input('Weight (kg):', min_value=0, value=70)
    weight_pounds = st.number_input('Weight (lbs):', min_value=0, value=150)
    weight_kg = convert_weight_to_kg(weight_pounds)


    # Question 8: Education Level
    education = st.selectbox(
        'Education Level:',
        ['College graduate or above', 'High school graduate/GED or equivalent', 'Less than 9th grade', 'Some college or AA degree']
    )

    # Question 9: Do you have angina?
    has_angina = st.selectbox(
        'Do you have angina (frequent chest pain)?',
        ['Yes', 'No']
    )

    # Question 10: Do you have a family history of cardiovascular disease?
    has_family_history = st.selectbox(
        'Do you have a family history of cardiovascular disease?',
        ['Yes', 'No']
    )

 # Predict button
    if st.button('Predict'):
        # Create a dictionary of input data
        input_data = {
            'sex': 1 if sex == 'Male' else 0,
            'age_bins_20-25': 1 if age_bin == '20-25' else 0,
            'age_bins_26-30': 1 if age_bin == '26-30' else 0,
            'age_bins_31-35': 1 if age_bin == '31-35' else 0,
            'age_bins_36-40': 1 if age_bin == '36-40' else 0,
            'age_bins_41-45': 1 if age_bin == '41-45' else 0,
            'age_bins_46-50': 1 if age_bin == '46-50' else 0,
            'age_bins_51-55': 1 if age_bin == '51-55' else 0,
            'age_bins_56-60': 1 if age_bin == '56-60' else 0,
            'age_bins_61-65': 1 if age_bin == '61-65' else 0,
            'age_bins_66-70': 1 if age_bin == '66-70' else 0,
            'age_bins_71-75': 1 if age_bin == '71-75' else 0,
            'age_bins_76-80': 1 if age_bin == '76-80' else 0,
            'age_bins_81+': 1 if age_bin == '81+' else 0,
            'height_cm': height_cm,
            'weight_kg': weight_kg,
            'Education_College graduate or above': 1 if education == 'College graduate or above' else 0,
            'Education_High school graduate/GED or equivalent': 1 if education == 'High school graduate/GED or equivalent' else 0,
            'Education_Less than 9th grade': 1 if education == 'Less than 9th grade' else 0,
            'Education_Some college or AA degree': 1 if education == 'Some college or AA degree' else 0,
            'has_angina': 1 if has_angina == 'Yes' else 0,
            'has_family_history': 1 if has_family_history == 'Yes' else 0,
            
        }
        
        # Get the risk probability
        risk_probability = predict_risk(input_data)

        # Convert the risk probability to a percentage
        risk_percentage = risk_probability[0] * 100

        if risk_percentage >= 61:
            risk_classification = "High"
            risk_color = "red" #red for high risk 
           # st.markdown("<h4 style='text-align: left; color: white;'> The ML Model Predicts Your Risk to Be: </h2>", unsafe_allow_html=True)
           # st.write('')

        elif risk_percentage >= 41:
            risk_classification = "Moderate"
            risk_color = "orange"
        else:
            risk_classification = "Low" 
           # st.markdown("<h4 style='text-align: left; color: white;'> The ML Model Predicts Your Risk to Be: </h2>", unsafe_allow_html=True)
           # st.write('The ML Model Predicts Your Risk to Be:')
            #st.write('Low')
            risk_color = "green"
            
        
        feature_importances = get_feature_importances(rf_smoteenn_tuned)

        # Display the result as percentage
        st.markdown(f"<h4 style='text-align: left; color: {risk_color};'> The ML Model Predicts Your Risk to Be: {risk_classification} ({risk_percentage:.2f}%)</h2>", unsafe_allow_html=True)

       # plot_feature_importances()
        personalized_feedback(input_data,feature_importances)
        
        
        # Display age distribution image 
        st.image('Streamlit/images/age_distribution.png', caption='Age Distribution of People with and without CVD', use_column_width=True)


        #st.markdown("<h4 style='text-align: left; color: white;'> Your Risk of CVD is: </h2>", unsafe_allow_html=True)
        #st.write(f"{risk_percentage:.2f}%")


        

    st.write('Disclaimer: This app should not be a replacement for professional medical advice. Please consult with a doctor or healthcare provider for questions concerning your health. ')


 
   
# Switch between pages
if st.session_state.page == 'intro':
    introduction_page()  # Show intro page
elif st.session_state.page == 'assessment':
    assessment_page()  # Show assessment page

#######################################################################################################################################

# add a data load function that does all the preprocessing and connects the interactivity to the pre-processing
#@st.cache_data #doesn't rerun the script again (makes it faster), if run once before, skip and return what you did last time 
