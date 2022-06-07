import dotenv
import os
dotenv.load_dotenv(dotenv.find_dotenv())

api_key_tt = os.getenv("api_key_tt")
api_secret_key_tt = os.getenv("api_secret_key_tt")


print(api_key_tt)