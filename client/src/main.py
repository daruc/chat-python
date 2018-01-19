import tkinter
from resources import StringsRegister
from resources import ConfigRegister


class MainWindow(tkinter.Frame):

    def __init__(self, strings_register):
        super().__init__()

        title = strings_register['main_window_title']
        self.master.title(title)


def main():
    config_register = ConfigRegister.get_instance()
    language = config_register['language']
    strings_register = StringsRegister(language)

    root = tkinter.Tk()
    window_size = config_register['window_size']
    root.geometry(window_size)
    MainWindow(strings_register)

    def on_closing():
        config_register['window_size'] = root.geometry()
        config_register.save()
        root.destroy()

    root.protocol('WM_DELETE_WINDOW', on_closing)
    root.mainloop()


if __name__ == '__main__':
    main()
