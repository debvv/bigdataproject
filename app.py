import streamlit as st
from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["migration_db"]
collection = db["specialists"]

# Функции CRUD
def create_specialist(data):
    collection.insert_one(data)

def read_specialists():
    return list(collection.find())

def update_specialist(specialist_id, updated_data):
    collection.update_one({"specialist_id": specialist_id}, {"$set": updated_data})

def delete_specialist(specialist_id):
    collection.delete_one({"specialist_id": specialist_id})

# Streamlit интерфейс
st.title("CRUD-приложение для работы с MongoDB")

# Добавление данных
st.header("Добавить нового специалиста")
specialist_id = st.number_input("ID специалиста", min_value=1, step=1)
name = st.text_input("Имя")
age = st.number_input("Возраст", min_value=18, step=1)
education = st.selectbox("Образование", ["Bachelor", "Master", "PhD"])
specialization = st.text_input("Специализация")
experience = st.number_input("Стаж работы (лет)", min_value=0, step=1)
salary = st.number_input("Зарплата", min_value=0, step=100)
migration_date = st.text_input("Дата миграции (YYYY-MM-DD)", value="")

if st.button("Добавить"):
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
    st.success("Данные успешно добавлены!")

# Просмотр данных
st.header("Просмотр специалистов")
specialists = read_specialists()
for specialist in specialists:
    st.write(specialist)

# Обновление данных
st.header("Обновление данных")
update_id = st.number_input("ID специалиста для обновления", min_value=1, step=1)
updated_name = st.text_input("Новое имя")
if st.button("Обновить"):
    update_specialist(update_id, {"name": updated_name})
    st.success("Данные успешно обновлены!")

# Удаление данных
st.header("Удаление специалиста")
delete_id = st.number_input("ID специалиста для удаления", min_value=1, step=1)
if st.button("Удалить"):
    delete_specialist(delete_id)
    st.success("Данные успешно удалены!")
