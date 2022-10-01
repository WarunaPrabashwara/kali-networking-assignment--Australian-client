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
    print( res.raw )
    with open( bingmapfile , 'wb') as outfile:
        outfile.write( res.content )

firstone()
