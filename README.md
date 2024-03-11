----- REQUIS -----

    Linux:
        Python 3
        Pygame (sudo apt install python3-pygame)
    Windows:
        Un éxécutable est fourni dans le dossier racine

    --- VERIFIER L'ARCHITECTURE DES DOSSIERS ---

    Les éxécutable et/ou fichers .py doivent être dans le même dossier 
    qui contient le dossier assets/ 

----- Controles -----

    [←,↑,→,↓] ---> déplacement
    [Espace] ---> voter boo est plus rapide mais plus long a freiner
    [Maj] ---> cacher ses yeux mais impossible de se déplacer dans cet état
    [Maj + F] ---> se moquer
    [P] ---> Afficher les pseudos des autres joueurs en mode en ligne, et celui des bots en mode solo
    [B] ---> Faire apparaître un bot (uniquement en solo)

    [!] ---> taper une commande

----- Commandes -----

    Solo:

        pse: Changer de pseudo ---> pse votre_nouveau_pseudo
        py: Éxécuter une ligne de python ---> py ligne_a_executer()
        color: Changer sa couleur ---> color couleur (classic,ash,gold)
        bot: Fait apparaître un bot

        kill: Tue un bot ---> arguments:
            kill nom_du_bot (tue le bot avec le nom donné)
            kill all (tue tout les bots)
            kill @r (tue un bot au hasard)

        mv: Vous déplace avec une valeur et une direction donnée ---> exemples:
            u: haut, d: bas, l: gauche, r: droite

            mv 600d (vous déplace de 600 vers le bas)
            mv 420l (vous déplace de 420 vers la gauche)

    Multijoueur:

        tpto: Se téléporter sur un joueur ---> tpto joueur (uniquement pour les opérateurs)
        stop: Quitter le serveur
        kick: Expulse un joueur (uniquement pour les opérateurs)
        pyserv: Envoyer du code a éxécuter au serveur (uniquement pour les opérateurs)

----- Partie Client -----

    Lors de la connection à un serveur, si aucun port n'est indiqué, le port
    par défaut sera le 12500.

    plusieurs formats de connection possibles:

        - xxx.xxx.xxx.xxx --- > ip:12500
        - xxx.xxx.xxx.xxx:port --- > ip:port
        - 0 --- > localhost:12500
        - 0:port --- > localhost:port

    /!\ Tout les autres formats vous donnerons un message d'erreur /!\

----- Partie Serveur -----

    Pour lancer le serveur, lancez simplement l'éxécutable du serveur

    Lorsque vous lancez le serveur, un message est affiché vous indiquant l'IP
    et le port sur lequel le serveur est lancé (par défaut 12500), pour changer 
    ce dernier, modifiez le contenu du fihcier ".port" qui doit être dans le 
    dossier assets, si le port n'est pas reconnu alors il sera remis par défaut 
    a 12500

    Pour ajouter des opérateurs, modifiez le contenu du fihcier ".ops" en écrivant
    le nom des opérateurs séparés par des espaces.

    /!\ Il se peut qu'aucun client n'arrive à se connecter a votre serveur, si cela arrive,
    essayez de désactiver le pare-feu et de réessayer /!\

    /!\ Parfois il y a des messages d'erreur lorsqu'un joueur quitte le serveur,
    cela n'affecte rien au serveur, mais j'aimerai bien empecher l'affichage de ces messages /!\

version 0.3