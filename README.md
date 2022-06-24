# weather-journal
A CLI (command-line interface) program (in python) that allows you to retrieve weather data regarding a city and store it with daily notes.

![image](https://user-images.githubusercontent.com/33736335/175537771-20345b16-a79a-496b-b055-e94575d60000.png)

### How To Use

Requirements (pip install)
```
plumbum
pyfiglet
questionary
yaml
ruamel.yaml
requests
bs4
textwrap
```

To run the program you will need to enter the weather-journal directory and run ```python3 main.py```. This journal is best experiences in Ubuntu command line.

### How it works

There are four options available.

View Weather:

![image](https://user-images.githubusercontent.com/33736335/175544400-2555187b-b7c9-4fb7-aadd-b6eeba98674a.png)

The program will ask you for a city name, and then you can input it (Shanghai is shown here as an example). It will output the temperature, time, sky, and other details.

Here is the output:

![image](https://user-images.githubusercontent.com/33736335/175548030-9d72951a-3018-4d31-9f01-1f857af07b4e.png)

Depending on where you live, you're results may be in a different language.

Write:

![image](https://user-images.githubusercontent.com/33736335/175548191-0c5e4e5e-9f4c-4aa1-a53e-a75ec43ca10d.png)

Writing allows you to combine the weather data with your own notes. Once again, it will ask you for a city, then it will ask you for a description/note. Once put it, it will be added to your entry for the day.

Read Entries:

![image](https://user-images.githubusercontent.com/33736335/175548396-3d305584-c065-40ce-b8b2-a39c37a30674.png)


You can also view entries by date by clicking on view entries and the date of entry you want to retrieve.


Any questions or bugs?

Email me at: billjz2@illinois.edu

Made originally for UIUC SOSP 2022
