
# libs
import streamlit as st
#from streamlit_tags import st_tags
import pandas as pd
import numpy as np
from numpy import mean
import requests


# intro
st.title('HUJI COURSES TIPS, by Yedidya Harris')

# paths
csv_file = 'tips.csv'

# convert gsheet to xlsx

csv_file = 'tips.csv'
URL = "https://docs.google.com/spreadsheets/d/1ohwGQIrCYEP0ptWq5UmIkMaBxhJjrKqNijecAoFoWr8/gviz/tq?tqx=out:csv&sheet=Form%20responses%201" # url to the gsheet
response = requests.get(URL)
open(csv_file, "wb").write(response.content)

# reading our csv file
df = pd.read_csv(csv_file)
df.columns = ['TIMESTAMP', 'Course Number', 'Course Name', 'Year', 'Lecture Tips', 'Project Tips', 'Excersize Classes', 'Summary', 'Exams', 'More Tips', 'Pros and Cons', 'Grade'] # To English
df.fillna('', inplace=True)

# Print value according to col
def printValues(df, title, col_name):
  html_str = f'**<div dir="rtl">{title}</div>**' # print title of values
  st.markdown(html_str, unsafe_allow_html=True) # print title of values
  
  # print the values together for each question
  for value in df[col_name].values:
    if type(value) == str: # check that it is not the grade
      if len(value) > 0: # make sure that that it is not empty
        # print course name only once 
        if col_name == 'Course Name':      
          html_str = f'<div dir="rtl">{value}</div>'
          st.markdown(html_str, unsafe_allow_html=True)
          break #break, to get only 1 course name
          
        # if it's not the course name, rather the other questions  
        else:
            html_str = f'<div dir="rtl">{value}</div>'
            st.markdown(html_str, unsafe_allow_html=True)
            
    # if it's the grade columns
    elif type(value) == float:
      if len(str(value)) > 0: # meaning that there is a value for the grade
         # print the average of the grades that were entered (average of all years)
         grade_average = pd.to_numeric(df[col_name], errors='coerce').mean()
         html_str = f'<div dir="rtl">{grade_average}</div>'
         st.markdown(html_str, unsafe_allow_html=True)
         break
         
          
          

#convert releveant cols to float
df["Course Number"] = pd.to_numeric(df["Course Number"]) # convert course number col to float
df["Year"] = pd.to_numeric(df["Year"], downcast="float") # convert course number col to float
#df["Grade"] = pd.to_numeric(df["Grade"], downcast="float") # convert course number col to float

#print(df.dtypes)

# for val in df['Course Number'].values:
#   print(val, type(val))

#get list of courses
AllCourses = set(sorted(df['Course Number'].values))
allcourses_sorted = sorted(AllCourses, reverse=False)
# all_courses_sorted_str = ([str(course) for course in allcourses_sorted]) # convert list of ints to list of strs - not needed


# choose course number from dropdown 
html_str = f'<div dir="rtl">בחירת מספר קורס:</div>'
st.markdown(html_str, unsafe_allow_html=True)
course_number  = st.selectbox('',list(allcourses_sorted))
if course_number not in allcourses_sorted:
  st.text('No feedback available!')

# locate the data for the selected course
courseNumberdf = df.loc[df['Course Number'] == course_number] 



# print the data on the screen for the selected course
# Print Course Name
printValues(courseNumberdf, 'שם הקורס:', 'Course Name')  

# Print Lecture Tips
printValues(courseNumberdf, 'דגשים בנוגע להרצאות:', 'Lecture Tips')
            
# Print Project Tips	
printValues(courseNumberdf, 'דגשים בנוגע למטלות:', 'Project Tips')

# Print Excersize Classes		
printValues(courseNumberdf, 'על התרגולים:', 'Excersize Classes')

# Print Summary	
printValues(courseNumberdf, 'סיכום מומלץ:', 'Summary')

# Print Exams	
printValues(courseNumberdf, 'קצת על הבחנים והמבחנים:', 'Exams')

# Print more tips	
printValues(courseNumberdf, 'דגשים נוספים:', 'More Tips')

# Print Pros and Cons
printValues(courseNumberdf, 'האם מומלץ:', 'Pros and Cons')

# Print Exam Grade
printValues(courseNumberdf, 'ציון ממוצע קורס:', 'Grade')