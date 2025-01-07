from . import create_app

if __name__ == '__main__':
    connex_app = create_app()
    connex_app.run(host='0.0.0.0', port=5000, debug=True)
