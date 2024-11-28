import streamlit as st
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Подключение к MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['recrutare']
collection = db['candidati']

# Заголовок приложения
st.title("Управление данными IT-специалистов")

# Главное меню
menu = ["Добавить специалиста", "Просмотр специалистов", "Обновить специалиста", "Удалить специалиста", "Анализ данных"]
choice = st.sidebar.selectbox("Выберите действие", menu)

# Функция: Получение данных из MongoDB
def fetch_all_data():
    data = list(collection.find({}, {"_id": 0}))
    return pd.DataFrame(data)

# Функция: Расчет индекса миграции
def calculate_migration_index(data):
    return data['unemployment_rate'] + (100 - data['life_quality_index']) - data['political_stability_index']

# Функция: Расчет индекса удержания
def calculate_retention_index(data):
    return data['current_salary'] + data['it_sector_investments'] - data['offers_received_abroad']

# Добавление специалиста
if choice == "Добавить специалиста":
    st.subheader("Добавить нового специалиста")
    with st.form("Добавление специалиста"):
        specialist_id = st.number_input("ID специалиста", min_value=1, step=1)
        name = st.text_input("Полное имя")
        age = st.number_input("Возраст", min_value=18, step=1)
        education = st.selectbox("Образование", ["Бакалавр", "Магистр", "PhD"])
        specialization = st.text_input("Специализация")
        years_experience = st.number_input("Опыт работы (лет)", min_value=0, step=1)
        current_salary = st.number_input("Текущая зарплата", min_value=0.0, step=100.0)
        job_satisfaction = st.slider("Удовлетворённость работой (1-10)", min_value=1, max_value=10)
        offers_received_abroad = st.number_input("Предложения из-за рубежа", min_value=0, step=1)
        destination_country = st.text_input("Страна назначения")
        reason_for_leaving = st.text_area("Причина ухода")

        submit_button = st.form_submit_button("Добавить")
        
        if submit_button:
            specialist = {
                "specialist_id": specialist_id,
                "name": name,
                "age": age,
                "education": education,
                "specialization": specialization,
                "years_experience": years_experience,
                "current_salary": current_salary,
                "job_satisfaction": job_satisfaction,
                "offers_received_abroad": offers_received_abroad,
                "destination_country": destination_country,
                "reason_for_leaving": reason_for_leaving,
                "migration_index": calculate_migration_index({
                    "unemployment_rate": 5,  # Примерные данные
                    "life_quality_index": 70,
                    "political_stability_index": 50
                }),
                "retention_index": calculate_retention_index({
                    "current_salary": current_salary,
                    "it_sector_investments": 10000,  # Примерные данные
                    "offers_received_abroad": offers_received_abroad
                })
            }
            collection.insert_one(specialist)
            st.success("Специалист успешно добавлен!")

# Просмотр специалистов
elif choice == "Просмотр специалистов":
    st.subheader("Список всех специалистов")
    data = fetch_all_data()
    if not data.empty:
        st.dataframe(data)
    else:
        st.warning("Нет данных для отображения.")

# Обновление специалиста
elif choice == "Обновить специалиста":
    st.subheader("Обновить данные специалиста")
    data = fetch_all_data()
    if not data.empty:
        specialist_id = st.selectbox("Выберите ID специалиста", data['specialist_id'])
        selected_specialist = collection.find_one({"specialist_id": specialist_id})
        
        if selected_specialist:
            with st.form("Обновление специалиста"):
                name = st.text_input("Полное имя", value=selected_specialist['name'])
                age = st.number_input("Возраст", value=selected_specialist['age'], min_value=18, step=1)
                education = st.selectbox("Образование", ["Бакалавр", "Магистр", "PhD"], index=["Бакалавр", "Магистр", "PhD"].index(selected_specialist['education']))
                specialization = st.text_input("Специализация", value=selected_specialist['specialization'])
                years_experience = st.number_input("Опыт работы (лет)", value=selected_specialist['years_experience'], min_value=0, step=1)
                current_salary = st.number_input("Текущая зарплата", value=selected_specialist['current_salary'], min_value=0.0, step=100.0)
                update_button = st.form_submit_button("Обновить")
                
                if update_button:
                    collection.update_one(
                        {"specialist_id": specialist_id},
                        {"$set": {
                            "name": name,
                            "age": age,
                            "education": education,
                            "specialization": specialization,
                            "years_experience": years_experience,
                            "current_salary": current_salary
                        }}
                    )
                    st.success("Данные специалиста успешно обновлены!")
    else:
        st.warning("Нет специалистов для обновления.")

# Удаление специалиста
elif choice == "Удалить специалиста":
    st.subheader("Удалить специалиста")
    data = fetch_all_data()
    if not data.empty:
        specialist_id = st.selectbox("Выберите ID специалиста", data['specialist_id'])
        delete_button = st.button(f"Удалить специалиста с ID {specialist_id}")
        
        if delete_button:
            collection.delete_one({"specialist_id": specialist_id})
            st.success(f"Специалист с ID {specialist_id} успешно удалён!")
    else:
        st.warning("Нет специалистов для удаления.")

# Анализ данных
elif choice == "Анализ данных":
    st.subheader("Анализ данных специалистов")
    data = fetch_all_data()
    if not data.empty:
        st.line_chart(data[["migration_index", "retention_index"]])
        fig, ax = plt.subplots()
        sns.histplot(data['job_satisfaction'], kde=True, ax=ax)
        st.pyplot(fig)
    else:
        st.warning("Нет данных для анализа.")
