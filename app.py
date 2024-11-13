from flask import Flask, request, jsonify, render_template
import mail_send #Импортируем класс для отправки писем

app = Flask(__name__) # Создаем экземпляр приложения Flask
sender = mail_send.EmailSender('vovaanime@mail.ru', 'dQ9cz8UYEY7hBBsRdne3', 'vovaanime@mail.ru') # Настройка отправителя

@app.route('/') # Декоратор для маршрута главной страницы
def index():
    return render_template('index.html') # Возвращаем HTML-шаблон формы

@app.route('/submit', methods=['POST']) # Декоратор для маршрута отправки формы/сообщения
def submit_application(): # Получаем данные из формы
    # data = request.get_json()
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    
    # Получаем вложения
    attachment = request.files.getlist('attachment') # Список вложений
    
    #Отправка письма egor2002i@mail.ru
    if sender.send_mail('vovaanime@mail.ru', subject='Новая заявка', body=f'Имя {name}\nmail: {email}\n\n{message}', attachment=attachment[0]) == 'failed':
        return jsonify({'status': 'failed'}), 500 #Ошибка
    else:
        return jsonify({'status': 'success'}), 200 #Успешно

if __name__ == '__main__':
    app.run(debug=True, port=80) # Запуск сервера на порту 80 с отладкой