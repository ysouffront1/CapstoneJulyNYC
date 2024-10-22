# Cardiovascular Disease Risk Prediction Using NHANES 2013-2014 Data
### Project Overview
This project leverages data from the 2013-2014 CDC NHANES (National Health and Nutrition Examination Survey) dataset to create a predictive model that assesses the cardiovascular risk of individuals aged 20 and above. The primary goal is to develop a practical cardiovascular risk assessment tool that uses only demographic data, such as age, cardiovascular history, symptoms, and education level, as input. This tool is deployed through a Streamlit web application.

### Dataset Source
The dataset used in this project was sourced from [Kaggle](https://www.kaggle.com/datasets/cdc/national-health-and-nutrition-examination-survey/data), which includes the following sub-datasets:

- Demographics
- Diet
- Examination
- Labs
- Medications
- Questionnaire
  
The focus was on demographic factors for the final model, but the broader dataset provides comprehensive health information on the survey participants.

## Project Motivation
### Problem Area
Heart disease is the leading cause of death in the United States and globally, affecting men, women, and individuals of various ethnic backgrounds. Early detection of cardiovascular risk can help prevent the onset of heart disease, reduce mortality rates, and improve population health. This project aims to create a machine learning model capable of predicting cardiovascular disease (CVD) risk based on simple, non-invasive demographic factors.

### The Impact
Reducing cardiovascular disease-related deaths has profound societal and economic benefits:

__Healthier Workforce__: A healthier population leads to increased productivity and reduced sick days.

__Lower Healthcare Costs__: Early intervention can reduce the need for expensive treatments.

__Global Relevance__: Though the dataset pertains to the U.S., insights and models can be generalized or adapted to other countries with similar health challenges.

### Data Used
The NHANES dataset provides rich information about the health of participants, segmented into various categories. For this project, we utilized:

__Demographic Data__: Age, sex, education level, marital status

__Questionnaire__: Cardiovascular history, smoking habits, and symptoms

__Examination Data__: Height, weight, and blood pressure

### Dataset Descriptions:
__Demographic__: Holds basic demographic information of survey participants, such as age, sex, education level, and income.

__Questionnaire__: Contains responses about medical history, smoking habits, dietary behavior, and family-level information.

__Labs__: Blood and urine test results, including cholesterol, blood glucose, and other metabolic markers.

__Diet__: Detailed dietary intake information of participants.

__Examination__: Physical examination results, including BMI, height, waist circumference, and blood pressure.

## Methodology
### Approach
The following process was done during this project:
1. Data Cleaning
2. Data Preprocessing
3. Modeling
4. Model Evaluation 

### Data Cleaning
1. __Imputation:__  Missing values were imputed using the mean, median or random imputation from observed column values.
2. __Re-encode Features:__ All features had to be re-encoded and one hot encoded prior to the modeling phase for better feature interpretation. 
3. __Rename Features:__ All features were renamed in each dataset, and a dictionary was used to map the SEQN or respondent number to each dataset to ensure the same respondents were present all throughout the datasets. 

### Data Preprocessing
1. __Feature Selection:__ Respondent gender, age, height, weight, education level, cardiovascular illness symptoms, and family history were prioritized in this project.
2. __Feature Engineering:__ Age bins were created to handle class imbalance, as well as additional features such as "has_angina" and "has_family_history" as Cardiovascular Disease Indicators, and "have_cvd", derived from the one hot encoded features of cardiovascular disease conditions (congestive_heart_failure_Yes, coronary_heart_disease_Yes, heart_attack_Yes, stroke_Yes) as those who already have CVD. 

### Modeling 

The project employs machine learning techniques to predict whether a participant is at risk of cardiovascular disease (CVD) based on the available demographic and cardiovascular symptom data. The following models were evaluated:

1. __Logistic Regression__

2. __Random Forest__

3. __XGBoost__

4. __Ensemble Methods__

### Model Evaluation

#### Final Model
After testing various models, the Random Forest algorithm was chosen for its superior performance in terms of accuracy and balance of precision/recall. The model is optimized using techniques like hyperparameter tuning, SMOTE-ENN sampling and Random Sampling to handle class imbalances.

#### Performance Metrics
The performance of the model was evaluated using:

- __Accuracy__
- __Precision__
- __Recall__
- __F1-Score__

The __Streamlit__ app allows users to input demographic data and assess their cardiovascular risk based on the model’s predictions.

## Streamlit App
The cardiovascular risk prediction model has been deployed as a web application using [Streamlit](https://predictingcvdquestionnaire.streamlit.app/). Users can input simple demographic information such as age, sex, cardiovascular history, education, and symptoms to receive a cardiovascular risk assessment.

### Installation Instructions

To run the app locally:

1. Clone this repository:
   ```
   git clone https://github.com/your-repo/cvd-risk-assessment.git
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the Streamlit app:
   ```
   streamlit run app.py
   ```
The application features:

__User Input Fields__: Age, sex, cardiovascular history, education level, smoking history, etc.

__Prediction Output__: Displays the predicted risk of cardiovascular disease.

## Future Work
This project can be further improved by:

__Expanding Input Features:__ Incorporating additional clinical and lab data to improve prediction accuracy.

__Testing Other Models:__ Exploring deep learning methods like neural networks to enhance predictive performance.

__Generalization:__ Applying the model to different populations to test its robustness across diverse demographic groups.

### Conclusion
By utilizing machine learning models on publicly available health data, this project demonstrates the potential of predictive analytics in the early detection of cardiovascular disease risk. The deployed Streamlit app makes it easy for users to input their data and receive actionable insights regarding their cardiovascular health.

##
Feel free to contribute to this project or raise any issues through GitHub.

## License
This project is licensed under the MIT License.

##
This README provides an overview of the project, instructions for running the app, and additional context for users and contributors. Let me know if you'd like to add or modify any sections!
