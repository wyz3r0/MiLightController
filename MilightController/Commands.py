
# The `Commands` class in Python provides static methods for generating commands to control various
# lighting settings, including turning lights on/off, setting colors, adjusting brightness, and
# changing modes for a smart lighting system.
class Commands:
    @staticmethod
    def light_on():
        '''The static function `light_on` returns a string of hexadecimal values representing
        a command to turn lights on.
        
        Returns
        -------
            "31 00 00 08 04 01 00 00 00".
        
        '''
        return "31 00 00 08 04 01 00 00 00"

    @staticmethod
    def light_off():
        '''The static function `light_off` returns a string of hexadecimal values representing
        a command to turn lights off.
        
        Returns
        -------
            "31 00 00 08 04 02 00 00 00".
        
        '''
        return "31 00 00 08 04 02 00 00 00"

    @staticmethod
    def night_light_on():
        '''The static function `night_light_on` returns a string of hexadecimal values representing
        a command to turn on night light.
        
        Returns
        -------
            "31 00 00 08 04 05 00 00 00".
        
        '''
        return "31 00 00 08 04 05 00 00 00"

    @staticmethod
    def white_light_on():
        '''The static function `white_light_on` returns a string of hexadecimal values representing
        a command to turn on white mode (Color RGB OFF).
        
        Returns
        -------
           "31 00 00 08 05 64 00 00 00".
        
        '''
        return "31 00 00 08 05 64 00 00 00"

    @staticmethod
    def set_color(color: str):
        '''The static function `set_color` returns a string of hexadecimal values representing
        a command to set color to passed hex value.
        
        Parameters
        ----------
        color: str
            The `color` parameter is a hexadecimal color value that needs to be converted to a hue value
        using the `__hex_to_hue` method from the `Commands` class. The converted hue value will then be
        used to generate a formatted string with the specified color values. It can be passed in any
        format f.e.:
        \n#af00ff
        \n#AF 00 FF
        \naf00ff
        \nAF 00 FF
        
        Returns
        -------
            "31 00 00 08 01 {color} {color} {color} {color}"
        
        '''
        color = Commands.__hex_to_hue(color)
        return "31 00 00 08 01 {} {} {} {}".format(color, color, color, color)

    @staticmethod
    def saturation(saturation: int):
        '''The static function `saturation` returns a string of hexadecimal values representing
        a command to set saturation to passed level.
        
        Parameters
        ----------
        saturation: int
            The `saturation` parameter is a value representing the saturation level of a color. It converts
        the saturation level to a hexadecimal value. Any value smaller than 0 and bigger than 100 will be 
        set to 0 or 100 respectively.
        
        Returns
        -------
            "31 00 00 08 02 {saturation} 00 00 00"
        
        '''
        # Ensure percent is within [0, 100] range
        saturation = max(0, min(100, saturation))
        saturation = 100 - saturation
        saturation = Commands.__percentage_to_hex(saturation)
        return "31 00 00 08 02 {} 00 00 00".format(saturation)

    @staticmethod
    def brightness(brightness: int):
        '''The static function `brightness` returns a string of hexadecimal values representing
        a command to set brightness to passed level.
        
        Parameters
        ----------
        brightness: int
            The `brightness` parameter is a value representing the brightness level, ranging from 0 to 100.
        The function takes this input value, ensures it is within the valid range of 0 to 100, converts it
        to a hexadecimal value. Any value smaller than 0 and bigger than 100 will be set to 0 or 100
        respectively.
        
        Returns
        -------
            "31 00 00 08 03 {brightness} 00 00 00"
        
        '''
        # Ensure percent is within [0, 100] range
        brightness = max(0, min(100, brightness))
        brightness = Commands.__percentage_to_hex(brightness)
        return "31 00 00 08 03 {} 00 00 00".format(brightness)

    @staticmethod
    def kelvin(temp: int):
        '''The static function `kelvin` returns a string of hexadecimal values representing
        a command to change color to white with passed color temperature.
        
        Parameters
        ----------
        temp: int
            It looks like the `temp` parameter is being converted to hexadecimal format using the
        `Commands.__KV_to_hex()` method and then formatted into a message string format. The resulting
        string containing converted `temp` value in a message position.
        
        Returns
        -------
            "31 00 00 08 05 {temp} 00 00 00"
        
        '''
        temp = Commands.__KV_to_hex(temp)
        return "31 00 00 08 05 {} 00 00 00".format(temp)

    @staticmethod
    def mode_number(mode_number):
        '''The static function `mode_number` returns a string of hexadecimal values representing
        a command to change mode.
        
        Parameters
        ----------
        mode_number
            The `mode_number` parameter is the input value that will be formatted and included in the
        output string. The `mode_number` will be converted to a hexadecimal representation with two
        digits and inserted into the message string.
        
        Returns
        -------
            "31 00 00 08 06 {mode} 00 00 00".
        
        '''
        return "31 00 00 08 06 {} 00 00 00".format(format(mode_number, '02X'))

    @staticmethod
    def mode_speed_decrease():
        '''The static function `mode_speed_decrease` returns a string of hexadecimal values representing
        a command to decrease speed of mode animation.
        
        Returns
        -------
            "31 00 00 08 04 04 00 00 00".
        
        '''
        return "31 00 00 08 04 04 00 00 00"

    @staticmethod
    def mode_speed_increase():
        '''The static function `mode_speed_increase` returns a string of hexadecimal values representing
        a command to increase speed of mode animation.
        
        Returns
        -------
            "31 00 00 08 04 03 00 00 00".
        
        '''
        return "31 00 00 08 04 03 00 00 00"

    # ! check functionality
    @staticmethod
    def link():
        '''The static function `link` returns a string of hexadecimal values representing
        a command to link.
        
        Returns
        -------
            "3D 00 00 08 00 00 00 00 00".
        
        '''
        return "3D 00 00 08 00 00 00 00 00"

    # ! check functionality
    @staticmethod
    def unlink():
        '''The static function `unlink` returns a string of hexadecimal values representing
        a command to unlink.
        
        Returns
        -------
            "3E 00 00 08 00 00 00 00 00".
        
        '''
        return "3E 00 00 08 00 00 00 00 00"

    @staticmethod
    def wifi_bridge_lamp_on():
        '''The static function `wifi_bridge_lamp_on` returns a string of hexadecimal values representing
        a command to turn on a Wi-Fi bridge lamp.
        
        Returns
        -------
            "31 00 00 00 03 03 00 00 00".
        
        '''
        return "31 00 00 00 03 03 00 00 00"

    @staticmethod
    def wifi_bridge_lamp_off():
        '''The static function `wifi_bridge_lamp_off` returns a string of hexadecimal values representing
        a command to turn off a Wi-Fi bridge lamp.
        
        Returns
        -------
            "31 00 00 00 03 04 00 00 00".
        
        '''
        return "31 00 00 00 03 04 00 00 00"

    @staticmethod
    def wifi_bridge_mode_number(mode_number):
        '''The static function `wifi_bridge_mode_number` returns a string of hexadecimal values representing
        a command to change Wi-Fi bridge mode.
        
        Parameters
        ----------
        mode_number
            The `mode_number` parameter is the input value that will be formatted and included in the
        output string. The `mode_number` will be converted to a hexadecimal representation with two
        digits and inserted into the message string.
        
        Returns
        -------
            "31 00 00 00 04 {mode} 00 00 00"
        
        '''
        return "31 00 00 00 04 {} 00 00 00".format(format(mode_number, '02X'))

    @staticmethod
    def wifi_bridge_mode_speed_decrease():
        '''The static function `wifi_bridge_mode_speed_decrease` returns a string of hexadecimal values representing
        a command to decrease speed of Wi-Fi bridge mode animation.
        
        Returns
        -------
            "31 00 00 00 03 01 00 00 00"
        
        '''
        return "31 00 00 00 03 01 00 00 00"

    @staticmethod
    def wifi_bridge_mode_speed_increase():
        '''The static function `wifi_bridge_mode_speed_increase` returns a string of hexadecimal values representing
        a command to increase speed of Wi-Fi bridge mode animation.
        
        Returns
        -------
            "31 00 00 00 03 02 00 00 00"
        
        '''
        return "31 00 00 00 03 02 00 00 00"

    @staticmethod
    def wifi_bridge_set_color(color):
        '''The static function `wifi_bridge_set_color` returns a string of hexadecimal values representing
        a command to set Wi-Fi bridge lamp's color to passed hex value.
        
        Parameters
        ----------
        color: str
            The `color` parameter is a hexadecimal color value that needs to be converted to a hue value
        using the `__hex_to_hue` method from the `Commands` class. The converted hue value will then be
        used to generate a formatted string with the specified color values. It can be passed in any
        format f.e.:
        \n#af00ff
        \n#AF 00 FF
        \naf00ff
        \nAF 00 FF
        
        Returns
        -------
            "31 00 00 00 01 {color} {color} {color} {color}"
        
        '''
        color = Commands.__hex_to_hue(color)
        return "31 00 00 00 01 {} {} {} {}".format(color, color, color, color)

    @staticmethod
    def wifi_bridge_set_color_to_white():
        '''The static function `wifi_bridge_set_color_to_white` returns a string of hexadecimal values representing
        a command to set Wi-Fi bridge color to white. (works ONLY when the lamp is ON)
        
        Returns
        -------
            "31 00 00 00 03 05 00 00 00"
        
        '''
        return "31 00 00 00 03 05 00 00 00"

    @staticmethod
    def wifi_bridge_brightness(brightness: int):
        '''The static function `wifi_bridge_brightness` returns a string of hexadecimal values representing
        a command to set Wi-Fi bridge brightness to passed value.
        
        Parameters
        ----------
        brightness
            The `wifi_bridge_brightness` method takes a `brightness` parameter, which represents the
        brightness level of a WiFi bridge device. The method ensures that the brightness value is within
        the range of 0 to 100, converts it to a hexadecimal value, and then constructs a command string
        based on the brightness
        
        Returns
        -------
            The method `wifi_bridge_brightness` is returning a formatted string with the brightness value
        converted to hexadecimal format. The returned string is: "31 00 00 00 02 {brightness} 00 00 00",
        where {brightness} is the converted hexadecimal value of the input brightness parameter.
        
        '''
        brightness = max(0, min(100, brightness))
        brightness = Commands.__percentage_to_hex(brightness)
        return "31 00 00 00 02 {} 00 00 00".format(brightness)
    
    @staticmethod
    def __hex_to_hue(hex_color: str):
        '''This static method converts a hexadecimal color code to its corresponding hue value in
        the range 00-FF.
        
        Parameters
        ----------
        hex_color : str
            The `hex_to_hue` method takes a hexadecimal color code as input and converts it to a hue value
        in the range of 00-FF. It ignores any spaces and "#" at the start.
        
        Returns
        -------
            String containing a hue value in the range of 00-FF.
        
        '''
        # Convert hex color to RGB
        hex_color = hex_color.strip("#").replace(" ", "")
        red = int(hex_color[0:2], 16)
        green = int(hex_color[2:4], 16)
        blue = int(hex_color[4:6], 16)
        
        # Convert RGB to HSL
        r = red / 255
        g = green / 255
        b = blue / 255
        
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        
        delta = max_val - min_val
        
        if delta == 0:
            hue = 0
        elif max_val == r:
            hue = ((g - b) / delta) % 6
        elif max_val == g:
            hue = ((b - r) / delta) + 2
        else:
            hue = ((r - g) / delta) + 4
        
        hue *= 60
        
        # Convert hue to range 00-FF
        hue = int(hue / 360 * 255)
        
        return format(hue, '02X')

    @staticmethod
    def __KV_to_hex(KV):
        '''The static function __KV_to_hex converts a Kelvin value to a hexadecimal representation.
        
        Parameters
        ----------
        KV
            KV represents a Kelvin value, typically used in lighting to indicate the color temperature of a
        light source. The function `__KV_to_hex` takes a Kelvin value as input, converts it to a
        hexadecimal value based on a message range, and returns the hexadecimal representation.
        
        Returns
        -------
            String containing a hexadecimal representation of the input KV value after converting it to
        a percentage based on a range of 2700 to 6500.
        
        '''
        hex_value = int((KV - 2700) / (6500 - 2700) * 100)
        return format(hex_value, '02X')
    
    @staticmethod
    def __percentage_to_hex(percent):
        '''The static method `__percentage_to_hex` converts a percentage value to a hexadecimal
        representation.
        
        Parameters
        ----------
        percent
            The `__percentage_to_hex` method takes a percentage value as input and converts it to a
        hexadecimal value. The `percent` parameter represents the percentage value that you want to
        convert to hexadecimal.
        
        Returns
        -------
            String containing hex representation of percentage passed.
        
        '''
        hex_value = int(percent / 100 * 100)
        
        return format(hex_value, '02X')