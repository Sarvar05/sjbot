import traceback

from mysql.connector import connect, Error, errorcode

from db.db_config import config_db


class DBHelper:

    def __init__(self):
        try:
            self.conn = connect(**config_db)
            self.cursor = self.conn.cursor(dictionary=True, buffered=True)
        except Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Something is wrong with your user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(traceback.format_exc())

    def get(self, table_name, id):
        sql = "SELECT * FROM " + table_name + " WHERE id = %s"
        self.cursor.execute(sql, (id,))
        row = self.cursor.fetchone()
        if row:
            return row
        else:
            return False

    def insert(self, table_name, data):
        keys = data.keys()
        values = data.values()
        params = ["%s" for i in range(len(data))]
        sql = "INSERT INTO {} ({}) VALUES ({})".format(table_name, ','.join(keys), ','.join(params))
        val = tuple(values)
        self.cursor.execute(sql, val)
        self.conn.commit()

        sql = "SELECT * FROM " + table_name + " ORDER BY id DESC LIMIT 1;"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row:
            return row['id']
        return False

    def get_all(self, table_name, conditions={}):
        keys = []
        values = []
        for key, value in conditions.items():
            keys.append(key + ' = %s')
            values.append(value)

        if len(conditions) > 0:
            sql = "SELECT * FROM " + table_name + " WHERE " + ' AND '.join(keys) + ";"
        else:
            sql = "SELECT * FROM " + table_name + ";"

        val = tuple(values)
        self.cursor.execute(sql, val)
        rows = self.cursor.fetchall()
        if len(rows):
            return rows
        else:
            return False

    def update(self, table_name, id, data):
        keys = []
        values = []
        for key, value in data.items():
            keys.append(key + ' = %s')
            values.append(value)
        values.append(int(id))
        sql = "UPDATE " + table_name + " SET " + ','.join(keys) + " WHERE id = %s;"
        val = tuple(values)
        self.cursor.execute(sql, val)
        self.conn.commit()

    def deactivate_user(self, id):
        sql = "UPDATE users SET status = %s WHERE id = %s"
        val = (False, id)
        self.cursor.execute(sql, val)
        self.conn.commit()

    def get_users_list(self):
        sql = "SELECT * from users WHERE status=%s;"
        self.cursor.execute(sql, (True, id))
        return self.cursor.fetchall()

    def statistic(self):
        # 1. barcha obunachilar soni
        sql = "SELECT COUNT(*) as countAll FROM users;"
        self.cursor.execute(sql)
        all = self.cursor.fetchall()[0]['countAll']
        # 2. barcha foydalanuvchilar soni
        sql = "SELECT COUNT(*) as active FROM users WHERE status=1;"
        self.cursor.execute(sql)
        active = self.cursor.fetchall()[0]['active']
        # 3. barcha obunani to'xtatgan foydalanuchilar  soni
        sql = "SELECT COUNT(*) as inactive FROM users WHERE status=0;"
        self.cursor.execute(sql)
        inactive = self.cursor.fetchall()[0]['inactive']
        return (all, active, inactive)

    def get_subjects(self, typ):
        sql = "SELECT * FROM subjects WHERE type=%s;"
        self.cursor.execute(sql, (typ,))
        return self.cursor.fetchall()

    def get_test(self, test_id):
        sql = '''
            SELECT tests.*,users.full_name as author,count(results.id) as participants_count 
            FROM tests 
            LEFT JOIN users ON users.id=tests.author_id
            LEFT JOIN results ON results.test_id=tests.id
            WHERE test_id = %s GROUP BY results.test_id;'''
        self.cursor.execute(sql, (test_id,))
        row = self.cursor.fetchone()

        if row:
            return row
        return False

    def check_result_exists(self, user_id, test_id):
        sql = '''
            SELECT * FROM results
            WHERE results.user_id = %s AND results.test_id = %s;'''

        self.cursor.execute(sql, (user_id, test_id))
        row = self.cursor.fetchone()
        if row:
            return True
        return False

    def get_result(self, id):
        sql = '''
            SELECT 
                results.*,
                tests.name as test_name,
                tests.count_tests as count_tests,
                users.full_name as full_name
            FROM results
                LEFT JOIN tests ON tests.id=results.test_id 
                LEFT JOIN users ON users.id=results.user_id 
            WHERE results.id = %s;'''

        self.cursor.execute(sql, (id,))
        row = self.cursor.fetchone()
        if row:
            return row
        return False

    def get_results(self, test_id):
        sql = '''
            SELECT 
                results.*,
                users.full_name as full_name
            FROM results
                LEFT JOIN users ON users.id=results.user_id 
            WHERE results.test_id=%s
            ORDER BY correct_answers_count DESC, test_time ASC;'''
        self.cursor.execute(sql, (test_id,))
        rows = self.cursor.fetchall()

        if len(rows) > 0:
            return rows

        return False