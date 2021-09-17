from datetime import datetime
from uttlv import TLV


def hexify_bytes(msg: bytes) -> str:
    return "".join("{:02X} ".format(x) for x in msg)


def get_tlv_len_size(tlvlen):
    if tlvlen == 0x84:
        return 4
    if tlvlen == 0x83:
        return 3
    if tlvlen == 0x82:
        return 2
    if tlvlen == 0x81:
        return 1
    return 0


def parse_tlv_log(input_file: str) -> str or None:
    print("parse")
    output_file = input_file[:-4] + "_parsed.log"

    try:
        with open(input_file, "rb") as f:
            readed = f.read()
    except FileNotFoundError:
        return None

    config = {
        0x01: {TLV.Config.Type: bytes, TLV.Config.Name: 'timestamp'},
        0x02: {TLV.Config.Type: str, TLV.Config.Name: 'tag'},
        0x03: {TLV.Config.Type: bytes, TLV.Config.Name: 'data'},
        0x04: {TLV.Config.Type: str, TLV.Config.Name: 'string'},
        0x05: {TLV.Config.Type: str, TLV.Config.Name: 'level'},
        0x2F: {TLV.Config.Type: TLV, TLV.Config.Name: 'main'},
    }
    TLV.set_tag_map(config)

    with open(output_file, "w") as f:
        index = 0
        while index < len(readed):
            tlvlen = readed[index + 1]
            tlvlen_size = get_tlv_len_size(tlvlen)
            if tlvlen_size > 0:
                tlvlen = int.from_bytes(readed[index + 2:index + 2 + tlvlen_size], byteorder='big')
            f.write("============\n")
            data = readed[index:index + tlvlen + 2 + tlvlen_size]
            t = TLV()
            t.parse_array(data)
            try:
                timestamp = int.from_bytes(t['main']['timestamp'], byteorder='little')
                f.write(datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'))
            except KeyError:
                pass
            try:
                f.write("[" + t['main']['level'] + "]")
            except KeyError:
                pass
            try:
                f.write("[" + t['main']['tag'] + "]")
            except KeyError:
                pass
            try:
                f.write(" " + hexify_bytes(t['main']['data']) + "\n")
            except KeyError:
                pass
            try:
                f.write(" " + t['main']['string'] + "\n")
            except KeyError:
                pass
            index += tlvlen + 2 + tlvlen_size
    return output_file


def main():
    parse_tlv_log("../kitbox_logs/123/log_2021-09-17-105711.log")


if __name__ == "__main__":
    main()
