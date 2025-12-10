from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.rifugio import Rifugio


class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    @staticmethod
    def readAllRifugi():
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print('Connection failed!')
            return None
        else:
            cursor = cnx.cursor(dictionary=True)
            query = "SELECT * FROM rifugio"
            cursor.execute(query)

            for row in cursor:
                rifugio = Rifugio(**row)
                result.append(rifugio)

            cursor.close()
            cnx.close()
            return result

    @staticmethod
    def readAllConnessioni(dict_rifugi, year):
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print('Connection failed!')
            return None
        else:
            cursor = cnx.cursor(dictionary=True)
            query = "SELECT * FROM connessione WHERE anno <= %s"
            cursor.execute(query, (year,))

            for row in cursor:
                connessione = Connessione(
                    dict_rifugi[row['id_rifugio1']],
                    dict_rifugi[row['id_rifugio2']],
                    row['distanza'],
                    row['difficolta'])
                result.append(connessione)

            cursor.close()
            cnx.close()
            return result