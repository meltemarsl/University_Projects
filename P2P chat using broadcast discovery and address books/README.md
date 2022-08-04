PCAP filter:
	(tcp.port == 12345 and tcp.flags.ack == 1 and tcp.flags.push == 1 and tcp.flags.fin == 0) or (udp.port==12345)