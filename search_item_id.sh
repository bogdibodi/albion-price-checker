#!/bin/bash
VAL=""
awk -v item="$1" '$0 ~ item {print $2}' items.txt
