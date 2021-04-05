#!/usr/bin/env python3

import os, sys, re, shutil, tempfile, argparse, time, colorama

from colorama import Fore, Back, Style

log_file = list()

# print a banner
def banner():

    print("\n\n")
    print(Back.BLACK + Style.BRIGHT + Fore. BLUE + "Welcome to...")
    time.sleep(1)
    print("\n\n")
    print("                          ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    print("                          ░█▀█░█▀█░█▀█░█▀▀░█░█░█▀▄▀█░█▀▀░")
    print("                          ░█▀█░█▀▀░█▀█░█░░░█▀█░█░░░█░█▀▀░")
    print("                          ░▀░▀░▀░░░▀░▀░▀▀▀░▀░▀░▀░░░▀░▀▀▀░")
    print("                          ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    time.sleep(1)
    print("\n")
    print("Creating back-up files...")
    time.sleep(2)

# check current directory for apachme and log_files directories. Make dir if it is not there.
def apachme_dir_check():
    if os.path.isdir('./apachme') is True:
        if os.path.isdir('./apachme/log_files') is False:
            os.mkdir('apachme/log_files')
    else:
        os.mkdir('./apachme')
        os.mkdir('./apachme/log_files')

# find config files in the given directory
def conf_files(path):
    config_files = list()
    for pd, directories, files in os.walk(path):
        for file in files:
            if file.endswith('apache2.conf'):
                fname = os.path.join(pd, file)
                config_files.append(fname)
            if file.endswith('security.conf'):
                fname = os.path.join(pd, file)
                config_files.append(fname)
            if file.endswith('httpd.conf'):
                fname = os.path.join(pd, file)
                config_files.append(fname)
    return config_files

# create backups of config files (zip) and add to ./apachme/backup_config_files
def backup_files(config_file_list):
    with tempfile.TemporaryDirectory() as directory:
        for files in config_file_list:
            shutil.copy2(files, directory)
        shutil.make_archive('./apachme/backup_config_files', 'zip', directory)
    print(Back.GREEN + Fore.BLACK + '\n\nAll configuration files have been backed up and zipped inside ./apachme/backup_config_files\n')
    time.sleep(2)
    print(Back. BLACK + Style.BRIGHT + Fore.BLUE + "\n\nPracticing Safe Server...")


# check each config file for a match to the default setting
def check_file(file, content):
    re_content = r'\b' + content + r'\b'
    with open(file, 'r') as x:
        for lines in x:
            if re.match(re_content, lines):
                return True


# create a list of config files with the setting to change
def setting_change_list(f_list, setting):
    change_list = list()
    for names in f_list:
        if check_file(names, setting):
            change_list.append(names)
    return change_list

# find and replace an existing default setting with the secure setting (lines in a config file)..
# Maybe we need a new function for finding and replacing large chunks of code with (# and <)?
def find_replace(file, item, new_line):
    rewritten_file = list()
    re_item = r'\b' + re.escape(item) + r'\b'
    with open(file, 'r') as y:
        for lines in y:
            if re.match(re_item, lines):
                rewritten_file.append(new_line + '\n')
            else:
                rewritten_file.append(lines)
    try:
        with open(file, 'w+') as new_config:
            for lines in rewritten_file:
                new_config.write(lines)
    except:
        print("User cannot write to configuration files. Please run as root.\n")
        sys.exit(1)

def change_setting (w_list, setting, new_setting, set_func):
    if set_func == 'find_replace':
        for items in w_list:
            find_replace(items, setting, new_setting)
            add_to_log(items, new_setting)
    w_list.clear()
    print('\n')


# ..or add a non-existing secure setting to the config file
def add_setting(newsetting, file):
    file_str = file.pop()
    with open(file_str, 'a+') as new_config:
        new_config.write(newsetting + '\n\n')
    add_to_log(file_str, newsetting)
    print('\n')

#main function for setting changes in a config file
def change_rule(file_list, setting, new_setting, ch_setting_func):
    working_list = setting_change_list(file_list, setting)
    if not working_list:
        for x in file_list:
            if 'apache2.conf' in x:
                working_list.append(x)
                add_setting(new_setting, working_list)
            elif 'httpd.conf' in x:
                working_list.append(x)
                add_setting(new_setting, working_list)
    else:
        change_setting(working_list, setting, new_setting, ch_setting_func)
    working_list.clear()

# create log file for our changes...add to this as we change settings
def add_to_log(item, new_setting):
    global log_file
    log_line = item + ' ApachME changed your default setting to: ' + new_setting + '\n'
    return log_file.append(log_line)

def write_log(log_file):
    if log_file:
        log_name = 'apachme_changes.log'
        with open('./apachme/log_files/' + log_name, 'w+') as final_log:
            for event in log_file:
                final_log.write(event + '\n')
            print(Back.GREEN + Fore.BLACK + f"\n\nReview default setting changes in ./apachme/log_files/{log_name}")
    else:
        print("\nNo settings were changed, no log file created.\n")

# default settings to change: print statement after each change
def main():
    # Usage statement/error message/help menu
    parser = argparse.ArgumentParser()
    parser.add_argument("path/to/directory", help="provide the path to the directory that contains your default configuration files. Usually Apache config files are found in the /etc/apache2 directory")
    args = parser.parse_args()

    # take the directory of apache config files in as an argument
    directory = sys.argv[1]

    # print banner
    banner()

    # find config files in the given directory
    file_list = conf_files(directory)
    # check current directory for apachme and log_files directories. Make dir if it is not there.
    apachme_dir_check()
    # create backups of config files (zip) and add to ./apachme/backup_config_files
    backup_files(file_list)
    time.sleep(2)
#       change each setting
#       print statement of the change

#   remove server version banner: Signature
    setting = 'ServerSignature'
    new_setting = 'ServerSignature Off'
    ch_setting_func = 'find_replace'
    change_rule(file_list, setting, new_setting, ch_setting_func)
    print(Style.BRIGHT + Fore.RED + "Your vulnerable banner signature has been removed...Phew!")
    time.sleep(2)

#   remove server version banner: Tokens
    setting = 'ServerTokens'
    new_setting = 'ServerTokens Prod'
    ch_setting_func = 'find_replace'
    change_rule(file_list, setting, new_setting, ch_setting_func)
    print("Your vulnerable banner token has also been removed.  You are no longer exposing yourself.")
    time.sleep(2)

#   Etag
    setting = 'FileETag'
    new_setting = 'FileETag None'
    ch_setting_func = 'find_replace'
    change_rule(file_list, setting, new_setting, ch_setting_func)
    print("No Etag to see here because you are getting so secure!")
    time.sleep(2)

#   change timeout value configuration (10-20 sec)
    setting = 'Timeout'
    new_setting = 'Timeout 10'
    ch_setting_func = 'find_replace'
    change_rule(file_list, setting, new_setting, ch_setting_func)
    print("Your time-out value just dropped.  Take that DJ Slow Loris!")
    time.sleep(2)

#   disable trace HTTP Request
    setting = 'TraceEnable'
    new_setting = 'TraceEnable off'
    ch_setting_func = 'find_replace'
    change_rule(file_list, setting, new_setting, ch_setting_func)
    print("ApachMe just saved your cookies!")
    time.sleep(2)

#   load header module
    setting = 'LoadModule headers_module'
    new_setting = 'LoadModule headers_module modules/mod_headers.so'
    ch_setting_func = 'find_replace'
    change_rule(file_list, setting, new_setting, ch_setting_func)
    print("Loading Headers module for the remaining patches...")
    time.sleep(2)

#   set cookie with HTTPOnly and Secure flag
    setting = 'Header edit Set-Cookie'
    new_setting = 'Header edit Set-Cookie ^(.*)$ $1;HttpOnly;Secure'
    ch_setting_func = 'find_replace'
    change_rule(file_list, setting, new_setting, ch_setting_func)
    print("You may no longer be manipulated through sessions or cookies. Unless you're into that.")
    time.sleep(2)

#   implement X-FRAME-Options in HTTP headers
    setting = 'Header set X-Frame-Options'
    new_setting = 'Header always append X-Frame-Options SAMEORIGIN'
#    new_setting = 'Header set X-Frame-Options: "sameorigin"'
    ch_setting_func = 'find_replace'
    change_rule(file_list, setting, new_setting, ch_setting_func)
    print("No more drive-by clickjackings.")
    time.sleep(2)

#   x-xss protection
    setting = 'Header set X-XSS-Protection'
    new_setting = 'Header set X-XSS-Protection "1; mode=block"'
    ch_setting_func = 'find_replace'
    change_rule(file_list, setting, new_setting, ch_setting_func)
    print("Nothing to fear from XXSS.")
    time.sleep(2)

#   MIME sniffing protection
    setting = 'Header set X-Content-Type-Options'
    new_setting = 'Header set X-Content-Type-Options nosniff'
    ch_setting_func = 'find_replace'
    change_rule(file_list, setting, new_setting, ch_setting_func)
    print("No more MIMEs to sniff!\n\n")
    time.sleep(2)
    print(Fore.BLUE + Style.BRIGHT + "\n\nLocking it down...")
    time.sleep(2)


# print exit/complete statement:
#   we're done
    print(Style.BRIGHT + Fore.BLUE + f"\n\nYour Apache default configurations are now more secure!\n")
    time.sleep(2)
    print(f"\nYour original configuration files have been backed up and zipped in ./apachme/backup_config_files.zip\n")
    time.sleep(1)
#   add statement to the log file
    write_log(log_file)
    time.sleep(1)

#   user instructions for enabling headers module and restarting apache2 server
    print(Back.WHITE + Fore.BLACK + f"\n\nIn order for these changes to take effect:")
    print(f"\n\t1. Run this command to enable the headers module : a2enmod headers")
    print(f"\n\t2. Restart your Apache server : systemctl restart apache2" + Style.RESET_ALL)

    time.sleep(2)

#   user instructions for how to return to your default settings
    print(Back.BLACK + Fore.RED + f"\n\nIf you wish to return to your less secure default configurations: \n\t1. Unzip your original default config files from ./apachme/backup_config_files.zip \n\t2. Delete the more secure config files from {directory} \n\t3. Move the unzipped config files back to {directory} \n\t4. Restart your Apache server for a less secure experience\n\n")

if __name__ == "__main__":
	main()