import tkinter
from resources import StringsRegister
from resources import ConfigRegister
import client


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
    main_window = MainWindow(strings_register)

    language_str = strings_register['language_label']
    language_label = tkinter.Label(root, text=language_str)
    language_label.grid(row=0, column=0)

    language_str = tkinter.StringVar()
    language_names_list = config_register['languages_list']
    language_str.set(language)

    def on_language_change(value):
        config_register['language'] = value
        config_register.save()
        nonlocal strings_register
        strings_register = StringsRegister(value)
        language_label['text'] = strings_register['language_label']
        nick_label['text'] = strings_register['nickname'] + ': ' + config_register['nickname']
        room_label['text'] = strings_register['room_label']
        nick_change_button['text'] = strings_register['nick_change_button']
        send_button['text'] = strings_register['send_button']
        MainWindow(strings_register)

    languages_list = tkinter.OptionMenu(root, language_str, *language_names_list, command=on_language_change)
    languages_list.grid(row=0, column=1)

    nick_str = strings_register['nickname'] + ': ' + config_register['nickname']
    nick_label = tkinter.Label(root, text=nick_str)
    nick_label.grid(row=1, column=0)

    nick_str = tkinter.StringVar()
    nick_str.set(config_register['nickname'])
    nick_entry = tkinter.Entry(root, textvariable=nick_str)
    nick_entry.grid(row=1, column=1)

    def on_nick_change():
        config_register['nickname'] = nick_entry.get()
        config_register.save()
        nick_label['text'] = strings_register['nickname'] + ': ' + config_register['nickname']

    nick_change_str = strings_register['nick_change_button']
    nick_change_button = tkinter.Button(root, text=nick_change_str, command=on_nick_change)
    nick_change_button.grid(row=1, column=2)

    room_str = strings_register['room_label']
    room_label = tkinter.Label(root, text=room_str)
    room_label.grid(row=2, column=0)

    room_names_list = client.get_rooms()
    room_number = 1

    def on_selecting(value):
        print(value)
        for idx, room in enumerate(room_names_list):
            if room == value:
                nonlocal room_number
                room_number = idx + 1
                break
        refresh()

    default_room = tkinter.StringVar(root)
    default_room.set(room_names_list[0])
    rooms_list = tkinter.OptionMenu(root, default_room, *room_names_list, command=on_selecting)
    rooms_list.grid(row=2, column=1)

    text_area = tkinter.Text(root, state=tkinter.DISABLED)
    text_area.grid(row=3, column=0, columnspan=3)

    input_area = tkinter.Text(root)
    input_area.grid(row=4, column=0, columnspan=3)

    def on_sending():
        message = input_area.get('1.0', tkinter.END)
        client.send(room_number, message)
        input_area.delete(1.0, tkinter.END)
        root.after(200, refresh)

    send_str = strings_register['send_button']
    send_button = tkinter.Button(root, text=send_str, command=on_sending)
    send_button.grid(row=5, column=0, columnspan=3)

    def on_closing():
        config_register['window_size'] = root.geometry()
        config_register.save()
        root.destroy()

    root.protocol('WM_DELETE_WINDOW', on_closing)

    def refresh():
        new_content = client.get(room_number)
        current_content = text_area.get("1.0", tkinter.END)

        if new_content.strip() != current_content.strip():
            print('refresh')
            text_area.config(state=tkinter.NORMAL)
            text_area.delete("1.0", tkinter.END)
            text_area.insert(tkinter.END, new_content)
            text_area.see(tkinter.END)
            text_area.config(state=tkinter.DISABLED)

    def repeat_refresh():
        refresh()
        root.after(1300, repeat_refresh)

    root.after(0, repeat_refresh)
    root.mainloop()


if __name__ == '__main__':
    main()
