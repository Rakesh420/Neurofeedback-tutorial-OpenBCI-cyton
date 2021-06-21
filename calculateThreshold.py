from oscpy.server import OSCThreadServer
import time
from time import sleep
import numpy as np
import threading
import progressbar

beta=[]

def data_handler():
	print("\n")
	print("CALIBRATING FEEDBACK THRESHOLD ")
	print("\n")
	print("CONCENTRATE FOR 30 SECONDS")
	print("\n")

	osc = OSCThreadServer()
	sock = osc.listen(address='127.0.0.1', port=12345, default=True)

	@osc.address(b'/out/beta')
	def callback(s):
		beta_avg = s
		beta.append(beta_avg)
		np_beta=np.array(beta)
		np.save('feedback_avg.npy',np_beta)


def compute_feedback():
	for i in progressbar.progressbar(range(30)):
		time.sleep(1)
	print("\n")

	inputFile = np.load('feedback_avg.npy').tolist()

	cleanedList_db = [x for x in inputFile if str(x) != 'nan']
	beta_avg_max = max(cleanedList_db)
	beta_avg_min = min(cleanedList_db)
	beta_avg = sum(cleanedList_db)/len(cleanedList_db)
	print("Beta Max :",beta_avg_max)
	print("Beta Min :",beta_avg_min)
	print("Beta Average :",beta_avg)
	print("\n")
	print("THRESHOLD VALUE TO BE SET IN NEUROMORE STUDIO : ",beta_avg)



if __name__ == "__main__":
	x = threading.Thread(target=data_handler)
	x.daemon = True
	x.start()
	compute_feedback()
	

