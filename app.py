import streamlit as st
import numpy as np
import pandas as pd
import pickle
from PIL import Image

st.title('Potential Customer Identifier')

st.write('created by Abraham Leung')

st.sidebar.write('''
Business Value:\n
This software can estimate whether a customer is a high income individial\n
So companies can specify their business strategies towards these target customers
''')

with st.sidebar.beta_expander('Definition'):
    st.write('''
    "Potential Customer Identifier" is a machine learning classification application.\n
    The dataset that used to train the algorithm was extracted by Barry Becker from the 1994 US Census database.\n
    As a result, it mainly focuses on customers in USA.\n
    "Potential Customer" is defined as a customer with over 50,000USD annual income.\n
    Model metrics:\n
    Sensitivity(Recall): 88%\n
    ''')
    
st.sidebar.write('''
-------------------------\n
Contact:
''')

linkedin1, linkedin2 = st.sidebar.beta_columns([1,4])

with linkedin1:
    image1 = Image.open('image\linkedin_logo.png')
    st.image(image1, width=30)

with linkedin2:
    link1 = "[Abraham's LinkedIn](https://www.linkedin.com/in/abraham-leung-data-science)"
    st.markdown(link1, unsafe_allow_html=True)

github1, github2 = st.sidebar.beta_columns([1,4])

with github1:
    image2 = Image.open('image\github_logo.png')
    st.image(image2, width=30)

with github2:
    link2 = "[Abraham's GitHub](https://github.com/yatfungleung)"
    st.markdown(link2, unsafe_allow_html=True)

# link2 = '[GitHub](https://github.com/yatfungleung)'
# st.sidebar.markdown(link2, unsafe_allow_html=True)


# load model
file_name = 'decision_tree_model.pkl'
with open(file_name, 'rb') as file:
    model = pickle.load(file)

# data list for users to select
hours_per_week_list = list(range(100))
workclass_list = [
    'State-gov', 'Self-emp-not-inc', 'Private', 'Federal-gov',
    'Local-gov', 'Self-emp-inc', 'Without-pay', 'Never-worked'
]
occupation_list = [
    'Adm-clerical', 'Exec-managerial', 'Handlers-cleaners', 'Prof-specialty',
    'Other-service', 'Sales', 'Craft-repair', 'Transport-moving',
    'Farming-fishing', 'Machine-op-inspct', 'Tech-support', 'Protective-serv',
    'Armed-Forces', 'Priv-house-serv'
]
education_list = [
    'Bachelors', 'HS-grad', '11th', 'Masters',
    '9th', 'Some-college', 'Assoc-acdm', 'Assoc-voc',
    '7th-8th', 'Doctorate', 'Prof-school', '5th-6th',
    '10th', '1st-4th', 'Preschool', '12th'
]
race_list = ['White', 'Black', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other']
marital_status_list = [
    'Never-married', 'Married-civ-spouse', 'Divorced', 'Married-spouse-absent',
    'Separated', 'Married-AF-spouse', 'Widowed'
]
relationship_list = [
    'Not-in-family', 'Husband', 'Wife', 'Own-child',
    'Unmarried', 'Other-relative'
]
sex_list = ['Female', 'Male']
age_list = list(range(17,81))
capital_change_list = [
    'Capital Gain (>50,000 USD)',
    'Capital Gain (<=50,000 USD)',
    'No Capital Change',
    'Capital Loss']
native_country_list = [
    'United-States', 'Cuba', 'Jamaica', 'India', 'Mexico', 'South',
    'Puerto-Rico', 'Honduras', 'England', 'Canada', 'Germany', 'Iran',
    'Philippines', 'Italy', 'Poland', 'Columbia', 'Cambodia',
    'Thailand', 'Ecuador', 'Laos', 'Taiwan', 'Haiti', 'Portugal',
    'Dominican-Republic', 'El-Salvador', 'France', 'Guatemala',
    'China', 'Japan', 'Yugoslavia', 'Peru',
    'Outlying-US(Guam-USVI-etc)', 'Scotland', 'Trinadad&Tobago',
    'Greece', 'Nicaragua', 'Vietnam', 'Hong', 'Ireland', 'Hungary',
    'Holand-Netherlands'
]

st.write('\n')

customer_details = st.beta_expander('customer details', expanded=True)

with customer_details:
    with st.form(key='my_form'):
        info = st.beta_columns(3)

        with info[0]:
            hours_per_week = st.selectbox('Hours per Week:', hours_per_week_list)
            workclass = st.selectbox('Working Class:', workclass_list)
            occupation = st.selectbox('Occupation:', occupation_list)
            education = st.selectbox('Education Level:', education_list)

        with info[1]:
            race = st.selectbox('Race:', race_list)
            marital_status = st.selectbox('Marital Status:', marital_status_list)
            relationship = st.selectbox('Position within Family:', relationship_list)
            sex = st.selectbox('Sex:', sex_list)

        with info[2]:
            age = st.selectbox('Age:', age_list)
            native_country = st.selectbox('Native Country:', native_country_list)
            capital_change = st.selectbox('Capital Change* in Last Year:', capital_change_list)
            st.write('*"Capital Change" means irregular cash flow, for example: inheritance, company liquidation, etc')

        submit_button = st.form_submit_button(label='Submit')

# education encoder
def educ_encoder(x):
    if x in ['Doctorate']:
        return 4
    elif x in ['Masters', 'Prof-school']:
        return 3
    elif x in ['Bachelors']:
        return 2
    elif x in ['Some-college', 'Assoc-voc', 'Assoc-acdm']:
        return 1
    else:
        return 0

education = educ_encoder(education)

# capital change encoder
def capital_change_encoder(x):
    if x in ['Capital Gain (>50,000 USD)']:
        return 'equal to 99999'
    elif x in ['Capital Gain (<=50,000 USD)']:
        return 'between 0 and 50K'
    elif x in ['No Capital Change']:
        return 'equal to 0'
    else:
        return 'between -50K and 0'

capital_change = capital_change_encoder(capital_change)

# new instance
new = [[
    age, workclass, education, marital_status, occupation,
    relationship, race, sex, capital_change, hours_per_week,
    native_country
]]

df_new = pd.DataFrame(np.array(new), columns=['age', 'workclass', 'education', 'marital_status', 'occupation',
       'relationship', 'race', 'sex', 'capital_change', 'hours_per_week',
       'native_country'])

# prediction by the trained model
prediction = model.predict(df_new)

result = {
    0: 'This is NOT a Potential Customer!',
    1: 'This IS a Potential Customer!'
    
}

st.write('\n')
st.write('\n')
st.write('According Our Classifier, ')
st.title(result[prediction.tolist()[0]])