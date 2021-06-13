#importing module
import logging

def Logger(nameoffile):
    #Create and configure logger
    logging.basicConfig(filename=f"{nameoffile}"+str()+".log",
                        format='%(asctime)s %(message)s',
                        filemode='a+')
    
    #Creating an object
    logger=logging.getLogger()
    
    #Setting the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)
    return logger
