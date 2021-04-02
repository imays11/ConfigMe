#!/usr/bin/env python3

import os, sys, re, shutil, tempfile, argparse, time, colorama

from colorama import Fore, Back, Style

log_file = list()

#print a banner
def banner():

    print("\n")
    print(Back.BLACK + Style.BRIGHT + Fore.BLUE + "Welcome to...")
    time.sleep(1)
    print("\n")
    print("                        _   _        __ _      __  __ ")
    print("                       | \ | | __ _ / _(_)_  _|  \/  | ___ ")
    print("                       |  \| |/ _` | |_| \ \/ / |\/| |/ _ \ ")
    print("                       | |\  | (_| |  _| |>  <| |  | |  __/ ")
    print("                       |_| \_|\__, |_| |_/_/\_\_|  |_|\___| ")
    print("                              |___/ ")
    time.sleep(1)
    print("\n")
    print("Creating back-up files...")
    time.sleep(2)

# check current directory for ngfixme and log_files directories. Make dir if it is not there.
def ngfixme_dir_check():
    if os.path.isdir('./ngfixme') is True:
        if os.path.isdir('./ngfixme/log_files') is False:
            os.mkdir('ngfixme/log_files')
    else:
        os.mkdir('./ngfixme')
        os.mkdir('./ngfixme/log_files')


# find config files in the given directory
def conf_files(path):
    config_files = list()
    for pd, directories, files in os.walk(path):
        for file in files:
            if file.endswith('nginx.conf'):
                fname = os.path.join(pd, file)
                config_files.append(fname)
    return config_files


# create backups of config files (zip) and add to ./ngfixme/backup_config_files
def backup_files(config_file_list):
    with tempfile.TemporaryDirectory() as directory:
        for files in config_file_list:
            shutil.copy2(files, directory)
        shutil.make_archive('./ngfixme/backup_config_files', 'zip', directory)
    print(Back.GREEN + Fore.BLACK + '\n\nAll configuration files have been backed up and zipped inside ./ngfixme/backup_config_files')
    time.sleep(2)
    print(Back.BLACK + Style.BRIGHT + Fore.BLUE + "\n\nPracticing Safe Server...")


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

def change_setting(w_list, setting, new_setting, set_func):
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

# main function for setting changes in a config file
def change_rule(file_list, setting, new_setting, ch_setting_func):
    working_list = setting_change_list(file_list, setting)
    if not working_list:
        for x in file_list:
            if 'nginx.conf' in x:
                working_list.append(x)
                add_setting(new_setting, working_list)
    else:
        change_setting(working_list, setting, new_setting, ch_setting_func)
    working_list.clear()

# create log file for our changes...add to this as we change settings
def add_to_log(item, new_setting):
    global log_file
    log_line = item + ' NgfixME changed your default setting to: ' + new_setting + '\n'
    return log_file.append(log_line)

def write_log(log_file):
    if log_file:
        log_name = 'ngfixme_changes.log'
        with open('./ngfixme/log_files/' + log_name, 'w+') as final_log:
            for event in log_file:
                final_log.write(event + '\n')
            print(Back.GREEN + Fore.BLACK + f"\n\nReview default setting changes in ./ngfixme/log_files/{log_name}")
    else:
        print("\nNo settings were changed, no log file created.\n")

# default settings to change: print statement after each change
def main():
    #   Usage statement/error message/help menu
    parser = argparse.ArgumentParser()
    parser.add_argument("path/to/directory", help="provide the path to the directory that contains your default configuration files. Usually Nginx config files are found in the /etc/nginx directory")
    args = parser.parse_args()

    # take the directory of ngfixme config files in as an argument
    directory = sys.argv[1]

    #   print banner
    banner()

    # find config files in the given directory
    file_list = conf_files(directory)
    # check current directory for ngfixme and log_files directories. Make dir if it is not there.
    ngfixme_dir_check()
    # create backups of config files (zip) and add to ./ngfixme/backup_config_files
    backup_files(file_list)
    time.sleep(2)
    #       change each setting
    #       print statement of the change
    # Changes:
    #   implement X-FRAME-Options in HTTP headers
    #   x-xss protection
    #   MIME sniffing protection
    #   resource control: prevent DOS buffer overflow
    #   remove server version banner: Tokens
    setting = 'http'
    new_setting = 'http {\n\tadd_header X-Frame-Options "SAMEORIGIN";\n\tadd_header X-XSS-Protection "1; mode=block";\n\tadd_header X-Content-Type-Options nosniff;\n\n\t##buffer policy\n\tclient_body_buffer_size 1K;\n\tclient_header_buffer_size 1k;\n\tclient_max_body_size 1k;\n\tlarge_client_header_buffers 2 1k;\n\t##end buffer policy\n\n\tserver_tokens off;'
    ch_setting_func = 'find_replace'
    change_rule(file_list, setting, new_setting, ch_setting_func)
    print(Style.BRIGHT + Fore.RED + "No more drive-by clickjackings!")
    time.sleep(2)
    print("Nothing to fear from XXSS!")
    time.sleep(2)
    print("No more MIMEs to sniff!")
    time.sleep(2)
    print("Buffer Overflow is now Buffer OverNO!")
    time.sleep(2)
    print("Your vulnerable banner token has also been removed. You are no longer exposing yourself.")
    time.sleep(2)
    print(Fore.BLUE + Style.BRIGHT + "\n\nLocking it down...")
    time.sleep(2)

    # print exit/complete statement:
    #   we're done

    print(Style.BRIGHT + Fore.BLUE + f"\n\nYour Nginx default configurations are now more secure!\n")
    time.sleep(2)
    print(f"\nYour original configuration files have been backed up and zipped in ./ngfixme/backup_config_files.zip\n")
    time.sleep(1)
    #   add statement to the log file
    write_log(log_file)
    time.sleep(1)

    #   user instructions for restarting nginx server
    print(Back.WHITE + Fore.BLACK + f"\n\nRestart your Nginx server for these settings to take effect: systemctl restart nginx" + Style.RESET_ALL)

    time.sleep(2)

    #   user instruction for how to return to your default settings
    print(Back.BLACK + Fore.RED + f"\n\nIf you wish to return to your less secure default configurations:")
    print("\n\t1. Unzip your original default config files from ./ngfixme/backup_config_files.zip")
    print("\n\t2. Delete the more secure config files from {directory}")
    print("\n\t3. Move the unzipped config files back to {directory}")
    print("\n\t4. Restart your Nginx server for a less secure experience.\n\n")

if __name__ == "__main__":
    main()