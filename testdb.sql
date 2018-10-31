--
-- Comandi SQL per (ri-)creare il DB testdb usato a lezione
-- USO: mysql -p < testdb.sql
--

DROP DATABASE IF EXISTS testdb;

CREATE database testdb;
USE testdb;

CREATE TABLE `Campionati` (
       `id` INT(11) NOT NULL,
       `nome` VARCHAR(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Squadre` (
       `id` INT(11) NOT NULL,
       `nome` VARCHAR(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Calendario` (
       `id` INT(11) NOT NULL,
       `campionato` int(11) NOT NULL,
       `giornata` int(2) NOT NULL,
       `AR` CHAR(1) NOT NULL,
       `data` VARCHAR(10) NOT NULL,
       `locali` int(11) NOT NULL,
       `ospiti` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Risultati` (
       `id` INT(11) NOT NULL,
       `partita` int(11) NOT NULL,
       `retiLocali` int(2) NOT NULL,
       `retiOspiti` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE `Campionati`
      ADD PRIMARY KEY (`id`);

ALTER TABLE `Squadre`
      ADD PRIMARY KEY (`id`);

ALTER TABLE `Calendario`
      ADD PRIMARY KEY (`id`);

ALTER TABLE `Risultati`
      ADD PRIMARY KEY (`id`);

ALTER TABLE `Campionati`
      MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

ALTER TABLE `Squadre`
      MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

ALTER TABLE `Calendario`
      MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

ALTER TABLE `Risultati`
      MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

ALTER TABLE `Calendario`
      ADD FOREIGN KEY (campionato) REFERENCES Campionati(id);

ALTER TABLE `Calendario`
      ADD FOREIGN KEY (locali) REFERENCES Squadre(id);

ALTER TABLE `Calendario`
      ADD FOREIGN KEY (ospiti) REFERENCES Squadre(id);

ALTER TABLE `Risultati`
      ADD FOREIGN KEY (partita) REFERENCES Calendario(id);
