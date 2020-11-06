commandArray = {}

if (devicechanged['green'] == 'On')  then
    os.execute ('curl -s -k "https://familievisser.ddns.net/json.htm?username=QWRtaW4=&password=V2FsdmlzaW5kZXplZTIw&type=command&param=switchlight&idx=8&switchcmd=Off"')
end



return commandArray
