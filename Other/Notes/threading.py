# https://pymotw.com/2/threading/

'''
def worker(n):
	print('Worker: %s' % n)

threads = []

for i in range(5):
	t = threading.Thread(target=worker, args=(i,))
	threads.append(t)
	t.start()
'''

'''
def worker():
	print( threading.currentThread().getName(), 'starting ', time.time() )
	time.sleep(2)
	print( threading.currentThread().getName(), 'exiting ', time.time() )

def my_service():
	print( threading.currentThread().getName(), 'starting ', time.time() )
	time.sleep(3)
	print( threading.currentThread().getName(), 'exiting ', time.time() )

t1 = threading.Thread(target=worker)
t2 = threading.Thread(target=my_service, name='at you service')

t1.start()
t2.start()
'''

'''
def doTheThing(self, e, j, k):
	
	# https://pymotw.com/2/threading/
	threading.Thread(
		target = self.doTheThing_, 
		args = (e, j, k) 
	).start()

def keepTicking(self, duration, callback):

	if time.clock() < duration: # seconds
		threading.Timer( self.halfPeriod, callback ).start()
			
def main():
	global clock 
	clock.halfTick()

	if clock.isRising:
		# FSM(clock.value)

	clock.keepTicking(1, main)  # seconds
'''