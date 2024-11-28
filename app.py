import streamlit as st
from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient("mongodb+srv://scofieldtestmongodb:<scofieldtestmongodb##@@>@cluster0.4jiw1.mongodb.net/migration_db?retryWrites=true&w=majority")
db = client["migration_db"]
collection = db["specialists"]

# CREATE function
def create_specialist(data):
    collection.insert_one(data)

# READ function
def read_specialists():
    return list(collection.find())

# UPDATE function
def update_specialist(specialist_id, updated_data):
    collection.update_one({"specialist_id": specialist_id}, {"$set": updated_data})

# DELETE function
def delete_specialist(specialist_id):
    collection.delete_one({"specialist_id": specialist_id})

# Streamlit interface
st.title("CRUD Application for MongoDB")

# CREATE Section
st.header("Add a New Specialist")
specialist_id = st.number_input("Specialist ID", min_value=1, step=1)
name = st.text_input("Name")
age = st.number_input("Age", min_value=18, step=1)
education = st.selectbox("Education Level", ["Bachelor", "Master", "PhD"])
specialization = st.text_input("Specialization")
experience = st.number_input("Years of Experience", min_value=0, step=1)
salary = st.number_input("Current Salary", min_value=0, step=100)
migration_date = st.text_input("Migration
