import psycopg2


class MyPSQL:

    def __init__(self, db_name, user, password, data_checking):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.data_checking = data_checking

    def checking_database(self):
        try:
            conn = psycopg2.connect(database=self.db_name, user=self.user,
                                    password=self.password)
            conn.close()
            return print(
                f'Подключение к базе данных {self.db_name} прошло успешно.'
            )
        except:
            self.create_db()

    def create_db(self):
        try:
            conn = psycopg2.connect(user=self.user, password=self.password)
            with conn.cursor() as cur:
                conn.autocommit = True
                cur.execute(f"CREATE DATABASE {self.db_name}")
            conn.close()
            return print('База данных создана успешно.')
        except:
            self.data_checking = False
            return self.data_checking

    def create_table(self):
        with psycopg2.connect(database=f'{self.db_name}', user=self.user,
                              password=self.password) as conn:
            with conn.cursor() as cur:
                cur.execute('''
                CREATE TABLE IF NOT EXISTS personal_datas(
                    id SERIAL PRIMARY KEY, 
                    personal_data VARCHAR(40) UNIQUE NOT NULL
                );
                ''')

                cur.execute('''
                CREATE TABLE IF NOT EXISTS contact_datas(
                    id SERIAL PRIMARY KEY,
                    phone_number VARCHAR(40),
                    email_address  VARCHAR(40),
                    personal_data_id INTEGER NOT NULL 
                        REFERENCES personal_datas(id)
                );
                ''')
                conn.commit()
        return print(f'Таблицы успешно созданы.')

    def add_new_client(self, name):
        try:
            with psycopg2.connect(database=f'{self.db_name}', user=self.user,
                                  password=self.password) as conn:
                with conn.cursor() as cur:
                    cur.execute(f'''
                    INSERT INTO 
                        personal_datas(personal_data)
                    VALUES
                        ('{name}');
                    ''')
                    conn.commit()
            return print(f'Клиент {name} успешно добавлен в базу данных.')
        except print(f'Клиент с именем {name} уже существует.'):
            return

    def add_new_information(self, id_, telephone, mail):
        with psycopg2.connect(database=f'{self.db_name}', user=self.user,
                              password=self.password) as conn:
            with conn.cursor() as cur:
                cur.execute(f'''
                INSERT INTO 
                    contact_datas(phone_number, email_address, personal_data_id)
                VALUES
                    ({telephone}, '{mail}', {id_});
                ''')
                conn.commit()
        return print('Данные добавлены успешно.')

    def get_id(self, data, table, column, name):
        try:
            with psycopg2.connect(database=f'{self.db_name}', user=self.user,
                                  password=self.password) as conn:
                with conn.cursor() as cur:
                    cur.execute(f'''
                    SELECT 
                        {data} 
                    FROM 
                        {table} 
                    WHERE 
                        {column}=%s;  
                    ''', (name, ))
                    return cur.fetchone()[0]
        except:
            return 0

    def get_user_information(self, id_user):
        try:
            with psycopg2.connect(database=f'{self.db_name}', user=self.user,
                                  password=self.password) as conn:
                with conn.cursor() as cur:
                    cur.execute(f'''
                    SELECT
                        pd.personal_data, cd.id, cd.phone_number, 
                        cd.email_address
                    FROM 
                        personal_datas pd
                    FULL OUTER JOIN 
                        contact_datas cd on pd.id = cd.personal_data_id
                    WHERE pd.id=%s;
                    ''', (id_user, ))
                    res = cur.fetchall()
            return res
        except:
            return 0

    def get_all_information(self):
        try:
            with psycopg2.connect(database=f'{self.db_name}', user=self.user,
                                  password=self.password) as conn:
                with conn.cursor() as cur:
                    cur.execute(f'''
                    SELECT
                        pd.personal_data, cd.id, cd.phone_number, 
                        cd.email_address
                    FROM 
                        personal_datas pd
                    FULL OUTER JOIN 
                        contact_datas cd on pd.id = cd.personal_data_id;
                    ''')
                    res = cur.fetchall()
            return res
        except:
            return 0

    def change(self, table, column, id_, name):
        with psycopg2.connect(database=f'{self.db_name}', user=self.user,
                              password=self.password) as conn:
            with conn.cursor() as cur:
                cur.execute(f'''
                UPDATE {table} SET {column}=%s
                WHERE id=%s;
                ''', (name, id_))
                conn.commit()
        return print('Изменения внесены успешно')

    def delete(self, table, id_):
        with psycopg2.connect(database=f'{self.db_name}', user=self.user,
                              password=self.password) as conn:
            with conn.cursor() as cur:
                cur.execute(f'''
                DELETE FROM {table}
                WHERE id=%s;
                ''', (id_, ))
                conn.commit()
        return
