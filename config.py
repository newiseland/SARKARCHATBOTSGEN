from os import getenv

from dotenv import load_dotenv

load_dotenv()

API_ID = "6435225"
# -------------------------------------------------------------
API_HASH = "4e984ea35f854762dcde906dce426c2d"
# --------------------------------------------------------------
BOT_TOKEN = getenv("BOT_TOKEN", None)
MONGO_URL = getenv("MONGO_URL", None)
OWNER_ID = int(getenv("OWNER_ID", "8128368055"))
SUPPORT_GRP = "SARKAR_SUPPORT"
UPDATE_CHNL = "PROMOTION_UPDATE"
OWNER_USERNAME = "ll_SARKAR_OWNER_ll"
