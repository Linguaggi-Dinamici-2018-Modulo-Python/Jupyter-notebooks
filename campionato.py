#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 14:35:48 2018

@author: mauro
"""
import pymysql
import json
from functools import reduce

class campionato:
    
    # return codes
    QUERY_OK = 0
    ERR_INS = -1
    ERR_SEL = -2
    ERR_VIEW = -3
    
    def __init__(self, nome=None):
        '''
        nome è una stringa del tipo "Serie A 2015/16" oppure
        il nome completo di un file json con tutti i dati sul campionato
        '''
        if not nome:
            return
        retcode, results = \
            self.__selOneQuery("SELECT id FROM Campionati WHERE nome = %s;", \
                               nome)
        if retcode == campionato.QUERY_OK:
            if not results:
                self.__nuovoCamp(nome)
            else:
                self.__nomecamp = nome
                self.__risultati = "`Risultati_" + \
                                    self.__nomecamp.replace(" ","_") + "`";
                self.__punti = "`Risultati_" + \
                                    self.__nomecamp.replace(" ","_") + "_2`";
        else:
            return retcode                            

    def __dbOpen(self, autocommit=False):
        '''
        Apre una connessione con il database di test
        '''
        return pymysql.connect("localhost","testuser","testpasswd",\
                               "testdb",autocommit=autocommit)    
    
    def __selOneQuery(self, query, params=None):
        '''
        Esegue una query di selezione e restituisce un unico (o l'unico) record
        '''
        with self.__dbOpen() as cursor:
            try:
                cursor.execute(query, params)
                results = cursor.fetchone()
                retcode = campionato.QUERY_OK
            except Exception as e:
                retcode = campionato.ERR_SEL
                results = str(e)
            cursor.close()
        return retcode, results
    
    def __selQuery(self, query, params=None):
        '''
        Esegue una query di selezione e retituisce tutti i record
        '''
        with self.__dbOpen() as cursor:
            try:
                cursor.execute(query, params)
                results = cursor.fetchall()
                retcode = campionato.QUERY_OK
            except Exception as e:
                retcode = campionato.ERR_SEL
                results = str(e)
            cursor.close()
        return retcode, results
            
    def __insQuery(self, query, params=None):
        '''
        Esegue una query di inserimento (o, più generalmente, che prevede
        una modifica del DB). La query è atomicizzata: se prevede più modifiche
        ma si verificano errori, allora nessuna modifica viene effettuata
        '''
        with self.__dbOpen() as cursor:
            try:
                cursor.execute(query, params)
                cursor.connection.commit()
                retcode = campionato.QUERY_OK
            except:
                cursor.connection.rollback()
                retcode = campionato.ERR_INS
            cursor.close()
        return retcode
 
    def __getIdSquadre(self,squadre):
        '''
        Metodo chiamato solo nel caso di nuovo campionato.
        Recupera dal DB gli identificatori delle squadre partecipanti.
        Se una squadra non è ancora inserita (caso prevedibilmnete raro
        in un DB reale) la inserisce e poi ne recupera subito l'id
        '''
        query = "SELECT id FROM Squadre WHERE nome = %s;"
        query2 = "INSERT INTO Squadre (nome) VALUES (%s);"
        idSquadre = {} 
        with self.__dbOpen() as cursor:
            for squadra in squadre:
                try:
                    nlines = cursor.execute(query,squadra)
                except:
                    return campionato.ERR_SEL, squadra
                if nlines == 0:
                    try:
                        cursor.execute(query2, squadra)
                        cursor.connection.commit()
                    except:
                        cursor.connection.rollback()
                        return campionato.ERR_INS, squadra
                    try:
                        cursor.execute(query, squadra)
                    except:
                        return campionato.ERR_SEL, squadra                
                idSquadre[squadra] = cursor.fetchone()[0]   
        return campionato.QUERY_OK, idSquadre
    
    def __nuovoCamp(self, nome):
        '''
        Legge il file json e inserisce il nuovo campionato.
        Inserisce poi tutte le partite in calendario e i risultati.
        Infine, genera due viste utilizzate per semplificare le
        query di risposta alle interrogazioni utente e per generare
        automaticamente la classifica.
        '''
        with open(nome) as f:
            nuovocamp = json.load(f)
        self.__nomecamp = nuovocamp['name']
        # Controlliamo comunque che il campionato non sia già stato inserito
        query = "SELECT id FROM Campionati WHERE nome=%s;"
        retcode, result = self.__selOneQuery(query, self.__nomecamp)
        if retcode != campionato.QUERY_OK:
            return retcode
        if result:
            self.squadre
            return self.__init__(self.__nomecamp)
            
        # Il campionato non esiste e va inserito
        query = "INSERT INTO Campionati (nome) VALUES (%s);"
        retcode = self.__insQuery(query, self.__nomecamp)
        if retcode != campionato.QUERY_OK:
            return retcode
        
        # Dobbiamo subito recuperare l'id del campionato appena inserito
        query = "SELECT id FROM Campionati WHERE nome=%s;"
        retcode, result = self.__selOneQuery(query, self.__nomecamp)
        if retcode  != campionato.QUERY_OK:
            return retcode
        idcamp = result[0]
            
        # Determinazione delle squadre partecipanti e loro (eventuale) 
        # inserimento nel database
        giornate = nuovocamp['rounds']
        prima = [(partita['team1']['name'],partita['team2']['name']) \
                 for partita in giornate[0]['matches']]
        self.__squadre = reduce(lambda x,y: x+y, prima)
        retcode, ids = self.__getIdSquadre(self.__squadre)
        if retcode != campionato.QUERY_OK:
            return retcode
        self.__idSquadre = ids
   
        # Inserimento delle partite in calendario e dei risultati
        numsquadre = len(self.__squadre)
        durata = numsquadre-1
        query = "INSERT INTO Calendario " + \
                "(campionato, giornata, AR, data, locali, ospiti) " +\
                "VALUES (%s, %s, %s, %s, %s, %s);"
        query2 = "SELECT id FROM Calendario WHERE " + \
                 "locali = %s AND ospiti = %s AND data = %s;"
        query3 = "INSERT INTO Risultati " + \
                 "(partita, retiLocali, retiOspiti) " + \
                 "VALUES (%s, %s, %s);"
        for numGiornata, giornata in enumerate(giornate):
            for partita in giornata['matches']:
                params = (idcamp, numGiornata%durata+1, \
                           ['A','R'][numGiornata>=durata], \
                           partita['date'], \
                           self.__idSquadre[partita['team1']['name']], \
                           self.__idSquadre[partita['team2']['name']])
                retcode = self.__insQuery(query, params)
                if retcode != campionato.QUERY_OK:
                    return retcode

                params2 = (self.__idSquadre[partita['team1']['name']], \
                           self.__idSquadre[partita['team2']['name']], \
                           partita['date'])
                
                retcode, result = self.__selOneQuery(query2, params2)
                if retcode  != campionato.QUERY_OK:
                    return retcode
                idGara = result[0]
                retcode = self.__insQuery(query3, (idGara, \
                                            partita['score1'], \
                                            partita['score2']))
                if retcode != campionato.QUERY_OK:
                    return retcode
                
        # Creazione delle viste
        self.__risultati = "`Risultati_" + \
                                self.__nomecamp.replace(" ","_") + "`";
        query = "CREATE VIEW " + self.__risultati + " AS " + \
        "SELECT Cal.giornata AS giornata, Cal.Ar AS girone, " + \
        "       Cal.data AS data, " + \
        "       SC.nome AS locali, SO.nome AS ospiti, " + \
        "       Ris.retiLocali AS retiLocali, Ris.retiOspiti AS retiOspiti " +\
        "FROM Campionati AS Cam " + \
        "INNER JOIN Calendario AS Cal ON Cal.campionato = Cam.id " + \
        "INNER JOIN Squadre AS SC ON Cal.locali = SC.id " + \
        "INNER JOIN Squadre AS SO ON Cal.ospiti = SO.id " + \
        "LEFT JOIN Risultati AS Ris ON Ris.partita = Cal.id " + \
        "WHERE Cam.id=%s ORDER BY girone ASC, Giornata ASC;"
        retcode = self.__insQuery(query, idcamp)
        if retcode  != campionato.QUERY_OK:
            return retcode
        
        self.__punti = "`Risultati_" + \
                            self.__nomecamp.replace(" ","_") + "_2`";
        query = "CREATE VIEW " + self.__punti + " AS " + \
        "SELECT R.giornata AS giornata, " + \
        "       R.locali AS squadra, 'C' AS casa_fuori, " + \
        "       R.retiLocali AS reti_fatte, " + \
        "       R.retiOspiti AS reti_subite, " + \
        " (CASE WHEN (R.retiLocali > R.retiOspiti) THEN 3 " + \
        "       WHEN (R.retiLocali = R.retiOspiti) THEN 1 " + \
        "       ELSE 0 END) AS Punti " + \
        "FROM " +  self.__risultati + " AS R " + \
        "WHERE (R.retiLocali IS NOT NULL) " + \
        "UNION " + \
        "SELECT R.giornata AS giornata, " + \
        "       R.ospiti AS squadra, 'F' AS casa_fuori, " + \
        "       R.retiOspiti AS reti_fatte, " + \
        "       R.retiLocali AS reti_subite, " + \
        " (CASE WHEN (R.retiOspiti > R.retiLocali) THEN 3 " + \
        "       WHEN (R.retiLocali = R.retiOspiti) THEN 1 " + \
        "       ELSE 0 END) AS Punti " + \
        "FROM " +  self.__risultati + " AS R " + \
        "WHERE (R.retiLocali IS NOT NULL);"
        retcode = self.__insQuery(query)
        if retcode  != campionato.QUERY_OK:
            return retcode
        
    def partita(self, locali, ospiti):
        '''
        Restituisce i dati di una singola partita, specificata
        tramite i nomi (in ordine) delle due squadre
        '''
        query = "SELECT giornata, girone, data, retiLocali, retiOspiti " + \
                "FROM " + self.__risultati + \
                "WHERE locali = %s AND ospiti = %s;"
        retcode, results = self.__selOneQuery(query, (locali, ospiti))
        if retcode != campionato.QUERY_OK:
            return retcode
        return results
    
    def doppioConfronto(self, sq1, sq2):
        '''
        Restituisce i dati del doppio confronto fra due squadre;
        prima il risultato dell'andata e poi quello del ritorno,
        indipendentemente dall'ordine con cui sono state specificate 
        le due squadre
        '''
        p1 = self.partita(sq1, sq2)
        if p1 == campionato.ERR_SEL:
            return campionato.ERR_SEL
        p2 = self.partita(sq2, sq1)
        if p2 == campionato.ERR_SEL:
            return campionato.ERR_SEL
        if p1[2]<p2[2]:
            return [(sq1,sq2)+p1, (sq2,sq1)+p2]
        else:
            return [(sq2,sq1)+p2, (sq1,sq2)+p1]
    
    def cammino(self, squadra):
        '''
        Restituisce tutti i risultati (in ordine di giornata)
        di una data squadra
        '''
        query = "SELECT * FROM " + self.__risultati + \
                "WHERE locali = %s OR ospiti = %s;"
        retcode, results = self.__selQuery(query, (squadra, squadra))
        if retcode != campionato.QUERY_OK:
            return retcode
        return results
    
    def giornata(self, numero, girone):
        '''
        Restituisce i risultati di una giornata, specificata
        col numero e con l'indicazione di andata (A) o ritorno (R)
        '''
        query = "SELECT data, locali, ospiti, retiLocali, retiOspiti FROM " + \
                                                 self.__risultati + \
                "WHERE giornata = %s AND girone = %s;"
        retcode, results = self.__selQuery(query, (numero, girone))
        if retcode != campionato.QUERY_OK:
            return retcode
        return results   
        
    def classifica(self):
        '''
        Genera e restituisce la classifica
        '''
        query = "SELECT squadra, " + \
        "       SUM(punti) AS Pt, COUNT(*) as G, " + \
        "       SUM(CASE WHEN punti=3 THEN 1 ELSE 0 END) AS V, " + \
        "       SUM(CASE WHEN punti=1 THEN 1 ELSE 0 END) AS N, " + \
        "       SUM(CASE WHEN punti=0 THEN 1 ELSE 0 END) AS P, " + \
        "       SUM(reti_fatte) AS GF, " + \
        "       SUM(reti_subite) AS GS, " + \
        "       SUM(reti_fatte)-SUM(reti_subite) AS Diff " + \
        "FROM " + self.__punti + \
        "GROUP BY squadra " + \
        "ORDER BY 2 DESC, 9 DESC, 1 ASC;"
        retcode, results = self.__selQuery(query)
        if retcode != campionato.QUERY_OK:
            return retcode
        return [(sq[0], int(sq[1]), sq[2], int(sq[3]), int(sq[4]), int(sq[5]), \
             int(sq[6]), int(sq[7]), int(sq[8])) for sq in  results]
        
    def __getattr__(self,name):
        if name == '_campionato__squadre':
            query = "SELECT DISTINCT Squadre.nome FROM Squadre " + \
                    "INNER JOIN Calendario ON Calendario.locali=Squadre.id " + \
                    "INNER JOIN Campionati ON campionato=Campionati.id " + \
                    "WHERE Campionati.nome=%s;"
            retcode, results = self.__selQuery(query,self.nome)
            if retcode == campionato.QUERY_OK:
                self.__squadre = reduce(lambda x,y: x+y, results)
                return self.__squadre
        else:
            print("La classe campionato non ha attributo "+name)
            return
            
    @property
    def nome(self):
        return self.__nomecamp
    
    @property
    def squadre(self):
        return self.__squadre
        
        
        
        
        
        
        
        