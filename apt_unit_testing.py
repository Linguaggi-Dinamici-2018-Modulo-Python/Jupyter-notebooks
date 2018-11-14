#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 08:57:38 2018

@author: mauro
"""

import unittest
import networkx as nx
import pygraphviz as pgv

from random import randint
from functools import reduce
from apts import repository, apts

class packageDependencies(unittest.TestCase):
    '''
    Classe che contiene il test per verificare la correttezza
    del calcolo delle dipendenze di un pacchetto. 
    '''
    
    def test_dependencies(self):
        for gt in ('gn','gnr','gnc','scale_free','erdos_renyi','nSCC_graph'):
            for size,prob in ((10,0.2),(50,0.6),(100,0.02)):
                # Creazione dell'insieme di pacchetti di test a parire da
                # un grafo che specifica le dipendenze
                T = testPackages(size, fn='test_repo.txt', \
                             graphType=gt, prob=prob)
                sccG, scc = T.SCC # Grafo delle c.f.c. e elenco delle stesse
                R = repository('test_repo.txt') # Costruzione del repository
                apt = apts(R) # Inizializzazione del sistema apt simulato
                              # dal lato client
                # Scelta casuale di un vertice. Si decide casualmente una c.f.c.
                # e si considera il suo rappresentante
                C = scc[randint(0,len(scc)-1)]
                pkg = T._repMember(C)
                # Le dipendenze vengono ora determinate in due modi:
                # 1) direttamente sul grafo usato per la costruzione dei 
                #    pacchetti
                # 2) usando la funzione __listRequiredPackages di apt, funzione
                #    di cui si vuole testare la correttezza
                nodes = set([x for x in nx.ancestors(sccG, pkg)])
                nodes = reduce(lambda x,y: x.union(y),\
                          [c for c in scc if c.intersection(nodes)!=set()\
                              or c.intersection({pkg})!=set()],set())
                depends = apt._apts__listRequiredPackages(str(pkg), set())
                self.assertEqual(depends, set([str(x) for x in nodes]))

def test(n, fn='test_repo.txt', g='erdos_renyi', prob=0.05, pdf=False):
    '''Esegue un singolo test ma, opzionalmente, produce anche dei
       file pdf per "ispezione grafica".
    '''
    # Creazione del file con le informazioni di controllo dei pacchetti
    # e del grafo (casuale) che ne rappresenta le dipendenze. Oltre al grafo,
    # che può avere dipendenze cicliche, viene generato anche il grafo
    # (aciclico) delle componenti fortemente connesse
    T = testPackages(n, fn=fn, graphType=g, prob=prob)
    sccG, scc = T.SCC
    # Eventuale creazione dei file pdf del grafo e del grafo delle c.f.c.
    if pdf:
        T.toPDF(T.graph, 'pkg_graph')
        T.toPDF(sccG, 'scc_pkg_graph')
    # Creazione del repository a partire dal file di controllo
    R = repository(fn)
    # Inizializzazione di apt,
    apt = apts(R)
    # Scelta casuale di un vertice. Si decide casualmente una c.f.c.
    # e si considera il suo rappresentante
    C = scc[randint(0,len(scc)-1)]
    pkg = T._repMember(C)
    # Calcolo degli "antenati" sul grafo iniziale casuale
    nodes = set([x for x in nx.ancestors(sccG, pkg)])
    nodes = reduce(lambda x,y: x.union(y),\
                 [c for c in scc if c.intersection(nodes)!=set()\
                  or c.intersection({pkg})!=set()],set())
    # Calcolo degli antenati da parte di apt
    depends = apt._apts__listRequiredPackages(str(pkg), set())
    if pdf:
        GR = apt._apts__graph
        T.toPDF(GR, 'pkg_graph_with_dependencies', nodes=depends)
    # Si ricordi che apt.__graph ha nodi denotati da stringhe                 
    # anche nel caso in cui i nomi dei package siano numeri interi 
    # Per "testare" i risultati ottenuti usando il programma con 
    # quelli ottenuti usando networkx è dunque necessario operare
    # conversioni da intero a stringa
    print("Root node: ",pkg)
    return depends==set([str(x) for x in nodes])

class testPackages:
    '''
    Classe utilizzata per scopi di test. La creazione di un'istanza
    genera un control file "artificiale" per l'esecuzione di unit test.
    In fase di inizializzazione è possibile specificare un grafo diretto
    (deve essere un DiGraph di networkx) oppure il nome di un tipo di grafo
    fra alcuni possibili, sempre di networkx. Come ultima opzione,
    può essere specificato il tipo di grafo nSCC_graph, formato collegando
    (senza formare cicli) un opportuno numero di sottografi fortemente
    connessi. Si tratta, in tutti i casi, di grafi diretti.
    Dopo la creazione del grafo viene creato un file con i campi di 
    controllo che descrivono i vari package "fittizi", rappresentati dai
    vertici del grafo generato): ad esempio, i campi size e installed-size
    sono generati a caso, mentre i nomi dei package sono numeri interi
    1, 2, ..., numPackages (essi coincidono con i nome dei vertici).
    Infine, vengono calcolate le componenti fortemente connesse (c.f.c.)  
    del grafo e creato il corrispondente grafo delle c.f.c     
    '''
    def __init__(self, numPackages, fn='test_repo.txt', \
                 graph=None, graphType='erdos_renyi', prob=0.3):
        
        def graph_sel(graphType, n, p):
            '''
            Funzione che genera e restituisce un grafo del tipo prescelto.
            Viene invocata solo se, nell'inizializzazione del repository,
            non viene direttamente specifica un grafo ma solo un graph type.
            '''
            return {
                'gn': lambda: nx.gn_graph(n),
                'gnr': lambda: nx.gnr_graph(n, p),
                'gnc': lambda: nx.gnc_graph(n),
                'scale_free': lambda: nx.scale_free_graph(n),
                'erdos_renyi': lambda: nx.erdos_renyi_graph(n, p, directed=True),
                'nSCC_graph': lambda: self.nSCC_graph(n)
            }.get(graphType, graphType)()
        
        if not graph:
            graph = graph_sel(graphType, numPackages, prob)
            
        with open(fn, 'w') as f:
            for n in graph.nodes:
                f.write('Package: '+str(n)+'\n')
                version = str(randint(1,4))+'.'+str(randint(0,9))
                f.write('Version: '+version+'\n')
                inst_size = randint(10,1000)
                f.write('Installed-Size: '+str(inst_size)+'\n')
                if graph.in_edges(n):
                    dep = 'Depends:'
                    for e in graph.in_edges(n):
                        dep += ' '+str(e[0])+','
                    f.write(dep[:-1]+'\n')
                f.write('Description: Description of package pkg-'+str(n)+'\n')
                uncompressed_size = inst_size*1024
                size = randint(int(uncompressed_size*0.3),\
                               int(uncompressed_size*0.7))
                f.write('Size: '+str(size)+'\n')
        self.__graph = graph  # Il grafo è il valore dell'attributo __graph
        self._SCCGraph()     # Creazione del grafo delle c.f.c.
        
    def _SCCGraph(self):
        '''
        Calcola le componenti fortemente connesse del grafo 
        self.__graph e il lo stesso grafo delle componenti connesse.
        Le componenti fortemente connesse vengono calcolate da una
        funzione della libreria nx. Il grafo è invece ottenuto
        con un semplice "doppio ciclo" sulle singole componenti
        ed è quindi poco efficiente nel caso in queste siano dello stesso
        ordine dei nodi del grafo di partenza.
        La lista delle componenti fortemente connesse del grafo viene
        determinata usando una funzione di libreria di networkx.
        '''
        SCC = list(nx.strongly_connected_components(self.__graph))
        G = nx.DiGraph()
        # Per ogni componente fortemente connessa, viene aggiunto al grafo
        # un vertice etichettato con il minimo numero di vertice fra quelli
        # presenti nella stessa componente
        for C in SCC:
            G.add_node(self._repMember(C))
        # Gli archi vengono aggiunti, in modo non efficiente...,
        # considerando ogni possibile coppia di componenti C1 e C2 e 
        # verificando l'eventuale collegamento di C1 con C2 o di C2 con C1.
        for C1 in SCC:
            c1 = self._repMember(C1)
            for C2 in SCC:
                c2 = self._repMember(C2)
                if c1 != c2:
                    if nx.has_path(self.__graph,c1,c2):
                        G.add_edge(c1,c2)
                    elif nx.has_path(self.__graph,c2,c1):
                        G.add_edge(c2,c1)
        self.__SCC = (G,SCC)

    def _repMember(self, C):
        return min(C)
        
    @staticmethod                               
    def toPDF(G, fn, nodes=set(), color='Red'):
        '''
        Semplice metodo statico per generare un stringa in formato dot.
        La stringa definisce un grafo diretto del quale si possono evidenziare
        solo i nodi specificati con il colore specificato. Altre opzioni
        non sono previste.
        '''
        S = 'strict digraph "" {'
        for n in nodes:
            S += str(n)+' [color='+color+'];'
        for e in G.edges:
            S += '\n\t'+str(e[0])+' -> '+str(e[1])+';'
        S += '\n}\n'
        H = pgv.AGraph().from_string(S)
        H.draw(fn+'.pdf', prog='dot',args='-Grankdir=LR')

    @staticmethod                    
    def nSCC_graph(n):
        '''
        Costruisce un grafo costituita da components componenti
        fortemente connesse (semplici cicli) e aggiungendo archi fra
        coppie di vertici in componenti distinte. L'inserimento
        di queste ultime coppie viene fatto "a caso" ma gli archi vengono
        inseriti in modo da non formare componenti più grandi.
        '''
        assert n>=10, "Il numero di vertici del grafo deve essere almeno 10"
        maxnodes = 4
        components = int(n/maxnodes)+1
        sizes = [randint(1,maxnodes) for _ in range(components)]
        SCC = [set(range(sizes[0]))]
        base = 0
        for i in range(1,components):
            base += sizes[i-1]
            SCC.append(set(range(base,base+sizes[i])))
        G = nx.DiGraph()
        for N in range(components-1,-1,-1):
            l = len(SCC[N])
            m = min(SCC[N])
            G.add_nodes_from([base + i for i in range(l)])
            base -= sizes[N-1]
            if l>1:
                G.add_edges_from([(m+i,m+(i+1)%l) for i in range(l)])
        for i in range(components-1):
            k = randint(0,components-i-1)
            tailComponents = []
            for i in range(k):
                j = randint(i+1,components-1)
                while j in tailComponents:
                    j = randint(i+1,components-1)
                G.add_edge(min(SCC[i]),min(SCC[j]))
        return G

    @property       
    def graph(self):
        return self.__graph
    
    @property
    def SCC(self):
        return self.__SCC
