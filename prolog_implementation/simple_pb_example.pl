/*
Example pour simplfier le pb : 

Nous disposons d'une journée pour jouer, un samedi.
Il y a donc deux créneaux de jeux : 
- samedi après-midi
- samedi soir

Il y a 10 joueurs : 
- Alice : voudrait jouer à D&D ou Scion.
- Bob : voudrait jouer à Alien ou Scion.
- Clément : voudrait joueur à Scion ou Alien.
- David : voudrait jouer à Alien ou Scion.
- Emilie : Voudrait jouer à Ryuutama ou D&D.
- Fanny : Voudrait jouer à Ryuutama ou Scion.
- Godric : Voudrait jouer à Scion ou D&D.
- Hermione : Voudrait jouer à Ryuutama et avoir une pause.
- Ingrid : Voudrait jouer à Alien et avoir une pause.
- Joe : Voudrait jouer à D&D et avoir une pause. 

Il y a quatre parties de proposées : 
- Alice en propose une, à 4 joueurs, le soir : Alien RPG.
- David en propose deux, une à 5 joueurs, une à 6 joueurs, peu importe quand : Ryuutama et D&D.
- Fanny en propose une à 5 joueurs, peu importe quand : Scion.
*/

/* ----- Règles du problème ----- */
/* Trouver un créneau compatible avec la préférence exprimée. */
time_appropriate_for_playing(Time, RPG):-
    time(Time),
    proposed_rpg(RPG),
    moment(Time, X),
    best_moment(RPG, X).
    % Comment gérer les parties sans préférence ?

/* Peut jouer si:
    - Ne meujeute pas => OK
    - Si nb max de places pas encore atteint => TODO
    - Si ne joue pas déjà à autre chose => TODO
*/
can_play(Player, RPG):-
    player(Player),
    proposed_rpg(RPG),
    not(rpg_proposed_by(RPG, Player)). % Ne meujeute pas

/* ----- Variables du problème ----- */
/* --- Définition des créneaux horaires --- */
/* Créneaux */
time(samedi_am).
time(samedi_soir).

/* Types des créneaux */
moment(samedi_am, am).
moment(samedi_soir, soir).

/* --- Définition des joueureuses --- */
player(alice).
player(bob).
player(clement).
player(david).
player(emilie).
player(fanny).
player(godric).
player(hermione).
player(ingrid).
player(joe).

/* --- Définition des contraintes de MJ/parties --- */
/* Parties proposées */
proposed_rpg(alien_rpg).
proposed_rpg(ryuutama).
proposed_rpg(dnd).
proposed_rpg(scion).

rpg_proposed_by(alien_rpg, alice).
rpg_proposed_by(ryuutama, david).
rpg_proposed_by(dnd, david).
rpg_proposed_by(scion, alice).

rpg_player_nb(alien_rpg, 4).
rpg_player_nb(ryuutama, 5).
rpg_player_nb(dnd, 6).
rpg_player_nb(scion, 5).

/* Préférences horaires (après-midi/soir) */
best_moment(alien_rpg, soir).

/* --- Définition des contraintes de joueureuses --- /*
/* Disponibilité (si certain.e.s joueureuses ne sont pas présent tous les jours) */
/* Non-applicable ici */

/* Parties demandées (choix exprimés) */
would_like_to_play(alice, [dnd, scion]).
would_like_to_play(bob, [alien_rpg, scion]).
would_like_to_play(clement, [scion, alien_rpg]).
would_like_to_play(david, [alien_rpg, scion]).
would_like_to_play(emilie, [ryuutama, dnd]).
would_like_to_play(fanny, [ryuutama, scion]).
would_like_to_play(godric, [scion, dnd]).
would_like_to_play(hermione, [ryuutama]).
would_like_to_play(ingrid, [alien_rpg]).
would_like_to_play(joe, [dnd]).

/* Pauses demandées (nombre exprimé) */
would_like_to_rest(hermione, 1).
would_like_to_rest(ingrid, 1).
would_like_to_rest(joe, 1).