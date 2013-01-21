# sneMail

## Installing
    * download source
    * edit etc/snemail.conf with appropriate database configuration
    * run ./install.py --install
        Options to the script:
        --os OSNAME     :   The script will assume 'centos' for now, if --os is not set, in the future, more options will be allowed
        --prefix PREFIX :   Sets the location in which to place the snemail executable, will assume /usr/local/bin if not set
