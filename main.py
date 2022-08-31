""" Program entry point """
from gui import html as HtmlGui
from util.backup import Backup

def start_app_with_html():
    HtmlGui.start_gui()

if __name__ == "__main__":
    Backup().execute()
    start_app_with_html()
