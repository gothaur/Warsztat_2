from clcrypto import password_hash, check_password


class User:
    def __init__(self, _id, username, email, password):
        """

        :param _id:
        :param username:
        :param email:
        :param password:
        """
        self._id = _id
        self.username = username
        self.email = email
        self.password = password

    def __str__(self):
        return self.username

    @staticmethod
    def get_user(db_conn, _id,):
        """

        :param db_conn: connection to database
        :param _id: identifier of user to get
        :return: user if found otherwise None
        """
        cursor = db_conn.cursor()
        cursor.execute("select id, username, email, hashed_password from Users where id=%s", [_id])
        user_data = cursor.fetchone()
        user = User(user_data[0], user_data[1], user_data[2], user_data[3])
        cursor.close()
        return user

    @staticmethod
    def get_user_by_name(db_conn, username):
        """

        :param db_conn:
        :param username:
        :return:
        """
        cursor = db_conn.cursor()
        cursor.execute("select id, username, email, hashed_password from Users where username=%s", [username])
        if cursor.rowcount > 0:
            user_data = cursor.fetchone()
            user = User(user_data[0], user_data[1], user_data[2], user_data[3])
            cursor.close()
            return user

    @staticmethod
    def get_all_users(db_conn):
        """

        :param db_conn: connection to database
        :return: list of all users
        """
        cursor = db_conn.cursor()
        cursor.execute("select id, username, email, hashed_password from Users")
        # fetchall() to get all users data
        all_users_data = cursor.fetchall()
        all_users = []
        for user_data in all_users_data:
            user = User(user_data[0], user_data[1], user_data[2], user_data[3])
            all_users.append(user)
        cursor.close()
        return all_users

    def get_user_id(self):
        return self._id

    def save_to_db(self, db_conn):
        """

        :param db_conn:
        :return:
        """
        cursor = db_conn.cursor()
        self.password = password_hash(self.password)
        cursor.execute('insert into Users(username, email, hashed_password) values (%s,%s,%s) returning id',
                       [self.username, self.email, self.password])
        new_id = cursor.fetchone()[0]
        self._id = new_id
        cursor.close()

    @staticmethod
    def verify(db_conn, username, password):
        """

        :param db_conn:
        :param username:
        :param password:
        :return: True if valid password otherwise False
        """
        cursor = db_conn.cursor()
        cursor.execute("SELECT hashed_password FROM users WHERE username=%s", [username])
        result = False

        if cursor.rowcount > 0:
            db_hashed_password = cursor.fetchone()[0]
            result = check_password(password, db_hashed_password)

        cursor.close()
        return result

    def change(self, db_conn, new_email=None, new_username=None, new_password=None):
        """

        :param db_conn:
        :param new_email:
        :param new_username:
        :param new_password:
        :return:
        """
        cursor = db_conn.cursor()
        if new_email is None:
            new_email = self.email
        if new_username is None:
            new_username = self.username
        if new_password is None:
            new_password = self.password

        hashed_password = password_hash(new_password)
        cursor.execute("UPDATE users SET username=%s, email=%s, hashed_password=%s WHERE id=%s",
                       [new_username, new_email, hashed_password, self._id])
        self.password = hashed_password
        self.username = new_username
        self.email = new_email
        cursor.close()

    def delete(self, db_conn):
        """

        :param db_conn:
        :return:
        """
        cursor = db_conn.cursor()
        cursor.execute("DELETE FROM Users WHERE id=%s", [self._id])
        self._id = None
        cursor.close()

    # @staticmethod
    # def delete(db_conn, username):
    #     """
    #
    #     :param db_conn:
    #     :param username:
    #     :return:
    #     """
    #     cursor = db_conn.cursor()
    #     cursor.execute("DELETE FROM Users WHERE username=%s", [username])
    #     cursor.close()
