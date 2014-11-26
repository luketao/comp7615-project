wget http://www.pax-pentest.net/wp-content/uploads/2014/05/ipsec.txt -O ipsec.py
mv ipsec.py /usr/lib/python2.7/dist-packages/scapy/layers
echo "load_layer('ipsec')" > ~/.scapy_startup.py
