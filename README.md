# ClientServer_RSA

<table>
    <tr>
        <th colspan=2>Keamanan Informasi D</th>
    </tr>
    <tr>
        <th>NRP</th>
        <th>Nama</th>
    </tr>
    <tr>
        <td>5025211121</td>
        <td>Frederick Yonatan Susanto</td>
    </tr>
</table>   

#### Dalam melakukan komunikasi di sini, saya memanfaatkan GNS-3 dan mengimplementasikan Python3.

## Topologi

![image](https://github.com/Yoyo999111222/ClientServer_DES/assets/106955551/2bf7b697-7744-4797-b01d-55fb22030313)

## Config

- **Router**
```
auto eth0
 iface eth0 inet dhcp

auto eth1
 iface eth1 inet static
 	address 10.44.1.1
 	netmask 255.255.255.0

auto eth2
 iface eth2 inet static
 	address 10.44.2.1
 	netmask 255.255.255.0
```

- **Server**
```
auto eth0
 iface eth0 inet static
 	address 10.44.1.2
 	netmask 255.255.255.0
 	gateway 10.44.1.1
```

- **Client1**
```
auto eth0
 iface eth0 inet static
 	address 10.44.2.2
 	netmask 255.255.255.0
 	gateway 10.44.2.1
```

- **Client2**
```
auto eth0
 iface eth0 inet static
 	address 10.44.2.3
 	netmask 255.255.255.0
 	gateway 10.44.2.1
```

## Setup
Pada ./bashrc menggunakan nano :

- **Server**
```
echo "nameserver 192.168.122.1" > /etc/resolv.conf
apt-get update
apt-get install python3
```

- **Client 1 dan Client2**
```
echo "nameserver 10.44.1.2
nameserver 192.168.122.1
" > /etc/resolv.conf

apt-get update
apt-get install python3
```

## Result
- **Run file server.py pada node server serta client.py pada node client1 dan client2:**

    ![Screenshot (5078)](https://github.com/Yoyo999111222/ClientServer_RSA/assets/106955551/3f30e3ba-0f77-45df-b836-8ef2fbf07d4a)
    ![Screenshot (5079)](https://github.com/Yoyo999111222/ClientServer_RSA/assets/106955551/91702742-cd93-465e-ab03-46221e86999a)
    ![Screenshot (5080)](https://github.com/Yoyo999111222/ClientServer_RSA/assets/106955551/9c0cf0c4-dbdf-4c7b-b028-76146e0ebf0e)
    ![Screenshot (5081)](https://github.com/Yoyo999111222/ClientServer_RSA/assets/106955551/1cbb7daa-a983-4e53-bd83-1ba796824923)
    ![Screenshot (5082)](https://github.com/Yoyo999111222/ClientServer_RSA/assets/106955551/82b03b8f-2565-4c23-90ff-c5862b8171ce)
    ![Screenshot (5083)](https://github.com/Yoyo999111222/ClientServer_RSA/assets/106955551/d7dbd2c4-cfa6-4f08-bcf6-28bae60de290)
    ![Screenshot (5084)](https://github.com/Yoyo999111222/ClientServer_RSA/assets/106955551/f443cb6b-3913-4e32-8867-c89189d7fd45)
    ![Screenshot (5087)](https://github.com/Yoyo999111222/ClientServer_RSA/assets/106955551/89e0a75a-8db1-44a6-a193-e78f64e12142)


