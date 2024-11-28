from pymongo import MongoClient

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
