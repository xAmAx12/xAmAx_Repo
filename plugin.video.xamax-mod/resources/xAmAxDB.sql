BEGIN TRANSACTION;
CREATE TABLE "UrlBouquet" (
	`IDUrlB`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`IdBouquet`	INTEGER,
	`IDChaine`	INTEGER,
	`Url`	TEXT,
	`NomAffichChaine`	TEXT
);
CREATE TABLE `RegroupChaine` (
	`IDRegroup`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`NomAffiche`	TEXT,
	`NomRegroup`	TEXT,
	`PasDansNom`	TEXT
);
INSERT INTO `RegroupChaine` VALUES (1,'TF1','%TF1',NULL);
INSERT INTO `RegroupChaine` VALUES (2,'FRANCE_TV','%FRANCE','#%'' AND Nom NOT LIKE ''%*%'' AND Nom NOT LIKE ''%I%T%'' AND Nom NOT LIKE ''%M');
INSERT INTO `RegroupChaine` VALUES (3,'M6','%M6','');
INSERT INTO `RegroupChaine` VALUES (4,'EURO_NEWS','%EURO%NEWS',NULL);
INSERT INTO `RegroupChaine` VALUES (5,'TV5','%TV5',NULL);
INSERT INTO `RegroupChaine` VALUES (6,'ARTE','ARTE','CA');
INSERT INTO `RegroupChaine` VALUES (7,'BREIZH','%BREIZH',NULL);
INSERT INTO `RegroupChaine` VALUES (8,'6TER','%6%TER',NULL);
INSERT INTO `RegroupChaine` VALUES (9,'WEO','%WEO',NULL);
INSERT INTO `RegroupChaine` VALUES (10,'BFM','%BFM',NULL);
INSERT INTO `RegroupChaine` VALUES (11,'NT1','%NT1',NULL);
INSERT INTO `RegroupChaine` VALUES (12,'D8','%D%8','80');
INSERT INTO `RegroupChaine` VALUES (13,'D17','%D%17',NULL);
INSERT INTO `RegroupChaine` VALUES (14,'W9','%W%9',NULL);
INSERT INTO `RegroupChaine` VALUES (15,'RTL','%RTL',NULL);
INSERT INTO `RegroupChaine` VALUES (16,'TMC','%TMC',NULL);
INSERT INTO `RegroupChaine` VALUES (17,'NRJ','%NRJ',NULL);
INSERT INTO `RegroupChaine` VALUES (18,'SYFY','%SYFY',NULL);
INSERT INTO `RegroupChaine` VALUES (19,'TEVA','T%VA',NULL);
INSERT INTO `RegroupChaine` VALUES (20,'PARIS_PREMIERE','%PARIS PREMIERE',NULL);
INSERT INTO `RegroupChaine` VALUES (21,'PARAMOUNT','%PARAMOUNT',NULL);
INSERT INTO `RegroupChaine` VALUES (22,'MANGA','%MANGA',NULL);
INSERT INTO `RegroupChaine` VALUES (23,'GULLI','%GULLI',NULL);
INSERT INTO `RegroupChaine` VALUES (24,'PIWI','%PIWI',NULL);
INSERT INTO `RegroupChaine` VALUES (25,'BOOMERANG','%BOOMERANG',NULL);
INSERT INTO `RegroupChaine` VALUES (26,'TELETOON','%T%L%TOON',NULL);
INSERT INTO `RegroupChaine` VALUES (27,'CARTOON','%CARTOON',NULL);
INSERT INTO `RegroupChaine` VALUES (28,'DISNEY','%DISNEY',NULL);
INSERT INTO `RegroupChaine` VALUES (29,'GAME_ONE','%GAME%ONE',NULL);
INSERT INTO `RegroupChaine` VALUES (30,'CINE','%CIN','MA');
INSERT INTO `RegroupChaine` VALUES (31,'CANAL','%CANAL',NULL);
INSERT INTO `RegroupChaine` VALUES (32,'ANIMAUX','%ANIM%AUX',NULL);
INSERT INTO `RegroupChaine` VALUES (33,'USHUAIA','%USHUA%A',NULL);
INSERT INTO `RegroupChaine` VALUES (34,'VOYAGE','%VOYAGE',NULL);
INSERT INTO `RegroupChaine` VALUES (35,'NATIONAL_GEO','%NAT%GEO',NULL);
INSERT INTO `RegroupChaine` VALUES (36,'DISCOVERY','%ISCOVERY',NULL);
INSERT INTO `RegroupChaine` VALUES (37,'SCIENCE_&_VIE','%SCIENCE%VIE',NULL);
INSERT INTO `RegroupChaine` VALUES (38,'RMC','%RMC',NULL);
INSERT INTO `RegroupChaine` VALUES (39,'PLANETE','%PLAN%T',NULL);
INSERT INTO `RegroupChaine` VALUES (40,'CHASSE_&_PECHE','%CHASSE%P%CHE',NULL);
INSERT INTO `RegroupChaine` VALUES (41,'COMEDIE','%COMEDI',NULL);
INSERT INTO `RegroupChaine` VALUES (42,'SERIE_CLUB','%SERIE%CLUB',NULL);
INSERT INTO `RegroupChaine` VALUES (43,'CHERIE_25','%CH%RIE%25',NULL);
INSERT INTO `RegroupChaine` VALUES (44,'ACTION','%ACTION',NULL);
INSERT INTO `RegroupChaine` VALUES (45,'AB1','%AB1',NULL);
INSERT INTO `RegroupChaine` VALUES (46,'AB3','%AB3',NULL);
INSERT INTO `RegroupChaine` VALUES (47,'AB_MOTEUR','%AB%MOT',NULL);
INSERT INTO `RegroupChaine` VALUES (48,'GOLF','%GOLF',NULL);
INSERT INTO `RegroupChaine` VALUES (49,'BEIN_SPORT','%B%SPORT','UB%'' AND Nom NOT LIKE ''%BF%'' AND Nom NOT LIKE ''%MB');
INSERT INTO `RegroupChaine` VALUES (50,'MA_CHAINE_SPORT','%CHAINE%SPORT',NULL);
INSERT INTO `RegroupChaine` VALUES (51,'INFOSPORT','%INFOSPORT',NULL);
INSERT INTO `RegroupChaine` VALUES (52,'EUROSPORT','%EUROSP',NULL);
INSERT INTO `RegroupChaine` VALUES (53,'EQUIDIA','%EQUIDIA',NULL);
INSERT INTO `RegroupChaine` VALUES (54,'SPORT_+','%SPORT_+','');
INSERT INTO `RegroupChaine` VALUES (55,'A_LA_CARTE','%A LA CARTE',NULL);
INSERT INTO `RegroupChaine` VALUES (57,'OCS','%OCS',NULL);
INSERT INTO `RegroupChaine` VALUES (58,'BOING','%BOING',NULL);
INSERT INTO `RegroupChaine` VALUES (59,'SUNDANCE','%SUNDANCE',NULL);
INSERT INTO `RegroupChaine` VALUES (60,'MUSEUM','%MUSEUM',NULL);
INSERT INTO `RegroupChaine` VALUES (61,'MOTORS','%MOTORS',NULL);
INSERT INTO `RegroupChaine` VALUES (62,'I-TELE','%I%TELE',NULL);
INSERT INTO `RegroupChaine` VALUES (63,'13EME_RUE','%13%RUE',NULL);
INSERT INTO `RegroupChaine` VALUES (64,'C8','%C%8','CI%'' AND Nom NOT LIKE ''%CA%'' AND Nom NOT LIKE ''%80');
INSERT INTO `RegroupChaine` VALUES (65,'MTV','MTV','BF%'' AND Nom NOT LIKE ''%XE');
INSERT INTO `RegroupChaine` VALUES (66,'C_STAR','%C%STAR','CL');
INSERT INTO `RegroupChaine` VALUES (67,'E!','%E!',NULL);
INSERT INTO `RegroupChaine` VALUES (68,'L''EQUIPE','%EQUIPE',NULL);
INSERT INTO `RegroupChaine` VALUES (69,'FOOT_24','%FOOT',NULL);
INSERT INTO `RegroupChaine` VALUES (70,'HD1','HD%1%(_)','10');
INSERT INTO `RegroupChaine` VALUES (71,'HISTOIRE','%HISTOIRE',NULL);
INSERT INTO `RegroupChaine` VALUES (72,'MUSIC','%MUSIC',NULL);
INSERT INTO `RegroupChaine` VALUES (73,'LCI','%LCI',NULL);
INSERT INTO `RegroupChaine` VALUES (74,'LCP','%LCP',NULL);
INSERT INTO `RegroupChaine` VALUES (75,'NICKELODEON','%NICKELODEON',NULL);
INSERT INTO `RegroupChaine` VALUES (76,'NUMERO_23','%NUM%RO%23',NULL);
INSERT INTO `RegroupChaine` VALUES (77,'OL_TV','%OL%TV',NULL);
INSERT INTO `RegroupChaine` VALUES (79,'SFR_SPORT','%S%SPORT','SR');
INSERT INTO `RegroupChaine` VALUES (80,'TIJI','%TIJI',NULL);
INSERT INTO `RegroupChaine` VALUES (81,'TREK','%TREK',NULL);
INSERT INTO `RegroupChaine` VALUES (82,'ZOUZOU_TV','%ZOUZOU',NULL);
INSERT INTO `RegroupChaine` VALUES (83,'ORANGE','ORANGE',NULL);
INSERT INTO `RegroupChaine` VALUES (84,'BELGIQUE','%BE','BET%'' AND Nom NOT LIKE ''%BEIN');
CREATE TABLE `Parametres` (
	`IdParam`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`Nom`	TEXT,
	`Valeur`	TEXT
);
CREATE TABLE `ListePrincipale` (
	`IDLP`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`Nom`	TEXT,
	`Url`	TEXT,
	`Entete`	TEXT
);
CREATE TABLE List4 (`IDLP` INTEGER PRIMARY KEY AUTOINCREMENT, `Nom` TEXT, `Url` TEXT, `Entete` TEXT);
CREATE TABLE List3 (`IDLP` INTEGER PRIMARY KEY AUTOINCREMENT, `Nom` TEXT, `Url` TEXT, `Entete` TEXT);
CREATE TABLE List2 (`IDLP` INTEGER PRIMARY KEY AUTOINCREMENT, `Nom` TEXT, `Url` TEXT, `Entete` TEXT);
CREATE TABLE List1 (`IDLP` INTEGER PRIMARY KEY AUTOINCREMENT, `Nom` TEXT, `Url` TEXT, `Entete` TEXT);
CREATE TABLE "ChaineBouquet" (
	`IDChaineB`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`IDBouqChaine`	INTEGER,
	`NomChaine`	TEXT,
	`PasDansChaine`	TEXT,
	`Ordre`	INTEGER
);
INSERT INTO `ChaineBouquet` VALUES (1,1,'tf1',NULL,1);
INSERT INTO `ChaineBouquet` VALUES (2,1,'france 2','24',2);
INSERT INTO `ChaineBouquet` VALUES (3,1,'france 3',NULL,3);
INSERT INTO `ChaineBouquet` VALUES (4,1,'france 4',NULL,4);
INSERT INTO `ChaineBouquet` VALUES (5,1,'france 5',NULL,5);
INSERT INTO `ChaineBouquet` VALUES (6,1,'france O',NULL,6);
INSERT INTO `ChaineBouquet` VALUES (7,1,'m6','music,boutique',7);
INSERT INTO `ChaineBouquet` VALUES (8,1,'tmc',NULL,8);
INSERT INTO `ChaineBouquet` VALUES (9,1,'6ter',NULL,9);
INSERT INTO `ChaineBouquet` VALUES (10,1,'cherie 25',NULL,10);
INSERT INTO `ChaineBouquet` VALUES (11,1,'hd1',NULL,11);
INSERT INTO `ChaineBouquet` VALUES (12,1,'c8',NULL,12);
INSERT INTO `ChaineBouquet` VALUES (13,1,'cstar',NULL,13);
INSERT INTO `ChaineBouquet` VALUES (14,1,'arte','carte',14);
INSERT INTO `ChaineBouquet` VALUES (15,1,'bfm','Business',15);
INSERT INTO `ChaineBouquet` VALUES (16,1,'itele',NULL,16);
INSERT INTO `ChaineBouquet` VALUES (17,1,'euronews',NULL,17);
INSERT INTO `ChaineBouquet` VALUES (18,1,'france 24',NULL,18);
INSERT INTO `ChaineBouquet` VALUES (19,2,'sport',NULL,1);
INSERT INTO `ChaineBouquet` VALUES (20,2,'foot',NULL,2);
INSERT INTO `ChaineBouquet` VALUES (25,2,'ab moteur',NULL,4);
INSERT INTO `ChaineBouquet` VALUES (26,2,'equidia',NULL,5);
INSERT INTO `ChaineBouquet` VALUES (27,3,'bfm',NULL,4);
INSERT INTO `ChaineBouquet` VALUES (28,3,'itele',NULL,3);
INSERT INTO `ChaineBouquet` VALUES (29,3,'France 24',NULL,1);
INSERT INTO `ChaineBouquet` VALUES (30,3,'EURONEWS',NULL,5);
INSERT INTO `ChaineBouquet` VALUES (31,3,'FRANCE INFO',NULL,2);
INSERT INTO `ChaineBouquet` VALUES (32,3,'lci',NULL,6);
INSERT INTO `ChaineBouquet` VALUES (33,3,'cnn',NULL,7);
INSERT INTO `ChaineBouquet` VALUES (34,3,'bbc',NULL,8);
INSERT INTO `ChaineBouquet` VALUES (35,3,'cnbc',NULL,9);
INSERT INTO `ChaineBouquet` VALUES (36,3,'i24',NULL,10);
INSERT INTO `ChaineBouquet` VALUES (37,2,'OM TV',NULL,5);
INSERT INTO `ChaineBouquet` VALUES (38,2,'OL TV',NULL,6);
INSERT INTO `ChaineBouquet` VALUES (39,2,'ONZEO',NULL,7);
INSERT INTO `ChaineBouquet` VALUES (40,2,'GIRONDINS',NULL,8);
INSERT INTO `ChaineBouquet` VALUES (41,2,'GOLF',NULL,9);
INSERT INTO `ChaineBouquet` VALUES (42,2,'MOTORs',NULL,10);
INSERT INTO `ChaineBouquet` VALUES (43,2,'equipe',NULL,11);
INSERT INTO `ChaineBouquet` VALUES (44,3,'tv5',NULL,11);
INSERT INTO `ChaineBouquet` VALUES (45,3,'ptc',NULL,12);
INSERT INTO `ChaineBouquet` VALUES (46,3,'rtc',NULL,13);
INSERT INTO `ChaineBouquet` VALUES (47,3,'MONACO INFOS',NULL,14);
INSERT INTO `ChaineBouquet` VALUES (48,3,'Assemblee Nationale',NULL,15);
INSERT INTO `ChaineBouquet` VALUES (49,4,'Paramount',NULL,1);
INSERT INTO `ChaineBouquet` VALUES (50,4,'canal','sport,j,kid',2);
INSERT INTO `ChaineBouquet` VALUES (51,4,'cine',NULL,3);
INSERT INTO `ChaineBouquet` VALUES (52,4,'ocs',NULL,4);
INSERT INTO `ChaineBouquet` VALUES (53,4,'syfy',NULL,5);
INSERT INTO `ChaineBouquet` VALUES (54,4,'serie',NULL,6);
INSERT INTO `ChaineBouquet` VALUES (55,4,'premiere',NULL,7);
INSERT INTO `ChaineBouquet` VALUES (56,4,'carte',NULL,8);
INSERT INTO `ChaineBouquet` VALUES (57,4,'13 eme',NULL,9);
INSERT INTO `ChaineBouquet` VALUES (58,4,'action',NULL,10);
INSERT INTO `ChaineBouquet` VALUES (59,5,'tiji',NULL,1);
INSERT INTO `ChaineBouquet` VALUES (60,5,'teletoon',NULL,2);
INSERT INTO `ChaineBouquet` VALUES (61,5,'disney',NULL,3);
INSERT INTO `ChaineBouquet` VALUES (62,5,'Gulli',NULL,4);
INSERT INTO `ChaineBouquet` VALUES (63,5,'canal j',NULL,5);
INSERT INTO `ChaineBouquet` VALUES (64,5,'game',NULL,6);
INSERT INTO `ChaineBouquet` VALUES (65,5,'piwi',NULL,7);
INSERT INTO `ChaineBouquet` VALUES (66,5,'kid',NULL,8);
INSERT INTO `ChaineBouquet` VALUES (67,5,'manga',NULL,9);
INSERT INTO `ChaineBouquet` VALUES (68,5,'junior',NULL,10);
INSERT INTO `ChaineBouquet` VALUES (69,5,'zouzou',NULL,11);
INSERT INTO `ChaineBouquet` VALUES (70,6,'ushuaia',NULL,1);
INSERT INTO `ChaineBouquet` VALUES (71,6,'discover',NULL,2);
INSERT INTO `ChaineBouquet` VALUES (72,6,'planete',NULL,3);
INSERT INTO `ChaineBouquet` VALUES (73,6,'geo',NULL,4);
INSERT INTO `ChaineBouquet` VALUES (74,6,'animaux',NULL,5);
INSERT INTO `ChaineBouquet` VALUES (75,6,'museum',NULL,6);
INSERT INTO `ChaineBouquet` VALUES (76,6,'voyage',NULL,7);
INSERT INTO `ChaineBouquet` VALUES (77,6,'chasse',NULL,8);
INSERT INTO `ChaineBouquet` VALUES (79,6,'trek',NULL,9);
INSERT INTO `ChaineBouquet` VALUES (80,6,'decouverte',NULL,10);
INSERT INTO `ChaineBouquet` VALUES (81,6,'science',NULL,11);
INSERT INTO `ChaineBouquet` VALUES (82,6,'histoire',NULL,12);
INSERT INTO `ChaineBouquet` VALUES (83,6,'tv5',NULL,13);
INSERT INTO `ChaineBouquet` VALUES (85,7,'Music',NULL,1);
INSERT INTO `ChaineBouquet` VALUES (86,4,'comedi',NULL,11);
INSERT INTO `ChaineBouquet` VALUES (87,5,'Boomrang',NULL,12);
INSERT INTO `ChaineBouquet` VALUES (88,7,'Trance',NULL,2);
INSERT INTO `ChaineBouquet` VALUES (89,7,'hits','',3);
INSERT INTO `ChaineBouquet` VALUES (90,7,'SUNDANCE',NULL,4);
INSERT INTO `ChaineBouquet` VALUES (91,8,'BE','BEI%'' AND Nom NOT LIKE ''%BET',1);
CREATE TABLE "Bouquet" (
	`IDBouquet`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`NomBouq`	TEXT,
	`Ordre`	INTEGER,
	`TriDesChaines`	TEXT,
	`TriDesUrl`	TEXT
);
INSERT INTO `Bouquet` VALUES (1,'TNT',1,'Ordre','IDUrlB');
INSERT INTO `Bouquet` VALUES (2,'Sport',3,'NomChaine','NomAffichChaine');
INSERT INTO `Bouquet` VALUES (3,'Info',2,'Ordre','IDUrlB');
INSERT INTO `Bouquet` VALUES (4,'Film et Serie',4,'Ordre','NomAffichChaine');
INSERT INTO `Bouquet` VALUES (5,'Jeunesse',5,'Ordre','NomAffichChaine');
INSERT INTO `Bouquet` VALUES (6,'Decouverte',6,'Ordre','NomAffichChaine');
INSERT INTO `Bouquet` VALUES (7,'Musique',7,'Ordre','NomAffichChaine');
INSERT INTO `Bouquet` VALUES (8,'Belgique',8,'Ordre','NomAffichChaine');
COMMIT;
