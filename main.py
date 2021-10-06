import signal
import logging
import os
import argparse

class DelayedKeyboardInterrupt:

    def __enter__(self):
        self.signal_received = False
        self.old_handler = signal.signal(signal.SIGINT, self.handler)
                
    def handler(self, sig, frame):
        self.signal_received = (sig, frame)
        logging.debug('SIGINT received. Delaying KeyboardInterrupt.')
    
    def __exit__(self, type, value, traceback):
        signal.signal(signal.SIGINT, self.old_handler)
        if self.signal_received:
            self.old_handler(*self.signal_received)


with DelayedKeyboardInterrupt():
    pacmanCmd = "sudo pacman -Syu"
    aptCmd = "sudo apt update"
    sudoPromptCmd = "[sudo]: password for "

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--terminal", help = "Default text to display on the beginning of every line")
    parser.add_argument("-u", "--user", help = "Name of the host user")
    parser.add_argument("-m", "--packageManager", help = "Package manager that the host OS uses")
    parser.add_argument("-b", "--breakCommand", help = "Command to exit the fake terminal")


    args = parser.parse_args()
    if not args.terminal or not args.packageManager or not args.breakCommand or not args.user:
        print("Missing arguments - type [--help] to display help.")
        quit()
    else:
        args.terminal += " "
        os.system("clear")
        if args.packageManager == "apt":
            print(args.terminal + aptCmd)
            print(sudoPromptCmd + args.user + ":")
            print(open("aptOutput.txt").read())
        elif args.packageManager == "pacman":
            print(args.terminal + pacmanCmd)
            print(sudoPromptCmd + args.user + ":")
            print(open("pacmanOutput.txt").read())

        while True:
            code = input(args.terminal)
            if code == args.breakCommand:
                quit()
            else:
                print("Ne. :)")