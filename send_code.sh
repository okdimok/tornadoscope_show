cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" 

lftp -u tornadoscope,tornadoscope -p 2121 192.168.11.93 <<EOF
mirror -R . .
bye
EOF
