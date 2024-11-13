from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from email.utils import encode_rfc2231


# Настройки почтового сервера 
class EmailSender:
    def __init__(self, sender_email, sender_password, login, smtp_server = 'smtp.mail.ru', smtp_port=465): #Конструктор класса, инициализация параметров
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.login = login
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    
    def send_mail(self, receiver_email, attachment=None, subject='Завка', body='Текст'):
        msg = MIMEMultipart() # Создваем сообщение
        msg['From'] = self.sender_email #Указываем отправителя
        msg['To'] = receiver_email # Указываем получателя 
        msg['Subject'] = subject # Указываем тему
        
        
        msg.attach(MIMEText(body, 'plain')) # Добавляем текстовоое тело сообщения
        
        if attachment:
            part = MIMEBase('application', 'octet-stream') # Создаем часть для вложения
            part.set_payload(attachment.read()) # Читаем файл
            encoders.encode_base64(part) # Кодируем файл в base64
            print(attachment.filename)
            print(attachment)
            part.add_header('Content-Disposition', f'attachment; filename*="{encode_rfc2231(attachment.filename, charset="utf-8")}"') # Заголовок но зачем??
            print(part)
            msg.attach(part) # Добавляем вложение к сообщению
                   
        
        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.login, self.sender_password) # Авторизация на SMTP сервере
                text = msg.as_string() # Преобразуем сообщение в строку
                server.sendmail(self.sender_email, [receiver_email], text) # Отправка письма
                print('Письмо отправлено')
                return 'success'
        except Exception as e:
            print('Ошибка при отправке письма: ', e)
            return 'failed'