import streamlit as st
from pymongo import MongoClient
from urllib.parse import quote_plus
# MongoDB connection
#client = MongoClient("mongodb+srv://<username>:<password>@cluster0.mongodb.net/<database_name>?retryWrites=true&w=majority")

##client = MongoClient("mongodb+srv://scofieldtestmongodb:<scofieldtestmongodb##@@>@cluster0.4jiw1.mongodb.net/")


username = "scofieldtestmongodb"  # Замените своим именем пользователя
password = "scofieldtestmongodb##@@"  # Замените своим паролем
encoded_password = quote_plus(password)

uri = f"mongodb+srv://{username}:{encoded_password}@cluster0.mongodb.net/migration_db?retryWrites=true&w=majority"
print(uri)

db = client["migration_db"]
collection = db["specialists"]

# Create function
def create_specialist(data):
    collection.insert_one(data)

# Read function
def read_specialists():
    return list(collection.find())

# Update function
def update_specialist(specialist_id, updated_data):
    collection.update_one({"specialist_id": specialist_id}, {"$set": updated_data})

# Delete function
def delete_specialist(specialist_id):
    collection.delete_one({"specialist_id": specialist_id})

# Streamlit interface
st.title("CRUD Application for MongoDB")

# CREATE
st.header("Add a New Specialist")
specialist_id = st.number_input("Specialist ID", min_value=1, step=1)
name = st.text_input("Name")
age = st.number_input("Age", min_value=18, step=1)
education = st.selectbox("Education Level", ["Bachelor", "Master", "PhD"])
specialization = st.text_input("Specialization")
experience = st.number_input("Years of Experience", min_value=0, step=1)
salary = st.number_input("Current Salary", min_value=0, step=100)
migration_date = st.text_input("Migration Date (YYYY-MM-DD)", value="")

if st.button("Add Specialist"):
    data = {
        "specialist_id": specialist_id,
        "name": name,
        "age": age,
        "education": education,
        "specialization": specialization,
        "years_experience": experience,
        "current_salary": salary,
        "migration_date": migration_date,
    }
    create_specialist(data)
    st.success("Specialist added successfully!")

# READ
st.header("View All Specialists")
specialists = read_specialists()
for specialist in specialists:
    st.write(specialist)

# UPDATE
st.header("Update Specialist Data")
update_id = st.number_input("Specialist ID to Update", min_value=1, step=1)
updated_field = st.selectbox("Field to Update", ["name", "age", "education", "specialization", "years_experience", "current_salary", "migration_date"])
updated_value = st.text_input(f"New Value for {updated_field}")

if st.button("Update Specialist"):
    update_specialist(update_id, {updated_field: updated_value})
    st.success("Specialist updated successfully!")

# DELETE
st.header("Delete Specialist")
delete_id = st.number_input("Specialist ID to Delete", min_value=1, step=1)

if st.button("Delete Specialist"):
    delete_specialist(delete_id)
    st.success("Specialist deleted successfully!")
