-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Creato il: Dic 14, 2025 alle 23:19
-- Versione del server: 5.7.24
-- Versione PHP: 8.3.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sviatoslav`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `categoria`
--

CREATE TABLE `categoria` (
  `ID_CATEGORIA` int(11) NOT NULL,
  `NOME_CATEGORIA` varchar(50) NOT NULL,
  `ID_UTENTE` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `categoria`
--

INSERT INTO `categoria` (`ID_CATEGORIA`, `NOME_CATEGORIA`, `ID_UTENTE`) VALUES
(1, 'Concerto', 1),
(3, 'Pizzata', 1),
(4, 'Passeggiata', 1);

-- --------------------------------------------------------

--
-- Struttura della tabella `evento`
--

CREATE TABLE `evento` (
  `ID_EVENTO` int(11) NOT NULL,
  `NOME_EVENTO` varchar(50) NOT NULL,
  `DESCRIZIONE_EVENTO` text NOT NULL,
  `DATA_EVENTO` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `COSTO` decimal(10,2) NOT NULL DEFAULT '0.00',
  `MAX_PARTECIPANTI` int(11) DEFAULT NULL,
  `CHECK_MAGGIORENNI` tinyint(1) NOT NULL DEFAULT '0',
  `INDIRIZZO_EVENTO` varchar(255) NOT NULL,
  `COORDINATE_EVENTO` point NOT NULL,
  `PASSWORD_EVENTO` varchar(255) DEFAULT NULL,
  `ID_UTENTE` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `evento`
--

INSERT INTO `evento` (`ID_EVENTO`, `NOME_EVENTO`, `DESCRIZIONE_EVENTO`, `DATA_EVENTO`, `COSTO`, `MAX_PARTECIPANTI`, `CHECK_MAGGIORENNI`, `INDIRIZZO_EVENTO`, `COORDINATE_EVENTO`, `PASSWORD_EVENTO`, `ID_UTENTE`) VALUES
(14, 'Concerto Jazz al Parco', 'Una serata di musica jazz dal vivo sotto le stelle.', '2026-12-04 11:43:15', '15.00', 10, 1, 'Parco Sempione, Milano, Italia', 0xe61000000101000000ecede0719b5a2240189062258bbc4640, '$2b$12$nZF3q6DlT/mn0pE9umhZx.D2PsM9FwnMbssdr2e/fPg9xlln.EsVW', 1),
(15, 'Meeting in luogo a caso', 'Naruto run', '2026-12-02 09:00:00', '0.00', 0, 0, 'Farmacia Aurora, 29, Via Aurora, Incirano, Paderno Dugnano, Zona Omogenea Milano Nord, Milano, Lombardia, 20037, Italia', 0xe6100000010100000013bc7c467d55224014db937659c94640, NULL, 2),
(16, 'MotoMeet', 'Una serata di musica jazz dal vivo sotto le stelle.', '2026-06-15 19:00:00', '85.00', 10, 1, 'Parco Paradiso, Paradiso, Svizzera', 0xe61000000101000000a0d10c9876e42140c6c210397dfe4640, '$2b$12$dWem1u6RzzWy/bsO6bDOM.DCIbz5s7WtBXU2I87.95z2/BYGwsB62', 1),
(28, 'TEST', 'L’evento TEST è pensato come un momento speciale dedicato a chi desidera trascorrere una serata diversa dal solito, immerso in un’atmosfera vivace e coinvolgente. Programmato per il 15 giugno 2026 alle ore 21:00, questo appuntamento si terrà presso TEST, una location scelta per garantire comfort, praticità e un ambiente ideale per vivere l’esperienza al meglio.\n\nLa serata combina due elementi molto amati dal pubblico: da una parte l’energia unica di un concerto, capace di regalare emozioni autentiche attraverso musica, performance e interazione con i partecipanti; dall’altra il clima informale e conviviale tipico di una pizzata, perfetta per socializzare, conoscersi e condividere momenti di divertimento davanti a un buon piatto.\n\nL’ingresso prevede un costo di 100€, che include tutte le attività previste durante la serata. È richiesto il rispetto della verifica di maggiore età, poiché l’evento è pensato esclusivamente per un pubblico adulto. Sebbene non sia previsto un limite massimo di partecipanti, l’evento mantiene comunque un’impronta organizzata e gestita in sicurezza, garantendo un’esperienza piacevole a chiunque decida di prendervi parte.\n\nPer accedere sarà necessario utilizzare la password dell’evento, pensata per mantenere un clima riservato e assicurare che solo gli invitati o chi ha ricevuto le informazioni corrette possa partecipare. Questa scelta contribuisce a creare un ambiente selezionato, tranquillo e perfetto per godersi ogni istante della serata.\n\nIn sintesi, TEST è un appuntamento che unisce musica, gusto e socialità in un’unica occasione, ideale per chi cerca una serata ricca di emozioni, buona compagnia e momenti indimenticabili. Una combinazione semplice ma efficace, pensata per offrire un’esperienza piacevole e memorabile. Buon divertimento!', '2026-06-15 19:00:00', '100.00', 0, 1, 'TEST', 0xe61000000101000000e919b1057357494080553f8056fd4040, '$2b$12$iAbrkpnBqv1D7RPVKZQfzeNP3ZM3E/T7KsFzjdtiBB1ANvwHR0xdu', 1),
(29, 'Angular', '...', '2026-02-11 23:00:00', '1.00', 0, 0, 'Via Roma', 0xe6100000010100000097c62fbc92bc1f406d14a3f842594640, NULL, 1);

-- --------------------------------------------------------

--
-- Struttura della tabella `evento_categoria`
--

CREATE TABLE `evento_categoria` (
  `ID_EVENTO_CATEGORIA` int(11) NOT NULL,
  `ID_CATEGORIA` int(11) NOT NULL,
  `ID_EVENTO` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `evento_categoria`
--

INSERT INTO `evento_categoria` (`ID_EVENTO_CATEGORIA`, `ID_CATEGORIA`, `ID_EVENTO`) VALUES
(6, 3, 28),
(7, 1, 28),
(8, 4, 28),
(9, 4, 29);

-- --------------------------------------------------------

--
-- Struttura della tabella `iscrizione`
--

CREATE TABLE `iscrizione` (
  `ID_ISCRIZIONE` int(11) NOT NULL,
  `ID_UTENTE` int(11) NOT NULL,
  `ID_EVENTO` int(11) NOT NULL,
  `DATA_ISCRIZIONE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `iscrizione`
--

INSERT INTO `iscrizione` (`ID_ISCRIZIONE`, `ID_UTENTE`, `ID_EVENTO`, `DATA_ISCRIZIONE`) VALUES
(14, 2, 14, '2025-12-04 11:44:54'),
(40, 1, 14, '2025-12-14 20:13:35'),
(46, 2, 15, '2025-12-14 20:25:43'),
(47, 2, 28, '2025-12-14 20:29:31'),
(48, 1, 16, '2025-12-14 20:31:58');

-- --------------------------------------------------------

--
-- Struttura della tabella `utente`
--

CREATE TABLE `utente` (
  `ID_UTENTE` int(11) NOT NULL,
  `EMAIL_UTENTE` varchar(255) NOT NULL,
  `NOME_UTENTE` varchar(50) NOT NULL,
  `PASSWORD_UTENTE` varchar(255) NOT NULL,
  `COORDINATE_UTENTE` point NOT NULL,
  `INDIRIZZO_UTENTE` varchar(255) NOT NULL,
  `DATA_REGISTRAZIONE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CHECK_ADMIN` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `utente`
--

INSERT INTO `utente` (`ID_UTENTE`, `EMAIL_UTENTE`, `NOME_UTENTE`, `PASSWORD_UTENTE`, `COORDINATE_UTENTE`, `INDIRIZZO_UTENTE`, `DATA_REGISTRAZIONE`, `CHECK_ADMIN`) VALUES
(1, 'user1@gmail.com', 'user_1', '$2b$12$WXHR/YeMZXz2pWQQz4qCpuiEkNYlhIgr1pjtmND4ZNBeWF/tlRZSm', 0xe6100000010100000090604fe042f728402cadd05158f24440, 'Roma', '2025-12-14 19:38:36', 1),
(2, 'user2@gmail.com', 'user', '$2b$12$JAAtPHCTBnDHV8V1Xf63BOhnjzUNWrwqmywn4GbIqznQ8.fm2fVVW', 0xe61000000101000000bc38961c1c9d2340780b24287ed84640, 'Via del Convento, 1, 24060 San Paolo d\'Argon BG', '2025-12-04 11:14:18', 0),
(9, 'user3@gmail.com', 'user', '$2b$12$2aDbxBRpObH8tBlL.PeEfOsAy2PApWRQpA3j8Wvwrf8NVeXW6HMYy', 0xe61000000101000000bc38961c1c9d2340780b24287ed84640, 'Via del Convento, 1, 24060 San Paolo d\'Argon BG', '2025-12-02 22:13:01', 0),
(10, 'user4@gmail.com', 'user', '$2b$12$13AugDPTFX5mvNuFtlcUKeJkCr2BsQMOqVg3T5eshZGOWT.mX4ZaC', 0xe61000000101000000bc38961c1c9d2340780b24287ed84640, 'Abbazia di San Paolo d’Argon, 1, Via del Convento, San Paolo d\'Argon, Bergamo, Lombardia, 24060, Italia', '2025-12-02 22:13:47', 0);

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `categoria`
--
ALTER TABLE `categoria`
  ADD PRIMARY KEY (`ID_CATEGORIA`),
  ADD UNIQUE KEY `unique_nome_categoria` (`NOME_CATEGORIA`),
  ADD KEY `ID_CATEGORIA_UTENTE` (`ID_UTENTE`);

--
-- Indici per le tabelle `evento`
--
ALTER TABLE `evento`
  ADD PRIMARY KEY (`ID_EVENTO`),
  ADD SPATIAL KEY `COORDINATE_EVENTO` (`COORDINATE_EVENTO`),
  ADD KEY `UTENTE_EVENTO` (`ID_UTENTE`);

--
-- Indici per le tabelle `evento_categoria`
--
ALTER TABLE `evento_categoria`
  ADD PRIMARY KEY (`ID_EVENTO_CATEGORIA`),
  ADD KEY `ID_EVENTO_CATEGORIA` (`ID_EVENTO`),
  ADD KEY `ID_CATEGORIA` (`ID_CATEGORIA`);

--
-- Indici per le tabelle `iscrizione`
--
ALTER TABLE `iscrizione`
  ADD PRIMARY KEY (`ID_ISCRIZIONE`),
  ADD KEY `EVENTO_ISCRIZIONE` (`ID_EVENTO`),
  ADD KEY `UTENTE_ISCRIZIONE` (`ID_UTENTE`);

--
-- Indici per le tabelle `utente`
--
ALTER TABLE `utente`
  ADD PRIMARY KEY (`ID_UTENTE`),
  ADD SPATIAL KEY `COORDINATE_UTENTE` (`COORDINATE_UTENTE`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `categoria`
--
ALTER TABLE `categoria`
  MODIFY `ID_CATEGORIA` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT per la tabella `evento`
--
ALTER TABLE `evento`
  MODIFY `ID_EVENTO` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT per la tabella `evento_categoria`
--
ALTER TABLE `evento_categoria`
  MODIFY `ID_EVENTO_CATEGORIA` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT per la tabella `iscrizione`
--
ALTER TABLE `iscrizione`
  MODIFY `ID_ISCRIZIONE` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=54;

--
-- AUTO_INCREMENT per la tabella `utente`
--
ALTER TABLE `utente`
  MODIFY `ID_UTENTE` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `categoria`
--
ALTER TABLE `categoria`
  ADD CONSTRAINT `ID_CATEGORIA_UTENTE` FOREIGN KEY (`ID_UTENTE`) REFERENCES `utente` (`ID_UTENTE`) ON DELETE NO ACTION;

--
-- Limiti per la tabella `evento`
--
ALTER TABLE `evento`
  ADD CONSTRAINT `UTENTE_EVENTO` FOREIGN KEY (`ID_UTENTE`) REFERENCES `utente` (`ID_UTENTE`);

--
-- Limiti per la tabella `evento_categoria`
--
ALTER TABLE `evento_categoria`
  ADD CONSTRAINT `ID_CATEGORIA` FOREIGN KEY (`ID_CATEGORIA`) REFERENCES `categoria` (`ID_CATEGORIA`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ID_EVENTO_CATEGORIA` FOREIGN KEY (`ID_EVENTO`) REFERENCES `evento` (`ID_EVENTO`);

--
-- Limiti per la tabella `iscrizione`
--
ALTER TABLE `iscrizione`
  ADD CONSTRAINT `EVENTO_ISCRIZIONE` FOREIGN KEY (`ID_EVENTO`) REFERENCES `evento` (`ID_EVENTO`) ON DELETE CASCADE,
  ADD CONSTRAINT `UTENTE_ISCRIZIONE` FOREIGN KEY (`ID_UTENTE`) REFERENCES `utente` (`ID_UTENTE`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
