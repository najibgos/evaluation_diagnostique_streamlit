# -*- coding: utf-8 -*-
"""
============================================================================
 ÉVALUATION DIAGNOSTIQUE — SYSTÈMES D'EXPLOITATION I
 Application Streamlit avec correction automatique et rapport PDF
============================================================================
 Contenu du cours : « Systèmes d'exploitation I » — Pr. S. EL MOUMNI (EMSI)

 Fonctionnement :
   1. L'étudiant saisit son nom et sa classe.
   2. Il répond à 20 questions (QCM + Vrai/Faux) couvrant les 3 parties
      du cours.
   3. À la soumission : correction automatique, score, bilan par partie.
   4. Un rapport PDF autocorrigé est généré et téléchargeable.

 Lancement :
   pip install -r requirements.txt
   streamlit run app.py
============================================================================
"""

from eval_logic import (
    PARTIES,
    QUESTIONS,
    appreciation,
    bilan_par_partie,
    corriger,
    generer_pdf,
    mention,
)

import streamlit as st

# ---------------------------------------------------------------------------
# Configuration de la page
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Évaluation Diagnostique — Systèmes d'exploitation I",
    page_icon="🖥️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Petite couche de style pour une interface sobre et professionnelle
st.markdown(
    """
    <style>
        .bloc-partie {
            background: linear-gradient(90deg, #1f3b73, #2f5aa8);
            color: #ffffff;
            padding: 10px 16px;
            border-radius: 10px;
            font-size: 1.05rem;
            font-weight: 600;
            margin-top: 22px;
            margin-bottom: 4px;
        }
        .carte-info {
            background: #eef3fb;
            border-left: 5px solid #1f3b73;
            padding: 14px 18px;
            border-radius: 8px;
            color: #1f2a44;
            font-size: 0.98rem;
        }
        div[data-testid="stRadio"] > div {
            gap: 0.35rem;
        }
        div[data-testid="stMetric"] {
            background: #f6f8fc;
            border: 1px solid #dfe6f2;
            border-radius: 10px;
            padding: 10px 14px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# État de session (3 phases : accueil -> quiz -> resultat)
# ---------------------------------------------------------------------------
if "phase" not in st.session_state:
    st.session_state.phase = "accueil"
if "etudiant" not in st.session_state:
    st.session_state.etudiant = {}
if "correction" not in st.session_state:
    st.session_state.correction = None
if "bilan" not in st.session_state:
    st.session_state.bilan = {}
if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None


def slugifier(texte: str) -> str:
    """Rend un texte utilisable dans un nom de fichier."""
    return "".join(c if c.isalnum() else "_" for c in texte.strip())[:40] or "etudiant"


# ---------------------------------------------------------------------------
# Barre latérale : informations sur l'évaluation
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 📋 À propos de l'évaluation")
    st.markdown(
        """
        **Module :** Systèmes d'exploitation I
        **Enseignant :** Pr. S. EL MOUMNI (EMSI)

        ---
        - **20 questions** (QCM et Vrai/Faux)
        - **3 parties** couvertes :
          - Introduction aux SE
          - Architecture et composants des SE
          - Gestion des ressources par un SE
        - **Barème :** 1 point par question
        - **Durée conseillée :** 20 minutes
        - **Rapport PDF** autocorrigé généré à la fin
        """
    )
    st.markdown("---")
    phases = {
        "accueil": "🏠 Page d'accueil",
        "quiz": "📝 Évaluation en cours",
        "resultat": "📊 Résultats et rapport PDF",
    }
    st.caption(f"**Étape actuelle :** {phases[st.session_state.phase]}")

# ---------------------------------------------------------------------------
# Titre principal
# ---------------------------------------------------------------------------
st.title("🖥️ Évaluation Diagnostique")
st.markdown("### Systèmes d'exploitation I")
st.caption("Basée sur le cours de Pr. S. EL MOUMNI — EMSI")

# ===========================================================================
# PHASE 1 — ACCUEIL : saisie du nom et de la classe
# ===========================================================================
if st.session_state.phase == "accueil":
    st.markdown(
        """
        <div class="carte-info">
        👋 <b>Bienvenue dans cette évaluation diagnostique.</b><br>
        Elle a pour objectif de mesurer vos connaissances sur l'ensemble du
        cours <i>Systèmes d'exploitation I</i> : introduction aux SE,
        architecture et composants, ainsi que la gestion des ressources
        (processus, ordonnancement, mémoire).
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        "Veuillez renseigner votre **nom** et votre **classe** pour commencer."
    )

    with st.form("form_identite", clear_on_submit=False):
        col1, col2 = st.columns(2)
        nom = col1.text_input("Nom complet de l'étudiant ✱",
                              placeholder="Ex. : ALAMI Ahmed")
        classe = col2.text_input("Classe / Groupe ✱",
                                 placeholder="Ex. : 2AP-G2")
        commencer = st.form_submit_button(
            "▶️  Commencer l'évaluation"
        )

    if commencer:
        if not nom.strip() or not classe.strip():
            st.error(
                "⚠️ Veuillez renseigner votre **nom** et votre **classe** "
                "avant de commencer l'évaluation."
            )
        else:
            st.session_state.etudiant = {
                "nom": nom.strip(),
                "classe": classe.strip(),
            }
            st.session_state.phase = "quiz"
            st.rerun()

# ===========================================================================
# PHASE 2 — QUIZ : 20 questions réparties sur les 3 parties
# ===========================================================================
elif st.session_state.phase == "quiz":
    nom = st.session_state.etudiant["nom"]
    classe = st.session_state.etudiant["classe"]
    st.info(f"👤 Étudiant : **{nom}**    |    🎓 Classe : **{classe}**")
    st.markdown(
        "Répondez à **toutes les questions** puis cliquez sur "
        "« Soumettre mes réponses ». Chaque question vaut **1 point**."
    )

    reponses = {}
    with st.form("form_quiz", clear_on_submit=False):
        for partie in PARTIES:
            st.markdown(
                f'<div class="bloc-partie">📘 {partie}</div>',
                unsafe_allow_html=True,
            )
            questions_partie = [q for q in QUESTIONS if q["partie"] == partie]
            for q in questions_partie:
                st.markdown(f"**Question {q['id']}.** {q['enonce']}")
                horizontal = q.get("type") == "vf"
                reponses[f"q{q['id']}"] = st.radio(
                    "Votre réponse :",
                    q["options"],
                    index=None,
                    key=f"q{q['id']}",
                    label_visibility="collapsed",
                    horizontal=horizontal,
                )
                st.markdown("<div style='height:12px'></div>",
                            unsafe_allow_html=True)

        soumettre = st.form_submit_button(
            "✅  Soumettre mes réponses et corriger"
        )

    if soumettre:
        non_repondues = [k for k, v in reponses.items() if v is None]
        if non_repondues:
            st.error(
                f"⚠️ Il reste **{len(non_repondues)} question(s) sans réponse** "
                "(n° " + ", ".join(str(k[1:]) for k in sorted(
                    non_repondues, key=lambda x: int(x[1:]))) + "). "
                "Veuillez y répondre avant de soumettre."
            )
        else:
            correction = corriger(reponses)
            st.session_state.correction = correction
            st.session_state.bilan = bilan_par_partie(correction["resultats"])
            st.session_state.pdf_bytes = generer_pdf(
                nom, classe, correction, st.session_state.bilan
            )
            st.session_state.phase = "resultat"
            st.rerun()

# ===========================================================================
# PHASE 3 — RÉSULTATS : score, correction détaillée et PDF téléchargeable
# ===========================================================================
elif st.session_state.phase == "resultat":
    nom = st.session_state.etudiant["nom"]
    classe = st.session_state.etudiant["classe"]
    correction = st.session_state.correction
    bilan = st.session_state.bilan
    score = correction["score"]
    total = correction["total"]
    pct = round(score / total * 100)

    st.success(
        f"✅ Évaluation terminée, **{nom}** ! Voici votre correction "
        "automatique."
    )

    # -------------------- Indicateurs globaux --------------------
    c1, c2, c3 = st.columns(3)
    c1.metric("🎯 Score", f"{score} / {total}")
    c2.metric("📊 Pourcentage", f"{pct} %")
    c3.metric("🏅 Mention", mention(pct))
    st.progress(pct, text=f"Progression de la maîtrise : {pct} %")
    st.markdown(
        f"💬 **Appréciation :** {appreciation(pct)}"
    )

    # -------------------- Bilan par partie --------------------
    st.markdown("## 📚 Résultats par partie du cours")
    parties_a_reviser = []
    for partie, b in bilan.items():
        taux = round(b["obtenu"] / b["total"] * 100)
        st.markdown(f"**{partie}** — {b['obtenu']}/{b['total']} ({taux} %)")
        st.progress(int(taux))
        if taux < 60:
            parties_a_reviser.append(partie)

    if parties_a_reviser:
        st.warning(
            "🔎 **Révision conseillée :** " + " • ".join(parties_a_reviser)
        )
    else:
        st.info("👍 Aucune partie en dessous de 60 % : bons prérequis globaux !")

    # -------------------- Correction détaillée --------------------
    st.markdown("## 🧾 Correction détaillée des réponses")
    lignes = []
    for r in correction["resultats"]:
        lignes.append(
            {
                "N°": f"Q{r['numero']}",
                "Question": r["enonce"],
                "Votre réponse": r["reponse_etudiant"],
                "Bonne réponse": r["bonne_reponse"],
                "Résultat": "✔ Correct" if r["correct"] else "✘ Incorrect",
            }
        )
    st.dataframe(
        lignes,
        hide_index=True,
        column_config={
            "N°": st.column_config.TextColumn(width="small"),
            "Question": st.column_config.TextColumn(width="large"),
            "Votre réponse": st.column_config.TextColumn(width="medium"),
            "Bonne réponse": st.column_config.TextColumn(width="medium"),
            "Résultat": st.column_config.TextColumn(width="small"),
        },
    )

    # -------------------- Rapport PDF --------------------
    st.markdown("## 📄 Rapport PDF autocorrigé")
    st.markdown(
        "Un rapport complet (identification, score, bilan par partie, "
        "correction détaillée et appréciation) a été généré automatiquement. "
        "Téléchargez-le ci-dessous."
    )
    nom_fichier = (
        f"evaluation_diagnostique_{slugifier(nom)}_{slugifier(classe)}.pdf"
    )
    st.download_button(
        label="📄 Télécharger le rapport PDF autocorrigé",
        data=st.session_state.pdf_bytes,
        file_name=nom_fichier,
        mime="application/pdf",
    )

    st.markdown("---")
    if st.button("🔄 Recommencer l'évaluation"):
        st.session_state.clear()
        st.rerun()
