
import socket
import threading
import time

from MilightController.Zone import Zone


class MilightController:
    #! not sure what the v4 port is
    __PORT_v4: int = 8899
    __PORT_v6: int = 5987

    def __init__(self, options: dict[str, str]) -> None:
        self.options: dict[str, str] = options or {"type": "all"}
        self.port: int = self.options.get("port", 48899)
        self.host: str = self.options.get("address", "255.255.255.255")
        self.timeout: int = self.options.get("timeout", 3000)
        self.discover_legacy: str = (
            not self.options.get("type")
            or self.options.get("type") == "all"
            or self.options.get("type") == "legacy"
        )
        self.discover_v6: str = (
            self.options.get("type") == "all" or self.options.get("type") == "v6"
        )
        self.discovery_message_legacy: bytes = b"\x4C\x69\x6E\x6B\x5F\x57\x69\x2D\x46\x69"
        self.discovery_message_v6: bytes = (
            b"\x48\x46\x2D\x41\x31\x31\x41\x53\x53\x49\x53\x54\x48\x52\x45\x41\x44"
        )
        # self.timeout_id = None
        self.disco_results: list[dict[str, str]] = []
        self.sequenceNumber: int = 0

    def discover(self) -> list[dict[str, str]]:
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
            discoverer_attempts: int = 10
            print(f"Sending discover request {discoverer_attempts} times")
            for _ in range(discoverer_attempts):
                if self.discover_legacy:
                    discoverer.sendto(
                        self.discovery_message_legacy, (self.host, self.port)
                    )
                if self.discover_v6:
                    discoverer.sendto(self.discovery_message_v6, (self.host, self.port))
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
        # Send command to get Wifi Bridge Session ID
        command: bytes = bytes.fromhex(
            "20 00 00 00 16 02 62 3A D5 ED A3 01 AE 08 2D 46 61 41 A7 F6 DC AF D3 E6 00 00 1E"
        )
        udp_socket.sendto(command, (device.get("ip"), device.get("port")))
        print("Sent reqest to get session ID:", self.__add_spaces_to_hex(command.hex()))

        # Receive responses
        while True:
            data, _ = udp_socket.recvfrom(1024)
            response: str = data.hex()
            print("Got response: ", self.__add_spaces_to_hex(response))

            # Extract WB1 and WB2 from the response
            wb1: str = response[38:40]
            wb2: str = response[40:42]
            print("WB1:", wb1)
            print("WB2:", wb2)

            # Break the loop after receiving all responses
            if len(data) < 28:
                break

        # Return session ID
        return (wb1, wb2)

    # UDP Hex Send Format: 80 00 00 00 11 {WifiBridgeSessionID1} {WifiBridgeSessionID2} 00 {SequenceNumber} 00 {COMMAND} {ZONE NUMBER} 00 {Checksum}
    def send_command(self, device: dict, command: str, zone: Zone = Zone.ALL) -> str:
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
        data = message.decode("ascii").split(",")
        if len(data) >= 2:
            ip: str = data[0]
            mac: str = "".join([f"{x:02X}:" for x in bytearray(data[1], "ascii")])[:-1]
            name: str = data[2]
            type: str = "legacy" if name == "" else "v6"
            port: str = self.__PORT_v4 if name == "" else self.__PORT_v6
            new_device: dict[str, str] = {
                "ip": ip,
                "port": port,
                "mac": mac,
                "name": name,
                "type": type,
            }
            if new_device not in self.disco_results:
                self.disco_results.append(new_device)

    def __calc_checksum(self, hex_string: str) -> str:
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
        # Using list comprehension to split the string into chunks of 2 characters
        chunks = [hex_string[i : i + 2] for i in range(0, len(hex_string), 2)]
        # Joining the chunks with a space between them
        spaced_hex_string = " ".join(chunks)
        return spaced_hex_string
