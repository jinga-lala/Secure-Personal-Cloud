#! /bin/bash/
echo "$2" "$1"
if [[ $1 == "en" ]]; then
	if [[ $2 == "AES" ]]; then
		openssl enc -aes-128-ctr -in "$4" -out "$5" -base64 -A -K "$3" -iv "00000000000000000000000000000000"
		# openssl enc -a -in "$5" -out "$5"".1"
		#statements
	fi
	if [[ $2 == "DES-3" ]]; then
		# echo "Making dir"
		openssl enc -des-ede3-cbc -in "$4" -out "$5" -base64 -A -K "$3" -iv "00000000000000000000000000000000"
		# openssl enc -a "$5"
		#statements
	fi
	if [[ $2 == "RC4" ]]; then
		openssl enc -rc4 -in "$4" -out "$5" -base64 -A -K "$3" 
		#statements
	fi
	# if [[ $2=="" ]]; then
	# 	#statements
	# fi
	#statements
elif [[ $1 == "de" ]]; then
	if [[ $2 == "AES" ]]; then
		# openssl enc -d -a -aes-128-ctr -in "$4" -out "$5" -K "$3" -A
		openssl enc -d -aes-128-ctr -in "$4" -out "$5" -base64 -A -K "$3" -iv "00000000000000000000000000000000"
		#statements
	fi
	if [[ $2 == "DES-3" ]]; then
		openssl enc -d -des-ede3-cbc -in "$4" -out "$5" -base64 -A -K "$3" -iv "00000000000000000000000000000000"
		#statements
	fi
	if [[ $2 == "RC4" ]]; then
		openssl enc -d -rc4 -in "$4" -out "$5" -base64 -A -K "$3" 
		#statements
	fi
fi


