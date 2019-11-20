from models.DatabaseConnection import connect_to_database
from models.User import User
import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Panel administracyjny pozwalający zarządzać użytkownikami")
    parser.add_argument("-u", "--username", default="test1234", help="Nazwa użutkownika [wymagana]")
    parser.add_argument("-p", "--password", default="test1234", help="Hasło [wymagane]")
    parser.add_argument("-n", "--new-pass", help="Nowe hasło [opcjonalnie]", required=False, dest="new_pass")
    parser.add_argument("-l", "--list", help="Wylistowanie wszystkich użytkowników", action="store_true",
                        required=False, dest="list_of_users")
    parser.add_argument("-d", "--delete", help="Usuwanie zalogowanego użytkownika [nazwa uzytkownika musi zostac raz"
                                               " jeszcze podana", required=False, dest="delete_user")
    parser.add_argument("-e", "--edit", action="store_true", help="Edycja danych użytkownika", required=False)

    args = parser.parse_args()

    username = args.username
    password = args.password
    new_pass = args.new_pass
    list_of_users = args.list_of_users
    delete_user = args.delete_user
    edit = args.edit

    connection_to_db = connect_to_database("postgres", "coderslab", "127.0.0.1", "warsztat_2")

    if list_of_users:
        print("Lista wszystkich użytkowników:")
        for u in User.get_all_users(connection_to_db):
            print(u)

    if User.get_user_by_name(connection_to_db, username) and User.verify(connection_to_db, username, password):
        print("Zalogowano poprawnie")
        user = User.get_user_by_name(connection_to_db, username)
        if new_pass:
            if edit:
                user.change(connection_to_db, new_password=new_pass)
                print('Hasło zmienione')
                new_pass = None
            else:
                print("aby zmienić hasło wpisz --edit --new_pass <nowe_haslo>")
        if delete_user:
            if delete_user == username:
                user.delete(connection_to_db)
                print("Uzytkownik zostal usuniety")
            else:
                print("nipowodzenie")
    else:
        user = User(None, username, f"email@{username}.com", password)
        try:
            user.save_to_db(connection_to_db)
        except Exception:
            print(f'Błędny login lub hasło')
        else:
            print(f"Utworzono nowe konto: username: {username}, email: email@{username}.com, password: {password}")
            password = None
