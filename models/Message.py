class Message:

    def __init__(self, _id, from_id, to_id, message, creation_date):
        self._id = _id
        self.from_id = from_id
        self.to_id = to_id
        self.message = message
        self.creation_date = creation_date

    def __str__(self):
        return self.message

    def save_to_db(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute("INSERT INTO Message(from_id, to_id, msg, creation_date) VALUES(%s, %s, %s, %s) RETURNING id",
                       [self.from_id, self.to_id, self.message, 'now'])
        new_id = cursor.fetchone()[0]
        self._id = new_id
        cursor.close()

    @staticmethod
    def get_all_messages(db_connection, user_id, receiver_id=None, for_me=False):
        """
        Returns all messages sent by user or sent to user when receiver_id not None
        :param db_connection: connection to database
        :param user_id: user who make request
        :param receiver_id: optional [required when
        :param for_me: optional [required when
        :return: list of messages
        """
        cursor = db_connection.cursor()
        if receiver_id:
            if for_me:
                cursor.execute("SELECT id, from_id, to_id, msg, creation_date FROM Message WHERE to_id=%s",
                               [user_id])
            else:
                cursor.execute("SELECT id, from_id, to_id, msg, creation_date FROM Message WHERE from_id=%s "
                               "AND to_id=%s", [user_id, receiver_id])
        else:
            cursor.execute("SELECT id, from_id, to_id, msg, creation_date FROM Message WHERE from_id=%s",
                           [user_id])
        _all_messages = []
        all_messages_data = cursor.fetchall()
        for message_data in all_messages_data:
            message = Message(message_data[0], message_data[1], message_data[2], message_data[3], message_data[4])
            _all_messages.append(message)
        cursor.close()
        return _all_messages
