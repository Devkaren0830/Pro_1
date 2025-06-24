import datetime

class fecha_timestamp():
    def fecha(fecha):
        fecha = fecha.split('-')
        fecha_2 = datetime.datetime(int(fecha[0]), int(fecha[1]), int(fecha[2]))
        fecha_timestamp = int(fecha_2.timestamp())
        return fecha_timestamp