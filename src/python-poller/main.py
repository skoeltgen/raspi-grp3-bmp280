import time
import mariadb
import sys

from smbus2 import SMBus
from bmp280 import BMP280

# Initialise the BMP280
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)

# Initialize mariadb connection
try:
	conn = mariadb.connect(
		user="root",
		password="example",
		host="mariadb",
		port=3306,
		database="python-measurement"
	)
except mariadb.Error as e:
	print(f"Error connecting to MariaDB Platform: {e}")
	sys.exit(1)

# Get Cursor
cur = conn.cursor()
while True:
	try:
		cur.execute(
			"INSERT INTO metric"
			"(time, temperature, pressure) "
			"VALUES (?, ?, ?)",
			(time.time(), bmp280.get_temperature(), bmp280.get_pressure())
		)
	except mariadb.Error as e:
		print(f"Error: {e}")

	conn.commit()
	time.sleep(60)
