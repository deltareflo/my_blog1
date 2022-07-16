# This is a sample Python script.
import datetime
import locale
# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    hoy = datetime.datetime.now()
    print(hoy.strftime('%B %d, %Y'))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
