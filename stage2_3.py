import bluetooth
from  stage3 import * 
import sys
import time
bd_addr = "98:D3:61:F5:D7:C0"
port = 1


try:
    sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((bd_addr, port))
    print('Connected')
    # Initialize an empty string to store the received message
    received_message = ''
    # Receive and process data from the Bluetooth connection
    while (1):
        # Receive data from the Bluetooth connection
        data = sock.recv(1024)  # Adjust buffer size as needed  
        dataed= data.decode('utf-8')
        # Append received data to the message
        received_message += dataed

        # Check if the special character '*' is present in the received data
        if '*' in dataed:
            print("Received message:", received_message)

            if (received_message=="BUZZED*"):
                show_team_a()
            # Empty the received message string for reuse
            received_message = ''

except KeyboardInterrupt:
    print("Keyboard interrupt detected. Exiting...")
finally:
    # Close the Bluetooth connection
    sock.close()
