create table JOUEUR(
    idJoueur int primary key auto_increment,
    pseudo varchar(25),
    mdp char(25) not null
);                  


create table PARTIE(
    idpartie varchar(8) primary key auto_increment,
    idJoueur1 varchar(15),
    idJoueur2 varchar(15),
    resultat varchar(25), 
    coups text,
    foreign key idJoueur1 references JOUEUR(idJoueur),
    foreign key idJoueur2 references JOUEUR(idJoueur)
);

create table STATISTIQUES(
    idStat int primary key auto_increment,
    joueurId int, 
    nbPartiesJouees int,
    nbVictoires int,
    nbDefaites int,
    nbNulles int,
    
    FOREIGN KEY (joueurId) REFERENCES JOUEUR(idJoueur)
);