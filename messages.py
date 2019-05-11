""" Provides Message class to construct messages for the TimeBox """

class TimeBoxMessages:
    """Support the formation of messages to communicatie with the TimeBox."""

    def checksum(self, payload):
        """Compute the payload checksum. Returned as list with LSM, MSB"""
        csum = sum(payload)
        lsb = csum & 0b11111111
        msb = csum >> 8
        return [lsb, msb]

    def escape_payload(self, payload):
        """Escape the payload. It is not allowed to have occurrences of the codes
        0x01, 0x02 and 0x03. They mut be escaped by a leading 0x03 followed by 0x04,
        0x05 or 0x06 respectively"""
        escpayload = []
        for payload_data in payload:
            escpayload += \
                [0x03, payload_data + 0x03] if payload_data in range(0x01, 0x04) else [payload_data]
        return escpayload

    def unescape(self, data):
        """unescape the data. """
        unesc = []
        _unescape_next = False
        for _item in data:
            if _unescape_next:
                if _item < 0x04 or _item > 6:
                    raise Exception('Error in escaped sequence.')
                unesc.append(_item - 0x03)
                _unescape_next = False
            else:
                if _item == 0x03:
                    _unescape_next = True
                else:
                    unesc.append(_item)
        return unesc

    def decode(self, msg):
        """remove leading 1, trailing 2 and checksum and un-escape. Return 'error' if
        msg is not a correctmessage """
        if len(msg) < 4:
            raise Exception('error: too short')
        if msg[0] != 0x01 or msg[-1] != 0x02:
            raise Exception('error: no delimiters')
        unesc = self.unescape(msg[1:-1])
        csum = self.checksum(unesc[0:-2])
        if csum != unesc[-2:]:
            raise Exception('error: wrong checksum')
        return unesc[:-2]

    def _extend_with_checksum(self, payload):
        """Extend the payload with two byte with its checksum."""
        return payload + self.checksum(payload)

    def make_message(self, payload):
        """Make a complete message from the paload data. Add leading 0x01 and
        trailing check sum and 0x02 and escape the payload"""
        cs_payload = self._extend_with_checksum(payload)
        escaped_payload = self.escape_payload(cs_payload)
        return [0x01] + escaped_payload + [0x02]

    @classmethod
    def static_image_payload(cls, imag):
        """Create the message payload for the image."""
        resmsg = [0] * (((imag.height * imag.width * 3 + 1) >> 1) + 7)
        resmsg[0:7] = [0xbd, 0x00, 0x44, 0x00, 0x0a, 0x0a, 0x04]

        # nibble index to write next pixel value
        nix = 14
        for yix in range(imag.height):
            for xix in range(imag.width):
                for cix in range(3):
                    pdat = imag.get_pixel_data(xix, yix, cix)
                    if nix&1 != 0:
                        pdat = pdat << 4
                    resmsg[nix>>1] |= pdat
                    nix = nix + 1
        return resmsg

    @classmethod
    def dynamic_image_payload(cls, imag, frame_num, frame_delay):
        """Create the message payload for the image in an animation."""
        resmsg = [0] * 191
        resmsg[0:9] = [0xbf, 0x00, 0x49, 0x00, 0x0a, 0x0a, 0x04, frame_num, frame_delay]

        # nibble index to write next pixel value
        nix = 18
        for yix in range(imag.width):
            for xix in range(imag.height):
                for cix in range(3):
                    pdat = imag.get_pixel_data(xix, yix, cix)
                    if nix&1 != 0:
                        pdat = pdat << 4
                    resmsg[nix>>1] |= pdat
                    nix = nix + 1
        return resmsg

    def command_message(self, command, arguments=None):
        """Make a message from a command number and optional arguments"""
        payload = [command]
        if not arguments is None:
            payload += arguments
        return self.make_message(payload)

    def static_image_message(self, image):
        """Creates a static image message from a TimeBoxImage."""
        return self.make_message(self.static_image_payload(image))

    def dynamic_image_message(self, image, frame_num, frame_delay):
        """Creates a static image message from a TimeBoxImage."""
        return self.make_message(self.dynamic_image_payload(image, frame_num, frame_delay))
