import time

from arktos.hardware.can.can_connection import CanConnection
from arktos.hardware.hardware_interface import RGBColor
from arktos.hardware.can.can_protocol import CanProtocol


connection = CanConnection()
connection.open()

while(True):
    #connection.write(CanProtocol.get_button(CanProtocol.BROADCAST_ADDRESS))
    time.sleep(0.1)
    recieved = connection.read()
    if recieved:
        data = recieved.data
        
        if(data != bytearray(b'\x00')):
            def test_bit(data, bit_offset):
                is_set = bool(data[0] & (1 << bit_offset))
                return is_set

            if(test_bit(data, 0)):
                connection.write(CanProtocol.set_leds(CanProtocol.BROADCAST_ADDRESS, 0, RGBColor(255, 0, 255)))
            if(test_bit(data, 1)):
                connection.write(CanProtocol.set_leds(CanProtocol.BROADCAST_ADDRESS, 1, RGBColor(0, 255, 255)))
            if(test_bit(data, 2)):
                connection.write(CanProtocol.set_leds(CanProtocol.BROADCAST_ADDRESS, 2, RGBColor(255, 255, 0)))
            
            print(''.join(format(byte, '08b') for byte in data))
            #print(int.from_bytes(data))
    else:
        connection.write(CanProtocol.set_leds(CanProtocol.BROADCAST_ADDRESS, 0, RGBColor(0,0,0)))

    # for i in range(255):
    #     for j in range(3): 
    #         r = 255 * i/255 if j == 0 else 0
    #         g = 255 * i/255 if j == 1 else 0
    #         b = 255 * i/255 if j == 2 else 0
            
    #         color = RGBColor(r,b,g)
    #         connection.write(CanProtocol.set_leds(CanProtocol.BROADCAST_ADDRESS, j, color))
    #         time.sleep(0.05)

                    
