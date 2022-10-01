import subprocess
import requests

bingmapfile = 'map.png'
ftpin = "ftp_inventory.txt"
httpinv = "http_inventory.txt"


"""
Question 1
"""
def firstone():
    res = requests.get('http://dev.virtualearth.net/REST/v1/Imagery/Map/Road/-16.9206560000013,145.777730700002/15?mapSize=500,500&key=AlcGIVqXiv8dcy8S47kNuk5ny62Jlcp_N5wJflZV6SzyWAfAN74toaGHN8ma_EGt' )
    #print( res.raw )
    with open( bingmapfile , 'wb') as outfile:
        outfile.write( res.content )



"""
Question 2
"""

def coommon( grep_var , create_or_check , lines =[] ):
    ipofinterfc = subprocess.check_output(" ip a |  grep -E  '([0-9]{1,3}[\.]){3}[0-9]{1,3}'  ", shell=True).decode().split("\n")
    for i in range( len(ipofinterfc)) :
        if i > 0 and  i < len(ipofinterfc) -1 :
            try:
                var = ipofinterfc[i].split("inet ")[1].split(" ")[0]
                validiplist = "nmap -sn "+ var + " |  grep -E  '([0-9]{1,3}[\.]){3}[0-9]{1,3}' "
                valdip = subprocess.check_output( validiplist  , shell=True).split("\n")
                for j in range ( len( valdip)) :
                    if j > 0 and j < len( valdip )- 1 :
                        hostips = valdip[j].split(" ")[4]    
                        grepServ = " nmap  -sV -O "+ hostips + " |grep " + grep_var + "  ; exit 0  "
                        grepservice =  subprocess.check_output( grepServ  , stderr=subprocess.STDOUT,  shell=True )
                        if grepservice != "" :
                                grepservice = grepservice.split("\n")
                                for k in range( len( grepservice)):
                                    if k < len((grepservice)) -1 :
                                        ipAndServ = hostips + " : " + grepservice[0] 
                                        if create_or_check == "create"  and grep_var == "ftp" :
                                            subprocess.check_output("echo '"+ ipAndServ + "' >> " + ftpin +"  ; exit 0 ", stderr=subprocess.STDOUT , shell=True  )
                                        if create_or_check == "check" and grep_var == "ftp":
                                            if ipAndServ not in lines :
                                                print( ipAndServ  +"                is not an allowed ftp server")
                                            if grepservice[0].split(" ")[-1] == "2.3.4" :
                                                print( "Server with ip  "  + hostips + " has ftp version 2.3.4" )
                                        if create_or_check == "create" and grep_var == "'open  http'":  
                                                subprocess.check_output("echo '"+ ipAndServ + "' >> " + httpinv +"  ; exit 0 ", stderr=subprocess.STDOUT , shell=True  )  
                                        if create_or_check == "check" and grep_var == "'open  http'":
                                            if ipAndServ not in lines :
                                                print( ipAndServ  +"     http server is not allowed")


                                                str = "ssh root@"+hostips+" apachectl status |grep Status"
                                                output = subprocess.check_output(str  , shell=True  )
                                                if  output.split("requests/sec: ")[1].split("; Current")[0]  == "0" :
                                                    print( "Server with ip " + hostips + " has zero idle workers")



                                                url = 'http://'+ hostips +'/DVWA/login.php'
                                                s = requests.Session()
                                                x = s.post(url)
                                                if x.status_code == 200:
                                                    print("THe server " + hostips + " contains a DVWA. Trying to login  with uname : admin and password: password ") 
                                                    pattern = r'\b\w{32}\b'
                                                    result =  re.findall( pattern , x.text    )
                                                    myobj = {'username': 'admin' , 'password': 'password', 'user_token': result[0]  ,  'Login': 'Login'  }
                                                    m = s.post( url , data  =  myobj  )
                                                    try:
                                                        re.search( 'take responsibility for the way in which any', m.text).group(0)  
                                                        print("Login was successful")
                                                    except AttributeError:
                                                        print("Login was failed")    
            except:
                continue




def Q2P1() :
    subprocess.check_output(" > " + ftpin + " ", shell=True)
    coommon( "ftp" , "create")
     

def Q2P2():
    lines = []
    with open( ftpin ) as file:
        for line in file:
                lines.append(line.rstrip())
    coommon( "ftp" , "check" , lines )




"""
Question 3
"""

def Q3P1() :
    subprocess.check_output(" > " + httpinv + "  ", shell=True)
    coommon( "'open  http'" , "create")

def Q3P2():
    lines = []
    with open( httpinv ) as file:
        for line in file:
                lines.append(line.rstrip())
    coommon( "'open  http'" , "check")

  



print(" please enter \n1 to make the bing map \n2 to make the input ftp inventory file \n3 to check the network with the ftp file \n4 to create the http inventory file \n5 to check the network with the http inventory file")
choice = input().lower()
if choice == "1":
   print("please wait for a few minutes") 
   firstone()
elif choice == "2" :
   print("please wait for a few minutes") 
   Q2P1()
elif choice == "3" :
   print("please wait for a few minutes") 
   Q2P2()
elif choice == "4" :
   print("please wait for a few minutes") 
   Q3P1()
elif choice == "5" :
   print("please wait for a few minutes") 
   Q3P2()
else:
   print("please provide valid input")


