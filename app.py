# Copyright information
__author__ = "Vishal Verma"
__copyright__ = "Copyright (C) 2004 Vishal Verma"
__license__ = "Public Domain"
__version__ = "1.5"

from file_monitor import Monitor
import multiprocessing
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as msgt
import os
from app_data import read_json
from autostart import start
import psutil
import json
import config

monitor = Monitor()

__config_file = open(os.path.join(config.meta_folder_path,"config.json"), "r")
meta_folder_path = json.load(__config_file)["meta_folder_path"]
__config_file.close()
class Window_:
    def __init__(self):
        # Checkboxes and variables
        # Create variables
        # Defining the datatypes each widget holds
        global root
        root = Tk()
        root.wm_deiconify()
        self.root = root
        self.__create = IntVar()
        self.__delete = IntVar()
        self.__modify = IntVar()
        self.__move = IntVar()
        self.__patt = StringVar()
        self.__ign_patt = StringVar()
        self.__ign_dir = IntVar()
        self.__case_sensitive = IntVar()
        self.__refresh_rate = StringVar()
        self.__show_logs = IntVar()
        self.__auto_start = IntVar()

        # Setting the default values for the widget
        self.__create.set(1)
        self.__delete.set(1)
        self.__modify.set(1)
        self.__move.set(1)
        self.__case_sensitive.set(1)
        self.__patt.set("*")
        self.__ign_patt.set("*.log*,*.json*")
        self.__refresh_rate.set("1 sec")
        self.__show_logs.set(0)
        self.__auto_start.set(1)

        self.__started_main_process = False
        self.logbox = None
        self.log_file = os.path.join(meta_folder_path, "monitor.log")
        self.config_json_file = os.path.join(meta_folder_path, "config.json")
        self.__selected_folder = "."
        self.__start_process = None
        self.stop_but = None
        self.start_but = None

        # Creating the self.root window

    def start(self):
        self.logbox.configure(state="normal")
        self.logbox.delete('1.0', END)
        self.logbox.insert(END, "Application has started...\n")
        self.logbox.insert(END, "Logging has also started...\n\n")
        self.logbox.insert(END, f"Monitoring the folder {self.__selected_folder}\n")
        if self.__show_logs.get():
            self.logbox.insert(END, "Logging details will be displayed shortly...\n")

        if self.__auto_start.get():
            self.logbox.insert(END, "\nApplication will now be able to auto start with the server reboot...\n")
            self.logbox.insert(END, "Created monitor.json file ==> Contains configuration details\n\n")
            self.logbox.insert(END, "NOTE: Next time you will restart the app, this GUI will not appear,\n"
                                    "but the app will run in the background.\n"
                                    "This is because you have selected auto_start = True\n\n")
            self.logbox.insert(END, "NOTE: You can use monitor.json file to configure this app,\n"
                                    "or if you want to configure using this GUI,\n"
                                    "then first delete monitor.json file, and then rerun this application.\n\n")
            self.logbox.insert(END, "When you are all done with the configuration, you can close this GUI\n"
                                    "and let the app function in the background\n\n")
            self.logbox.insert(END, "You don't need to worry much as next time when the server reboots,\n"
                                    "the app will run automatically using the configurations in monitor.json file.\n\n")

        else:
            if os.path.exists(os.path.join(meta_folder_path, "monitor.json")):
                os.remove(os.path.join(meta_folder_path, "monitor.json"))

            self.logbox.insert(END, "\nNOTE: The app is not configured as auto-start.\n"
                                    "You may lose all the configurations in case the app\n"
                                    "accidentally crashes or the server reboots\n")
            self.logbox.insert(END, "\nFor now, you can close this GUI, and the app\n"
                                    "will run in the background as intended.\n\n")
        self.logbox.configure(state="disabled")

        msgt.showinfo("Crucial", "Please read the information carefully in the right window"
                                 " as that will help you in configuring.")

        if not self.__started_main_process:
            self.__start_process = multiprocessing.Process(
                target=monitor.start, args=(self.__selected_folder,
                                            self.__create.get(), self.__delete.get(), self.__modify.get(),
                                            self.__move.get(), self.__patt.get(), self.__ign_patt.get(),
                                            self.__ign_dir.get(), self.__case_sensitive.get(),
                                            self.__refresh_rate.get(), self.__show_logs.get(),
                                            self.__auto_start.get(), self.log_file, main_pid))
            self.__start_process.start()
            self.__started_main_process = True

        else:
            self.__start_process.kill()
            self.__started_main_process = True

        self.start_but["text"] = "Started"
        self.stop_but["text"] = "stop"

    def stop(self):
        self.__started_main_process = False
        self.__start_process.kill()
        self.logbox.configure(state="normal")
        self.logbox.insert(END, "Application stopped\n")
        self.logbox.insert(END, "Logging also stopped\n")
        self.logbox.configure(state="disabled")

        self.start_but["text"] = "start"
        self.stop_but["text"] = "stopped"

    def folder(self):
        self.__selected_folder = filedialog.askdirectory(initialdir=".")

    def clear_logs(self):
        try:
            self.logbox.configure(state="normal")
            self.logbox.delete('1.0', END)
            self.logbox.configure(state="disabled")
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
                self.logbox.configure(state="normal")
                self.logbox.insert(END, "Log file removed!\n")
                self.logbox.configure(state="disabled")

        except PermissionError:
            msgt.showerror("Process still running", "Please stop the process first to clear the log file and config.json file.")

    def clear_configs(self):
        try:
            self.logbox.configure(state="normal")
            self.logbox.delete('1.0', END)
            self.logbox.configure(state="disabled")

            if os.path.exists(self.config_json_file):
                os.remove(self.config_json_file)
                self.logbox.configure(state="normal")
                self.logbox.delete('1.0', END)
                self.logbox.insert(END, "config.json file removed!\n")
                self.logbox.configure(state="disabled")
        except PermissionError:
            msgt.showerror("Process still running", "Please stop the process first to clear the log file and config.json file.")


    def create_window(self):
        self.root.geometry("900x600")
        self.root.title("File monitor")

        def disable_event():
            if self.__start_process and self.__start_process.is_alive():
                if self.__auto_start.get():
                    event1 = msgt.askokcancel("Process still running",
                                         "When you close the window, the process will still be running in the background")
                    if event1:
                        self.root.destroy()
                else:
                    event2 = msgt.askokcancel("The process will end!", "Since you have not set auto-start, "
                                                                       "the process will end once you close this window\n"
                                                                       "Do you want to close?")
                    if event2:
                        self.stop()
                        self.root.destroy()
            else:
                self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", disable_event)

        log_frame = Frame(self.root)
        scrollbar = Scrollbar(self.root)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.logbox = Text(log_frame, width=300, height=100, wrap=WORD, yscrollcommand=scrollbar.set)
        self.logbox.pack(fill=BOTH, expand=True)
        log_frame.place(x=150)

        # Start and stop bottons
        self.start_but = Button(self.root, text="start", width=6, command=self.start)
        self.start_but.place(x=5, y=10)

        self.stop_but = Button(self.root, text="Stop", width=6, command=self.stop)
        self.stop_but.place(x=65, y=10)
        # Folder button
        select_folder = Button(self.root, text="select folder", command=self.folder)
        select_folder.place(x=20, y=50)
        # events handler label
        events_header = Label(self.root, text="Events", font="areal 10 underline")
        events_header.place(x=30, y=80)
        # log frame

        # Creating check buttons
        Checkbutton(self.root, text="on creation", variable=self.__create).place(x=0, y=100)

        Checkbutton(self.root, text="on deletion", variable=self.__delete).place(x=0, y=120)

        Checkbutton(self.root, text="on modify", variable=self.__modify).place(x=0, y=140)

        Checkbutton(self.root, text="on move", variable=self.__move).place(x=0, y=160)
        # divider
        Label(self.root, text="-----------------").place(x=0, y=200)

        # Pattern
        Label(self.root, text="Patt.").place(x=0, y=220)
        Entry(self.root, textvariable=self.__patt).place(x=2, y=240, width=120)
        # ignore pattern
        Label(self.root, text="Ignore Patt.").place(x=0, y=260)
        Entry(self.root, textvariable=self.__ign_patt).place(x=2, y=280, width=120)
        # igonre directory
        Checkbutton(self.root, text="Ignore dir", variable=self.__ign_dir).place(x=0, y=310)
        # Ignoring case sensitivity
        Checkbutton(self.root, text="Case-sensitive", variable=self.__case_sensitive).place(x=0, y=330)
        # Show log console
        Checkbutton(self.root, text="Show logs", variable=self.__show_logs).place(x=0, y=350)
        # Restart automatically
        Checkbutton(self.root, text="auto-start", variable=self.__auto_start).place(x=0, y=370)

        # divider
        Label(self.root, text="-----------------").place(x=0, y=400)

        Label(self.root, text="Refresh rate").place(x=0, y=420)
        Entry(self.root, textvariable=self.__refresh_rate).place(x=2, y=440, width=120)

        # Clear all
        clear_logs = Button(self.root, text="Clear logs", command=self.clear_logs)
        clear_config = Button(self.root, text="Clear configs", command=self.clear_configs)

        clear_logs.place(x=0, y=480)
        clear_config.place(x=65, y=480)

        self.root.mainloop()

if __name__ == "__main__":
    main_pid = os.getpid()
    multiprocessing.freeze_support()
    win = Window_()
    json_path = os.path.join(meta_folder_path, "monitor.json")
    if os.path.exists(json_path):
        meta_data = read_json(json_path)
        previous_mainpid = meta_data["app_related"]["PID"]
        if psutil.pid_exists(previous_mainpid):
            root.withdraw()
            event = msgt.askokcancel("Process in background",
                                     f"Already an event of this app is running in the background. PID = {previous_mainpid}\n"
                                     f"NOTE: The currently running instance can be closed through task manager.\n\n"
                                     f"Create new process?\n")
            if event:
                start(meta_data, main_pid)
        else:
            start(meta_data, main_pid)
    else:
        if not os.path.exists(meta_folder_path):
            os.mkdir(meta_folder_path)
        win.create_window()
