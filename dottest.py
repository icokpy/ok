import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  #dotenv_path="/Users/cicorias/tmp/cse/okpy/.env")

def foo():
    print(os.getenv("GOOGLE_SECRET"))
    print(os.getenv("GOOGLE_ID"))

foo()
