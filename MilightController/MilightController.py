
import socket
import threading
import time

from MilightController.Zone import Zone


# The `MilightController` class in Python provides functionality for network discovery and sending
# commands to devices using UDP communication.
class MilightController:
    __PORT_v6: int = 5987

    def __init__(self, port: int = 48899, address: str = "255.255.255.255", timeout: int = 3000) -> None:
        '''The function initializes attributes for a network discovery tool in Python.
        
        Parameters
        ----------
        port : int, optional
            The `port` parameter in the `__init__` method is used to specify the port number for the
        network communication. In this case, the default value for `port` is set to 48899 if no value is
        provided when creating an instance of the class.
        address : str, optional
            The `address` parameter in the `__init__` method is a string that represents the IP address. In
        this case, the default value is set to "255.255.255.255". This parameter is used to specify the
        network address to which the code will connect or send data.
        timeout : int, optional
            The `timeout` parameter in the `__init__` method is used to specify the duration in
        milliseconds for which the program will wait for a response before timing out. In this case, the
        default value for `timeout` is set to 3000 milliseconds (3 seconds). This means that if
        
        '''
        self.port: int = port
        self.host: str = address
        self.timeout: int = timeout
        self.discovery_message_v6: bytes = (
            b"\x48\x46\x2D\x41\x31\x31\x41\x53\x53\x49\x53\x54\x48\x52\x45\x41\x44" 
        )
        self.disco_results: list[dict[str, str]] = []
        self.sequenceNumber: int = 0

    def discover(self) -> list[dict[str, str]]:
        '''The `discover` function in the provided Python code sends a discover request multiple times,
        receives responses asynchronously, and returns a list of discovered devices.
        
        Returns
        -------
            A list of dictionaries containing information about discovered devices is being returned. If no
        devices are discovered, `None` is returned.
        
        '''
        def receive():
            while True:
                data, _ = discoverer.recvfrom(1024)
                self.__handle_message(data)

        discoverer: socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        discoverer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        discoverer.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        discoverer.bind(("0.0.0.0", self.port))

        threading.Thread(target=receive, daemon=True).start()

        try:
            discoverer_attempts: int = 3
            print(f"Sending discover request {discoverer_attempts} times")
            
            for _ in range(discoverer_attempts):
                discoverer.sendto(self.discovery_message_v6, (self.host, self.port))
                if self.disco_results:
                    break
                time.sleep(0.2)

            time.sleep(self.timeout / 1000)
        finally:
            discoverer.close()

        print(f"Discovered {len(self.disco_results)} devices")

        if self.disco_results:
            return self.disco_results
        else:
            return None

    def establish_session(self, udp_socket: socket, device: dict) -> tuple[str, str]:
        '''This function establishes a session with a device using a UDP socket and retrieves the session
        ID from the response.
        
        Parameters
        ----------
        udp_socket : socket
            The `udp_socket` parameter in the `establish_session` method is expected to be a UDP socket
        object that will be used to send and receive data over the network. It should be an instance of
        the `socket` class in Python's socket module.
        device : dict
            The `device` parameter is a dictionary containing information about the device. It should have
        the following keys:
        
        Returns
        -------
            The function `establish_session` is returning a tuple containing two strings, which are the
        values of `wb1` and `wb2` extracted from the response received after sending a command to get
        the Wifi Bridge Session ID.
        
        '''
        # Send command to get Wifi Bridge Session ID
        command = bytes.fromhex(
            "20 00 00 00 16 02 62 3A D5 ED A3 01 AE 08 2D 46 61 41 A7 F6 DC AF D3 E6 00 00 1E"
        )
        udp_socket.sendto(command, (device.get("ip"), device.get("port")))
        print("Sent reqest to get session ID:", self.__add_spaces_to_hex(command.hex()))

        # Receive responses
        while True:
            data, _ = udp_socket.recvfrom(1024)
            response = data.hex()
            print("Got response: ", self.__add_spaces_to_hex(response))

            # Extract WB1 and WB2 from the response
            wb1 = response[38:40]
            wb2 = response[40:42]
            print("WB1:", wb1)
            print("WB2:", wb2)

            # Break the loop after receiving all responses
            if len(data) < 28:
                break

        # Return session ID
        return (wb1, wb2)

    # UDP Hex Send Format: 80 00 00 00 11 {WifiBridgeSessionID1} {WifiBridgeSessionID2} 00 {SequenceNumber} 00 {COMMAND} {ZONE NUMBER} 00 {Checksum}
    def send_command(self, device: dict, command: str, zone: Zone = Zone.ALL) -> str:
        '''The function `send_command` sends a command to a device using UDP socket communication and
        returns the response in hexadecimal format.
        
        Parameters
        ----------
        device : dict
            The `device` parameter in the `send_command` method is expected to be a dictionary containing
        information about the device to which the command will be sent. It should have the keys "ip" and
        "port" to specify the IP address and port number of the device respectively.
        command : str
            The `send_command` method you provided is used to send a command to a device over UDP and
        receive a response. The `command` parameter in this method is a string that represents the
        specific command you want to send to the device. This command could be any valid command that
        the device understands and
        zone : Zone
            The `zone` parameter in the `send_command` method is of type `Zone`, which is an enumeration.
        The `Zone` enumeration likely contains different zone values that can be used to specify a
        particular zone for the command being sent. In the code snippet provided, the default value for
        the `
        
        Returns
        -------
            The `send_command` method returns the response received from the device after sending the
        command. This response is in hexadecimal format and represents the device's acknowledgment or
        response to the command that was sent.
        
        '''
        # Create UDP socket
        udp_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Establish connection and get session ID
        wb1, wb2 = self.establish_session(udp_socket, device)

        # Calculate sequence number
        self.sequenceNumber = (self.sequenceNumber + 1) % 255
        sn: str = "%02X" % self.sequenceNumber
        
        # Get zone code (default "00")
        zone_hex: str = zone.value

        # Generate packet
        packet: str = "80 00 00 00 11 {} {} 00 {} 00 {} {} 00".format(wb1, wb2, sn, command, zone_hex)

        # Calculate packet checksum
        checksum: str = self.__calc_checksum(packet.strip(" "))

        # Add checksum to the end of the packet
        packet += checksum

        # Convert string to bytes
        command: bytes = bytes.fromhex(packet)

        # Send the command
        udp_socket.sendto(command, (device.get("ip"), device.get("port")))
        print("Sent request:", self.__add_spaces_to_hex(command.hex()))

        # Receive response
        response, _ = udp_socket.recvfrom(1024)
        response_hex: str = response.hex()
        print("Received response:", self.__add_spaces_to_hex(response_hex))

        # Close the socket
        udp_socket.close()

        return response_hex

    def __handle_message(self, message: bytes) -> None:
        """
        The function `__handle_message` decodes a message, extracts IP, MAC, and name information, and
        appends a new device dictionary to a list if it is not already present.
        
        :param message: The `message` parameter in the `__handle_message` method is expected to be a
        byte string containing information about a network device. The method decodes this byte string
        as ASCII and splits it into a list using a comma as the delimiter. The decoded data is then used
        to extract the IP address
        :type message: bytes
        """
        data = message.decode("ascii").split(",")
        if len(data) >= 2:
            ip: str = data[0]
            mac: str = "".join([f"{x:02X}:" for x in bytearray(data[1], "ascii")])[:-1]
            name: str = data[2]
            new_device: dict[str, str] = {
                "ip": ip,
                "port": self.__PORT_v6,
                "mac": mac,
                "name": name,
                "type": "v6",
            }
            if new_device not in self.disco_results:
                self.disco_results.append(new_device)

    def __calc_checksum(self, hex_string: str) -> str:
        """
        The function calculates a checksum for a given hexadecimal string and appends it to the string.
        
        :param hex_string: The `hex_string` parameter is a string representing a sequence of hexadecimal
        values. The function `__calc_checksum` calculates a checksum for the last 11 hex values in the
        input string and appends it to the end of the string. If the input string is less than 22
        characters long,
        :type hex_string: str
        :return: The function `__calc_checksum` returns the last 2 characters of the
        `hex_string_with_checksum` variable, which represents the checksum calculated based on the input
        `hex_string`.
        """
        if len(hex_string) >= 22:
            # Each hex value is 2 characters, so 11 values means 22 characters
            # Convert hex string to bytes
            bytes_array: bytes = bytes.fromhex(hex_string)

            # Calculate the modulo 256 checksum
            checksum: int = sum(bytes_array[-11:]) % 256

            # Append the checksum to the bytes array
            bytes_array += bytes([checksum])

            # Convert bytes back to hex string
            hex_string_with_checksum: str = bytes_array.hex()
        else:
            hex_string_with_checksum: str = hex_string

        return hex_string_with_checksum[-2:]

    def __add_spaces_to_hex(self, hex_string: str) -> str:
        """
        The function `__add_spaces_to_hex` takes a hexadecimal string and adds spaces between every two
        characters.
        
        :param hex_string: Hexadecimal string that needs to have spaces added between every two
        characters
        :type hex_string: str
        :return: The function `__add_spaces_to_hex` takes a hexadecimal string as input and returns the
        same string with spaces added between every two characters.
        """
        # Using list comprehension to split the string into chunks of 2 characters
        chunks = [hex_string[i : i + 2] for i in range(0, len(hex_string), 2)]
        # Joining the chunks with a space between them
        spaced_hex_string = " ".join(chunks)
        return spaced_hex_string
