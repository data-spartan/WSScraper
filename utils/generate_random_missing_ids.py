import pandas as pd
import numpy as np
from os import getenv
from dotenv import load_dotenv
from pathlib import Path
from logger.log_func import *

load_dotenv(".env")
logg=logging_func("random-ids-generator",getenv("sender_logs"))[1] #get only logger object

def generate_miss_ids_first_time():
	"""
	generate unique random ids only first time when neotech_3_live is on production
	checking if file exists if true create file else ignore
	"""
	if not Path(getenv("ids_random_path")).exists():
		logg.info("Created random missing pool of ids.")
		pd.DataFrame(np.random.randint(10**7,10**8-1,40000)).to_csv(getenv("ids_random_path"),index=False,header=False)
	else:
		pass

if __name__ == "__main__":
	generate_miss_ids_first_time()
