import datetime

class date_timestamp():
    # Converit fecha año mes y dia a timestamp
    def date(date):
        date = date.split('-')
        date_2 = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
        date_timestamp = int(date_2.timestamp())
        return date_timestamp
    

    # Fecha actual obtener en timestamp
    def current_date():
        return int(datetime.datetime.now().timestamp())