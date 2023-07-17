import logging
import Environment_variables
import smtplib
import ssl
from email.mime.text import MIMEText
from http.server import BaseHTTPRequestHandler, HTTPServer

# logging.basicConfig(filename='vertex.log', level=logging.INFO,
#                     format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S')


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formater = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                             datefmt='%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler('vertex.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formater)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formater)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


# TIMEZONE = 'Asia/Tel_Aviv'  # Replace with your actual timezone
# LOG_FILENAME = 'vertex.log'


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            log_message = 'Received GET request'
            logger.info(log_message)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello, world!')
        except Exception as e:
            error_message = f'Error occurred while handling GET request: {str(e)}'
            logger.error(error_message)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'Something went wrong')

def send_error_email(error_message):
    subject = 'Error occurred in server'
    body = f'The following error occurred while handling a GET request:\n\n{error_message}'

    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = Environment_variables.Email_ID
    message['To'] = Environment_variables.Email_ID

    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login(Environment_variables.Email_ID, Environment_variables.Password)
        smtp_server.send_message(message)
        smtp_server.quit()
        logger.info('Error notification email sent')
    except Exception as e:
        logger.error(f'Failed to send error notification email: {str(e)}')


def send_startup_email():
    logger.info('Sending startup notification email...')
    Password =Environment_variables.Password
    subject = 'Server Started'
    body = 'The server has been started successfully.'
    send_startup_email = ssl.create_default_context()
    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = Environment_variables.Email_ID
    message['To'] = Environment_variables.Email_ID

    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls(context=send_startup_email)
        smtp_server.login(Environment_variables.Email_ID, Environment_variables.Password)
        smtp_server.send_message(message)
        smtp_server.quit()
        logger.info('Startup notification email sent')
    except Exception as e:
        logger.error(f'Failed to send startup notification email: {str(e)}')


def run_server():
    server_address = ('',3000)
    httpd = HTTPServer(server_address, RequestHandler)
    logger.info('Starting server...')
    send_startup_email()
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()