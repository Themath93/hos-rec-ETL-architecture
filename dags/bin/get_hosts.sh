#!/bin/bash
STR=$(sed -n "7, \$p" /etc/hosts)

STR_ARRY=(`echo $STR | tr " " "\n"`)

for x in "${STR_ARRY[@]}"
do
	if [[ ! $x == *"172"*  ]]; then
		if [ ! $x == $HOSTNAME ]; then
			ssh-keyscan -t rsa $x >> ~/.ssh/known_hosts
			echo "$x has been scanned by ssh-keyscan."
		fi
	fi
done
