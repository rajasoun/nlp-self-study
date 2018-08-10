chkconfig b2b-trinity
if [ $? -eq 0 ]; then
    service b2b-trinity stop
fi
