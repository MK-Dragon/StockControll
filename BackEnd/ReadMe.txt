How to Run Locally:

1) Install Python and all packages needed to run the app:
    - Python 3.10 or higher
    - flask
    - sqlite3
    - pycryptodome
    - logging
    - tabulate
2) Run the server_main.py


How to Run on LAN:

1) Install Python and all packages needed to run the app:
    - Python 3.10 or higher
    - flask
    - sqlite3
    - pycryptodome
    - logging
    - tabulate
2) Add exception to FireWall to not Block port 5000
3) Run the server_main.py Python file
4) Note your IP address


To Add some Test Data:
Just run the DataBase_Manager.py
This add 3 users, one of them is 'Renata' with Password: '123'



Plan for deployment:

> Hardware:
    > 2x Raspberry Pi 4/5
        > Cooler
        > Charger
        > Case (likely 3D Printed)
        > RJ45 Cable for Network

> Software options:
    > Docker
    > Kubernetes
    > Reverse DNS:
        > NGinX
        > Duck DNS