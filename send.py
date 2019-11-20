from models.DatabaseConnection import connect_to_database
from models.User import User
from models.Message import Message
import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Skrypt umozliwiajacy dodawanie, zmienianie, logowanie uzytkownikow"
                                                 "oraz wymiane wiadomosci pomiedzy nimi")
    parser.add_argument("-u", "--username", default="test1234", help="Nazwa użutkownika [wymagana]")
    parser.add_argument("-p", "--password", default="test1234", help="Hasło [wymagane]")
    parser.add_argument("-l", "--list", help="Wylistowanie wszystkich komunikatów użytkownika", action="store_true",
                        required=False, dest="list_of_messages")
    parser.add_argument("-t", "--to", help="Nazwa użytkownika do którego wiadomość ma zostać wysłana",
                        dest="send_to")
    parser.add_argument("-s", "--send", help="Treść wiadomości", dest="message")

    args = parser.parse_args()

    username = args.username
    password = args.password
    list_of_messages = args.list_of_messages
    send_to = args.send_to
    message = args.message

    connection_to_db = connect_to_database("postgres", "coderslab", "127.0.0.1", "warsztat_2")

    if User.get_user_by_name(connection_to_db, username):
        print("Zalogowano poprawnie")
        user = User.get_user_by_name(connection_to_db, username)

        if list_of_messages:
            if send_to == username:
                print(f"Wiadomosci przysłane do mnie:")
                _to = User.get_user_by_name(connection_to_db, send_to).get_user_id()
                print(_to)
                messages = Message.get_all_messages(connection_to_db, user.get_user_id(), receiver_id=1, for_me=True)
                for i, m in enumerate(messages):
                    print(f"    Wiadomość {i + 1}: {m}")
            elif send_to:
                print(f"Wiadomosci wysłane do użytkownika {send_to}:")
                _to = User.get_user_by_name(connection_to_db, send_to).get_user_id()
                messages = Message.get_all_messages(connection_to_db, user.get_user_id(), receiver_id=_to)
                for i, m in enumerate(messages):
                    print(f"    Wiadomość {i + 1}: {m}")
            else:
                print(f'Wiadomości wysłane przez użytkownika: {username}')
                messages = Message.get_all_messages(connection_to_db, user.get_user_id())
                for i, m in enumerate(messages):
                    print(f"    Wiadomość {i + 1}: {m}")

        if send_to or message:
            if message and send_to:
                _to = User.get_user_by_name(connection_to_db, send_to)
                if _to:
                    msg = Message(None, user.get_user_id(), _to.get_user_id(), message, 'now')
                    msg.save_to_db(connection_to_db)
                    print(f"Wiadomość: '{msg}' została wysłana")
                else:
                    print(f"Użytkownik {send_to} nie istnieje")
            elif list_of_messages:
                pass
            else:
                print("Podaj adresata oraz treść wiadomości")
    else:
        print("nieprawidłowy login lub hasło")
