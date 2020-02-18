from blog import app  # this file use app.run() so import app here
import os


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    # print(app.config['MAIL_USERNAME'])
    # print(app.config['MAIL_PASSWORD'])
