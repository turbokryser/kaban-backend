import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings
from app.logging_config import logger


async def send_activation_email(email: str, username: str, activation_token: str):
    """
    Отправляет email с ссылкой активации аккаунта через Mail.ru SMTP
    """
    # Формируем ссылку активации
    activation_url = f"{settings.FRONTEND_URL}/auth/activate?token={activation_token}"
    
    # Создаем письмо
    message = MIMEMultipart("alternative")
    message["Subject"] = "Подтверждение регистрации в Kaban X"
    message["From"] = settings.SMTP_FROM_EMAIL
    message["To"] = email
    
    # HTML версия письма
    html_content = f"""
    <html>
      <body>
        <h2>Здравствуйте, {username}!</h2>
        <p>Спасибо за регистрацию в Kaban X.</p>
        <p>Для активации вашего аккаунта, пожалуйста, перейдите по следующей ссылке:</p>
        <p><a href="{activation_url}">{activation_url}</a></p>
        <p>Ссылка действительна в течение 24 часов.</p>
        <p>Если вы не регистрировались в Kaban X, просто проигнорируйте это письмо.</p>
        <br>
        <p>С уважением,<br>Команда Kaban X</p>
      </body>
    </html>
    """
    
    # Текстовая версия письма
    text_content = f"""
    Здравствуйте, {username}!
    
    Спасибо за регистрацию в Kaban X.
    
    Для активации вашего аккаунта, пожалуйста, перейдите по следующей ссылке:
    {activation_url}
    
    Ссылка действительна в течение 24 часов.
    
    Если вы не регистрировались в Kaban X, просто проигнорируйте это письмо.
    
    С уважением,
    Команда Kaban X
    """
    
    # Добавляем обе версии в письмо
    text_part = MIMEText(text_content, "plain", "utf-8")
    html_part = MIMEText(html_content, "html", "utf-8")
    
    message.attach(text_part)
    message.attach(html_part)
    
    try:
        # Подключаемся к SMTP серверу Mail.ru
        logger.debug(f"Connecting to SMTP server: {settings.SMTP_HOST}:{settings.SMTP_PORT}")
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()  # Включаем TLS шифрование
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_FROM_EMAIL, email, message.as_string())
        logger.info(f"Activation email sent successfully to: {email}")
        return True
    except Exception as e:
        logger.error(f"Error sending activation email to {email}: {str(e)}", exc_info=True)
        return False


async def send_reset_password_email(email: str, username: str, reset_token: str):
    """
    Отправляет email со ссылкой для восстановления пароля через Mail.ru SMTP.
    """
    reset_url = f"{settings.FRONTEND_URL}/auth/reset-password?token={reset_token}"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Сброс пароля в Kaban X"
    message["From"] = settings.SMTP_FROM_EMAIL
    message["To"] = email

    html_content = f"""
    <html>
      <body>
        <h2>Здравствуйте, {username}!</h2>
        <p>Поступил запрос на смену пароля в Kaban X.</p>
        <p>Чтобы задать новый пароль, перейдите по ссылке:</p>
        <p><a href="{reset_url}">{reset_url}</a></p>
        <p>Ссылка действительна 1 час.</p>
        <p>Если вы не запрашивали смену пароля, просто проигнорируйте это письмо.</p>
        <br>
        <p>С уважением,<br>Команда Kaban X</p>
      </body>
    </html>
    """

    text_content = f"""
    Здравствуйте, {username}!

    Поступил запрос на смену пароля в Kaban X.

    Чтобы задать новый пароль, перейдите по ссылке:
    {reset_url}

    Ссылка действительна 1 час.

    Если вы не запрашивали смену пароля, просто проигнорируйте это письмо.

    С уважением,
    Команда Kaban X
    """

    text_part = MIMEText(text_content, "plain", "utf-8")
    html_part = MIMEText(html_content, "html", "utf-8")

    message.attach(text_part)
    message.attach(html_part)

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_FROM_EMAIL, email, message.as_string())
        return True
    except Exception as e:
        print(f"Ошибка при отправке email: {e}")
        return False

