# Page Finder Python 3 Script

Python3 script that searches for a few interesting web pages. This script is currently hard coded to search only on ports 8080 and 10250, but that can easily be modified in the code.

-------------------------

This script works in the following way:

1. Attempts a socket connection to hosts in the provided IP range
2. Builds a list of all hosts it was able to successfully connect to port 8080 on as well as port 10250 on
3. For each host in each list (#3 above), the script searches for the following interesting pages:

*Jenkins unauthenticated script console page (/script)

*Tomcat HTML Manager page (/manager/html)

*Tomcat Text Manager page (/manager/text)

*/Console page (such as what is used by the Werkzeug debugger)

*/Command page (any interesting pages)

*/Kuberntes nodes with system:anonymous viewing of the /pods page

--------------------------
Usage:

-pip3 install -r requirements.txt

-python3 -W ignore page-finder.py -r [range] -t [threads]

