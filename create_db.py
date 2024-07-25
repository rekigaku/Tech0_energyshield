import sqlite3
import shutil
import os

def create_tables():
    conn = sqlite3.connect('backend/app/database.db')
    cursor = conn.cursor()

    # テーブル作成
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_master (
        user_id INTEGER PRIMARY KEY,
        user_name TEXT,
        login_id TEXT UNIQUE,
        password TEXT,
        register_date DATE,
        birthday DATE,
        gender TEXT,
        postcode TEXT,
        address_pref TEXT,
        address_town TEXT,
        address_detail TEXT,
        email TEXT UNIQUE,
        tel TEXT,
        profession TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clinic_master (
        clinic_id INTEGER PRIMARY KEY,
        clinic_name TEXT,
        register_date DATE,
        postcode TEXT,
        address_pref TEXT,
        address_town TEXT,
        address_detail TEXT,
        email TEXT,
        tel TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS device_master (
        device_id INTEGER PRIMARY KEY,
        device_name TEXT,
        manufacture TEXT,
        basic_price REAL,
        symptoms_id INTEGER,
        effect_id INTEGER,
        device_photo TEXT,
        FOREIGN KEY (symptoms_id) REFERENCES symptoms(symptoms_id),
        FOREIGN KEY (effect_id) REFERENCES effect(effect_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS symptoms (
        symptoms_id INTEGER PRIMARY KEY,
        description TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS effect (
        effect_id INTEGER PRIMARY KEY,
        description TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS evaluation (
        device_id INTEGER PRIMARY KEY,
        evaluation_service TEXT,
        evaluation_device TEXT,
        FOREIGN KEY (device_id) REFERENCES device_master(device_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clinic_device (
        clinic_id INTEGER,
        device_id INTEGER,
        PRIMARY KEY (clinic_id, device_id),
        FOREIGN KEY (clinic_id) REFERENCES clinic_master(clinic_id),
        FOREIGN KEY (device_id) REFERENCES device_master(device_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clinic_device_rental_price (
        clinic_id INTEGER,
        device_id INTEGER,
        rental_duration INTEGER,
        rental_price REAL,
        PRIMARY KEY (clinic_id, device_id, rental_duration),
        FOREIGN KEY (clinic_id) REFERENCES clinic_master(clinic_id),
        FOREIGN KEY (device_id) REFERENCES device_master(device_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservation_records (
        reserve_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        clinic_id INTEGER,
        device_id INTEGER,
        reservation_date DATE,
        start_time TIME,
        rental_duration INTEGER,
        payment REAL,
        after_service TEXT,
        evaluation_clinic TEXT,
        evaluation_service TEXT,
        evaluation_device TEXT,
        FOREIGN KEY (user_id) REFERENCES user_master(user_id),
        FOREIGN KEY (clinic_id) REFERENCES clinic_master(clinic_id),
        FOREIGN KEY (device_id) REFERENCES device_master(device_id)
    )
    ''')

    conn.commit()
    conn.close()

def add_column():
    conn = sqlite3.connect('backend/app/database.db')
    cursor = conn.cursor()

    # device_masterテーブルにdevice_photoカラムを追加
    cursor.execute('''
    ALTER TABLE device_master
    ADD COLUMN device_photo TEXT
    ''')

    conn.commit()
    conn.close()

def insert_device_with_photo(device_id, device_name, manufacture, basic_price, symptoms_id, effect_id, photo_path):
    # 画像ファイルを指定のディレクトリにコピー
    destination_dir = 'frontend/public/images'
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    destination_path = os.path.join(destination_dir, f'{device_id}.jpg')
    shutil.copy(photo_path, destination_path)

    conn = sqlite3.connect('backend/app/database.db')
    cursor = conn.cursor()

    # device_masterにデータを挿入
    cursor.execute('''
    INSERT INTO device_master (device_id, device_name, manufacture, basic_price, symptoms_id, effect_id, device_photo)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (device_id, device_name, manufacture, basic_price, symptoms_id, effect_id, destination_path))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    try:
        add_column()
    except sqlite3.OperationalError:
        # カラムが既に存在する場合のエラーハンドリング
        print("Column already exists, skipping add_column step.")
    
    # デバイスの情報と画像のパスを指定して関数を呼び出し
    insert_device_with_photo(1, 'Massage Chair', 'Health Co.', 3000.0, 1, 1, 'frontend/public/images/massage_chair.jpg')
