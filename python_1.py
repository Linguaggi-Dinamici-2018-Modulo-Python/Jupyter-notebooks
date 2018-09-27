
# coding: utf-8

# # Obiettivi del modulo Python (6 CFU)
# ## Python ... pythonic
# ## Salto di qualità negli skill di programmazione
# ## Capacità progettuali
# ## Implementazione di algoritmi non banali
# ## Strutture dati e data management
# ## -----------------------------------------------------------------------------------------
# ## Materiale disponibile su: 
# ##     https://github.com/Linguaggi-Dinamici-2018-Modulo-Python/

# # Quale Python e quale ambiente di lavoro?
# 
# 1. Useremo Python 3, naturalmente in ambiente Linux
# 2. Ma potremo "far girare" i nostri programmi (script) in molti modi diversi, "secondo i gusti"
#     3. Invocando gli script da shell (dopo averli resi eseguibili)
#     4. Interagendo direttamente con l'interprete
#     5. Usando la shell interattiva ipython3 (sudo apt-get install ipython3)
#     6. Usando (ipython3 da) notebook jupyter (sudo apt-get install jupyter)
#     7. Usando un IDE
# 4. ... con l'ulteriore grado di libertà di usare Python nella distribuzione Anaconda
# 5. Due fra i possibili IDE disponibili
#     8. Spyder per Python 3 (sudo apt-get install spyder3)
#     9. PyCharm: https://www.jetbrains.com/pycharm/download/#section=linux) oppure (debian/ubuntu/...)
#                sudo apt-get install snapd
#                sudo snap install pycharm-community --classic

# ## Per chi preferisce (o "per quando dovremo") lavorare con editor+shell command

# In[ ]:


#!/usr/bin/env python3


if __name__=='__main__':
    # qui inserire il codice Python
    # partendo da questo livello di indent
    # Ecco il più semplice degli esempi
    print("Hello world!")


# ### Per eseguire lo script
# 
# \> python3 hello_world.py
# 
# ### ... oppure
# 
# \> chmod u+x hello_world.py
# 
# \> ./hello_world.py

# # Iterabili e iteratori

# ### Problema: generare, uniformemente a caso, 10 numeri interi nell'intervallo [1,10] 

# In[ ]:


from random import random
i = 0
while i<10:
 print(1+int(random()*10))
 i = i+1
print(i)    


# ## Come script completo

# In[ ]:


#!/usr/bin/env python3


if __name__=='__main__':
    from random import random
    i = 0
    while i<10:
        print(1+int(random()*10))
        i = i+1


# ## o anche...

# In[ ]:


#!/usr/bin/env python3


from random import random

def main():
    i = 0
    while i<10:
        print(1+int(random()*10))
        i = i+1

if __name__=='__main__':
    main()


# ### Inciso: Python dispone di una sterminata quantità di moduli (librerie) utilizzabili in toto o in parte

# In[ ]:


from random import random
# importa la definizione della funzione random 
# (incluse tutte le eventuali dipendenze) dal modulo omonimo


# ### Fare le cose nel modo giusto in Python $\longrightarrow$ in ***pythonic***
# ### In Python non non si può scrivere (con nessuna "variante sintattica") qualcosa del tipo:

# In[ ]:


for i=0 to 9:                   # Non funziona
    print(1+int(random()*10))
for (i=0, i<10, i++):           # Non funziona
    print(1+int(random()*10))


# In[ ]:


#### In Python (diremmo anzi "in pythonic") si scrive:


# In[ ]:


for i in range(10):
    print(1+int(random()*10))
    
# range() restituisce un iterabile, ovvero un oggetto Python che può essere
# "visitato" sequenzialmente (elemento dopo elemento) secondo un ben preciso ordine. 


# In[ ]:


# range può avere fino a tre parametri espliciti (start, stop, step)
for i in range(0,10,2):
    print(i)


# ### Sono molti gli oggetti Python ***iterabili***, cioè che possono essere visitati in questo modo (con brutta traduzione tecnica, diremo "iterati")

# ### Ad esempio, le liste sono iterabili

# In[ ]:


L = ['assert','pass','with','continue','break','yield']
for simple_statement in L:
    print("{} is a simple statement".format(simple_statement))


# 
# ### Poiché i dettagli su "come" iterare, dipendono dal particolare oggetto, il processo di iterazione si articola in due fasi:
# 
# 1) dall'iterabile di definisce un oggetto ***iteratore***, che "sa" come accedere agli elementi, uno per volta;
# 
# 2) ogni iteratore espone poi funzioni standard che possono essere usate per l'iterazione
# 
# ### Gli iteratori possono essere esplicitamente "estratti" dagli iterabili 

# In[ ]:


R=range(0,10,2)  # R è un iterabile
print(R.start,R.stop,R.step) # start, stop e step sono attributi di un iterabile
RI = iter(R)     # La funzione iter "estrae" un iteratore da un iterabile
i = next(RI)     # Finalmente è la funzione next che "percorre" gli elementi
while i<R.stop:
    print(i)
    i = next(RI)


# In[ ]:


L = ['assert','pass','with','continue','break','yield']
iterator = iter(L)
L.append('dummy')
while True:
    try:
        simple_statement = next(iterator)
        print("{} is a simple statement".format(simple_statement))
    except StopIteration:
        break


# ### Ritorneremo più avanti sull'argomento degli iteratori e degli iterabili 

# # Altri ***Compound statements***

# ## ***If [else]*** statement

# In[ ]:


def eqn1solve(a,b):
    """Solve equation a*x+b=0"""
    if (a==0):
        if (b!=0):
            print("Eqn impossible")
        else:
            print("Identity 0=0")
    else:
        if (b==0):
            print("Solution x=0")
        else:
            print("Solution x={0}".format(-b/a))
            
eqn1solve(2,1)
help(eqn1solve)
print(eqn1solve.__doc__)


# ## ***If [elif] [else]*** statement

# In[ ]:


def eqn1solve(a,b):
    """Solve equation a*x+b=0"""
    if (a==0 and b==1):
        print("Eqn impossible")
    elif (a==0):
        print("Identity 0=0")
    elif (b==0):
        print("Solution x=0")
    else:
        print("Solution x={0}".format(-b/a))

eqn1solve(2,1)


# ## ***try ... except***

# In[ ]:


class OutOfBound(Exception):
    pass

while True:
    try:
        v = input("Scegli un numero intero fra 1 e 10: ")
        n = int(v)
        if (n<1 or n>10):
            raise OutOfBound
        break
    except ValueError:
        print("Letterale non riconosciuto come numero intero! Riprovare ...")
    except OutOfBound:
        print("Il numero non è compreso nell'intervallo desiderato! Riprovare ...")

print("Hai scelto il numero {}".format(v))


# # I tipi di dato in Python

# ## Tipi predefiniti

# In[ ]:


print(type(3))
print(type(3.14))
print(type('Hello world'))
print(type("Hello world"))
print(type(True))
print(type(('a',1,'b',2)))
print(type(['a',1,'b',2]))
print(type({'a':1,'b':2}))
print(type({'a','b','c'}))


# ### Sono tutti ***first class objects***

# In[ ]:


print(type(complex('1-2j')))
print(type(complex(1,-2)))
print(type(range(0,10,3)))
def f1(x):
    return x+1

exec("""def f2(x):
    y = x+1
    return y""")

f3 = f2
print("s1: {0}\ns2: {1}\ns3: {2}".format(type(f1),type(f2),type(f3)))

print(type(lambda x: x+1))

print(f2(2))

def f4(x):
    def f2(x):
        return 2*x
    return f2(x)

print(f4(4))
print(f2(4))


# ### In python il tipo è associato all'oggetto, non alla variabile (nome), che non deve essere dichiarata

# In[ ]:


x = 10
print(type(x))
x = 3.14
print(type(x))
x = "Pi greco"
print(type(x))


# ### Il C, come la grande maggioranza dei linguaggi imperativi, modella l'accesso agli oggetti mediante i due concetti di ***ambiente*** e ***memoria*** (***store*** e ***environment***). A grandi linee, l'ambiente mappa nomi in locazioni di memoria mentre lo store mappa locazioni in oggetti (valori). In Python esistono solo mapping diretti fra nomi e oggetti, chiamati ***namespace***
# 
# ### int a = 10 
# ### /\* In C il "nome" a identifica una locazione di memoria in cui viene inizialmente scritto il numero intero 10 */

# In[ ]:


x = 10
print(id(x))
x = 3.14
print(id(x))
x = "Pi greco"
print(id(x))
y = 10
print(id(y))
z = "Pi greco"
print(id(z))
print(x == z)
print(x is z)
print([1,2] is [1,2])
print([1,2] == [1,2])
x = [1,2]
z = x
print(x is z)
from copy import copy
z = copy(x)
print(x is z)
print(x == z)
z = x
z[1] = 3
print(x is z)


# # Tipi di dato ***user defined***: classi e oggetti

# In[ ]:


class counter:
    '''Attempt 1.0'''
    val = 0
    def getval():
        '''Return the value of the counter'''
        return val
    def inc():
        '''Increment the counter'''
        val += 1

print(counter.val)
print(counter.inc.__doc__)
print(counter.__doc__)
counter.val = 5
print(counter.val)


# In[ ]:


print(counter.getval())  # Produce (volutamente) errore


# In[ ]:


val = 34
print(counter.getval())


# In[ ]:


class counter:
    '''Attempt 1.1'''
    val = 0
    def getval():
        '''Return the value of the counter'''
        return r.val
    def inc():
        '''Increment the counter'''
        counter.val += 1
print(counter.getval())
counter.inc()
print(counter.getval())


# In[ ]:


c = counter()


# In[ ]:


print(c.val)
print(c.getval())  # Produce (volutamente) errore


# In[ ]:


c.inc()  # Produce (volutamente) errore


# In[ ]:


class counter:
    '''Attempt 1.2'''
    val = 0
    def getval(self):
        '''Return the value of the counter'''
        return counter.val
    def inc(self):
        '''Increment the counter'''
        counter.val += 1
    def reset(self):
        '''Set the counter value back to 0'''
        counter.val = 0


# In[ ]:


c = counter()
print(c.getval())
c.inc()
print(c.getval())
c.reset()
print(c.getval())
counter.inc(c)
print(c.getval())


# In[ ]:


c2 = counter()
print(c2.getval())


# In[ ]:


class counter:
    '''Attempt 2.0'''
    def __init__(self):
        self.val = 0
    def getval(self):
        '''Return the value of the counter'''
        return self.val
    def inc(self):
        '''Increment the counter'''
        self.val += 1
    def reset(self,start=0):
        '''Set the counter value back to 0'''
        self.val = start


# In[ ]:


c = counter()
c.inc()
c.inc()
print(c.getval())
c2 = counter()
print(c2.getval())
print(c.getval())


# ## Un approfondimento su ***iterabili*** e ***iteratori***

# In[ ]:


class Fibonacci:
    '''Iterarable that yields (becomes) an iterator for the Fibonacci numbers'''

    def __init__(self, last):
        self.last = last

    def __iter__(self):
        '''Initialize Fibonacci recurrence'''
        self.x = 0         # F_0
        self.nextx = 1     # F_1
        self.n = 1         # n=1
        return self

    def __next__(self):
        '''Fibonacci-specific cursor method'''
        val = self.x
        if self.n > self.last:
            raise StopIteration
        self.x, self.nextx = self.nextx, self.x + self.nextx  # Pythonic
        self.n += 1
        return val

help(Fibonacci)


# In[ ]:


F = Fibonacci(10)


# ### F è un ***iterabile*** perché implementa il metodo \__iter\__

# In[ ]:


FI = iter(F)


# ### FI è un ***iteratore*** perché implementa il metodo \__next\__

# In[ ]:


for i in range(10):
    print(next(FI))


# ### Si noti che le funzioni ***iter*** e ***next*** sono "zucchero sintattico" rispetto alla chiamata esplicita dei corrispondenti metodi

# In[ ]:


FI = Fibonacci.__iter__(F)
for i in range(10):
    print(Fibonacci.__next__(FI))


# In[ ]:


# Il costrutto for rende tutto ancora più trasparente:
for f in Fibonacci(10):
    print(f)


# ### Qualcuno ha notato che "F is FI"?

# In[ ]:


F is FI


# ### Però attenzione ...

# In[ ]:


F = Fibonacci(10)
for i in range(10):
    print(next(F))


# ### È vero che la classe Fibonacci implementa entrambi i metodi \__iter\__ e \__next\__, ma \__next\__ funziona solo dopo che è stato chiamato \__iter\__, perché quest'ultimo inizializza propriamente la ricorrenza

# ### Viene allora spontanea la domanda: non possiamo spostare le funzionalità di \__iter\__ in \__init\__? In questo modo \__next\__ funzionerebbe subito, evitando così la chiamata di \__iter\__. È quel che fa la classe ***Fibonacci2***

# In[ ]:


class Fibonacci2:
    '''Iterarable for the Fibonacci numbers that coincides with an iterator'''

    def __init__(self, last):
        self.last = last
        self.x = 0         # F_0
        self.nextx = 1     # F_1
        self.n = 1         # n=1

    def __next__(self):
        '''Fibonacci-specific cursor method'''
        val = self.x
        if self.n > self.last:
            raise StopIteration
        self.x, self.nextx = self.nextx, self.x + self.nextx  # Pythonic
        self.n += 1
        return val


# In[ ]:


F = Fibonacci2(10)
for i in range(10):
    print(next(F))


# ### Sembra funzionare perfettamente e abbiamo saltato un passaggio. Ma...

# In[ ]:


for f in Fibonacci2(10):
    print(f)


# ### Fibonacci2 non è un iterabile perché non implementa \__iter\__ e dunque il costrutto ***for*** (che si applica ad iterabili) produce errore.

# ### Basta un semplice aggiustamento, ma la soluzione che si delinea è un po' meno "pulita". Perché?

# In[ ]:


class Fibonacci2:
    '''Iterarable for the Fibonacci numbers that coincides with an iterator'''

    def __init__(self, last):
        self.last = last
        self.x = 0         # F_0
        self.nextx = 1     # F_1
        self.n = 1         # n=1
        
    def __iter__(self):
        return self

    def __next__(self):
        '''Fibonacci-specific cursor method'''
        val = self.x
        if self.n > self.last:
            raise StopIteration
        self.x, self.nextx = self.nextx, self.x + self.nextx  # Pythonic
        self.n += 1
        return val


# In[ ]:


for f in Fibonacci2(10):
    print(f)


# ### Una soluzione ancora diversa, a scopo illustrativo. 

# In[ ]:


class Fibonacci3:
    '''Iterarable for the Fibonacci numbers that pre-computes the whole series'''

    def __init__(self, last):
        self.last = max(2,last)

    def __iter__(self):
        self.seq = [0,1]
        self.n = 0
        for i in range(2,self.last):
            self.seq.append(self.seq[-2]+self.seq[-1])
        return self

    def __next__(self):
        '''Fibonacci-specific cursor method'''
        if self.n==self.last:
            raise StopIteration
        val = self.seq[self.n]
        self.n += 1
        return val


# In[ ]:


F = Fibonacci3(10)
FI = iter(F)
print(FI.seq)


# In[ ]:


for i in range(10):
    print(next(FI))


# ### Un'ultima proposta: iterabile ed iteratore come oggetti di tipo diverso

# In[ ]:


class Fibonacci4:
    '''Iterarable that dynamically "construct" an iterator 
       object for the Fibonacci numbers'''
    class Fibiter:
        pass
    
    def __init__(self, last):
        self.last = last

    def __iter__(self):
        fbi = Fibonacci4.Fibiter()
        fbi.x = 0
        fbi.nextx = 1
        fbi.n = 1
        fbi.last = self.last
        def next(self):
             '''Fibonacci-specific cursor method'''
             val = self.x
             if self.n > self.last:
                raise StopIteration
             self.x, self.nextx = self.nextx, self.x + self.nextx  # Pythonic
             self.n += 1
             return val
        Fibonacci4.Fibiter.__next__ = next
        # fbi.__next__ = next  non funzionerebbe
        return fbi


# In[ ]:


F = Fibonacci4(10)
FI = iter(F)


# ### F è un iterabile ma non un iteratore

# In[ ]:


next(F)


# In[ ]:


print(type(F))
print(type(FI))


# ### L'iteratore è ovviamente FI

# In[ ]:


for i in range(10):
    print(next(FI))


# ### Il costrutto ***for*** "trova tutto a posto"

# In[ ]:


for f in Fibonacci4(10):
    print(f)


# ## Information hiding?

# In[ ]:


class CC:
    """
    Classe per la gestione di un c/c: v1.0 """
    
    def __init__(self, deposito_iniziale = 0):
        print("Apertura conto con {} Euro".format(deposito_iniziale))
        self.saldo_disponibile = deposito_iniziale
        self.saldo()
        
    def versamento(self, importo):
        self.saldo_disponibile += importo
        self.saldo()
        
    def prelievo(self, importo):
        self.saldo_disponibile -= importo
        self.saldo()
        
    def saldo(self):
        print("La disponibilità è di {} Euro".format(self.saldo_disponibile))


# ### La classe ci permette di aprire conti ed eseguire le operazione base di versamento, prelevamento e richiesta del saldo

# In[ ]:


X=CC(100)


# In[ ]:


X.versamento(50)


# In[ ]:


X.prelievo(30)


# In[ ]:


X.saldo()


# ### In Python gli attributi di un oggetto sono però direttamente accessibili

# In[ ]:


X.saldo_disponibile -= 50
print(X.saldo_disponibile)
X.saldo_disponibile = -1000
print(X.saldo_disponibile)


# ### Attributi che iniziano con il doppio underscore in Python sono detti ***superprivati***. È un termine fuorviante. Sono infatti attributi pubblici, ma il cui accesse è reso "complicato" al solo scopo di evitare errori accidentali. La versione 1.1 usa un tale attributo.

# In[ ]:


class CC:
    """
    Classe per la gestione di un c/c: v1.1 """

    def __init__(self, deposito_iniziale = 0):
        print("Apertura conto con {} Euro".format(deposito_iniziale))
        self.__saldo_disponibile = deposito_iniziale
        self.saldo()
        
    def versamento(self, importo):
        print("Versamento di {} Euro".format(importo))
        self.__saldo_disponibile += importo
        self.saldo()
        
    def prelievo(self, importo):
        print("Prelievo di {} Euro".format(importo))
        self.__saldo_disponibile -= importo
        self.saldo()
        
    def saldo(self):
        print("La disponibilità è di {} Euro".format(self.__saldo_disponibile))


# ### Un accesso diretto all'attributo provoca errore

# In[ ]:


X=CC(100)
print(X.__saldo_disponibile)


# ### mentre, chiaramente, l'accesso con i "metodi" della classe è OK

# In[ ]:


X=CC(100)
X.versamento(50)
X.prelievo(50)


# ### Attenzione poi a non confondersi. L'attributo superprivato, non facilmente accessibile in lettura, non è neppure facilmente accessibile in scrittura, come sembrerebbe invece dal fatto che il seguente comando non provoca errore

# In[ ]:


X.__saldo_disponibile = -1000


# ### Il comando semplicemente introduce un nuovo attributo per il solo oggetto X (e non per tutta la classe), attributo che non coincide con quello superprivato definito in CC

# In[ ]:


print(X.__saldo_disponibile)
X.saldo()


# ### Python usa il lo schema cosiddetto del ***name mangling*** per cambiare il nome di un attributo superprivato in modo da evitare riferimenti "accidentali"

# In[ ]:


X._CC__saldo_disponibile = -1000
print(X._CC__saldo_disponibile)
X.saldo()


# ### Non abbiamo dunque effettuato un vero incapsulamento dei dati.
# ### Qualcosa si può comunque fare, restando nella prospettiva "aperta" di Python

# ## Una soluzione ***pythonic***
# ### Obiettivi:
# 1. Inserire almeno controlli per evitare modifiche palesemente errato (tipo versare somme negative) ...
# 2. ... ma evitare di dover ricompilare codice client che faccia accesso diretto agli attributi

# In[ ]:


class CC:
    """
    Classe per la gestione di un c/c: v2.0 """
    
    def __init__(self, deposito_iniziale = 0):
        print("Apertura conto con {} Euro".format(deposito_iniziale))
        self.saldo_disponibile = deposito_iniziale
        
    def valorediretto(self,importo):
        if (importo<0):
            raise ValueError("Non si può assegnare al saldo un valore negativo")
        self.__saldo_disponibile = importo
        self.saldo()
        
    def versamento(self, importo):
        if (importo<0):
            raise ValueError("Non si può versare una somma negativa")
        elif importo>0:
            print("Versamento di {} Euro".format(importo))
            self.__saldo_disponibile += importo
        self.saldo()
        
    def prelievo(self, importo=0):
        if importo<0:
            raise ValueError("Non si può prelevare una somma negativa")
        elif importo>0 and self.__saldo_disponibile-importo<0:
            raise ValueError("Operazione bloccata: il conto andrebbe in rosso")
        elif importo>0:
            print("Prelievo di {} Euro".format(importo))
            self.__saldo_disponibile -= importo
        self.saldo()
                
    def saldo(self):
        print("La disponibilità è di {} Euro".format(self.__saldo_disponibile))
    
    saldo_disponibile=property(prelievo,valorediretto) # Pythonic


# In[ ]:


X=CC(100)


# In[ ]:


X.versamento(200)


# In[ ]:


X.prelievo(10)


# In[ ]:


X.saldo()


# In[ ]:


X.saldo_disponibile = 50


# In[ ]:


X.saldo_disponibile = -50

