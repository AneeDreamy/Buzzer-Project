A Simple Bluetooth-Connected Buzzer -That's Connected to Your Computer!

The code works for a modified a pre-existing buzzer toy (link to instructions are coming soon). This project uses the pybluez bluetooth library. I will link a small tutorial on how to install the library on my GitHub page. 

1. Run bluetooth_check.py to get the address of the bluetooth modules.
2. Add the address of the bluetooth module into the GUI_final.py part of the code (shown below):

class BluetoothApp:
    def __init__(self):
        self.devices = [
            {"name": "Team A", "bd_addr": "98:D3:61:F5:D7:C0", "port": 1},
            {"name": "Team G", "bd_addr": "00:24:01:01:04:7E", "port": 1},
            # Add more devices as needed
      .
      .
      .

3. Make sure the bluetooth devices are connected to your computer. See instructions in the link
4. Load the button_code_debounced.ino into your Arduino board. The connections are as follows:
   Button pins to Arduino -> PIN 5, GND
   TX,RX of Bluetooth Module -> PIN 2 (RX), and PIN 4 (TX) of Arduino board. The TX of the bluetooth is connected to RX of the Arduino board and vice versa.
5. Run the GUI_final.py!



