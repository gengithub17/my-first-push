import sqlite3

# FILENAME = "ClientInfo.db"
# TABLE_NAME = "Client"
# CONNECTION = sqlite3.connect(FILENAME)
# CURSOR = CONNECTION.cursor()

# query = """
#     SELECT *
#     FROM Client
#     """
# CURSOR.execute(query)
# print(CURSOR.fetchall())

import datetime
print(datetime.datetime.now().strftime('%H%M'))
