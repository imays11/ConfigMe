# Harden WebServer Configuration Files
These command line tools aim to make Apache and Nginx Web Servers more secure by replacing insecure default configuration files with more secure settings. 

Right now this suite supports Ubuntu/Debian users but as the project grows we intend to support more operating systems and other open-source web servers. 

Best practices were based on the Center for Internet Security's Benchmark Configuration Guidelines found here: [https://www.cisecurity.org/cis-benchmarks/]    

While these scripts are a good first step in hardening your server, we suggest you refer to the Benchmark Configuration Guides to further secure your system. 

##ApachMe
ApachMe is a user-friendly Python script that will harden the configuration settings of your default Apache web server. 

**Requirements:** 
    
    - Sudo/Root permissions to write to configuration files
    - Python3 and the following modules: os, colorama, time. 
    - Apache Headers module which will need to be enabled after running the script.

###**Usage** 
ApachMe takes in your path to the directory hosting your configuration files as an argument. It is important that you do not include a specific configuration file in the path, instead you provide the directory that holds the configuration files as we will need to collect more than one file for your system. Your configuration files will likely be in /etc/apache2.

    $ sudo python3 apachme.py /etc/apache2      #script will run and show output along the way
    
    $ sudo a2enmod headers                      #enable Apache headers module
    
    $ sudo systemctl restart apache2            #restart your Apache server

##NgFixMe
NgFixMe is a user-friendly Python script that will harden the configuration settings of your default Nginx web server. 

**Requirements:** 
    
    - Sudo/Root permissions to write to configuration files
    - Python3 and the following modules: os, colorama, time. 

###**Usage** 
NgFixMe takes in your path to the directory hosting your configuration files as an argument. It is important that you do not include a specific configuration file in the path, instead you provide the directory that holds the configuration file. Your configuration file will likely be in /etc/nginx.

    $ sudo python3 ngfixme.py /etc/nginx      #script will run and show output along the way
     
    $ sudo systemctl restart nginx            #restart your Nginx server


##Authors
Isai Mays and Kathy Collins authored these scripts. 
A demonstration of this project by its creators can be found here:
