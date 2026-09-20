from enum import IntEnum
import can

from ..hardware_interface import RGBColor

class CanProtocol():

    class MessagePriority(IntEnum):
        HIGHEST = 0
        HIGH = 1
        LOW = 2
        LOWEST = 3


    class MessageType(IntEnum):
        BUS_CONTROL = 0b010
        PROGRAM = 0b011
        SCHOLLE = 0b100


    class ScholleCommand(IntEnum):
        SET_COLOR = 0b00001101
        BUTTON_STATE = 0b00001010
        BUTTON_STATE_REQUEST = 0b00000010
        SWAP_BUFFERS = 0b00000100
        BUTTON_DEBUG_MODE = 0b00010000


    class BusControlMessage(IntEnum):
        PING = 0b10000011
        PING_RESPONSE = 0b10000100
        MULTICAST_GROUP_JOIN = 0b10000101
        MULTICAST_GROUP_JOIN_ACK = 0b10000110
        MULTICAST_GROUP_LEAVE = 0b10000111
        MULTICAST_GROUP_LEAVE_ACK = 0b10001000


    DEFAULT_PRIORITY = MessagePriority.LOW
    BROADCAST_ADDRESS = 0b01000000

    @classmethod
    def parse_arbitration_id(cls, arbitration_id):
        priority = (arbitration_id >> 27) & 0x03
        message_type = (arbitration_id >> 24) & 0x07
        destination_address = (arbitration_id >> 16) & 0xFF
        source_id = (arbitration_id >> 8) & 0xFF
        protocol_header = arbitration_id & 0xFF

        return {
            "priority": priority,
            "message_type": message_type,
            "destination_address": destination_address,
            "source_id": source_id,
            "protocol_header": protocol_header,
        }

    @classmethod
    def arbitration_id(cls, priority, message_type, destination_address, source_id, protocol_header):

        # Message header used as CAN2.0B extended can id (29 bits)
        # bits 27 - 28: priority field, implicitly regarded by CSMA/CR can arbitration
        # bits 24 - 26: message protocol id
        # bits 16 - 23: 8 bit destination address
        # bits 8 - 15: 8 bit source address
        # bits 0 - 7: protocol specific header

        arb_id = (priority << 27) | (message_type << 24) | (destination_address << 16) | (source_id << 8) | protocol_header
        return arb_id

    @classmethod
    def ping(cls, destination_address):
        # Arbitration
        priority = CanProtocol.MessagePriority.HIGH
        message_type = CanProtocol.MessageType.BUS_CONTROL
        source_id = 4
        protocol_header = CanProtocol.BusControlMessage.PING

        arbitration_id = CanProtocol.arbitration_id( priority,
                                                        message_type,
                                                        destination_address,
                                                        source_id,
                                                        protocol_header)

        sequence_number = 1
        data = bytes([
            sequence_number,
        ])

        # Build Message
        message = can.Message(arbitration_id=arbitration_id, is_extended_id=True, data=data)
        return message

    @classmethod
    def set_leds(cls, destination_address, sub_hexagon: int, color: RGBColor):
            # Arbitration
            priority = CanProtocol.MessagePriority.HIGH
            message_type = CanProtocol.MessageType.SCHOLLE
            source_id = 4
            protocol_header = CanProtocol.ScholleCommand.SET_COLOR
    
            arbitration_id = CanProtocol.arbitration_id( priority,
                                                         message_type,
                                                         destination_address,
                                                         source_id,
                                                         protocol_header)
    
            # Data for RGB
            data = 0
            hexagon_offset = sub_hexagon * 21
            RESOLUTION = 127
            color_scaled = tuple(int(RESOLUTION * x) for x in color.to_percent())
    
            color_offset = 0
            for component in color_scaled:
                data |= (component & 0x7F) << (hexagon_offset + color_offset)
                color_offset += 7
            
            # Convert data to little endian
            data_bytes = data.to_bytes(8, byteorder="little")
            
            # Build Message
            message = can.Message(arbitration_id=arbitration_id, is_extended_id=True, data=data_bytes)

            return message

    @classmethod
    def get_button(cls, destination_address):
        # Arbitration
        priority = CanProtocol.DEFAULT_PRIORITY
        message_type = CanProtocol.MessageType.SCHOLLE
        source_id = 4
        protocol_header = CanProtocol.ScholleCommand.BUTTON_STATE_REQUEST
        arbitration_id = CanProtocol.arbitration_id( priority,
                                                    message_type,
                                                    destination_address,
                                                    source_id,
                                                    protocol_header)
                    
        message = can.Message(arbitration_id=arbitration_id, is_extended_id=True, data=None)
        return message
    
