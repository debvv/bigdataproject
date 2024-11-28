from pymongo import MongoClient
import streamlit as st
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client['migration_db']
    collection = db['specialists']

    # Проверка данных
    specialists = list(collection.find({}))
    print(f"Найдено {len(specialists)} записей в коллекции 'specialists'")
    for specialist in specialists:
        print(specialist)
    # Заголовок приложения
    st.title("1")
except Exception as e:
    print(f"Ошибка подключения: {e}")
    # Заголовок приложения
    st.title("2")

    data = fetch_all_data()
    st.write("Отладка: данные из MongoDB", data)
    if not data.empty:
        st.dataframe(data)
    else:
        st.warning("Нет данных для отображения.")
