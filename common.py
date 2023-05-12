import sqlite3

def _rgb(rgb):
	#RGB FUNCTION IN PYTHON
	return "#%02x%02x%02x" % rgb

def optenerUsuarioActivo():
	with sqlite3.connect("bbdd/BBDD") as bd:
		cursor = bd.cursor()

		cursor.execute("SELECT * FROM USUARIOACTIVO")
		active_user = cursor.fetchall()

		if active_user == []:
			active_user = 1
		else:
			active_user = active_user[0][0]

		return active_user

def optenerTazaCambiaria():
	with sqlite3.connect("bbdd/BBDD") as bd:
		cursor = bd.cursor()

		cursor.execute("SELECT * FROM TAZACAMBIARIA")
		taza = cursor.fetchall()

		return taza[0][0] 