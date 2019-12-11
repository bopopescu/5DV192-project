from . import app_main


@app_main.route('/')
def main_route():
    return "Hello World!"
