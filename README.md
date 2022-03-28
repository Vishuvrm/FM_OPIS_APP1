# FileMonitor_OPIS_APP1
<strong>About the application:</strong> This application is build to make the file monitoring tasks easier and automate the process of running the tasks if an even occurs. In simple terms, this application allows you to monitor a folder for any file(based on the configuration you set) and allows to set set specific set of actions when that file is received.

- To start with this application, got to Installer folder and download <b>FileMonitor_OPIS_app1_SETUP.exe</b> file. 
- After downloading the setup file, just install the application and run it in admin mode.
- You will see a GUI like this:
![image](https://user-images.githubusercontent.com/50429258/160334893-c0c8ad61-7d7a-4f0b-8388-1cea6fad7446.png)

## As you can see, this application has various configuration options:
Most of the options are self explanatory, so I will deal with the main ones here.
1. start button => When you press it, it will start the monitoring process in the background with the default configuration
  - NOTE: Always press this button after verifying the configutraion.
2. Stop button => It is used to stop the current running monitoring process in the background.
3. select folder button => Press this button to select the folder you want to monitor. By default, it is the folder in which the application is saved.
4. Events => It contains the list of events or triggers which you want to set for the files in the selected folder.
5. Patt. input field => You can set the pattern for the files in this field, and the application will only trigger on the files which have names matching the patterns you gave.
  NOTE: You can give as many patterns you want. Just separate them by a comma and space(optional)
6. Ignore Patt. => Application will ignore only those files in the folder whose name matches the pattern you mentioned in this field.
7. Ignore dir => Check it if you don't want to capture the directory creation, modification or deletion.
8. Case-sensitive => Check this if you want your pattern to be case sensitive.
9. Show logs => If checked, it will open a live log window which will show you every background process related to the application, happening in real time.
10. auto-start => If checked, next time when you start your application, it will run with the previously saved configuration and this configuration window will not appear.
11. Refresh rate => It is the time interval at which you want the application to monitor the folder.
12. Clear logs => Press this button to clear the generated logs file(monitor.log).
13. Clear configs => Press this button to clear the config.json file.(The importance of config.json file is discussed later.)

## After you are done with the configuration, press the start button.
1. You will get an info pop up. Just click OK.<br><br>
![image](https://user-images.githubusercontent.com/50429258/160337463-384997ee-3975-4123-a16f-7a3794fa18fa.png)

2. After you click ok, you will get following results:<br><br>
- This is the base application window<br>
![image](https://user-images.githubusercontent.com/50429258/160337738-e2a4be41-dd17-407c-8e85-b6eef1aa01c7.png)
- This is the log window<br>
![image](https://user-images.githubusercontent.com/50429258/160337898-22f1535d-4b8e-4662-8574-c4397a6e2197.png)


 
