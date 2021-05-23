#!/bin/sh
# echo "$@"
# echo "$#"

if [ "$#" -eq 2 ];then
	python 2018201053_1.py "$@"
elif [ "$#" -eq 1 ];then 
	python 2018201053_2.py "$@"
else
	echo "Pass valid number of arguments"
fi