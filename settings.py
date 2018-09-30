import os
import environ


# Load DATABASE_URL and Google API credentials from local environment file
cur_path = os.path.dirname(__file__)
env_file = os.path.join(cur_path, 'local.env')
if os.path.exists(env_file):
    environ.Env.read_env(str(env_file))

DATABASE_URL = os.environ['DATABASE_URL']
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
