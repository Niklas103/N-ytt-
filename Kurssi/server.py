# Tätä waitressia käytetään jos on Renderiä varten konfiguroitu, että
# käytössä on guvicorn, joka taas ei toimi Windowsissa.

from waitress import serve

from Kurssi.wsgi import application

if __name__ == '__main__':
    print("Open browser in https://localhost:8000")
    print("Shut down server with 'control + c'")
    serve(application, port='8000')