import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Configuration de la page
st.set_page_config(page_title="Simulation Lois de Kepler", layout="centered")
st.title("🪐 Modélisation des Lois de Kepler")
st.write("Explorez le mouvement des corps célestes autour du Soleil à travers les trois lois fondamentales.")

# Données réelles du Système solaire
# Format : 'Nom': [a (UA), e (excentricité), T (années)]
donnees_planetes = {
    "Mercure": [0.387, 0.206, 0.241],
    "Vénus": [0.723, 0.007, 0.615],
    "Terre": [1.000, 0.017, 1.000],
    "Mars": [1.524, 0.093, 1.881],
    "Jupiter": [5.203, 0.048, 11.86],
    "Saturne": [9.537, 0.054, 29.45],
    "Uranus": [19.191, 0.047, 84.02],
    "Neptune": [30.069, 0.009, 164.8],
    "Comète (Excentricité forcée)": [5.000, 0.600, 11.18] # Ajout pédagogique pour bien voir l'ellipse et la loi des aires
}

# Sélection de l'astre dans la barre latérale
st.sidebar.header("Configuration Céleste")
nom_astre = st.sidebar.selectbox("Choisir une planète ou un corps :", list(donnees_planetes.keys()), index=2)

# Récupération des constantes de l'astre sélectionné
a, e, T = donnees_planetes[nom_astre]
b = a * np.sqrt(1 - e**2)  # Demi-petit axe
c = a * e                  # Distance centre-foyer

# Création des trois onglets de lois
onglet1, onglet2, onglet3 = st.tabs(["1ère Loi (Orbites)", "2ème Loi (Aires)", "3ème Loi (Périodes)"])

# -----------------------------------------------------------------
# ONGLET 1 : PREMIÈRE LOI (LOI DES ORBITES)
# -----------------------------------------------------------------
with onglet1:
    st.header("1ère Loi : Les trajectoires elliptiques")
    st.write(f"Trajectoire de **{nom_astre}** autour du Soleil.")
    
    # Génération des points de l'ellipse
    theta = np.linspace(0, 2*np.pi, 500)
    # Équation paramétrique par rapport au centre de l'ellipse : x = a*cos(t), y = b*sin(t)
    # Le Soleil étant au foyer (x = +c ou -c), on décale pour placer le Soleil à l'origine (0,0)
    x_ellipse = a * np.cos(theta) - c
    y_ellipse = b * np.sin(theta)
    
    fig1, ax1 = plt.subplots(figsize=(7, 7))
    ax1.plot(x_ellipse, y_ellipse, color='#3182ce', linewidth=2, label=f"Orbite de {nom_astre}")
    
    # Position du Soleil au foyer
    ax1.plot(0, 0, 'yo', markersize=14, label="Soleil (Foyer F1)")
    # Position du second foyer vide
    ax1.plot(-2*c, 0, 'kx', markersize=8, alpha=0.5, label="Foyer vide (F2)")
    # Centre de l'ellipse
    ax1.plot(-c, 0, 'k+', markersize=8, alpha=0.5, label="Centre de l'ellipse")
    
    # Points remarquables (Périhélie et Aphélie)
    ax1.plot(a - c, 0, 'ro', markersize=6, label=f"Périhélie (d_min = {a*(1-e):.3f} UA)")
    ax1.plot(-a - c, 0, 'bo', markersize=6, label=f"Aphélie (d_max = {a*(1+e):.3f} UA)")
    
    ax1.set_xlabel("x (Unités Astronomiques - UA)")
    ax1.set_ylabel("y (Unités Astronomiques - UA)")
    ax1.set_xlim(-a*1.3 - c, a*1.3 - c)
    ax1.set_ylim(-a*1.3, a*1.3)
    ax1.axhline(0, color='gray', linestyle='--', linewidth=0.5)
    ax1.axvline(0, color='gray', linestyle='--', linewidth=0.5)
    ax1.grid(True, linestyle=':', alpha=0.5)
    ax1.legend(loc="upper right", fontsize=9)
    ax1.set_aspect('equal', 'box') # Indispensable pour ne pas déformer l'ellipse
    
    st.pyplot(fig1)
    st.info(f"💡 **Données géométriques :** Demi-grand axe $a = {a:.3f}$ UA | Excentricité $e = {e:.3f}$. \n\n"
            f"*Remarque :* Plus l'excentricité $e$ est proche de 0, plus la trajectoire ressemble à un cercle parfait.")

# -----------------------------------------------------------------
# ONGLET 2 : DEUXIÈME LOI (LOI DES AIRES)
# -----------------------------------------------------------------
with onglet2:
    st.header("2ème Loi : Loi des aires et vitesse")
    st.write("Le rayon vecteur balaie des aires égales pendant des intervalles de temps égaux.")
    
    # Curseur pour simuler deux positions temporelles distinctes (Périhélie vs Aphélie)
    st.write("Visualisons deux secteurs correspondant à la même durée $\\Delta t$ à deux moments de l'orbite :")
    
    # Construction géométrique de secteurs d'aires égales
    # Près du Périhélie (à droite, vitesse rapide -> grand angle)
    t_peri = np.linspace(-0.25, 0.25, 100)
    x_p = a * np.cos(t_peri) - c
    y_p = b * np.sin(t_peri)
    
    # Près de l'Aphélie (à gauche, vitesse lente -> petit angle pour compenser la grande distance)
    # L'angle corrigé pour garder une aire identique dépend fortement de l'excentricité
    facteur_angle = ((1-e)/(1+e))**1.5
    t_aphe = np.linspace(np.pi - 0.25*facteur_angle, np.pi + 0.25*facteur_angle, 100)
    x_a = a * np.cos(t_aphe) - c
    y_a = b * np.sin(t_aphe)
    
    fig2, ax2 = plt.subplots(figsize=(7, 7))
    ax2.plot(x_ellipse, y_ellipse, color='gray', linestyle='--', alpha=0.7)
    ax2.plot(0, 0, 'yo', markersize=14, label="Soleil")
    
    # Remplissage des secteurs (Aires)
    px = np.concatenate(([0], x_p, [0]))
    py = np.concatenate(([0], y_p, [0]))
    ax2.fill(px, py, color='green', alpha=0.4, label="Aire 1 (Périhélie : proche, donc rapide)")
    
    ax_x = np.concatenate(([0], x_a, [0]))
    ax_y = np.concatenate(([0], y_a, [0]))
    ax_2 = ax2.fill(ax_x, ax_y, color='purple', alpha=0.4, label="Aire 2 (Aphélie : loin, donc lent)")
    
    ax2.set_xlabel("x (UA)")
    ax2.set_ylabel("y (UA)")
    ax2.set_xlim(-a*1.3 - c, a*1.3 - c)
    ax2.set_ylim(-a*1.3, a*1.3)
    ax2.grid(True, linestyle=':', alpha=0.5)
    ax2.legend(loc="upper right", fontsize=9)
    ax2.set_aspect('equal', 'box')
    
    st.pyplot(fig2)
    st.warning("📈 **Observation majeure :** Les deux surfaces colorées ont la **même aire**. "
               "On voit clairement que près du Soleil (vert), le segment est court mais l'arc parcouru est grand : la planète va **vite**. "
               "Loin du Soleil (violet), le segment est long et l'arc est court : la planète va **lentement**.")

# -----------------------------------------------------------------
# ONGLET 3 : TROISIÈME LOI (LOI DES PÉRIODES)
# -----------------------------------------------------------------
with onglet3:
    st.header("3ème Loi : T² / a³ = Constante")
    st.write("Vérification de la loi des périodes pour les corps du Système solaire.")
    
    # Calcul du rapport pour l'astre choisi
    rapport = (T**2) / (a**3)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Période T (années) :", f"{T:.2f}")
    col2.metric("Demi-grand axe a (UA) :", f"{a:.3f}")
    col3.metric("Rapport T² / a³ :", f"{rapport:.4f}")
    
    # Construction du graphique global comparatif
    fig3, ax3 = plt.subplots(figsize=(9, 4.5))
    
    liste_a = []
    liste_T2 = []
    for p, valeurs in donnees_planetes.items():
        if p != "Comète (Excentricité forcée)": # On garde les vraies planètes
            liste_a.append(valeurs[0]**3)
            liste_T2.append(valeurs[2]**2)
            ax3.scatter(valeurs[0]**3, valeurs[2]**2, color='#2b6cb0', s=60, zorder=3)
            ax3.text(valeurs[0]**3 * 1.05, valeurs[2]**2 * 0.9, p, fontsize=8)
            
    # Droite théorique de pente 1
    axes_x = np.linspace(0, max(liste_a)*1.1, 500)
    ax3.plot(axes_x, axes_x, color='red', linestyle='-', label="Modèle théorique : T² = a³")
    
    ax3.set_title("Vérification graphique de la 3ème loi de Kepler", fontsize=11, fontweight='bold')
    ax3.set_xlabel("a³ (en UA³)", fontsize=10)
    ax3.set_ylabel("T² (en années²)", fontsize=10)
    ax3.grid(True, linestyle=':', alpha=0.6)
    ax3.legend()
    
    st.pyplot(fig3)
    st.success(f"📝 **Conclusion :** Pour toutes les planètes gravitant autour du Soleil, le rapport $\\frac{{T^2}}{{a^3}}$ vaut environ **1,00** (avec les unités UA et années). "
               f"Ce rapport ne dépend pas de la masse de la planète, mais uniquement de la masse de l'étoile centrale ($M_{{Soleil}}$).")
