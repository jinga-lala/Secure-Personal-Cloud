read -p "Enter the path for installation (Default is ~/) '\n'" path
echo "$path"
# cp -R Secure_Personal_Cloud "$path"
alias_bash="alias spc=python3 $path/Secure-Personal-Cloud/linux/main.py"
# echo "$alias_bash"
echo "$alias_bash" >> ~/.bashrc
pip3 install requests
pip3 install json
pip3 install time
pip3 install pickle
pip3 install os
pip3 install subprocess
pip3 install pycryptodome
pip3 install shutil
pip3 install getpass
pip3 install difflib
echo "Run server, then run script"