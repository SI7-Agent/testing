import psycopg2
import datetime

def get_all_otdel(database):
	rows1 = database.fetchall()

	all_otdel = []

	for row in rows1:
		if row[3] not in all_otdel:
			all_otdel.append(row[3])

	return all_otdel

def find_otdel_with_late(database):
	rows1 = database[0].fetchall()
	rows2 = database[1].fetchall()

	bad_otdel = []
	checked_person = []

	for row in rows2:
		if row[4] == 1 and (row[3].hour > 9 or row[3].hour == 9 and row[3].minute > 0) and (row[1] - datetime.datetime.now()).day <= 10:
			 if row[0] not in checked_person:
				checked_person.append(row[0])
				if rows1[row[0] - 1][3] not in bad_otdel:
					bad_otdel.append(rows1[row[0] - 1][3])
	return bad_otdel

def find_most_common_out_empoyees(database):
	rows1 = database[0].fetchall()
	rows2 = database[1].fetchall()

	num_of_outs = [0]*len(rows1)
	bad_guys = []

	for i in rows1:
		for j in rows2:
			if rows1[0] == rows2[0]:
				if 9 < rows2[3].hour < 18 and rows2[4] == 2:				
					num_of_outs[rows1[0] - 1] += 1

	

def find_otdel_with_no_late(database):
	rows1 = database[0].fetchall()
	rows2 = database[1].fetchall()

	bad_otdel = []
	good_otdel = get_all_otdel(database[0])
	checked_person = []

	for row in rows2:
		if (row[3].hour > 9 or row[3].hour == 9 and row[3].minute > 0):
			if rows1[row[0] - 1][3] not in bad_otdel:
				bad_otdel.append(rows1[row[0] - 1][3])

	for i in bad_otdel:
		if i in good_otdel:
			good_otdel.remove(i)
	return good_otdel

conn = psycopg2.connect(database="rk3",
  user="postgres",
  password="rocketman1",
  host="127.0.0.1",
  port="5432"
)

emp = conn.cursor()
emp.execute("SELECT * FROM empoyees")

tim = conn.cursor()
tim.execute("SELECT * FROM empoyees_time")

#print(find_otdel_with_no_late((emp, tim)))

print("success")