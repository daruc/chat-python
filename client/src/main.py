"""Main module of the client application.
Creates GUI and invokes back-end modules."""

import tkinter
from resources import StringsRegister
from resources import ConfigRegister
import client


def main():
    """Creates GUI and sends requests to server via other modules."""

    config_register = ConfigRegister.get_instance()
    strings_register = StringsRegister(config_register['language'])

    root = tkinter.Tk()

    root.geometry(config_register['window_size'])
    create_main_frame(strings_register, root)

    widgets = dict()

    widgets['language_label'] = tkinter.Label(root, text=strings_register['language_label'])
    widgets['language_label'].grid(row=0, column=0)

    def on_language_change_adapter(value):
        """Invokes changing language"""

        on_language_change(config_register, widgets, root, value)

    widgets['languages_list'] = tkinter.OptionMenu(root, create_language_string(config_register),
                                                   *config_register['languages_list'],
                                                   command=on_language_change_adapter)

    widgets['languages_list'].grid(row=0, column=1)

    widgets['nick_label'] = tkinter.Label(root, text=create_nickname_label(strings_register,
                                                                           config_register))
    widgets['nick_label'].grid(row=1, column=0)

    widgets['nick_entry'] = tkinter.Entry(root, textvariable=create_nick_string(config_register))
    widgets['nick_entry'].grid(row=1, column=1)

    def on_nick_change():
        """Changes users nickname."""

        config_register['nickname'] = widgets['nick_entry'].get()
        config_register.save()
        widgets['nick_label']['text'] = create_nickname_label(strings_register, config_register)

    widgets['nick_change_button'] = tkinter.Button(root,
                                                   text=strings_register['nick_change_button'],
                                                   command=on_nick_change)
    widgets['nick_change_button'].grid(row=1, column=2)

    widgets['room_label'] = tkinter.Label(root, text=strings_register['room_label'])
    widgets['room_label'].grid(row=2, column=0)

    room_names_list = client.get_rooms()
    room_number = 1

    def on_selecting(value):
        """Changes chosen chat room."""

        for idx, room in enumerate(room_names_list):
            if room == value:
                nonlocal room_number
                room_number = idx + 1
                break
        refresh()

    default_room = tkinter.StringVar(root)
    default_room.set(room_names_list[0])
    widgets['rooms_list'] = tkinter.OptionMenu(root, default_room, *room_names_list,
                                               command=on_selecting)
    widgets['rooms_list'].grid(row=2, column=1)

    widgets['text_area'] = tkinter.Text(root, state=tkinter.DISABLED)
    widgets['text_area'].grid(row=3, column=0, columnspan=3)

    widgets['input_area'] = tkinter.Text(root, height=10)
    widgets['input_area'].grid(row=4, column=0, columnspan=3)

    def on_sending():
        """Sends message to server."""

        message = widgets['input_area'].get('1.0', tkinter.END)
        client.send(room_number, message)
        widgets['input_area'].delete(1.0, tkinter.END)
        root.after(200, refresh)

    widgets['send_button'] = tkinter.Button(root, text=strings_register['send_button'],
                                            command=on_sending)
    widgets['send_button'].grid(row=5, column=0, columnspan=3)

    def on_closing():
        """Saves configuration and closes application."""

        config_register['window_size'] = root.geometry()
        config_register.save()
        root.destroy()

    root.protocol('WM_DELETE_WINDOW', on_closing)

    def refresh():
        """Refreshes state of the chat of the current room."""

        new_content = client.get(room_number)
        current_content = widgets['text_area'].get("1.0", tkinter.END)

        if new_content.strip() != current_content.strip():
            widgets['text_area'].config(state=tkinter.NORMAL)
            widgets['text_area'].delete("1.0", tkinter.END)
            widgets['text_area'].insert(tkinter.END, new_content)
            widgets['text_area'].see(tkinter.END)
            widgets['text_area'].config(state=tkinter.DISABLED)

    def repeat_refresh():
        """Plans new invoke of the refresh function."""

        refresh()
        root.after(1300, repeat_refresh)

    root.after(0, repeat_refresh)
    root.mainloop()


def create_main_frame(strings_register, root):
    """Creates main application window and sets title."""

    main_window = tkinter.Frame()
    root.title(strings_register['main_window_title'])
    return main_window


def create_nickname_label(strings_register, config_register):
    """Returns joined \"Nickname: \" with user's nickname."""

    return strings_register['nickname'] + ': ' + config_register['nickname']


def create_language_string(config_register):
    """Creates tkinter.StringVar with selected language."""

    language_string = tkinter.StringVar()
    language_string.set(config_register['language'])
    return language_string


def create_nick_string(config_register):
    """Creates tkinter.StringVar with nickname."""

    nick_str = tkinter.StringVar()
    nick_str.set(config_register['nickname'])
    return nick_str


def on_language_change(config_register, widgets, root, value):
    """Changes language of the UI."""

    config_register['language'] = value
    config_register.save()
    strings_register = StringsRegister(value)
    widgets['language_label']['text'] = strings_register['language_label']
    widgets['nick_label']['text'] = \
        strings_register['nickname'] + ': ' + config_register['nickname']
    widgets['room_label']['text'] = strings_register['room_label']
    widgets['nick_change_button']['text'] = strings_register['nick_change_button']
    widgets['send_button']['text'] = strings_register['send_button']
    create_main_frame(strings_register, root)


if __name__ == '__main__':
    main()
