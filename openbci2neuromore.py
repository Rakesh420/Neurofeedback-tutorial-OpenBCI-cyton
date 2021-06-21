import pylsl
from pylsl import StreamInlet, resolve_stream
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client


class streamOSC:
	def __init__(self):
		self.openbci_stream_name = 'obci_eeg1'
		self.openbci = resolve_stream('type', 'EEG')

	def openbci_stream(self):
		try:
			for i in range (len(self.openbci)):
				if (self.openbci[i].name() ==self. openbci_stream_name):
					index = i
					#return "OpenBCI stream available"

			self.inlet1 = StreamInlet(self.openbci[index])
			return self.inlet1
		except NameError:
			return "Error: OpenBCI stream not available\n\n\n"

	def sendOSC(self, channel, data):
		parser = argparse.ArgumentParser()
		parser.add_argument("--ip", default="127.0.0.1",help="The ip of the OSC server")
		parser.add_argument("--port", type=int, default=4545,help="The port the OSC server is listening on")
		args = parser.parse_args()
		client = udp_client.SimpleUDPClient(args.ip, args.port)
		client.send_message(channel ,data)

def main():
	stream_data = streamOSC()
	openbci_stream = stream_data.openbci_stream()	
	while True:
		sample, timestamp = openbci_stream.pull_sample()
		FP1 = sample[0]
		FP2 = sample[1]
		print("Electrode 1 : ",sample[0])
		print("Electrode 2 : ",sample[1])
		stream_data.sendOSC("/openbci/FP1",FP1)
		stream_data.sendOSC("/openbci/FP2",FP2)



if __name__ == "__main__":
	main()