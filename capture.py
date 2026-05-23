from scapy.all import sniff
from detector import analyze_packet


def process_packet(packet):

    try:

        # Check if packet has IP layer
        if packet.haslayer('IP'):

            src_ip = packet['IP'].src
            dst_ip = packet['IP'].dst

            packet_size = len(packet)

            protocol = packet['IP'].proto

            # Convert protocol numbers
            if protocol == 6:
                protocol_name = 'TCP'
            elif protocol == 17:
                protocol_name = 'UDP'
            else:
                protocol_name = 'ICMP'

            # Create packet data
            packet_data = {
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'packet_size': packet_size,
                'protocol': protocol_name,
                'connection_rate': 10
            }

            # Send to AI detector
            analyze_packet(packet_data)

    except Exception as e:
        print("Error:", e)


print("Starting live packet capture...")

sniff(prn=process_packet, store=False)