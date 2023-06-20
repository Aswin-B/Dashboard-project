import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Data
df = pd.read_csv('./notebooks/processed_data.csv')

# Display the dataframe
# st.dataframe(df, use_container_width=True)

# Configuration
st.set_page_config(page_title='Diabetes Dashboard', layout='wide')

st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    #padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

# sidebar

with st.sidebar:
    st.header('Controls')

    # Filter for Gender

    gender = st.radio(label='Select Gender', options=['Male', 'Female', 'Both'],
                      index=2, horizontal=True)

    gender_n = []

    if gender == 'Male':

        gender_n.append('Male')

    elif gender == 'Female':

        gender_n.append('Female')

    else:

        gender_n.append('Male')
        gender_n.append('Female')

    # st.write(gender_n)

    # Applying the user selected gender options from the original data frame (df)

    filter_gender = df.loc[df['gender'].isin(gender_n)]

    # -------------------------------------------------------------------------------------------

    # st.subheader('Filter for Age Categories')

    # Filter for age category

    ages = ['[0-10)', '[10-20)', '[20-30)', '[30-40)', '[40-50)', '[50-60)', '[60-70)',
            '[70-80)', '[80-90)', '[90-100)']

    age_option = st.radio(label='Select Age Category', options=['All', 'Range'], index=0, horizontal=True)

    if age_option == 'All':

        filter_age = df.loc[df['age'].isin(ages)]

        df_g = filter_gender[filter_gender['age'].isin(ages)]

    else:

        age_cat = st.multiselect(label='Choose Age Category Range', options=ages, default=ages)

        filter_age = df.loc[df['age'].isin(age_cat)]

        df_g = filter_gender[filter_gender['age'].isin(age_cat)]

    # --------------------------------------------------------------------------------------

    # Filter for Patient stays

    # st.subheader('Filter for Number of Days Patient stays')

    time_min = int(filter_age['time_in_hospital'].min())

    time_max = int(filter_age['time_in_hospital'].max())

    days = st.slider(label='Select the Number of Days',
                     min_value=time_min, max_value=time_max, value=(time_min, time_max))

    filter_days = filter_age[(filter_age['time_in_hospital'] >= days[0]) & (filter_age['time_in_hospital'] <= days[1])]

    # --------------------------------------------------------------------------------------------------

    # Download Button

    if (gender_n[0] == 'Male') & (len(gender_n) == 1):

        final = filter_days[filter_days['gender'] == 'Male']

    elif (gender_n[0] == 'Female') & (len(gender_n) == 1):

        final = filter_days[filter_days['gender'] == 'Female']

    else:

        final = filter_days.copy()

    st.write('Download Data')

    st.download_button(label='Download filtered data', data=final.to_csv(),
                       file_name='filtered_data.csv')

    # --------------------------------------------------------------------------------------------------

# Main window

df = filter_days.copy()

# Title

st.title('Diabetes Dashboard')

col_met = st.columns(6)

if (gender_n[0] == 'Male') & (len(gender_n) == 1):

    with col_met[0]:

        # Getting the male count using the gender_n which contains male
        st.metric(label='Male', value=df[df['gender'] == 'Male']['gender'].count())

    with col_met[1]:
        st.metric(label='Admission types', value=7)

    with col_met[2]:
        st.metric(label='Discharge types', value=25)

    with col_met[3]:
        st.metric(label='Admission sources', value=17)

    with col_met[4]:
        # Getting the unique value in time in hospital and passed to a variable time

        time = df['time_in_hospital'].unique()

        # Checks for the length of time list > 1, then apply min and max range

        if len(time) > 1:

            st.metric(label='Stayed', value=f"{time.min()} to {time.max()}")

        # checks if the length = 1, then display the value in the list

        else:

            st.metric(label='Stayed', value=f"{time[0]}")

elif (gender_n[0] == 'Female') & (len(gender_n) == 1):

    with col_met[0]:
        # Getting the female count using the gender_n which contains female
        st.metric(label='Female', value=df[df['gender'] == 'Female']['gender'].count())

    with col_met[1]:
        st.metric(label='Admission types', value=7)

    with col_met[2]:
        st.metric(label='Discharge types', value=25)

    with col_met[3]:
        st.metric(label='Admission sources', value=17)

    with col_met[4]:
        # Getting the unique value in time in hospital and passed to a variable time

        time = df['time_in_hospital'].unique()

        # Checks for the length of time list > 1, then apply min and max range

        if len(time) > 1:

            st.metric(label='Stayed', value=f"{time.min()} to {time.max()}")

        # checks if the length = 1, then display the value in the list

        else:

            st.metric(label='Stayed', value=f"{time[0]}")

elif (gender_n[0] == 'Male') & (gender_n[1] == 'Female') & (len(gender_n) == 2):

    with col_met[0]:
        # Getting the male count using the gender_n which contains male
        st.metric(label='Male', value=df[df['gender'] == 'Male']['gender'].count())

    with col_met[1]:
        # Getting the female count using the gender_n which contains female
        st.metric(label='Female', value=df[df['gender'] == 'Female']['gender'].count())

    with col_met[2]:
        st.metric(label='Admission types', value=7)

    with col_met[3]:
        st.metric(label='Discharge types', value=25)

    with col_met[4]:
        st.metric(label='Admission sources', value=17)

    with col_met[5]:
        # Getting the unique value in time in hospital and passed to a variable time

        time = df['time_in_hospital'].unique()

        # Checks for the length of time list > 1, then apply min and max range

        if len(time) > 1:

            st.metric(label='Stayed', value=f"{time.min()} to {time.max()}")

        # checks if the length = 1, then display the value in the list

        else:

            st.metric(label='Stayed', value=f"{time[0]}")

    # with col_met[5]:
    #     st.metric(label='Drugs', value=23)

# Tab layout

tab1, tab2 = st.tabs(["General Category", "Test and Drugs"])

with tab1:
    # Filter for Patient stays

    # st.subheader('Filter for Number of Days Patient stays')

    # 1st row with 4 columns
    columns = st.columns(4)

    # -------------------------------------------------------------------
    # Pie chart for male and female patients

    # Getting the value counts for the gender from the overall data
    comp = df['gender'].value_counts()

    with columns[0]:
        st.subheader('Gender')

        fig = plt.figure(figsize=(5, 5), facecolor='#2A2953')
        ax = fig.add_subplot()

        # Plotting line
        ax.pie(comp, autopct='%1.1f%%', explode=np.repeat(0.01, len(comp)),
               colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

        # setting title
        # ax.set_title('Composition of Male and Female Patients')

        legend = ax.legend(comp.index, loc=(0.23, -0.1), ncol=2, facecolor='#2A2953')

        for i in legend.get_texts():
            i.set_color('w')

        st.write(fig)
    # ----------------------------------------------------------------------------

    # Pie chart for admission types

    # Getting the value counts for the admission type id
    admission = df['admission_type_id'].value_counts()

    # Getting first 3 values
    ft = admission[:3]

    # Getting the sum for the last three values inorder to make as others category to a series named others
    others = pd.Series(admission[3:].sum())

    # Renaming the others series index value
    others = others.rename(index={0: 'Others'})

    # concatenating the ft series with others series to a new series named admission_new
    admission_new = pd.concat([ft, others])
    admission_new = admission_new.sort_values(ascending=False)

    with columns[1]:
        st.subheader('Admission types')

        # Applying the if the gender_n = male and length = 1

        if (gender_n[0] == 'Male') & (len(gender_n) == 1):

            # Getting the value counts for the df contains only male
            # and contains the selected admission types

            admission_male = df.loc[(df['gender'] == 'Male') &
                                    (df['admission_type_id'].isin(admission.index))][
                'admission_type_id'].value_counts()

            # Getting first 3 values
            ft = admission_male[:3]

            # Getting the sum for the last three values inorder to make as others category to a series named others
            others = pd.Series(admission_male[3:].sum())

            # Renaming the others series index value
            others = others.rename(index={0: 'Others'})

            # concatenating the ft series with others series to a new series named admission_new
            admission_male_new = pd.concat([ft, others])
            admission_male_new = admission_male_new.sort_values(ascending=False)

            fig = plt.figure(facecolor='#2A2953')
            ax = fig.add_subplot()

            # Plotting line
            ax.pie(admission_male_new, autopct='%1.1f%%', explode=np.repeat(0.01, len(admission_male_new)),
                   colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            # Setting title
            # ax.set_title('Number of Patients visited among in each Admission types')

            # setting legend
            legend = ax.legend(admission_male_new.index, loc=(0.17, -0.1), ncol=2, facecolor='#2A2953')

            for i in legend.get_texts():
                i.set_color('w')

            st.write(fig)

        # Applying the if the gender_n = female and length = 1

        elif (gender_n[0] == 'Female') & (len(gender_n) == 1):

            # Getting the value counts for the df contains only female
            # and contains the selected admission types

            admission_female = df.loc[(df['gender'] == 'Female') &
                                      (df['admission_type_id'].isin(admission.index))][
                'admission_type_id'].value_counts()

            # Getting first 3 values
            ft = admission_female[:3]

            # Getting the sum for the last three values inorder to make as others category to a series named others
            others = pd.Series(admission_female[3:].sum())

            # Renaming the others series index value
            others = others.rename(index={0: 'Others'})

            # concatenating the ft series with others series to a new series named admission_new
            admission_female_new = pd.concat([ft, others])
            admission_female_new = admission_female_new.sort_values(ascending=False)

            fig = plt.figure(facecolor='#2A2953')
            ax = fig.add_subplot()

            # Plotting line
            ax.pie(admission_female_new, autopct='%1.1f%%', explode=np.repeat(0.01, len(admission_female_new)),
                   colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            # Setting title
            # ax.set_title('Number of Patients visited among in each Admission types')

            # setting legend
            legend = ax.legend(admission_female_new.index, loc=(0.17, -0.1), ncol=2, facecolor='#2A2953')

            for i in legend.get_texts():
                i.set_color('w')

            st.write(fig)

        # This is for both category - if the gender_n contains male and female and length = 2

        elif (gender_n[0] == 'Male') & (gender_n[1] == 'Female') & (len(gender_n) == 2):

            fig = plt.figure(facecolor='#2A2953')
            ax = fig.add_subplot()

            # Plotting line
            ax.pie(admission_new, autopct='%1.1f%%', explode=np.repeat(0.01, len(admission_new)),
                   colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            # Setting title
            # ax.set_title('Number of Patients visited among in each Admission types')

            # setting legend
            legend = ax.legend(admission_new.index, loc=(0.17, -0.1), ncol=2, facecolor='#2A2953')

            for i in legend.get_texts():
                i.set_color('w')

            st.write(fig)

    # ------------------------------------------------------------------------------------

    # Paired-Bar chart for age category

    # Getting the value counts for the ages and sorted
    age_cat = df['age'].value_counts().sort_index()

    # Getting the index value of the ages
    age_index = np.array(age_cat.index)

    # Getting the age category for the males and getting the value counts for its age index
    # and sorting the values to display the age category in order
    age_male = df.loc[(df['gender'] == 'Male') &
                      (df['age'].isin(age_index))]['age'].value_counts().sort_index()

    # Getting the age category for the females and getting the value counts for its age index
    age_female = df.loc[(df['gender'] == 'Female') &
                        (df['age'].isin(age_index))]['age'].value_counts().sort_index()

    with columns[2]:
        st.subheader('Age Category')

        # Applying for the age category if the gender_n contains male and length of gender_n = 1

        if (gender_n[0] == 'Male') & (len(gender_n) == 1):

            fig = plt.figure(figsize=(6, 6.6), facecolor='#2A2953')
            ax = fig.add_subplot(facecolor='#2A2953')

            # plotting line
            ax.bar(age_male.index, age_male, color='#53C9F2', edgecolor='k')

            # setting title
            # ax.set_title('The most frequent admission source types')

            # setting ticks
            ax.set_xticks(range(len(age_male)))
            ax.set_xticklabels(age_male.index, rotation=90)
            ax.tick_params(axis='x', colors='w')
            ax.tick_params(axis='y', colors='w')

            # setting labels
            ax.set_xlabel('Age Category', labelpad=10, fontdict={'color': 'w'})
            ax.set_ylabel('Number of Patients', labelpad=10, fontdict={'color': 'w'})

            st.write(fig)

        # Applying for the age category if the gender_n contains female and length of gender_n = 1

        elif (gender_n[0] == 'Female') & (len(gender_n) == 1):

            fig = plt.figure(figsize=(6, 6.6), facecolor='#2A2953')
            ax = fig.add_subplot(facecolor='#2A2953')

            # plotting line
            ax.bar(age_female.index, age_female, color='#53C9F2', edgecolor='k')

            # setting title
            # ax.set_title('The most frequent admission source types')

            # setting ticks
            ax.set_xticks(range(len(age_female)))
            ax.set_xticklabels(age_female.index, rotation=90)
            ax.tick_params(axis='x', colors='w')
            ax.tick_params(axis='y', colors='w')

            # setting labels
            ax.set_xlabel('Age Category', labelpad=10, fontdict={'color': 'w'})
            ax.set_ylabel('Number of Patients', labelpad=10, fontdict={'color': 'w'})

            st.write(fig)

        # Applying for the age category if the gender_n contains male and female
        # and length of gender_n = 2

        elif (gender_n[0] == 'Male') & (gender_n[1] == 'Female') & (len(gender_n) == 2):

            # Applying if the length of age_male != age_index
            # and assigning that category to zero
            # This is done for plotting paired bar plot
            # ex: age_male = 4, age_index = 5 and age_female = 5

            if (len(age_male) != len(age_index)) & (len(age_female) == len(age_index)):

                # identifying the category in age_male not in age_index using for loop
                # and assigning to zero

                for i in age_index:

                    if i not in age_male.index:
                        missing_age_male = pd.Series(0)

                missing_age_male.rename(index={0: i})

                age_male = pd.concat([missing_age_male, age_male])

            # Applying if the length of age_male != age_index
            # and assigning that category to zero
            # This is done for plotting paired bar plot

            if (len(age_female) != len(age_index)) & (len(age_male) == len(age_index)):

                # identifying the category in age_female not in age_index using for loop
                # and assigning to zero

                for j in age_index:

                    if j not in age_female.index:
                        missing_age_female = pd.Series(0)

                missing_age_female.rename(index={0: j})

                age_female = pd.concat([missing_age_female, age_female])

            fig = plt.figure(figsize=(5, 5.4), facecolor='#2A2953')
            ax = fig.add_subplot(facecolor='#2A2953')

            x = np.arange(1, len(age_cat) + 1)

            # Plotting line
            ax.bar(x - 0.1, age_male, width=0.2, label='Male', color='#53C9F2', edgecolor='k')
            ax.bar(x + 0.1, age_female, width=0.2, label='Female', color='#55D047', edgecolor='k')

            # Setting title
            # ax.set_title('Number of Visited Patients in each Age category')

            # setting labels
            ax.set_xlabel('Age Category', labelpad=10, fontdict={'color': 'w'})
            ax.set_ylabel('Number of Patients', labelpad=10, fontdict={'color': 'w'})

            # setting ticks
            ax.set_xticks(range(1, len(age_cat) + 1))
            ax.set_xticklabels(age_index, rotation=90)
            ax.tick_params(axis='x', colors='w')
            ax.tick_params(axis='y', colors='w')

            # setting legend
            legend = ax.legend(facecolor='#2A2953')

            for i in legend.get_texts():
                i.set_color('w')

            st.write(fig)

    # -------------------------------------------------------------------------

    # Bar chart for medical specialty

    # Removing the ? values in the medical specialty column and getting the value counts for the remaining value
    specialty = df.loc[df['medical_specialty'] != '?']['medical_specialty']

    # Getting the top 5 value counts for the created specialty series
    specialty_sort = specialty.value_counts()[:5]

    with columns[3]:
        st.subheader('Medical Specialty')

        # Applying for the top medical specialty from the df and the gender_n = male

        if (gender_n[0] == 'Male') & (len(gender_n) == 1):

            spec_male = df[(df['gender'] == 'Male') &
                           df['medical_specialty'].isin(specialty_sort.index)]['medical_specialty'].value_counts()

            fig = plt.figure(figsize=(6, 5.2), facecolor='#2A2953')
            ax = fig.add_subplot(facecolor='#2A2953')

            # Plotting line
            ax.bar(spec_male.index, spec_male, color='#53C9F2', edgecolor='k')

            # setting title
            # ax.set_title('Top medical speciality of the admitting Physician')

            # setting labels
            ax.set_xlabel('Medical speciality', labelpad=10, fontdict={'color': 'w'})
            ax.set_ylabel('Number of Patients', labelpad=10, fontdict={'color': 'w'})

            # setting ticks
            ax.set_xticks(range(len(spec_male.index)))
            ax.set_xticklabels(spec_male.index, rotation=90)
            ax.tick_params(axis='x', colors='w')
            ax.tick_params(axis='y', colors='w')

            st.write(fig)

        # Applying for the top medical specialty from the df and the gender_n = female

        elif (gender_n[0] == 'Female') & (len(gender_n) == 1):

            spec_female = df[(df['gender'] == 'Female') &
                             df['medical_specialty'].isin(specialty_sort.index)]['medical_specialty'].value_counts()

            fig = plt.figure(figsize=(6, 5.2), facecolor='#2A2953')
            ax = fig.add_subplot(facecolor='#2A2953')

            # Plotting line
            ax.bar(spec_female.index, spec_female, color='#53C9F2', edgecolor='k')

            # setting title
            # ax.set_title('Top medical speciality of the admitting Physician')

            # setting labels
            ax.set_xlabel('Medical speciality', labelpad=10, fontdict={'color': 'w'})
            ax.set_ylabel('Number of Patients', labelpad=10, fontdict={'color': 'w'})

            # setting ticks
            ax.set_xticks(range(len(spec_female.index)))
            ax.set_xticklabels(spec_female.index, rotation=90)
            ax.tick_params(axis='x', colors='w')
            ax.tick_params(axis='y', colors='w')

            st.write(fig)

        # Applying for the top medical specialty from the df and the gender_n = male and female

        elif (gender_n[0] == 'Male') & (gender_n[1] == 'Female') & (len(gender_n) == 2):

            fig = plt.figure(figsize=(6, 5.2), facecolor='#2A2953')
            ax = fig.add_subplot(facecolor='#2A2953')

            # Plotting line
            ax.bar(specialty_sort.index, specialty_sort, color='#53C9F2', edgecolor='k')

            # setting title
            # ax.set_title('Top medical speciality of the admitting Physician')

            # setting labels
            ax.set_xlabel('Medical speciality', labelpad=10, fontdict={'color': 'w'})
            ax.set_ylabel('Number of Patients', labelpad=10, fontdict={'color': 'w'})

            # setting ticks
            ax.set_xticks(range(len(specialty_sort.index)))
            ax.set_xticklabels(specialty_sort.index, rotation=90)
            ax.tick_params(axis='x', colors='w')
            ax.tick_params(axis='y', colors='w')

            st.write(fig)

    # --------------------------------------------------------------------------------
    # 2nd row with 4 columns
    columns = st.columns(4)

    # Pie chart for discharge types

    # Getting the top 5 discharge disposition id
    discharge = df['discharge_disposition_id_new'].value_counts()[:5]

    tt_dis = discharge[:3]

    others_discharge = pd.Series(discharge[3:].sum())

    others_discharge = others_discharge.rename(index={0: 'Others'})

    dis = pd.concat([tt_dis, others_discharge])

    dis = dis.sort_values(ascending=False)

    # d_term = ['Home', 'SNF', 'Home with health service', 'Short term hospital', 'Rehab fac']

    with columns[0]:
        st.subheader('Discharge types')

        # Applying for the top discharge type from the df and the gender_n = male

        if (gender_n[0] == 'Male') & (len(gender_n) == 1):

            discharge_male = df[(df['gender'] == 'Male') &
                                (df['discharge_disposition_id_new'].isin(discharge.index))][
                                 'discharge_disposition_id_new'].value_counts()[:5]

            tt_dis = discharge_male[:3]

            others_discharge = pd.Series(discharge_male[3:].sum())

            others_discharge = others_discharge.rename(index={0: 'Others'})

            dis_male = pd.concat([tt_dis, others_discharge])

            dis_male = dis_male.sort_values(ascending=False)

            fig = plt.figure(figsize=(6, 4.7), facecolor='#2A2953')
            ax = fig.add_subplot()

            # plotting line
            ax.pie(dis_male, autopct='%1.1f%%', explode=np.repeat(0.01, len(dis)),
                   colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            # setting title
            # ax.set_title('The most frequent discharge types')

            # setting legend
            legend = ax.legend(dis_male.index, loc=(0.25, -0.06), ncol=2, facecolor='#2A2953')

            for i in legend.get_texts():
                i.set_color('w')

            st.write(fig)

        # Applying for the top discharge type from the df and the gender_n = female

        elif (gender_n[0] == 'Female') & (len(gender_n) == 1):

            discharge_female = df[(df['gender'] == 'Female') &
                                  (df['discharge_disposition_id_new'].isin(discharge.index))][
                                   'discharge_disposition_id_new'].value_counts()[:5]

            tt_dis = discharge_female[:3]

            others_discharge = pd.Series(discharge_female[3:].sum())

            others_discharge = others_discharge.rename(index={0: 'Others'})

            dis_female = pd.concat([tt_dis, others_discharge])

            dis_female = dis_female.sort_values(ascending=False)

            fig = plt.figure(figsize=(6, 4.7), facecolor='#2A2953')
            ax = fig.add_subplot()

            # plotting line
            ax.pie(dis_female, autopct='%1.1f%%', explode=np.repeat(0.01, len(dis)),
                   colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            # setting title
            # ax.set_title('The most frequent discharge types')

            # setting legend
            legend = ax.legend(dis_female.index, loc=(0.25, -0.06), ncol=2, facecolor='#2A2953')

            for i in legend.get_texts():
                i.set_color('w')

            st.write(fig)

        # Applying for the top discharge type from the df and the gender_n = male and female

        elif (gender_n[0] == 'Male') & (gender_n[1] == 'Female') & (len(gender_n) == 2):

            fig = plt.figure(figsize=(6, 4.7), facecolor='#2A2953')
            ax = fig.add_subplot()

            # plotting line
            ax.pie(dis, autopct='%1.1f%%', explode=np.repeat(0.01, len(dis)),
                   colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            # setting title
            # ax.set_title('The most frequent discharge types')

            # setting legend
            legend = ax.legend(dis.index, loc=(0.25, -0.06), ncol=2, facecolor='#2A2953')

            for i in legend.get_texts():
                i.set_color('w')

            st.write(fig)

    # -------------------------------------------------------------------------------

    # Pie chart for readmission

    # Getting the value counts for the readmitted
    readmitted = df['readmitted_new'].value_counts()

    # readmitted_values = ['NO', '>30 Days', '<30Days']

    with columns[1]:
        st.subheader('Readmission')

        # Applying for the readmission from the df and the gender_n = male

        if (gender_n[0] == 'Male') & (len(gender_n) == 1):

            readmitted_male = df[(df['gender'] == 'Male') &
                                 df['readmitted_new'].isin(readmitted.index)]['readmitted_new'].value_counts()

            fig = plt.figure(facecolor='#2A2953')
            ax = fig.add_subplot()

            # plotting line
            ax.pie(readmitted_male, autopct='%1.1f%%', explode=np.repeat(0.01, len(readmitted_male)),
                   colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            # setting title
            # ax.set_title('The Percentage composition of readmission of the visited patients''')

            legend = ax.legend(readmitted_male.index, loc=(0.05, -0.05), ncol=3, facecolor='#2A2953')

            for i in legend.get_texts():
                i.set_color('w')

            st.write(fig)

        # Applying for the readmission from the df and the gender_n = male

        elif (gender_n[0] == 'Female') & (len(gender_n) == 1):

            readmitted_female = df[(df['gender'] == 'Female') &
                                   df['readmitted_new'].isin(readmitted.index)]['readmitted_new'].value_counts()

            fig = plt.figure(facecolor='#2A2953')
            ax = fig.add_subplot()

            # plotting line
            ax.pie(readmitted_female, autopct='%1.1f%%', explode=np.repeat(0.01, len(readmitted_female)),
                   colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            # setting title
            # ax.set_title('The Percentage composition of readmission of the visited patients''')

            legend = ax.legend(readmitted_female.index, loc=(0.05, -0.05), ncol=3, facecolor='#2A2953')

            for i in legend.get_texts():
                i.set_color('w')

            st.write(fig)

        # Applying for the readmission from the df and the gender_n = male and female

        elif (gender_n[0] == 'Male') & (gender_n[1] == 'Female') & (len(gender_n) == 2):

            fig = plt.figure(facecolor='#2A2953')
            ax = fig.add_subplot()

            # plotting line
            ax.pie(readmitted, autopct='%1.1f%%', explode=np.repeat(0.01, len(readmitted)),
                   colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            # setting title
            # ax.set_title('The Percentage composition of readmission of the visited patients''')

            legend = ax.legend(readmitted.index, loc=(0.05, -0.05), ncol=3, facecolor='#2A2953')

            for i in legend.get_texts():
                i.set_color('w')

            st.write(fig)

    # -----------------------------------------------------------------------------------------------------------

    # Paired-bar chart for admission sources

    with columns[2]:
        st.subheader('Admission sources')

        # Getting the top 5 admission source id
        ad = df['admission_source_id_new'].value_counts()[:5]

        # Getting the index value of the top 5 admission source id
        ad_index = np.array(ad.index)

        # Getting the top 5 admission source id with its count for the male patients
        # it will display the bar plot in maximum to minimum
        male_ad = df.loc[(df['gender'] == 'Male') &
                         (df['admission_source_id_new'].isin(ad_index))][
            'admission_source_id_new'].value_counts()

        # Getting the top 5 admission source id with its for the female patients
        female_ad = df.loc[(df['gender'] == 'Female') &
                           (df['admission_source_id_new'].isin(ad_index))][
            'admission_source_id_new'].value_counts()

        # checking the gender_n = male and plotting for the top 5 male_ad

        if (gender_n[0] == 'Male') & (len(gender_n) == 1):

            fig = plt.figure(figsize=(6, 6.6), facecolor='#2A2953')
            ax = fig.add_subplot(facecolor='#2A2953')

            # plotting line
            ax.bar(male_ad.index, male_ad, color='#53C9F2', edgecolor='k')

            # setting title
            # ax.set_title('The most frequent admission source types')

            # setting ticks
            ax.set_xticks(range(len(male_ad)))
            ax.set_xticklabels(male_ad.index, rotation=90)
            ax.tick_params(axis='x', colors='w')
            ax.tick_params(axis='y', colors='w')

            # setting labels
            ax.set_xlabel('Admission source types', fontdict={'color': 'w'})
            ax.set_ylabel('Number of Patients', fontdict={'color': 'w'})

            st.write(fig)

        # checking the gender_n = female and plotting for the top 5 female_ad

        elif (gender_n[0] == 'Female') & (len(gender_n) == 1):
            fig = plt.figure(figsize=(6, 6.6), facecolor='#2A2953')
            ax = fig.add_subplot(facecolor='#2A2953')

            # plotting line
            ax.bar(female_ad.index, female_ad, color='#53C9F2', edgecolor='k')

            # setting title
            # ax.set_title('The most frequent admission source types')

            # setting ticks
            ax.set_xticks(range(len(female_ad)))
            ax.set_xticklabels(female_ad.index, rotation=90)
            ax.tick_params(axis='x', colors='w')
            ax.tick_params(axis='y', colors='w')

            # setting labels
            ax.set_xlabel('Admission source types', fontdict={'color': 'w'})
            ax.set_ylabel('Number of Patients', fontdict={'color': 'w'})

            st.write(fig)

        # checking the gender_n = male and female

        elif (gender_n[0] == 'Male') & (gender_n[1] == 'Female') & (len(gender_n) == 2):

            # Getting the top 5 admission source id
            addm = df['admission_source_id_new'].value_counts()[:5].sort_index()

            # Getting the index value of the top 5 admission source id
            addm_index = np.array(addm.index)

            # Getting the top 5 admission source id with its count for the male patients
            male_addm = df.loc[(df['gender'] == 'Male') & (df['admission_source_id_new'].isin(addm_index))][
                'admission_source_id_new'].value_counts().sort_index()

            # Getting the top 5 admission source id with its for the female patients
            female_addm = df.loc[(df['gender'] == 'Female') & (df['admission_source_id_new'].isin(addm_index))][
                'admission_source_id_new'].value_counts().sort_index()

            # checking if the length of male_addm != addm_index and length of female_addm != addm_index
            # ex: male_addm = 3, add_index = 5
            # female_addm = 4, add_index = 5

            if (len(male_addm) != len(addm_index)) & (len(female_addm) != len(addm_index)):

                missing_addm_male = pd.Series([])

                for i in addm_index:

                    if i not in male_addm.index:
                        missing_addm_male = missing_addm_male.append(pd.Series(0))

                        missing_addm_male = missing_addm_male.rename(index={0: i})

                male_addm_new = pd.concat([missing_addm_male, male_addm]).sort_values()
                # getting the appropriate male_addm_new with all values,
                # if no value for category it applies zero

            # checking if the length of male_addm != addm_index and length of female_addm != addm_index
            # ex: male_addm = 3, add_index = 5
            # female_addm = 4, add_index = 5

            if (len(female_addm) != len(addm_index)) & (len(male_addm) != len(addm_index)):

                missing_addm_female = pd.Series([])

                for i in addm_index:

                    if i not in female_addm.index:
                        missing_addm_female = missing_addm_female.append(pd.Series(0))

                        missing_addm_female = missing_addm_female.rename(index={0: i})

                female_addm_new = pd.concat([missing_addm_female, female_addm]).sort_values()

                male_addm = male_addm_new
                female_addm = female_addm_new
                # Then male_addm_new and female_addm_new passed to male_addm
                # and female_addm for plotting paired bar plot.
                # If this 2 condition is true, then we get the corrected male_addm and female_addm

            # checking if the length of male_addm != addm_index and length of female_addm = addm_index
            # ex: male_addm = 4, add_index = 5
            # female_addm = 5, add_index = 5

            if (len(male_addm) != len(addm_index)) & (len(female_addm) == len(addm_index)):

                missing_addm_male = pd.Series([])

                for i in addm_index:

                    if i not in male_addm.index:
                        missing_addm_male = missing_addm_male.append(pd.Series(0))

                        missing_addm_male.rename(index={0: i})

                male_addm = pd.concat([missing_addm_male, male_addm])

            if (len(male_addm) != len(addm_index)) & (len(female_addm) == len(addm_index)):

                missing_addm_male = pd.Series([])

                for i in addm_index:

                    if i not in male_addm.index:
                        missing_addm_male = missing_addm_male.append(pd.Series(0))

                        missing_addm_male.rename(index={0: i})

                male_addm = pd.concat([missing_addm_male, male_addm])

            # checking if the length of male_addm = addm_index and length of female_addm != addm_index
            # ex: male_addm = 5, add_index = 5
            # female_addm = 4, add_index = 5

            if (len(female_addm) != len(addm_index)) & (len(male_addm) == len(addm_index)):

                missing_addm_female = pd.Series([])

                for j in addm_index:

                    if j not in female_addm.index:
                        missing_addm_female = missing_addm_female.append(pd.Series(0))

                        missing_addm_female.rename(index={0: j})

                female_addm = pd.concat([missing_addm_female, female_addm])

            fig = plt.figure(figsize=(6, 6.6), facecolor='#2A2953')
            ax = fig.add_subplot(facecolor='#2A2953')

            x = np.arange(1, len(addm) + 1)
            # plotting line
            ax.bar(x - 0.1, male_addm, width=0.2, label='Male', color='#53C9F2', edgecolor='k')
            ax.bar(x + 0.1, female_addm, width=0.2, label='Female', color='#55D047', edgecolor='k')

            # setting title
            # ax.set_title('The most frequent admission source types')

            # setting ticks
            ax.set_xticks(range(1, len(male_addm) + 1))
            ax.set_xticklabels(male_addm.index, rotation=90)
            ax.tick_params(axis='x', colors='w')
            ax.tick_params(axis='y', colors='w')

            # setting labels
            ax.set_xlabel('Admission source types', fontdict={'color': 'w'})
            ax.set_ylabel('Number of Patients', fontdict={'color': 'w'})

            # Setting legend
            legend = ax.legend(facecolor='#2A2953')

            for i in legend.get_texts():
                i.set_color('w')

            st.write(fig)

    # ---------------------------------------------------------------------------------

    # Paired-bar chart for time in hospital

    # Getting the time in hospital value for the male patients and getting the
    # value counts to a series named time_male
    time_male = df.loc[df['gender'] == 'Male']['time_in_hospital'].value_counts()

    # sorted the index values in the time_male
    time_male = time_male.sort_index()

    # Getting the time in hospital value for the female patients and getting the
    # value counts to a series named time_female
    time_female = df.loc[df['gender'] == 'Female']['time_in_hospital'].value_counts()

    # sorted the index values in the time_female
    time_female = time_female.sort_index()

    with columns[3]:
        st.subheader('Patients stayed')

        # Applying for the time in hospital from the df and gender_n = male

        if (gender_n[0] == 'Male') & (len(gender_n) == 1):

            fig = plt.figure(figsize=(6, 6.6), facecolor='#2A2953')
            ax = fig.add_subplot(facecolor='#2A2953')

            # plotting line
            ax.bar(time_male.index, time_male, color='#53C9F2', edgecolor='k')

            # setting title
            # ax.set_title('The most frequent admission source types')

            # setting ticks
            ax.set_xticks(np.array(time_male.index))
            ax.set_xticklabels(time_male.index)
            ax.tick_params(axis='x', colors='w')
            ax.tick_params(axis='y', colors='w')

            # setting labels
            ax.set_xlabel('Number of Days', fontdict={'color': 'w'})
            ax.set_ylabel('Number of Patients', fontdict={'color': 'w'})

            st.write(fig)

        # Applying for the time in hospital and gender_n = female

        elif (gender_n[0] == 'Female') & (len(gender_n) == 1):
            fig = plt.figure(figsize=(6, 6.6), facecolor='#2A2953')
            ax = fig.add_subplot(facecolor='#2A2953')

            # plotting line
            ax.bar(time_female.index, time_female, color='#53C9F2', edgecolor='k')

            # setting title
            # ax.set_title('The most frequent admission source types')

            # setting ticks
            ax.set_xticks(np.array(time_female.index))
            ax.set_xticklabels(time_female.index)
            ax.tick_params(axis='x', colors='w')
            ax.tick_params(axis='y', colors='w')

            # setting labels
            ax.set_xlabel('Number of Days', fontdict={'color': 'w'})
            ax.set_ylabel('Number of Patients', fontdict={'color': 'w'})

            st.write(fig)

        # Applying for the time in hospital and gender_n = male and female

        elif (gender_n[0] == 'Male') & (gender_n[1] == 'Female') & (len(gender_n) == 2):

            fig = plt.figure(figsize=(6, 6.8), facecolor='#2A2953')
            ax = fig.add_subplot(facecolor='#2A2953')

            x = np.arange(1, len(time_male) + 1)

            # plotting line
            ax.bar(x - 0.1, time_male, width=0.2, label='Male', color='#53C9F2', edgecolor='k')
            ax.bar(x + 0.1, time_female, width=0.2, label='Female', color='#55D047', edgecolor='k')

            # setting ticks
            ax.set_xticks(range(1, len(time_male) + 1))
            ax.set_xticklabels(time_male.index)
            ax.tick_params(axis='x', colors='w')
            ax.tick_params(axis='y', colors='w')

            # setting labels
            ax.set_xlabel('Number of Days', fontdict={'color': 'w'})
            ax.set_ylabel('Number of Patients', fontdict={'color': 'w'})

            # setting title
            # ax.set_title('The total number of Patients stayed for 1 to 14 days')

            # setting legend
            legend = ax.legend(facecolor='#2A2953')

            for i in legend.get_texts():
                i.set_color('w')

            st.write(fig)

    # ------------------------------------------------------------------------------------------------------

with tab2:

    # 2nd row with 3 columns
    columns = st.columns(3)

    # --------------------------------------------------------------------------------------------------------
    # Pie chart for glucose serum test

    with columns[0]:

        st.subheader('Glucose Serum test')

        max_glu_serum = df_g.loc[df_g['max_glu_serum_new'] != 'None']['max_glu_serum_new'].value_counts()

        fig = plt.figure(facecolor='#2A2953')
        ax = fig.add_subplot()

        # plotting line
        glu = ax.pie(max_glu_serum, labels=max_glu_serum.index, autopct='%1.1f%%',
                     explode=np.repeat(0.01, len(max_glu_serum)),
                     colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

        for i in glu[1]:
            i.set_color('w')

        # setting title
        # ax.set_title('The composition of maximum Glucose Serum test conducted for the visited patients')

        st.write(fig)

    # --------------------------------------------------------------------------------------------------------
    # Pie chart for A1C result

    with columns[1]:
        st.subheader('A1C test result')

        a1c_result = df_g.loc[df_g['A1Cresult_new'] != 'None']['A1Cresult_new'].value_counts()

        fig = plt.figure(figsize=(8, 5.5), facecolor='#2A2953')
        ax = fig.add_subplot()

        # plotting line
        a1c = ax.pie(a1c_result, labels=a1c_result.index, autopct='%1.1f%%',
                     explode=np.repeat(0.01, len(a1c_result)),
                     colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

        for i in a1c[1]:
            i.set_color('w')

        # setting title
        # ax.set_title('The composition of A1C test conducted for the visited patients')

        st.write(fig)

    # -----------------------------------------------------------------------------------------------------

    # 2nd row with 1 column

    # columns = st.columns(1)

    drugs = ['metformin', 'repaglinide', 'nateglinide', 'chlorpropamide', 'glimepiride', 'glipizide', 'glyburide',
             'pioglitazone', 'rosiglitazone', 'acarbose', 'miglitol', 'tolazamide',
             'insulin', 'glyburide-metformin']

    columns_n = st.columns(3)

    with columns_n[0]:
        pass

    with columns_n[1]:
        pass

    with columns_n[2]:

        drug = st.selectbox(label='Select the Prescribed Drug', options=drugs)

    with columns[2]:

        st.subheader('Drug Dosage levels')

        if drug == 'metformin':

            # Pie chart for Metformin

            metformin = df_g.loc[df_g['metformin'] != 'No']['metformin'].value_counts()

            # st.write('Metformin')

            fig = plt.figure(figsize=(8, 7), facecolor='#2A2953')
            ax = fig.add_subplot()

            # plotting line

            met = ax.pie(metformin, labels=metformin.index, autopct='%1.1f%%',
                         colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            for i in met[1]:
                i.set_color('w')

            # setting title
            # ax.set_title('The composition of Dosage levels prescribed to the patients')

            st.write(fig)

        # ---------------------------------------------------------------------------------------------

        elif drug == 'repaglinide':

            # Pie chart for repaglinide

            repaglinide = df_g.loc[df_g['repaglinide'] != 'No']['repaglinide'].value_counts()

            # st.write('Repaglinide')

            fig = plt.figure(figsize=(8, 6.5), facecolor='#2A2953')
            ax = fig.add_subplot()

            # plotting line

            rep = ax.pie(repaglinide, labels=repaglinide.index, autopct='%1.1f%%',
                         colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            for i in rep[1]:
                i.set_color('w')

            # setting title
            # ax.set_title('The composition of Dosage levels prescribed to the patients')

            st.write(fig)

        # -----------------------------------------------------------------------------------------

        elif drug == 'nateglinide':

            # Pie chart for Nateglinide

            nateglinide = df_g.loc[df_g['nateglinide'] != 'No']['nateglinide'].value_counts()

            # st.write('Nateglinide')

            fig = plt.figure(figsize=(8, 7.3), facecolor='#2A2953')
            ax = fig.add_subplot()

            # plotting line

            nat = ax.pie(nateglinide, labels=nateglinide.index, autopct='%1.1f%%',
                         colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            for i in nat[1]:
                i.set_color('w')

            # setting title
            # ax.set_title('The composition of Dosage levels prescribed to the patients')

            st.write(fig)

        # --------------------------------------------------------------------------------------------

        elif drug == 'chlorpropamide':

            # Pie chart for Chlorpropamide

            chlorpropamide = df_g.loc[df_g['chlorpropamide'] != 'No']['chlorpropamide'].value_counts()

            # st.write('Chlorpropamide')

            fig = plt.figure(figsize=(8, 7), facecolor='#2A2953')
            ax = fig.add_subplot()

            # plotting line

            chl = ax.pie(chlorpropamide, labels=chlorpropamide.index, autopct='%1.1f%%',
                         colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            for i in chl[1]:
                i.set_color('w')

            # setting title
            # ax.set_title('The composition of Dosage levels prescribed to the patients')

            st.write(fig)

        # ----------------------------------------------------------------------------------------------

        elif drug == 'glimepiride':

            # Pie chart for Glimepiride

            glimepiride = df_g.loc[df_g['glimepiride'] != 'No']['glimepiride'].value_counts()

            # st.write('Glimepiride')

            fig = plt.figure(figsize=(8, 6.5), facecolor='#2A2953')
            ax = fig.add_subplot()

            # plotting line

            glim = ax.pie(glimepiride, labels=glimepiride.index, autopct='%1.1f%%',
                          colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            for i in glim[1]:
                i.set_color('w')

            # setting title
            # ax.set_title('The composition of Dosage levels prescribed to the patients')

            st.write(fig)

        # ---------------------------------------------------------------------------------------------------

        elif drug == 'glipizide':

            # Pie chart for Glipizide

            glipizide = df_g.loc[df_g['glipizide'] != 'No']['glipizide'].value_counts()

            # st.write('Glipizide')

            fig = plt.figure(figsize=(8, 6.5), facecolor='#2A2953')
            ax = fig.add_subplot()

            # plotting line

            glip = ax.pie(glipizide, labels=glipizide.index, autopct='%1.1f%%',
                          colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            for i in glip[1]:
                i.set_color('w')

            # setting title
            # ax.set_title('The composition of Dosage levels prescribed to the patients')

            st.write(fig)

        # --------------------------------------------------------------------------------------

        elif drug == 'glyburide':

            # Pie chart for Glyburide

            # st.write('Glyburide')

            glyburide = df_g.loc[df_g['glyburide'] != 'No']['glyburide'].value_counts()

            fig = plt.figure(figsize=(8, 6), facecolor='#2A2953')
            ax = fig.add_subplot()

            # plotting line

            gly = ax.pie(glyburide, labels=glyburide.index, autopct='%1.1f%%',
                         colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            for i in gly[1]:
                i.set_color('w')

            # setting title
            # ax.set_title('The composition of Dosage levels prescribed to the patients')

            st.write(fig)

        # ----------------------------------------------------------------------------------------------

        elif drug == 'pioglitazone':

            # Pie chart for Pioglitazone

            # st.write('Pioglitazone')

            pioglitazone = df_g.loc[df_g['pioglitazone'] != 'No']['pioglitazone'].value_counts()

            fig = plt.figure(figsize=(8, 7.3), facecolor='#2A2953')
            ax = fig.add_subplot()

            # plotting line

            piog = ax.pie(pioglitazone, labels=pioglitazone.index, autopct='%1.1f%%',
                          colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            for i in piog[1]:
                i.set_color('w')

            # setting title
            # ax.set_title('The composition of Dosage levels prescribed to the patients')

            st.write(fig)

        # ----------------------------------------------------------------------------------------------

        elif drug == 'rosiglitazone':

            # Pie chart for Rosiglitazone

            # st.write('Rosiglitazone')

            rosiglitazone = df_g.loc[df_g['rosiglitazone'] != 'No']['rosiglitazone'].value_counts()

            fig = plt.figure(figsize=(8, 7.2), facecolor='#2A2953')
            ax = fig.add_subplot()

            # plotting line

            ros = ax.pie(rosiglitazone, labels=rosiglitazone.index, autopct='%1.1f%%',
                         colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            for i in ros[1]:
                i.set_color('w')

            # setting title
            # ax.set_title('The composition of Dosage levels prescribed to the patients')

            st.write(fig)

        # --------------------------------------------------------------------------------------------

        elif drug == 'acarbose':

            # Pie chart for Acarbose

            # st.write('Acarbose')

            acarbose = df_g.loc[df_g['acarbose'] != 'No']['acarbose'].value_counts()

            fig = plt.figure(figsize=(8, 7.3), facecolor='#2A2953')
            ax = fig.add_subplot()

            # plotting line

            acar = ax.pie(acarbose, labels=acarbose.index, autopct='%1.1f%%',
                          colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            for i in acar[1]:
                i.set_color('w')

            # setting title
            # ax.set_title('The composition of Dosage levels prescribed to the patients')

            st.write(fig)

        # ---------------------------------------------------------------------------------------------

        elif drug == 'miglitol':

            # Pie chart for Miglitol

            # st.write('Miglitol')

            miglitol = df_g.loc[df_g['miglitol'] != 'No']['miglitol'].value_counts()

            fig = plt.figure(figsize=(9, 5), facecolor='#2A2953')
            ax = fig.add_subplot()

            # plotting line

            mig = ax.pie(miglitol, labels=miglitol.index, autopct='%1.1f%%',
                         colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            for i in mig[1]:
                i.set_color('w')

            # setting title
            # ax.set_title('The composition of Dosage levels prescribed to the patients')

            st.write(fig)

        # ------------------------------------------------------------------------------------------------

        elif drug == 'tolazamide':

            # Pie chart for Tolazamide

            # st.write('Tolazamide')

            tolazamide = df_g.loc[df_g['tolazamide'] != 'No']['tolazamide'].value_counts()

            fig = plt.figure(figsize=(8, 7), facecolor='#2A2953')
            ax = fig.add_subplot()

            # plotting line

            tol = ax.pie(tolazamide, labels=tolazamide.index, autopct='%1.1f%%',
                         colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            for i in tol[1]:
                i.set_color('w')

            # setting title
            # ax.set_title('The composition of Dosage levels prescribed to the patients')

            st.write(fig)

        # --------------------------------------------------------------------------------------------

        elif drug == 'insulin':

            # Pie chart for Insulin

            # st.write('Insulin')

            insulin = df_g.loc[df_g['insulin'] != 'No']['insulin'].value_counts()

            fig = plt.figure(figsize=(8, 7), facecolor='#2A2953')
            ax = fig.add_subplot()

            # plotting line

            ins = ax.pie(insulin, labels=insulin.index, autopct='%1.1f%%',
                         colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            for i in ins[1]:
                i.set_color('w')

            # setting title
            # ax.set_title('The composition of Dosage levels prescribed to the patients')

            st.write(fig)

        # --------------------------------------------------------------------------------------------

        else:

            # Pie chart for Glyburide_metformin

            # st.write('Glyburide-metformin')

            glyburide_metformin = df_g.loc[df_g['glyburide-metformin'] != 'No']['glyburide-metformin'].value_counts()

            fig = plt.figure(figsize=(8, 7.7), facecolor='#2A2953')
            ax = fig.add_subplot()

            # plotting line

            gly_met = ax.pie(glyburide_metformin, labels=glyburide_metformin.index, autopct='%1.1f%%',
                             colors=['#53C9F2', '#55D047', '#E9E82B', '#F74331', '#7E8178'])

            for i in gly_met[1]:
                i.set_color('w')

            # setting title
            # ax.set_title('The composition of Dosage levels prescribed to the patients')

            st.write(fig)

        # -------------------------------------------------------------------------------------------------------

# Citation
# Beata Strack, Jonathan P. DeShazo, Chris Gennings, Juan L. Olmo, Sebastian Ventura, Krzysztof J. Cios, John N. Clore,
# "Impact of HbA1c Measurement on Hospital Readmission Rates: Analysis of 70,000 Clinical Database Patient Records",
# BioMed Research International, vol. 2014,
# Article ID 781670, 11 pages, 2014. https://doi.org/10.1155/2014/781670

