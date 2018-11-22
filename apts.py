#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 08:57:38 2018

@author: mauro
"""

import networkx as nx
from random import randint
from functools import reduce
from copy import copy
from time import sleep
import pdb

class repository:
    
    def __init__(self, packageList):
        self.__createRepo(packageList)
    
    def __createRepo(self, packageFile):
        '''
        Crea una rappresentazione Python dei pacchetti disponibili in una
        data distribuzione, e descritti nel file in input. Per gli scupi di
        questa esercitazione, non vengono considerati due fattori importanti
        che vengono invece trattati da apt: (1) la dipendenza da particolari
        versioni di un dato pacchetto (in altri termini, è come se esistesse
        una sola versione del pacchetto, nonostante il version number venga
        registrato), (2) le dipendenze in alternata. A questo secondo
        riguardo, se esiste la dipendenza del pacchetto a dai pacchetti
        b, c o d (espressa come: b | c | d), viene considerata solo la
        dipendenza da b.
        '''
        def parseDependencies(depString):
            '''
            Funzione interna per il parsing della stringa che elenca le
            dipendenze. Esclude la dipendenza da una particolare versione come
            pure le dipendenze in alternativa (in caso usa solo la prima).
            '''
            dependencies = []
            for dep in depString.split(','):
                if dep.find('|') != -1:
                    dep = dep.split('|')[0]
                dependencies.append(dep.strip().split()[0])
            return dependencies
            
        with open(packageFile) as f:
            lines = f.readlines()
        self.__packages = {}
        name = ''
        for line in lines:
            if line.find('Package:') == 0:
                name = line.strip().split(' ')[1]
                self.__packages[name] = {}
            elif line.find('Version:') == 0:
                self.__packages[name]['Version'] = line.strip().split(' ')[1]
            elif line.find('Installed-Size:') == 0:
                self.__packages[name]['Installed-Size'] = \
                            int(line.strip().split(' ')[1])
            elif line.find('Size:') == 0:
                self.__packages[name]['Size'] = int(line.strip().split(' ')[1])
            elif line.find('Description:') == 0:
                self.__packages[name]['Description'] = \
                            line.split(':',1)[1].strip()
            elif line.find('Depends:') == 0:  
                self.__packages[name]['Depends'] = \
                            parseDependencies(line.split(':',1)[1].strip())
                
    def __newDependency(self, package, depends):
        '''
        Introduce una nuova dipendenza per package, se questa non esiste già
        '''
        dependencies =  self.__packages[package]['Depends']
        for p in dependencies:
            if p==depends:
                print('Package {} already depends on package {}'.\
                      format(package, depends))
                print('Repository unchanged')
                return
        self.__packages[package]['Depends'].append(depends)
    
    def __newVersion(self, package, version=None):
        '''
        Cambia il numero di versione di package in uno superiore
        (questo controllo per ora manca)
        '''
        self.__packages[package]['Version'] = version
    
    def packageInfo(self, package):
        '''
        Restituisce la stringa nel campo Description
        '''
        p = self.__packages.get(package, False)
        if not p:
            print("Package {} not found".format(package))
        else:
            print("Nome: {}".format(package))
            for key, value in p.items():
                print("{}: {}".format(key,value))

    def update(self, package1=None, version=None, package2=None):
        '''Si possono specificare due o tre paramatri ma obbligatoriamente
           deve essere specificato package1. Se è specificata una versione,
           questa viene applicata a package1. Se viene specificato package2,
           viene introdotta una nuova dipendenza per package1
        '''
        if not package1 or package1 not in self.__packages.keys():
            if package1:
                print("E: Unable to locate package {}".format(package1))
            else:
                print("package1 argument required")
            print('Repository unchanged')
            return
        # package1 specificato ed esistente
        if package2 and package2 in self.__packages.keys():
            # package1 specificato ed esistente
            if version:
                self.__newVersion(package1, version)
            self.__newDependency(package1, package2)
        elif package2:
            print("E: Unable to locate package {}".format(package2))
            if version:
                self.__newVersion(package1, version)
            else:
                print('Repository unchanged')
        elif version:
            self.__newVersion(package1, version)
        else:
            print('Missing both package2 and version information (one requited)')
                
    @property
    def packages(self):
        return self.__packages

class apts:
    '''Classe che simula il (una versione semplificata del) sistema
       di gestione dei pacchetti apt. Sono molte le semplificazioni, delle
       quali elenchiamo solo le più importanti.
       1) I pacchetti stessi "non esistono". La simulazione serve ad illustrare
          non l'installazione (o la rimozione) dei pacchetti bensì solo la loro
          gestione con, in particolare, il soddisfacimento delle relazioni di
          dipendenza. Un pacchetto risulterà "installato" semplicemente quando
          le sue informazioni di controllo saranno presenti nella struttura
          che rappresenta il valore dell'attributo __installed
       2) Le operazioni disponibili sono solo update, upgrade, install,
          remove e search
       3) Le dipendenze non riguardano le versioni, se il pacchetto A dipende
          dal pacchetto B, la dipendenza si ritiene soddisfatta se risulta
          installata una qualsiasi versione di B.
       4) Sono ignorate tutte le altre relazioni fra pacchetti (coflicts, 
          pre-depends, ...)
       5) Le modifiche consentite nel repository sono solo aggiornamento di
          versione e introduzione di una nuova dipendenza. Stante l'assunzione
          in 3), l'aggiornamento di versione fa si che un eventuale upgrade 
          riguardi solo il pacchetto aggiornato.
       6) In partenza sono eliminate dipendenze della forma "A dipende da B o C".
    '''
    def __init__(self, repository):
        self.__source = repository  # Indicazione della source
        self.__installed = {}       # Dizionario dei pacchetti installati
        self.update()
        #self.__packages, inizializzato da self.update, elenco di tutti i pkg
        #self.__graph, inizializzato da self.__dependencyGraph
        #self.__SCC, inizializzato da self.__dependencyGraph

    def __dependencyGraph(self):
        '''
        Calcola il grafo delle dipendenze dei packages e le
        sue componenti fortemente connesse.
        '''
        def cDict(N):
            '''
            Funzione interna. Se N è una componente fortemente connesse
            (rappresentata come insieme) decide un rappresentante e crea 
            un dizionario in cui le chiavi sono i nodi e i valori il 
            rappresentante. Il solo rappresentante ha come valore 
            l'insieme N originale.
            ''' 
            # Il rappresentante è (arbitrariamente) il minimo. Nel caso
            # i nomi siano stringhe che rappresentano numeri interi, il 
            # minimo sarà quello il cui valore numerico minimo. Ad esempio, 
            # min({'10','2'}) = '2'
            try:
                x = int(min(N))
                representative = str(min([int(x) for x in N]))
            except ValueError:
                representative = min(N)
            d = {representative: N}
            for node in N.difference({representative}):
                d[node] = representative
            return d
        
        nodes = self.__packages.keys() #I nodi sono i nomi dei package
        G = nx.DiGraph()
        G.add_nodes_from(nodes)
        # Per ogni nodo/package v, se esiste una dipendenza dal
        # nodo/package u (e u è stato incluso nel repository) allora
        # al grafo viene aggiunto l'arco orientato (u,v)
        for v in nodes:
            for u in self.__packages[v].get('Depends',[]):
                if u in nodes:
                    G.add_edge(u,v)
        self.__graph = G
        SCC = [C for C in nx.strongly_connected_components(G)]
        # self.__SCC è un unico dizionario che "fonde" i singoli
        # dizionari restituiti da cDict
        self.__SCC = reduce(lambda x, y: {**x, **y}, map(cDict,SCC))

    def __download(self, packageSet, delay=True):
        '''Simula il download dei packages'''
        for i, pkg in enumerate(packageSet):
            print("Get:{} {} ({})".\
                  format(i+1,pkg,self.__packages[pkg]['Version']))
            if delay:
                sleep(0.2)
            
    def __unpack(self, pkg, delay=True):
        '''Simula l'unpacking del package pkg'''
        print("Unpacking {} ({}) ...".\
              format(pkg,self.__packages[pkg]['Version']))
        if delay:
            sleep(0.1)

    def __setUp(self, pkg, delay=True):
        '''Simula il set up del package pkg'''
        print("Setting up {} ({}) ...".\
              format(pkg,self.__packages[pkg]['Version']))
        self.__installed[pkg] = copy(self.__packages[pkg])
        self.__installed[pkg]['outdated'] = False
        if delay:
            sleep(0.1)
    
    def _repMember(self, p):
        '''
        Restituisce il rappresentante dell'insieme al quale appartiene p
        '''
        try:
            repr = self.__SCC[p]
        except KeyError:
            return None
        if type(repr) == set:
            repr = p
        return repr
    
    def upToDate(self, package):
        '''Predicato che vale true se il pacchetto package risulta
           installato e aggiornato (cioè non marcato outdated)
        '''
        return self.__installed.get(package, False) and \
                    not self.__installed[package]['outdated']
    
    def __listRequiredPackages(self, name, toInstallAll):
        '''
        Calcola ricorsivamente l'insieme di tutti i package da cui name
        dipende (direttamente o indirettamente). Nella chiamata iniziale
        toInstallAll è l'insieme vuoto. Considera però solo i pacchetti
        non installati
        '''
        C = self.__SCC[self._repMember(name)].difference(toInstallAll)
        #if not C:
        #    return toInstallAll.union({name})
        if not C:
            return toInstallAll
        C = C.difference(set([p for p in C if self.upToDate(p)]))
        if not C:
            return toInstallAll.union({name})
        # Se si arriva a questo punto, C non è vuoto e contiene pacchetti
        # nella componente connessa di name che non sono già installati
        # e che non sono ancora presenti in toInstallAll
        toInstall = set()
        for p in C:
            dep = self.__packages[p].get('Depends', [])
            for pkg in dep:
                if pkg not in self.__SCC[self._repMember(name)] \
                          and self._repMember(pkg)\
                          and self._repMember(pkg) not in toInstall \
                          and not self.__installed.get(pkg, False):
                    toInstall.add(self._repMember(pkg))
        for p in toInstall:
            toInstallAll = \
                toInstallAll.union(self.__listRequiredPackages(p,toInstallAll))
        return toInstallAll.union(C)

    def __additionalInstall(self, packageSet):
        '''
        Determina l'insieme di tutti i package richiesti dalle dipendenze
        in packageSet
        '''
        installSet = set()
        for p in packageSet:
            installSet = \
                installSet.union(self.__listRequiredPackages(p,installSet))
        return installSet.difference(packageSet)
    
    def __computeSizes(self, packageSet):
        '''
        Calcola le dimensioni complessive dei pacchetti da scaricare
        e lo spazio addizionale richiesto (o liberato)
        '''
        size, installedSize = 0, 0
        for p in packageSet:
            size += self.__packages[p]['Size']
            if self.__installed.get(p, False):
                installedSize += (self.__packages[p]['Installed-Size'] - \
                                  self.__installed[p]['Installed-Size'])
            else:
                installedSize += self.__packages[p]['Installed-Size']
        if size >= 1024*1024:
            size = int(size/(1024*1024)*100)/100
            unit = 'MB'
        elif size >= 1024:
            size = int(size/1024.0*100)/100
            unit = 'KB'
        else:
            unit = 'B'
        if installedSize>1024:
            installedSize = int(installedSize/1024.0*100)/100
            unitI = 'MB'
        else:
            unitI = 'KB'
        return (size,unit,installedSize,unitI)
    
    def __install(self, toUpgrade, toInstall, depPackages, sizeInfo, delay=True):
        '''
        Metodo per l'installazione. Chiamato sia da upgrade che da install.
        Se chiamato da upgrade, l'insieme toInstall è vuoto. Se chiamato da 
        install, l'insieme toUpgrade è vuoto. depPackages può essere vuoto 
        o non vuoto. Se non vuoto è l'insieme dei pacchetti aggiuntivi
        da installare per soddisfare le dipendenze. In ogni caso, il conto
        delle dimensioni è gia stato fatto (da upgrade o da install) e
        sizeInfo è una quadrupla con le informazioni da visualizzare.
        '''
        nU = len(toUpgrade)
        nI = len(toInstall)
        nD = len(depPackages)
        if nU == 0 and nI == 0:
            # Nessuna operazione richiesta
            print("0 upgraded and 0 newly installed.")
            return
        size = sizeInfo[0]
        unit = sizeInfo[1]
        installedSize = sizeInfo[2]
        unitI = sizeInfo[3]
        if nU != 0:
            # 
            print("The following packages will be upgraded:")
            for p in toUpgrade:
                print(p, end=' ')
            print()
            if nD != 0:
                print("The following packages will be installed:")
                for p in depPackages.difference(toUpgrade):
                    print(p, end=' ')
                print()
            print("{} upgraded, {} newly installed".format(nU,nD))
        else:
            # nI != 0
            print("The following packages will be installed:")
            for p in toInstall:
                print(p, end=' ')
            print()
            if nD != 0:
                print("The following additional packages will be installed:")
                for p in depPackages.difference(toInstall):
                    print(p, end=' ')
                print()
        print("Need to get {}{} of archives".format(size,unit))
        if installedSize<0:
            op = 'freed'
        else:
            op = 'used'
        print("After this operation, {}{} of additional disk space will be {}".\
              format(installedSize,unitI,op))
        answer = input("Do you want to continue? [Y/n]")
        if answer not in {'Y',''}:
            return
        # (La simulazione de) l'installazione consiste semplicemente nel
        # copiare i pacchetti da self.__packages a self.__installed
        # Download e unpack (al momento) fanno solo stampe "scenografiche"
        self.__download(depPackages.union(toInstall).union(toUpgrade), delay=delay)
        for p in depPackages.union(toInstall).union(toUpgrade):
            self.__unpack(p, delay=delay)
        for p in depPackages.union(toInstall).union(toUpgrade):
            self.__setUp(p, delay=delay)
            self.__installed[p]['outdated'] = False

    def update(self):
        '''Aggiorna l'elenco locale dei pacchetti e marca come "outdatet"
           i pacchetti installati non più aggiornati
        '''
        self.__packages = self.__source.packages # Download del control file
        for name, package in self.__installed.items():
            if self.__packages[name]['Version'] != package['Version']:
                package['outdated'] = True
        self.__dependencyGraph()

    def upgrade(self, delay=True):
        '''Aggiorna i pacchetti marcati come 'outdated', eventualmente
           installando  pacchetti necessari mancanti
        '''
        # toBeUpgraded sono i pacchetti installati ma non aggiornati
        print("Reading package lists... ",end='')
        toUpgrade = {p for p in self.__installed.keys() \
                        if self.__installed[p]['outdated']}
        print("Done")
        print("Building dependency tree... ", end='')
        toInstall = self.__additionalInstall(toUpgrade)
        print("Done")
        print("Calculating upgrade... ", end='')
        sizeInfo = self.__computeSizes(toUpgrade.union(toInstall))
        print("Done")    
        self.__install(toUpgrade, set(), toInstall, sizeInfo, delay=delay)
    
    def install(self, *names, delay=True):
        '''Richiede l'installazione di uno o più pacchetti'''
        # toBeUpgraded sono i pacchetti installati ma non aggiornati
        print("Reading package lists... ",end='')
        unknown = []
        alreadyInstalled = []
        for name in names:
            if not self.__packages.get(name, False):
                unknown.append(name)
            elif self.upToDate(name):
                alreadyInstalled.append(name)
        print("Done")
        if unknown:
            for p in unknown:
                print("E: Unable to locate package {}".format(p))
            return
        print("Building dependency tree... ", end='')
        toInstall = set(names).difference(set(alreadyInstalled))
        depPackages = self.__additionalInstall(toInstall)
        print("Done")
        for p in alreadyInstalled:
            print("{} is already the newest version ({}.)".\
                         format(p,self.__packages[p]['Version']))
        sizeInfo = self.__computeSizes(toInstall.union(depPackages))
        self.__install(set(), toInstall, depPackages, sizeInfo, delay=delay)
        
    def remove(self, name):
        pass
    
    def search(self, name):
        '''Semplice ricerca nel campo nome del pacchetto'''
        for p in self.__source.packages:
            if p.find(name) != -1:
                print("Name: {}".format(p))
                desc = self.__source.packages[p].get('Description',False)
                if desc:
                    print("Description: {}".format(desc))

    @property
    def source(self):
        return self.__source
    
    @property
    def packages(self):
        return self.__packages