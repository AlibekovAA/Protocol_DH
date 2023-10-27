import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import simpledialog
import random
import json
from datetime import datetime
from sympy import primerange
import logging
import string
from tkinter import Text
from math import gcd as bltin_gcd
import ctypes

logging.basicConfig(level=logging.INFO)


def log_action(action):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{current_time}: {action}\n"
    log_text.insert(tk.END, log_entry)
    # logging.info(action)


def save_logs_to_file():
    logs = log_text.get(1.0, tk.END)
    filename = simpledialog.askstring("Сохранить логи", "Введите название текстового файла для сохранения логов:")
    if filename:
        filename = filename + ".txt"
        try:
            with open(filename, 'w') as log_file:
                log_file.write(logs)
            log_action(f"Логи были сохранены в файл: {filename}")
            messagebox.showinfo("Сохранение логов", "Логи были успешно сохранены.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении логов: {str(e)}")


def show_about():
    about_info = """
    Автор: Алибеков Аслан А-13а-20
    Индивидуальное задание: Реализация протокола Диффи-Хеллмана
    """
    tk.messagebox.showinfo("О программе", about_info)


def primRoots(modulo):
    required_set = {num for num in range(1, modulo) if bltin_gcd(num, modulo)}
    primitive_roots = []

    for g in range(1, modulo):
        if required_set == {pow(g, powers, modulo) for powers in range(1, modulo)}:
            primitive_roots.append(g)

            if len(primitive_roots) == 50:
                break

    return primitive_roots


def generate_DH_parameters():
    parameters = load_DH_parameters_from_file('DH_parameters.json')
    if parameters is not None:
        p, g = parameters
    else:
        primes = list(primerange(1000, 5000))
        p = random.choice(primes)
        g = random.choice(primRoots(p))
        save_DH_parameters_to_file('DH_parameters.json', p, g)
        log_action(f"Сгенерированы параметры p={p} и g={g}")
    return p, g


def save_DH_parameters_to_file(filename, p, g):
    parameters = {'p': p, 'g': g}
    with open(filename, 'w') as file:
        json.dump(parameters, file)


def load_DH_parameters_from_file(filename):
    try:
        with open(filename, 'r') as file:
            parameters = json.load(file)
            p = parameters['p']
            g = parameters['g']
            return p, g
    except FileNotFoundError:
        return None


def show_DH_parameters():
    parameters = load_DH_parameters_from_file('DH_parameters.json')
    if parameters is not None:
        p, g = parameters
        messagebox.showinfo("Параметры DH", f"p: {p}\ng: {g}")
        log_action("Были просмотрены параметры p и g")
    else:
        messagebox.showerror("Ошибка", "Параметры DH не найдены.")


def generate_keys(users):
    key = random.randint(10000, 300000)
    while key in users.values():
        key = random.randint(10000, 300000)
    return key


def save_users_to_file(filename, users):
    with open(filename, 'w') as file:
        json.dump(users, file)


def load_users_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def create_private_key_window(users, connections, chat_messages, chat_displays, existing_user_name, user_secret_keys,
                              connection_windows):
    private_key_window = tk.Toplevel(root)
    private_key_window.title("Введите закрытый ключ")
    private_key_window.geometry("300x150")

    def create_connection_with_private_key(users, connections, chat_messages, chat_displays, existing_user_name,
                                           user_secret_keys, connection_windows):
        user_private_key = private_key_entry.get().strip()
        log_action(f"Пользователь {existing_user_name} ввел закрытый ключ {'*' * len(str(user_private_key))}")
        if user_private_key.isdigit():
            user_private_key = int(user_private_key)
            if user_private_key:
                if existing_user_name in users:
                    user_public_key = users[existing_user_name]
                    create_connection_window(users, connections, chat_messages, chat_displays, existing_user_name,
                                             user_public_key, user_private_key, user_secret_keys, connection_windows)
                    private_key_window.destroy()
                else:
                    messagebox.showerror("Ошибка", "Пользователь не существует.")
            else:
                messagebox.showerror("Ошибка", "Закрытый ключ не введен.")
        else:
            messagebox.showerror("Ошибка", "Введите корректный закрытый ключ.")

    private_key_label = tk.Label(private_key_window, text="Закрытый ключ:")
    private_key_entry = tk.Entry(private_key_window, width=30, show='*')

    create_connection_button = tk.Button(private_key_window, text="Создать соединение",
                                         command=lambda: create_connection_with_private_key(users, connections,
                                                                                            chat_messages,
                                                                                            chat_displays,
                                                                                            existing_user_name,
                                                                                            user_secret_keys,
                                                                                            connection_windows))
    close_private_key_window_button = tk.Button(private_key_window, text="Закрыть", command=private_key_window.destroy)

    private_key_label.pack(pady=10)
    private_key_entry.pack()
    create_connection_button.pack(pady=10)
    close_private_key_window_button.pack()


def create_user_window(users, connections, chat_messages, chat_displays, user_secret_keys, connection_windows):
    user_window = tk.Toplevel(root)
    user_window.title("Создать пользователя")
    user_window.geometry("300x150")

    def create_user_and_connection(users, connections, chat_messages, chat_displays, user_secret_keys,
                                   connection_windows):
        user_name = user_name_entry.get().strip()
        if user_name:
            if user_name not in users.keys():
                if len(users) == 0:
                    p, g = generate_DH_parameters()
                    save_DH_parameters_to_file('DH_parameters.json', p, g)
                else:
                    p, g = load_DH_parameters_from_file('DH_parameters.json')
                user_private_key = generate_keys(users)
                log_action(f"Создан пользователь {user_name} с закрытым ключом {'*' * len(str(user_private_key))}")
                user_public_key = (g ** user_private_key) % p

                users[user_name] = user_public_key
                save_users_to_file(users_filename, users)
                log_action(f"{user_name} сгенерировал открытый ключ {user_public_key}")
                messagebox.showinfo("Пользователь создан",
                                    f"Пользователь {user_name} создан.\nОткрытый ключ: {user_public_key}\nЗакрытый ключ: {user_private_key}")
                create_connection_window(users, connections, chat_messages, chat_displays, user_name, user_public_key,
                                         user_private_key, user_secret_keys, connection_windows)
                user_window.destroy()
            else:
                user_window.destroy()
                create_private_key_window(users, connections, chat_messages, chat_displays, user_name, user_secret_keys,
                                          connection_windows)

        else:
            messagebox.showerror("Ошибка", "Введите имя пользователя.")

    user_name_label = tk.Label(user_window, text="Имя пользователя:")
    user_name_entry = tk.Entry(user_window, width=30)

    create_button = tk.Button(user_window, text="Создать/Войти",
                              command=lambda: create_user_and_connection(users, connections, chat_messages,
                                                                         chat_displays, user_secret_keys,
                                                                         connection_windows))
    close_button = tk.Button(user_window, text="Закрыть", command=user_window.destroy)

    user_name_label.pack(pady=10)
    user_name_entry.pack()
    create_button.pack(pady=10)
    close_button.pack()


def show_user_list(users):
    user_list_window = tk.Toplevel(root)
    user_list_window.title("Список пользователей")
    user_list_window.geometry("400x300")

    user_list_label = tk.Label(user_list_window, text="Список пользователей:")
    user_list_label.pack()

    users_data = load_users_from_file(users_filename)
    log_action("Был просмотрен список пользователей с их открытыми ключами")
    for user, data in users_data.items():
        user_info_label = tk.Label(user_list_window, text=f"Пользователь: {user}, Открытый ключ: {data}")
        user_info_label.pack()


def create_connection_window(users, connections, chat_messages, chat_displays, user1_name, user1_key, user1_private_key,
                             user_secret_keys, connection_windows):
    connection_window = tk.Toplevel(root)
    connection_window.title(f"{user1_name}")
    connection_window.geometry("600x400")
    connection_windows[user1_name] = connection_window

    def create_connection(users, connections, chat_messages, chat_displays, user1_name, user1_key, user1_private_key,
                          user_secret_keys):
        user2_key = user2_key_entry.get()
        p, g = load_DH_parameters_from_file('DH_parameters.json')
        if user1_name in users and int(user1_key) == users[user1_name]:
            if user2_key.isdigit() and int(user2_key) in users.values():
                user2_name = [name for name, key in users.items() if key == int(user2_key)][0]
                key_secret = int(user2_key) ** user1_private_key % p
                log_action(f"Пользователь {user1_name} ввел открытый ключ пользователя {user2_name}")
                log_action(f"Пользователь {user1_name} вычислил секретный ключ {'*' * len(str(key_secret))}")
                user_secret_keys[user1_name] = key_secret
                create_chat(user1_name, user2_name, chat_messages, chat_displays, user_secret_keys)
                if user1_name in connections:
                    connections[user1_name].append(user2_name)
                else:
                    connections[user1_name] = [user2_name]

                connection_window.destroy()
            else:
                messagebox.showerror("Ошибка", "Неверный ключ второго пользователя.")
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или ключ.")

    key = None

    def send_public_key(user1_name, user1_key, connection_windows):
        global key
        first_user_window = connection_windows.get(user1_name)
        if first_user_window:
            key = user1_key
        log_action(f"Пользователь {user1_name} отправил свой открытый ключ.")
        return key

    def receive_public_key(user1_key, user1_name, connection_windows):
        global key
        try:
            if key:
                second_user_window = connection_windows.get(user1_name)
                if second_user_window and key != user1_key:
                    log_action(f"Пользователь {user1_name} получил открытый ключ.")
                    user2_key_entry.delete(0, tk.END)
                    user2_key_entry.insert(0, str(key))
                    key = None
        except NameError:
            pass

    user1_name_label = tk.Label(connection_window, text="Имя первого пользователя:")
    user1_name_entry = tk.Entry(connection_window, width=30)
    user1_name_entry.insert(0, user1_name)
    user1_name_entry.config(state=tk.DISABLED)
    user1_key_label = tk.Label(connection_window, text="Открытый первого пользователя:")
    user1_key_entry = tk.Entry(connection_window, width=30)
    user1_key_entry.insert(0, user1_key)
    user1_key_entry.config(state=tk.DISABLED)
    user2_key_label = tk.Label(connection_window, text="Открытый ключ второго пользователя:")
    user2_key_entry = tk.Entry(connection_window, width=30)

    create_connection_button = tk.Button(connection_window, text="Создать соединение",
                                         command=lambda: create_connection(users, connections, chat_messages,
                                                                           chat_displays, user1_name, user1_key,
                                                                           user1_private_key, user_secret_keys))

    send_public_key_button = tk.Button(connection_window, text="Отправить открытый ключ",
                                       command=lambda: send_public_key(user1_name, user1_key, connection_windows))
    receive_public_key_button = tk.Button(connection_window, text="Получить открытый ключ",
                                          command=lambda: receive_public_key(user1_key, user1_name, connection_windows))

    def check_user_count_for_button(users, create_connection_button):
        if connection_window.winfo_exists():
            try:
                if len(users) >= 2:
                    create_connection_button.config(state=tk.NORMAL)
                else:
                    create_connection_button.config(state=tk.DISABLED)
            except KeyError:
                create_connection_button.config(state=tk.DISABLED)
            connection_window.after(1000, lambda: check_user_count_for_button(users, create_connection_button))

    check_user_count_for_button(users, create_connection_button)

    close_connection_button = tk.Button(connection_window, text="Закрыть", command=connection_window.destroy)

    user1_name_label.pack(pady=5)
    user1_name_entry.pack()
    user1_key_label.pack(pady=5)
    user1_key_entry.pack()
    user2_key_label.pack(pady=5)
    user2_key_entry.pack()
    create_connection_button.pack(pady=10)
    send_public_key_button.pack(pady=5)
    receive_public_key_button.pack(pady=5)
    close_connection_button.pack()


def are_connected(user1_name, user2_name, connections):
    if user1_name in connections[user2_name] and user2_name in connections[user1_name]:
        return True
    return False


def caesar_cipher(message, shift):
    result = ""
    rus_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    lat_alphabet = 'abcdefghijklmnopqrstuvwxyz'
    digits = '0123456789'

    for char in message:
        if char.isalpha():
            alphabet = lat_alphabet if char.lower() in lat_alphabet else rus_alphabet
            shift_amount = shift % len(alphabet)
            is_upper = char.isupper()
            shifted_char = alphabet[(alphabet.index(char.lower()) + shift_amount) % len(alphabet)]
            if is_upper:
                shifted_char = shifted_char.upper()
        elif char.isdigit():
            shift_amount = shift % 10
            shifted_char = digits[(digits.index(char) + shift_amount) % 10]
        elif char.isalnum() and not char.isdigit():
            shift_amount = shift % len(string.punctuation)  # TODO - !"#$%&'()*+, -./:;<=>?@[\]^_`{|}~
            shifted_char = string.punctuation[(string.punctuation.index(char) + shift_amount) % len(string.punctuation)]
        else:
            shifted_char = char
        result += shifted_char
    return result


def caesar_decipher(ciphertext, shift):
    result = ""
    rus_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    lat_alphabet = 'abcdefghijklmnopqrstuvwxyz'
    digits = '0123456789'

    for char in ciphertext:
        if char.isalpha():
            alphabet = lat_alphabet if char.lower() in lat_alphabet else rus_alphabet
            shift_amount = shift % len(alphabet)
            is_upper = char.isupper()
            shifted_char = alphabet[(alphabet.index(char.lower()) - shift_amount) % len(alphabet)]
            if is_upper:
                shifted_char = shifted_char.upper()
        elif char.isdigit():
            shift_amount = shift % 10
            shifted_char = digits[(digits.index(char) - shift_amount) % 10]
        elif char.isalnum() and not char.isdigit():
            shift_amount = shift % len(string.punctuation)
            shifted_char = string.punctuation[(string.punctuation.index(char) - shift_amount) % len(string.punctuation)]
        else:
            shifted_char = char
        result += shifted_char
    return result


def send_message(chat_displays, user1_name, user2_name, encrypted_message, user_secret_keys):
    if user_secret_keys.get(user1_name) is not None and user_secret_keys.get(
            user2_name) is not None and user_secret_keys.get(user1_name) == user_secret_keys.get(user2_name):
        log_action(f"Пользователь {user2_name} получил зашифрованное сообщение: {encrypted_message}")
        decrypted_message = caesar_decipher(encrypted_message, user_secret_keys.get(user2_name))
        log_action(f"Пользователь {user2_name} расшифровал зашифрованное сообщение: {decrypted_message}")

        for users, displays in chat_displays.items():
            if user1_name in users and user2_name in users:
                for display in displays:
                    if display.winfo_exists():
                        display.config(state=tk.NORMAL)
                        current_time = datetime.now().strftime("%H:%M:%S")
                        formatted_message = f"{user1_name} ({current_time}): {decrypted_message}"
                        display.insert(tk.END, f"{formatted_message}\n")
                        display.config(state=tk.DISABLED)
    else:
        log_action(f"Пользователь {user2_name} не получил сообщение")
        pair_key = (user1_name, user2_name)
        if pair_key in chat_displays:
            displays = chat_displays[pair_key]
            for display in displays:
                if isinstance(display, tk.Text) and display.winfo_exists():
                    display.config(state=tk.NORMAL)
                    current_time = datetime.now().strftime("%H:%M:%S")
                    decrypted_message = caesar_decipher(encrypted_message, user_secret_keys.get(user1_name))
                    formatted_message = f"{user1_name} ({current_time}): {decrypted_message}"
                    display.insert(tk.END, f"{formatted_message}\n")
                    display.config(state=tk.DISABLED)


def create_chat(user1_name, user2_name, chat_messages, chat_displays, user_secret_keys):
    chat_window = tk.Toplevel(root)
    chat_window.title(f"{user1_name}")
    chat_window.geometry("600x600")

    chat_display = tk.Text(chat_window, wrap=tk.WORD, state=tk.DISABLED)
    chat_display.pack(fill=tk.BOTH, expand=True)

    chat_displays.setdefault((user1_name, user2_name), []).append(chat_display)

    message_entry = tk.Entry(chat_window)
    message_entry.pack(fill=tk.X)

    def exit_button(user1_name, user2_name, connections, user_secret_keys):
        if are_connected(user1_name, user2_name, connections):
            connections[user1_name].remove(user2_name)
        chat_window.destroy()
        del chat_displays[user1_name, user2_name]
        del user_secret_keys[user1_name]
        log_action(f"Пользователь {user1_name} разорвал соединение с пользователем {user2_name}")

    def send_message_and_display(user_secret_keys):
        message = message_entry.get()
        if message:
            current_time = datetime.now().strftime("%H:%M:%S")
            encrypted_message = caesar_cipher(message, user_secret_keys.get(user1_name))
            log_action(f"Пользователь {user1_name} отправил зашифрованное сообщение: {encrypted_message}")

            chat_messages.append((user1_name, user2_name, encrypted_message))
            message_entry.delete(0, tk.END)

            send_message(chat_displays, user1_name, user2_name, encrypted_message, user_secret_keys)

    send_button = tk.Button(chat_window, text="Отправить", command=lambda: send_message_and_display(user_secret_keys))

    def check_connection(user1_name, user2_name):
        if chat_window.winfo_exists():
            try:
                if are_connected(user1_name, user2_name, connections):
                    send_button.config(state=tk.NORMAL)
                else:
                    send_button.config(state=tk.DISABLED)
            except KeyError:
                send_button.config(state=tk.DISABLED)
            chat_window.after(1000, lambda: check_connection(user1_name, user2_name))

    check_connection(user1_name, user2_name)

    send_button.pack()

    close_button = tk.Button(chat_window, text="Закрыть",
                             command=lambda: exit_button(user1_name, user2_name, connections, user_secret_keys))
    close_button.pack()


root = tk.Tk()
root.title("Diffie-Hellman")
root.geometry("950x400")
users_filename = "users.json"
users = load_users_from_file(users_filename)
connections = {}
chat_messages = []
user_secret_keys = {}
chat_displays = {}
connection_windows = {}

root.protocol("WM_DELETE_WINDOW", lambda: (save_users_to_file(users_filename, users), root.destroy()))

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Выход", command=root.destroy)

help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Справка", menu=help_menu)
help_menu.add_command(label="О программе", command=show_about)

button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, columnspan=2)

create_user_button = tk.Button(button_frame, text="Пользователь",
                               command=lambda: create_user_window(users, connections, chat_messages, chat_displays,
                                                                  user_secret_keys, connection_windows))
create_user_button.pack(side="left", padx=5)

show_user_list_button = tk.Button(button_frame, text="Показать список пользователей",
                                  command=lambda: show_user_list(users))
show_user_list_button.pack(side="left", padx=5)

show_parameters_button = tk.Button(button_frame, text="Показать параметры p и g", command=show_DH_parameters)
show_parameters_button.pack(side="left", padx=5)

log_text = Text(root, wrap=tk.WORD, width=110, height=20)
log_text.grid(row=8, column=0, columnspan=4, padx=10, pady=10)

save_logs_button = tk.Button(button_frame, text="Сохранить логи", command=save_logs_to_file)
save_logs_button.pack(side="left", padx=5)

root.mainloop()
