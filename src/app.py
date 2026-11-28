from valid8 import ValidationError
from menu import Menu, MenuHeader

class InputMismatchError(Exception):
    pass


def read_int(prompt=''):
    try:
        return int(input(prompt))
    except ValueError:
        raise InputMismatchError()
        
        
        
class App:
    def __init__(self):
        self.__running = True
        self.__menu = self.__build_menu()

    def __stop(self):
        self.__running = False

    def __build_menu(self):
        return (Menu.builder(MenuHeader('\n--- MENU ---'))
                .with_entry('Exit', self.__stop)

                .build())

    def __run_once(self):
        print('\n--- Car Sharing ---')
        print(self.__menu.textual_menu())
        try:
            self.__menu.user_choice(read_int('Enter your choice: '))
        except InputMismatchError:
            print('Invalid input. Please enter a number.')
        except (ValidationError, ValueError) as e:  # ValidationError may also be a TypeError
            print(f'Invalid data: {e}')

    def run(self):
        while self.__running:
            self.__run_once()
        print('Bye!')


def main():
    App().run()


if __name__ == '__main__':
    main()
