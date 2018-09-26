
# coding: utf-8

# # Obiettivi del modulo Python (6 CFU)
# ## Python ... pitonico
# ## Strutture dati e data management
# ## Implementazione di algoritmi non banali
# ## Salto di qualità negli skill di programmazione
# ## Abilità progettuale
# ## Materiale disponibile su: 
# ##     https://github.com/Linguaggi-Dinamici-2018-Modulo-Python/

# # Quale Python? Quale ambiente di lavoro?
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


# ## Come script completo

# In[ ]:




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
    elif (a==0 and b==0):
        print("Identity 0=0")
    elif (b==0):
        print("Solution x=0")
    else:
        print("Solution x={0}".format(-b/a))

eqn1solve(2,1)


# ## ***try ... except***

# In[ ]:


class OutOfLimit(Exception):
    pass

v=0
while True:
    try:
        v = input("Scegli un numero intero fra 1 e 10: ")
        n = int(v)
        if (n<1 or n>10):
            raise OutOfLimit
        break
    except ValueError:
        print("Letterale non riconosciuto come numero intero! Riprovare ...")
    except OutOfLimit:
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


# In[ ]:


print(counter.getval())


# In[ ]:


class counter:
    '''Attempt 1.1'''
    val = 0
    def getval():
        '''Return the value of the counter'''
        return counter.val
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
print(c.getval())


# In[ ]:


c.inc()


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
    def reset(self):
        '''Set the counter value back to 0'''
        self.val = 0


# In[ ]:


c = counter()
c.inc()
c.inc()
print(c.getval())
c2 = counter()
print(c2.getval())
print(c.getval())


# In[ ]:


class Fibonacci:
    '''Iterarable that yields (becomes) an iterator for the Fibonacci numbers'''

    def __init__(self, last):
        self.last = last

    def __iter__(self):
        self.x = 0
        self.nextx = 1
        self.n = 1
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


# ### Fibonacci è un ***iterabile*** perché implementa i metodi \__iter\__ e \__next\__

# In[ ]:


F=iter(Fibonacci(10))
for i in range(10):
    print(next(F))


# In[ ]:


# Pythonic
for n in Fibonacci(10):
    print(n)


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
        
    def prelevamento(self, importo):
        self.saldo_disponibile -= importo
        self.saldo()
        
    def saldo(self):
        print("La disponibilità è di {} Euro".format(self.saldo_disponibile))


# In[ ]:


X=CC(100)
X.versamento(50)
X.prelevamento(80)
X.saldo()


# ### In Python gli attributi di un oggetto sono però sempre direttamente accessibili

# In[ ]:


X.saldo_disponibile -= 50
print(X.saldo_disponibile)
X.saldo_disponibile = -1000
print(X.saldo_disponibile)


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
        
    def prelevamento(self, importo):
        print("Prelevamento di {} Euro".format(importo))
        self.__saldo_disponibile -= importo
        self.saldo()
        
    def saldo(self):
        print("La disponibilità è di {} Euro".format(self.__saldo_disponibile))


# ### Attributi come __saldo_disponibile sono detti ***superprivati***

# In[ ]:


X=CC(100)
print(X.__saldo_disponibile)


# In[ ]:


X=CC(100)
X.versamento(50)
X.prelevamento(50)


# In[ ]:


X.__saldo_disponibile = -1000
print(X.__saldo_disponibile)
X.saldo()


# ### Python usa il lo schema cosiddetto del ***name mangling*** per cambiare il nome di un attributo in modo da evitare riferimenti "accidentali"

# In[ ]:


X._CC__saldo_disponibile = -1000
print(X._CC__saldo_disponibile)
X.saldo()


# ## Una soluzione ***pythonic***
# ### Obiettivi:
# 1. Inserire controlli sulla saldo e sugli importi versati...
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
        
    def prelevamento(self, importo=0):
        if importo<0:
            raise ValueError("Non si può prelevare una somma negativa")
        elif importo>0 and self.__saldo_disponibile-importo<0:
            raise ValueError("Operazione bloccata: il conto andrebbe in rosso")
        elif importo>0:
            print("Prelevamento di {} Euro".format(importo))
            self.__saldo_disponibile -= importo
        self.saldo()
                
    def saldo(self):
        print("La disponibilità è di {} Euro".format(self.__saldo_disponibile))
    
    saldo_disponibile=property(prelevamento,valorediretto) # Pythonic


# In[ ]:


X=CC(100)
X.versamento(200)
X.prelevamento(120)
X.saldo()
X.saldo_disponibile = 50
X.saldo()
X.saldo_disponibile = -50

