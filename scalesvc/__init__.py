"""Scale service module"""

def pretty_hex(data: bytearray) -> str:
    """Pretty hex string a bytearrey
    
    Args:
        data:
            bytearray
    
    Returns:
        str
    """
    pretty_hex_str = ''
    for i, c in enumerate(data.hex()):
        pretty_hex_str += c
        if (i + 1) % 2 == 0:
            pretty_hex_str += ' '
    return pretty_hex_str