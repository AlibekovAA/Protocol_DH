### Структура 

 - log_action(): Записывает действия в главном меню.
 - save_logs_to_file(): Сохраняет содержимое виджета Text (логи) в текстовый файл.
 - show_about(): Отображает информацию о программе.
 - primRoots(modulo): Находит первообразные корни по модулю modulo.
 - generate_DH_parameters(): Генерирует параметры p и g для протокола Диффи-Хеллмана (p - простое число, g - первообразный корень по модулю p).
 - save_DH_parameters_to_file(): Сохраняет параметры p и g в файл.
 - load_DH_parameters_from_file(): Загружает параметры p и g из файла.
 - show_DH_parameters(): Отображает параметры p и g на экране.
 - generate_keys(): Генерирует закрытый ключ пользователя.
 - save_users_to_file(): Сохраняет информацию о пользователях в файл(Имя пользователя и его открытый ключ).
 - load_users_from_file(): Загружает информацию о пользователях из файла.
 - create_private_key_window(): Создает окно для ввода закрытого ключа пользователя, если такой пользователь существует.
 - create_user_window(): Создает окно для создания нового пользователя или входа существующего.
 - show_user_list(): Отображает список пользователей и их открытые ключи.
 - create_connection_window(): Создает окно для создания соединения между пользователями.
 - are_connected(): Проверяет, соединены ли два пользователя.
 - caesar_cipher(): Шифрует сообщение с помощью шифра Цезаря.
 - caesar_decipher(): Расшифровывает сообщение, зашифрованное шифром Цезаря.
 - send_message(): Отправляет и отображает зашифрованное сообщение между пользователями.
 - create_chat(): Создает окно чата между двумя пользователями.

### Работа программы

 - При первом запуске и создания первого пользователя генерируются параметры p и g. Появляется окно с именем, открытым и приватным ключом пользователя. После закрытия этого окна приватный ключ знает только пользователей. А открытый ключ и параметры можно просмотреть.
 - Реализована возможность отправлять свой открытый ключ и получать открытый ключ второго пользователя.
 - Если попытаться второй раз зайти под существующем пользователем будет запрошен приватный ключ. При неправильном вводе вычисленные секретные ключи будут не совпадать и сообщения не будут отправлятся между пользователями.
 - В виджете Text отобразаться логи, которые можно листать вниз-вверх.
 - При нажатии на сохранить логи откроется окно для ввода имени текстового файла. Расширение .txt припишется автоматически.  


### Запуск из исходников
 - Переходим в папку "Алибеков_курсовая_работа" с помощью cd <путь к папке>
 - Создаем виртуальное окружение

    python -m venv venv
    или
    python3 -m venv vevn

 - Активируем виртуальное окружение

  В Unix подобных системах

  source venv/bin/activate

  В Windows 

  .\venv\Scripts\activate 

 - Устанавливаем список нужных зависимостей

  - pip install -r requirements.txt

  - Запускаем код

    python Diffi-Helmann.py
    Или 
    python3 Diffi-Helmann.py

