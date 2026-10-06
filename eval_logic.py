# -*- coding: utf-8 -*-
"""
============================================================================
 ÉVALUATION DIAGNOSTIQUE — SYSTÈMES D'EXPLOITATION I
 Module de logique métier (indépendant de Streamlit)
============================================================================
 Contenu :
   - Banque de 20 questions (QCM + Vrai/Faux) basée sur le cours
     « Systèmes d'exploitation I » — Pr. S. EL MOUMNI (EMSI) :
       Partie I   : Introduction aux systèmes d'exploitation
       Partie II  : Architecture et composants des SE
       Partie III : Gestion des ressources par un SE
   - Correction automatique (1 point par question).
   - Génération du rapport PDF autocorrigé (fpdf2).
============================================================================
"""

from datetime import datetime
from io import BytesIO

from fpdf import FPDF

# ---------------------------------------------------------------------------
# 1. LES TROIS PARTIES DU COURS
# ---------------------------------------------------------------------------
PARTIE_I = "Partie I — Introduction aux systèmes d'exploitation"
PARTIE_II = "Partie II — Architecture et composants des SE"
PARTIE_III = "Partie III — Gestion des ressources par un SE"

PARTIES = [PARTIE_I, PARTIE_II, PARTIE_III]

# ---------------------------------------------------------------------------
# 2. BANQUE DE QUESTIONS
#    type "qcm" : choix multiple | type "vf" : Vrai / Faux
#    "bonne" doit être une chaîne EXACTEMENT identique à une des options.
# ---------------------------------------------------------------------------
QUESTIONS = [
    # ================= PARTIE I — INTRODUCTION AUX SE =================
    {
        "id": 1, "partie": PARTIE_I, "type": "qcm",
        "enonce": "Qu'est-ce qu'un système d'exploitation (SE) ?",
        "options": [
            "Un logiciel de bureautique permettant de créer des documents",
            "Un composant matériel chargé d'exécuter les instructions du processeur",
            "Un ensemble de programmes qui gère les ressources matérielles et logicielles de l'ordinateur et sert d'interface entre l'utilisateur et le matériel",
            "Un langage de programmation réservé aux développeurs système",
        ],
        "bonne": "Un ensemble de programmes qui gère les ressources matérielles et logicielles de l'ordinateur et sert d'interface entre l'utilisateur et le matériel",
    },
    {
        "id": 2, "partie": PARTIE_I, "type": "qcm",
        "enonce": "Quel est le premier logiciel exécuté lors de la mise sous tension d'un ordinateur ?",
        "options": [
            "Le système d'exploitation (Windows, Linux, ...)",
            "Le BIOS (Basic Input/Output System)",
            "Le navigateur Web",
            "Un logiciel d'application",
        ],
        "bonne": "Le BIOS (Basic Input/Output System)",
    },
    {
        "id": 3, "partie": PARTIE_I, "type": "vf",
        "enonce": "Le BIOS effectue une série de tests matériels appelés POST (Power-On Self Test) avant de transmettre le contrôle au système d'exploitation.",
        "options": ["Vrai", "Faux"],
        "bonne": "Vrai",
    },
    {
        "id": 4, "partie": PARTIE_I, "type": "qcm",
        "enonce": "Quelle relation entre les niveaux de machine est correcte ?",
        "options": [
            "Machine Abstraite = Machine Réelle + Système d'exploitation",
            "Machine Abstraite = Machine Réelle + Applications",
            "Machine Utilisable = Machine Réelle + Système d'exploitation",
            "Machine Abstraite = Machine Utilisable + Applications",
        ],
        "bonne": "Machine Abstraite = Machine Réelle + Système d'exploitation",
    },
    {
        "id": 5, "partie": PARTIE_I, "type": "qcm",
        "enonce": "Parmi les missions suivantes, laquelle n'est PAS un rôle d'un système d'exploitation ?",
        "options": [
            "Gérer et coordonner les ressources matérielles et logicielles",
            "Fournir une interface entre l'utilisateur et le matériel",
            "Compiler automatiquement tous les programmes installés",
            "Assurer la sécurité et le contrôle d'accès aux ressources",
        ],
        "bonne": "Compiler automatiquement tous les programmes installés",
    },
    {
        "id": 6, "partie": PARTIE_I, "type": "qcm",
        "enonce": "Comment se caractérise un hyperviseur de Type 2 (dit « hosted ») ?",
        "options": [
            "Il se lance directement sur la plateforme matérielle (bare-metal)",
            "Il remplace le BIOS au démarrage de la machine",
            "Il émule un processeur d'architecture totalement différente",
            "Il s'exécute à l'intérieur d'un autre système d'exploitation hôte (ex. : VirtualBox, VMware Workstation)",
        ],
        "bonne": "Il s'exécute à l'intérieur d'un autre système d'exploitation hôte (ex. : VirtualBox, VMware Workstation)",
    },
    # ============ PARTIE II — ARCHITECTURE ET COMPOSANTS DES SE ============
    {
        "id": 7, "partie": PARTIE_II, "type": "qcm",
        "enonce": "Quel composant est considéré comme le cœur du système d'exploitation ?",
        "options": [
            "Le shell (interpréteur de commandes)",
            "Le noyau (kernel)",
            "Le gestionnaire de fenêtres",
            "Le système de fichiers",
        ],
        "bonne": "Le noyau (kernel)",
    },
    {
        "id": 8, "partie": PARTIE_II, "type": "qcm",
        "enonce": "Parmi les tâches suivantes, lesquelles relèvent du noyau ?",
        "options": [
            "Uniquement la gestion des fichiers",
            "Uniquement l'affichage graphique de l'interface",
            "La gestion des processus, de la mémoire, des périphériques et des fichiers",
            "Uniquement la connexion aux réseaux",
        ],
        "bonne": "La gestion des processus, de la mémoire, des périphériques et des fichiers",
    },
    {
        "id": 9, "partie": PARTIE_II, "type": "qcm",
        "enonce": "Quelle architecture de noyau regroupe l'ensemble des services (pilotes, système de fichiers, IPC) dans un seul bloc exécuté en mode privilégié ?",
        "options": [
            "Le micro-noyau",
            "L'architecture en couches",
            "Le noyau hybride",
            "Le noyau monolithique",
        ],
        "bonne": "Le noyau monolithique",
    },
    {
        "id": 10, "partie": PARTIE_II, "type": "qcm",
        "enonce": "Que signifie l'acronyme IPC, utilisé dans l'architecture des systèmes d'exploitation ?",
        "options": [
            "Inter-Process Communication (communication entre processus)",
            "Integrated Peripheral Controller",
            "Internet Protocol Configuration",
            "Internal Program Compiler",
        ],
        "bonne": "Inter-Process Communication (communication entre processus)",
    },
    # ============ PARTIE III — GESTION DES RESSOURCES PAR UN SE ============
    {
        "id": 11, "partie": PARTIE_III, "type": "qcm",
        "enonce": "Quelle est la différence fondamentale entre un programme et un processus ?",
        "options": [
            "Un programme est passif (statique, stocké sur disque) tandis qu'un processus est actif (en cours d'exécution et consomme des ressources)",
            "Un processus est stocké sur le disque et un programme en mémoire vive",
            "Un programme consomme du CPU alors qu'un processus n'en consomme jamais",
            "Il n'existe aucune différence entre les deux notions",
        ],
        "bonne": "Un programme est passif (statique, stocké sur disque) tandis qu'un processus est actif (en cours d'exécution et consomme des ressources)",
    },
    {
        "id": 12, "partie": PARTIE_III, "type": "qcm",
        "enonce": "Un processus qui attend la fin d'une opération d'entrée/sortie (E/S) se trouve dans quel état ?",
        "options": [
            "Prêt (Ready)",
            "En exécution (Running)",
            "En attente (Waiting)",
            "Terminé (Terminated)",
        ],
        "bonne": "En attente (Waiting)",
    },
    {
        "id": 13, "partie": PARTIE_III, "type": "qcm",
        "enonce": "Que contient le PCB (Process Control Block) d'un processus ?",
        "options": [
            "Uniquement le code source du programme",
            "Le PID, l'état, le compteur de programme, les informations mémoire, les ressources utilisées et la priorité",
            "Uniquement la liste des utilisateurs connectés",
            "Le résultat final du calcul du processus",
        ],
        "bonne": "Le PID, l'état, le compteur de programme, les informations mémoire, les ressources utilisées et la priorité",
    },
    {
        "id": 14, "partie": PARTIE_III, "type": "qcm",
        "enonce": "Comment fonctionne l'algorithme d'ordonnancement Round Robin (tourniquet) ?",
        "options": [
            "Chaque processus s'exécute jusqu'à sa fin sans interruption",
            "Le processus le plus court est toujours exécuté en premier",
            "Chaque processus reçoit le processeur pendant un quantum fixe ; s'il n'a pas terminé, il repart en fin de file (préemptif)",
            "Les processus sont exécutés selon une priorité absolue, sans quantum",
        ],
        "bonne": "Chaque processus reçoit le processeur pendant un quantum fixe ; s'il n'a pas terminé, il repart en fin de file (préemptif)",
    },
    {
        "id": 15, "partie": PARTIE_III, "type": "qcm",
        "enonce": "Comment calcule-t-on le temps de retour (temps de rotation) d'un processus ?",
        "options": [
            "Temps de fin - Temps d'arrivée",
            "Temps d'arrivée - Temps de fin",
            "Temps d'attente + Temps d'E/S",
            "Nombre de processus terminés / Temps total",
        ],
        "bonne": "Temps de fin - Temps d'arrivée",
    },
    {
        "id": 16, "partie": PARTIE_III, "type": "qcm",
        "enonce": "Qu'est-ce qu'un thread (fil d'exécution) ?",
        "options": [
            "Un fichier système caché",
            "La plus petite unité d'exécution au sein d'un processus",
            "Un périphérique d'entrée/sortie",
            "Une partition du disque dur",
        ],
        "bonne": "La plus petite unité d'exécution au sein d'un processus",
    },
    {
        "id": 17, "partie": PARTIE_III, "type": "qcm",
        "enonce": "Quelle affirmation concernant les adresses mémoire est correcte ?",
        "options": [
            "L'adresse logique est l'adresse réelle de la mémoire RAM",
            "L'adresse physique est générée par le compilateur",
            "Les adresses logique et physique sont toujours identiques",
            "L'adresse logique est générée par le processeur et doit être traduite en adresse physique (emplacement réel dans la RAM)",
        ],
        "bonne": "L'adresse logique est générée par le processeur et doit être traduite en adresse physique (emplacement réel dans la RAM)",
    },
    {
        "id": 18, "partie": PARTIE_III, "type": "qcm",
        "enonce": "Quel composant matériel est responsable de la traduction des adresses logiques en adresses physiques ?",
        "options": [
            "Le TLB (Translation Lookaside Buffer)",
            "La MMU (Memory Management Unit)",
            "Le BIOS",
            "Le registre d'instruction (IR)",
        ],
        "bonne": "La MMU (Memory Management Unit)",
    },
    {
        "id": 19, "partie": PARTIE_III, "type": "qcm",
        "enonce": "Comment définit-on la fragmentation externe de la mémoire ?",
        "options": [
            "Des blocs inutilisés à l'intérieur des partitions allouées",
            "Une perte de données due à une coupure de courant",
            "Des blocs libres non contigus qui empêchent d'allouer un processus malgré une mémoire totale suffisante",
            "Un défaut du disque dur",
        ],
        "bonne": "Des blocs libres non contigus qui empêchent d'allouer un processus malgré une mémoire totale suffisante",
    },
    {
        "id": 20, "partie": PARTIE_III, "type": "vf",
        "enonce": "La pagination supprime la fragmentation externe, mais peut entraîner une fragmentation interne (dernière page partiellement occupée).",
        "options": ["Vrai", "Faux"],
        "bonne": "Vrai",
    },
]

# ---------------------------------------------------------------------------
# 3. CORRECTION AUTOMATIQUE
# ---------------------------------------------------------------------------


def corriger(reponses: dict) -> dict:
    """Corrige les réponses de l'étudiant.

    Paramètre :
        reponses : dict {f"q{id}": option choisie ou None}

    Retour :
        dict avec "resultats" (liste détaillée), "score" et "total".
    """
    resultats = []
    score = 0
    for q in QUESTIONS:
        rep = reponses.get(f"q{q['id']}")
        correct = rep is not None and rep == q["bonne"]
        resultats.append(
            {
                "numero": q["id"],
                "partie": q["partie"],
                "enonce": q["enonce"],
                "reponse_etudiant": rep if rep else "Non répondue",
                "bonne_reponse": q["bonne"],
                "correct": correct,
                "repondue": rep is not None,
            }
        )
        if correct:
            score += 1
    return {"resultats": resultats, "score": score, "total": len(QUESTIONS)}


def bilan_par_partie(resultats: list) -> dict:
    """Calcule le score obtenu pour chacune des trois parties du cours."""
    bilan = {}
    for r in resultats:
        p = r["partie"]
        bilan.setdefault(p, {"obtenu": 0, "total": 0})
        bilan[p]["total"] += 1
        if r["correct"]:
            bilan[p]["obtenu"] += 1
    return bilan


def mention(pct: float) -> str:
    """Mention associée au pourcentage de réussite."""
    if pct >= 80:
        return "Excellent"
    if pct >= 60:
        return "Bien"
    if pct >= 40:
        return "Passable"
    return "Insuffisant"


def appreciation(pct: float) -> str:
    """Commentaire pédagogique associé au pourcentage de réussite."""
    if pct >= 80:
        return (
            "Très bonne maîtrise des concepts fondamentaux des systèmes "
            "d'exploitation. L'étudiant dispose des prérequis solides pour "
            "aborder sereinement la suite du module."
        )
    if pct >= 60:
        return (
            "Bonne maîtrise globale du cours. Quelques révisions ciblées "
            "sont recommandées sur les notions manquées afin de consolider "
            "les acquis."
        )
    if pct >= 40:
        return (
            "Maîtrise partielle des concepts. Une relecture attentive des "
            "trois parties du cours est nécessaire, en particulier sur les "
            "thèmes échoués listés ci-dessus."
        )
    return (
        "Lacunes importantes sur l'ensemble du cours. Il est fortement "
        "conseillé de reprendre intégralement le support de cours et de "
        "refaire cette évaluation diagnostique."
    )


# ---------------------------------------------------------------------------
# 4. GÉNÉRATION DU RAPPORT PDF AUTOCORRIGÉ (fpdf2)
# ---------------------------------------------------------------------------
COULEUR_BLEU = (31, 59, 115)      # bleu EMSI
COULEUR_GRIS_CLAIR = (238, 242, 248)
VERT_OK = (40, 150, 70)
ROUGE_KO = (200, 60, 60)
GRIS_NREP = (140, 140, 140)


def _l(texte: str) -> str:
    """Rend une chaîne compatible avec l'encodage latin-1 des polices
    standard de fpdf2 (apostrophes typographiques, tirets, guillemets...)."""
    if texte is None:
        return ""
    remplacements = {
        "\u2019": "'", "\u2018": "'",          # apostrophes typographiques
        "\u201c": '"', "\u201d": '"',          # guillemets anglais
        "\u00ab": '"', "\u00bb": '"',          # guillemets français
        "\u2013": "-", "\u2014": "-",          # tirets
        "\u0153": "oe", "\u0152": "OE",        # ligatures
        "\u2026": "...", "\u00a0": " ",        # ellipse, espace insécable
    }
    for k, v in remplacements.items():
        texte = texte.replace(k, v)
    return texte.encode("latin-1", "replace").decode("latin-1")


class RapportPDF(FPDF):
    """Document PDF : en-tête et pied de page personnalisés."""

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_margins(12, 12, 12)
        self.set_auto_page_break(auto=True, margin=18)
        self.alias_nb_pages()

    def header(self):
        if self.page_no() == 1:
            self.set_fill_color(*COULEUR_BLEU)
            self.set_text_color(255, 255, 255)
            self.set_font("Helvetica", "B", 16)
            self.cell(0, 12, _l("ÉVALUATION DIAGNOSTIQUE"), align="C",
                      fill=True, new_x="LMARGIN", new_y="NEXT")
            self.set_font("Helvetica", "B", 13)
            self.cell(0, 10, _l("Systèmes d'exploitation I"), align="C",
                      fill=True, new_x="LMARGIN", new_y="NEXT")
            self.set_font("Helvetica", "I", 9)
            self.cell(0, 8, _l("Cours de Pr. S. EL MOUMNI — EMSI"), align="C",
                      fill=True, new_x="LMARGIN", new_y="NEXT")
            self.ln(6)
            self.set_text_color(0, 0, 0)
        else:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 6, _l("Évaluation diagnostique — Systèmes d'exploitation I"),
                      align="L", new_x="LMARGIN", new_y="NEXT")
            self.line(12, self.get_y(), 198, self.get_y())
            self.ln(4)
            self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, _l("Rapport généré automatiquement — Page ") +
                      str(self.page_no()) + "/{nb}", align="C")
        self.set_text_color(0, 0, 0)


def generer_pdf(nom: str, classe: str, correction: dict, bilan: dict) -> bytes:
    """Génère le rapport PDF autocorrigé et renvoie les octets du document."""
    score = correction["score"]
    total = correction["total"]
    pct = round(score / total * 100)

    pdf = RapportPDF()
    pdf.add_page()

    # -------------------- Bloc identification --------------------
    date_str = datetime.now().strftime("%d/%m/%Y à %H:%M")
    pdf.set_fill_color(*COULEUR_GRIS_CLAIR)
    pdf.set_draw_color(*COULEUR_BLEU)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, _l(f"Étudiant : {nom}"), border=1, fill=True,
             new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, _l(f"Classe / Groupe : {classe}"), border=1, fill=True,
             new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, _l(f"Date de l'évaluation : {date_str}"), border=1,
             fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # -------------------- Bloc score global --------------------
    if pct >= 60:
        couleur_score = VERT_OK
    elif pct >= 40:
        couleur_score = (220, 130, 30)
    else:
        couleur_score = ROUGE_KO
    pdf.set_fill_color(*couleur_score)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(0, 12, _l(f"Score global : {score} / {total}  ({pct} %)"),
             align="C", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 9, _l(f"Mention : {mention(pct)}"), align="C", fill=True,
             new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(6)

    # -------------------- Résultats par partie --------------------
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*COULEUR_BLEU)
    pdf.cell(0, 8, _l("1. Résultats par partie du cours"),
             new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(1)

    largeurs = [98, 32, 26, 34]
    entetes = ["Partie du cours", "Points", "Total", "Taux"]
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_fill_color(*COULEUR_BLEU)
    pdf.set_text_color(255, 255, 255)
    for lib, w in zip(entetes, largeurs):
        pdf.cell(w, 8, _l(lib), border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(0, 0, 0)

    pdf.set_font("Helvetica", "", 9)
    for i, (partie, b) in enumerate(bilan.items()):
        taux = round(b["obtenu"] / b["total"] * 100)
        if i % 2 == 0:
            pdf.set_fill_color(*COULEUR_GRIS_CLAIR)
            remplir = True
        else:
            remplir = False
        pdf.cell(largeurs[0], 7.5, _l(partie), border=1, fill=remplir)
        pdf.cell(largeurs[1], 7.5, _l(f"{b['obtenu']} / {b['total']}"),
                 border=1, fill=remplir, align="C")
        pdf.cell(largeurs[2], 7.5, _l(str(b["total"])), border=1,
                 fill=remplir, align="C")
        pdf.cell(largeurs[3], 7.5, _l(f"{taux} %"), border=1, fill=remplir,
                 align="C")
        pdf.ln()
    pdf.ln(4)

    # -------------------- Détail des réponses --------------------
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*COULEUR_BLEU)
    pdf.cell(0, 8, _l("2. Détail des réponses et correction automatique"),
             new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(1)

    partie_courante = None
    for r in correction["resultats"]:
        if r["partie"] != partie_courante:
            partie_courante = r["partie"]
            if pdf.get_y() > 250:
                pdf.add_page()
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 10.5)
            pdf.set_text_color(*COULEUR_BLEU)
            pdf.multi_cell(0, 7, _l(partie_courante),
                           new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(0, 0, 0)

        if pdf.get_y() > 258:
            pdf.add_page()

        # Énoncé de la question
        pdf.set_font("Helvetica", "B", 9.5)
        pdf.multi_cell(0, 5.5, _l(f"Q{r['numero']}. {r['enonce']}"),
                       new_x="LMARGIN", new_y="NEXT")

        # Badge de verdict + réponse de l'étudiant
        if not r["repondue"]:
            badge, fill = " NON REPONDUE ", GRIS_NREP
        elif r["correct"]:
            badge, fill = " CORRECT ", VERT_OK
        else:
            badge, fill = " INCORRECT ", ROUGE_KO
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.set_fill_color(*fill)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(27, 5.5, _l(badge), fill=True, align="C")
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(0, 5.5,
                       _l(f"  Votre réponse : {r['reponse_etudiant']}"),
                       new_x="LMARGIN", new_y="NEXT")

        # Bonne réponse si la réponse est mauvaise
        if not r["correct"]:
            pdf.set_text_color(20, 80, 160)
            pdf.multi_cell(0, 5.5,
                           _l(f"      Bonne réponse : {r['bonne_reponse']}"),
                           new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(0, 0, 0)
        pdf.ln(2.5)

    # -------------------- Appreciation finale --------------------
    if pdf.get_y() > 235:
        pdf.add_page()
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*COULEUR_BLEU)
    pdf.cell(0, 8, _l("3. Appréciation et conseils"),
             new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(*COULEUR_GRIS_CLAIR)
    pdf.set_font("Helvetica", "I", 10)
    pdf.multi_cell(0, 6,
                   _l(appreciation(pct)) + " " + _l(
                       "Ce rapport diagnostique identifie les parties du "
                       "cours à consolider avant la poursuite du module."),
                   border=1, fill=True, new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())
