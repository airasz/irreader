class color:
    def percentTo565Color(self, value):
        # Clamp the value to be between 0 and 100
        value = max(0, min(100, value))
        
        # Calculate the red and green components
        red = int((value / 100) * 255)  # Scale to 0-255
        green = 255 - red                # Inverse for green

        # Convert to RGB565
        r_565 = (red >> 3) & 0x1F  # 5 bits for red
        g_565 = (green >> 2) & 0x3F  # 6 bits for green
        b_565 = 0                   # Blue is always 0 in this gradient

        # Combine into a single 16-bit value
        rgb565 = (r_565 << 11) | (g_565 << 5) | b_565
        return rgb565


# Example usage
# colorc
# for i in range(0, 101, 10):
#     color = value_to_rgb565(i)
#     print(f"Value: {i}, RGB565: {color:#06x}")