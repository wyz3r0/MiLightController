class Commands:
    @staticmethod
    def light_on():
        return "31 00 00 08 04 01 00 00 00"

    @staticmethod
    def light_off():
        return "31 00 00 08 04 02 00 00 00"

    @staticmethod
    def night_light_on():
        return "31 00 00 08 04 05 00 00 00"

    @staticmethod
    def white_light_on():
        return "31 00 00 08 05 64 00 00 00"

    @staticmethod
    def set_color(color):
        color = Commands.hex_to_hue(color)
        return "31 00 00 08 01 {} {} {} {}".format(color, color, color, color)

    @staticmethod
    def saturation(saturation):
        # Ensure percent is within [0, 100] range
        saturation = max(0, min(100, saturation))
        saturation = 100 - saturation
        saturation = Commands.percentage_to_hex(saturation)
        return "31 00 00 08 02 {} 00 00 00".format(saturation)

    @staticmethod
    def brightness(brightness):
        # Ensure percent is within [0, 100] range
        brightness = max(0, min(100, brightness))
        brightness = Commands.percentage_to_hex(brightness)
        return "31 00 00 08 03 {} 00 00 00".format(brightness)

    @staticmethod
    def kelvin(kelvin):
        kelvin = Commands.KV_to_hex(kelvin)
        return "31 00 00 08 05 {} 00 00 00".format(kelvin)

    @staticmethod
    def mode_number(mode_number):
        return "31 00 00 08 06 {} 00 00 00".format(format(mode_number, '02X'))

    @staticmethod
    def mode_speed_decrease():
        return "31 00 00 08 04 04 00 00 00"

    @staticmethod
    def mode_speed_increase():
        return "31 00 00 08 04 03 00 00 00"

    @staticmethod
    def link():
        return "3D 00 00 08 00 00 00 00 00"

    @staticmethod
    def unlink():
        return "3E 00 00 08 00 00 00 00 00"

    @staticmethod
    def wifi_bridge_lamp_on():
        return "31 00 00 00 03 03 00 00 00"

    @staticmethod
    def wifi_bridge_lamp_off():
        return "31 00 00 00 03 04 00 00 00"

    @staticmethod
    def wifi_bridge_mode_number(mode_number):
        return "31 00 00 00 04 {} 00 00 00".format(format(mode_number, '02X'))

    @staticmethod
    def wifi_bridge_mode_speed_decrease():
        return "31 00 00 00 03 01 00 00 00"

    @staticmethod
    def wifi_bridge_mode_speed_increase():
        return "31 00 00 00 03 02 00 00 00"

    @staticmethod
    def wifi_bridge_set_color(color):
        color = Commands.hex_to_hue(color)
        return "31 00 00 00 01 {} {} {} {}".format(color, color, color, color)

    @staticmethod
    def set_color_to_white():
        return "31 00 00 00 03 05 00 00 00"

    @staticmethod
    def wifi_bridge_brightness(brightness):
        # Ensure percent is within [0, 100] range
        brightness = max(0, min(100, brightness))
        brightness = Commands.percentage_to_hex(brightness)
        return "31 00 00 00 02 {} 00 00 00".format(brightness)
    
    @staticmethod
    def hex_to_hue(hex_color: str):
        # Convert hex color to RGB
        hex_color = hex_color.strip("#")
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
    def KV_to_hex(KV):
        # Convert KV to hex
        hex_value = int((KV - 2700) / (6500 - 2700) * 100)
        return format(hex_value, '02X')
    
    @staticmethod
    def percentage_to_hex(percent):
        # Convert percentage to hex
        hex_value = int(percent / 100 * 100)
        
        return format(hex_value, '02X')