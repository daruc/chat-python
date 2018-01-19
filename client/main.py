import tkinter


class MainWindow(tkinter.Frame):

    def __init__(self):
        super().__init__()

        self.master.title("String app")


def main():
    root = tkinter.Tk()
    root.geometry("600x700+100+0")
    MainWindow()
    root.mainloop()

if __name__ == '__main__':
    main()