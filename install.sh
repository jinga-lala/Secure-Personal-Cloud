read -p "Enter the complete path for installation '\n'" path
echo "$path"
echo "Copying files"
cp -R Secure_Personal_Cloud "$path"
alias_bash="alias spc='python3 $path/Secure_Personal_Cloud/linux/main.py'"
echo "Creating man pages"
chmod 777 "$path/Secure_Personal_Cloud/*"
sudo cp ./Secure_Personal_Cloud/manual.1 /usr/share/man/man1/
sudo mandb
# echo "$alias_bash"
echo "$alias_bash" >> ~/.bashrc
echo "Installing python packages"
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
pip3 install django
pip3 install djangorestframework
pip3 install hashlib
echo "Server instructions"
echo "Run server, then run script server_refresh.py"

p1="$path""/Secure_Personal_Cloud/scheduler.sh"
p2="$path""/Secure_Personal_Cloud/sharer.sh"
# Put in crontab 
echo "Installing crontabs"
echo "0 */2 * * * $p1 $path" >>"$path""/mycron"
echo "*/20 * * * * $p2 $path">> "$path""/mycron"
crontab "$path""/mycron"
rm "$path""/mycron"
# rm -rf ./Secure_Personal_Cloud

