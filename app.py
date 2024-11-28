import streamlit as st
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Подключение к MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['migration_db']
collection = db['specialists']

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
def calculate_migration_index(current_salary, years_experience):
    # Простая модель: больше опыта и зарплаты — ниже вероятность миграции
    return max(0, 100 - (current_salary / 1000 + years_experience * 2))

# Функция: Расчет индекса удержания
def calculate_retention_index(current_salary, job_satisfaction):
    # Простая модель: высокая зарплата и удовлетворённость повышают удержание
    return min(100, current_salary / 1000 + job_satisfaction * 10)

# Добавление специалиста
if choice == "Добавить специалиста":
    st.subheader("Добавить нового специалиста")
    with st.form("Добавление специалиста"):
        specialist_id = st.number_input("ID специалиста", min_value=1, step=1)
        age = st.number_input("Возраст", min_value=18, step=1)
        education = st.selectbox("Образование", ["Bachelor", "Master", "PhD"])
        specialization = st.text_input("Специализация")
        years_experience = st.number_input("Опыт работы (лет)", min_value=0, step=1)
        current_salary = st.number_input("Текущая зарплата", min_value=0.0, step=100.0)
        migration_date = st.date_input("Дата миграции (если есть)", value=None)
        job_satisfaction = st.slider("Удовлетворённость работой (1-10)", min_value=1, max_value=10)

        submit_button = st.form_submit_button("Добавить")
        
        if submit_button:
            migration_index = calculate_migration_index(current_salary, years_experience)
            retention_index = calculate_retention_index(current_salary, job_satisfaction)
            
            specialist = {
                "specialist_id": specialist_id,
                "age": age,
                "education": education,
                "specialization": specialization,
                "years_experience": years_experience,
                "current_salary": current_salary,
                "migration_date": str(migration_date) if migration_date else None,
                "job_satisfaction": job_satisfaction,
                "migration_index": migration_index,
                "retention_index": retention_index
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
        selected_specialist = collection.find_one({"specialist_id": specialist_id}, {"_id": 0})
        
        if selected_specialist:
            with st.form("Обновление специалиста"):
                age = st.number_input("Возраст", value=selected_specialist['age'], min_value=18, step=1)
                education = st.selectbox("Образование", ["Bachelor", "Master", "PhD"], 
                                         index=["Bachelor", "Master", "PhD"].index(selected_specialist['education']))
                specialization = st.text_input("Специализация", value=selected_specialist['specialization'])
                years_experience = st.number_input("Опыт работы (лет)", value=selected_specialist['years_experience'], min_value=0, step=1)
                current_salary = st.number_input("Текущая зарплата", value=selected_specialist['current_salary'], min_value=0.0, step=100.0)
                job_satisfaction = st.slider("Удовлетворённость работой (1-10)", value=selected_specialist['job_satisfaction'], min_value=1, max_value=10)

                update_button = st.form_submit_button("Обновить")
                
                if update_button:
                    migration_index = calculate_migration_index(current_salary, years_experience)
                    retention_index = calculate_retention_index(current_salary, job_satisfaction)

                    collection.update_one(
                        {"specialist_id": specialist_id},
                        {"$set": {
                            "age": age,
                            "education": education,
                            "specialization": specialization,
                            "years_experience": years_experience,
                            "current_salary": current_salary,
                            "job_satisfaction": job_satisfaction,
                            "migration_index": migration_index,
                            "retention_index": retention_index
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
        st.bar_chart(data[['migration_index', 'retention_index']])
        fig, ax = plt.subplots()
        sns.histplot(data['current_salary'], kde=True, ax=ax, bins=20)
        ax.set_title("Распределение зарплат")
        st.pyplot(fig)
    else:
        st.warning("Нет данных для анализа.")
