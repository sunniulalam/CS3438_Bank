import customer_class
import teller_class
import queue
import random
import threading
import time

def output(lock, msg):
    with lock:
        print(msg)
def enter_bank(customer, line, lock):
    #output(lock, f"{customer} is going to go to the bank at {customer.arrival}.")
    time.sleep(customer.arrival)
    output(lock, f"{customer} is going to the bank")
    output(lock, f"{customer} is getting into line")
    line.put(customer)
def transact(teller, manager, safe, line, lock, start):
    while True:
        output(lock, f"{teller} is ready to serve")
        try:
            if(time.time()-start > 5):
                break
            customer_thread = line.get(timeout=(5-(time.time()-start)))
            output(lock, f"{customer_thread} introduces itself to {teller}")
            output(lock, f"{teller} is serving {customer_thread}")
            if(customer_thread.transaction==0):
                output(lock, f"{customer_thread} asks for a withdrawal transaction.")
                output(lock, f"{teller} is handling the withdrawal transaction.")
                output(lock, f"{teller} is going to the manager.")
                manager.acquire()
                output(lock, f"{teller} is getting the manager's permission.")
                time.sleep(round(random.uniform(0.005, 0.03), 3))
                output(lock, f"{teller} got the manager's permission.")
                manager.release()
            elif(customer_thread.transaction==1):
                output(lock, f"{customer_thread} asks for a deposit transaction.")
                output(lock, f"{teller} is handling the deposit transaction.")
            output(lock, f"{teller} is going to the safe.")
            safe.acquire()
            output(lock, f"{teller} is in the safe.")
            time.sleep(round(random.uniform(0.01, 0.05), 3))
            output(lock, f"{teller} has finished in the safe")
            safe.release()
            output(lock, f"{teller} is returning back to {customer_thread}")
            output(lock, f"{teller} informs {customer_thread} that the transaction is done.")
            output(lock, f"{customer_thread} leaves the bank.")
        except queue.Empty:
            break

if __name__ == "__main__":
    start=time.time()
    lock = threading.Lock()
    line = queue.Queue()
    manager= threading.Semaphore(1)
    safe= threading.Semaphore(2)
    output(lock, "Opening Time.")
    tellers = []
    customers = []
    for i in range(0, 100): 
        customer = customer_class.Customer(i, random.randint(0,1), round(random.uniform(0, 5), 3))
        customer_thread = threading.Thread(target=enter_bank, args=(customer, line, lock))
        customer_thread.start()
        customers.append(customer_thread)
    for i in range(0, 3):
        teller = teller_class.Teller(i)
        teller_thread = threading.Thread(target=transact, args=(teller, manager, safe, line, lock, start))
        teller_thread.start()
        tellers.append(teller_thread)
       
    for cus in customers:
        cus.join()
    for tel in tellers:
        tel.join()
    output(lock, "Closing time.")