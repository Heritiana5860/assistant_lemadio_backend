# 🛒 Création d'une Vente (Vente Directe et Revendeur)

Ce document détaille les deux processus de création de vente dans l'application Lemadio : **Vente Directe** (client final) et **Vente Revendeur** (approvisionnement ADES).

---

## 🧭 Initiation de la Vente : La Question Clé (`##`)

Pour commencer toute transaction, l'Assistant Lemadio demandera au vendeur de spécifier le type de vente.

### Point de Départ : Accès à la Page de Vente

La page des ventes s'ouvre automatiquement après une connexion réussie.

### Étapes pour Démarrer (Bouton « + »)

1.  Cliquez sur le **bouton rond vert** avec une icône « + » (situé en haut à droite de la barre de navigation inférieure).
2.  Deux options s’affichent :
    - **Vente revendeur :** Vente destinée aux revendeurs ADES (approvisionnement).
    - **Vente directe :** Vente aux clients finaux.

### 💬 Réponse Recommandée de l'Assistant

Si l'utilisateur demande : "Comment créer une vente ?" ou "Je veux faire une vente" :

> Pour vous aider au mieux, veuillez préciser si vous souhaitez créer :
>
> 1.  Une **Vente Directe** (pour un client final) ?
> 2.  Une **Vente Revendeur** (pour un revendeur ADES) ?

---

## 1️⃣ Processus de Vente Directe (Client Final) (`##`)

### Schéma du Flux

**Vente Directe** : `Page des Ventes` $\to$ `Informations Client` $\to$ `Sélection Facture` $\to$ `Vérification Client` $\to$ `Scan Réchaud` $\to$ `Conditions & Signature` $\to$ **Enregistrer**.

### Étape 1 : Remplir la Page d’Information Client

Le vendeur est redirigé vers cette page où tous les champs suivants sont **obligatoires** (sauf CIN) :

- **Catégorie :** Liste déroulante (Private, Hotel, Ecole, NGO, Restaurant, Hopital, Microbusiness, Prison).
- **Cluster :** Liste déroulante pour définir le type de réchaud vendu (Charcoal, Wood, Solar + OLI-b, Solar + OLI-c).
- **Identité :** Mme/Mr (nom), Surnom (prénom), Contact (numéro de téléphone), Adresse (adresse complète).
- **Localisation :** Cliquer sur l'icône de localisation pour ouvrir la carte OpenStreetMap.
- **Carte & Localisation :**
  - La carte récupère la position actuelle.
  - Utilisez la barre de recherche (Fokontany, Région, etc.) si nécessaire.
  - **Placez un marqueur rouge** sur l'endroit exact.
  - **Vérifiez et complétez manuellement** les champs auto-remplis si « Non spécifié » apparaît.
- **CIN (Facultatif) :** Capture photo du CIN recto et verso.
- **Action :** Cliquez sur **Valider** pour passer à l'étape suivante.

### Étape 2 : Sélectionner le Numéro de Facture

- Le vendeur doit sélectionner **un seul numéro de facture** disponible.
- Utilisez la barre de recherche pour filtrer la liste.
- **Action :** Cliquez sur **Valider** pour continuer.

### Étape 3 : Vérification des Informations Client

Cette page affiche les données saisies (Nom, Adresse, Région, etc.) pour une confirmation finale avec le client.

- **Action :** Si les informations sont correctes, cliquez sur **Valider** pour passer au scan. Utilisez le bouton retour pour corriger une erreur.

### Étape 4 : Scanner le(s) Réchaud(s)

1.  Lancez le scanner via le **bouton arrondi** dans le cadre jaune.
2.  Scannez le **code-barres** du réchaud.
3.  **Vérification :** Le système vérifie la présence du réchaud dans le stock local du vendeur. Un message d'erreur s'affiche si le réchaud n'est pas dans votre stock.
4.  **Prix et Zone :** Chaque réchaud scanné doit être associé à un prix et une zone.
    - **Les zones sont :** **Zone riche**, **Zone moyenne**, **Zone LNOB**.
    - Le prix unitaire dépend du **type de réchaud** et de la **zone géographique** du client.
5.  **Récapitulatif :** Le tableau en bas affiche le **Type de réchaud**, le **Prix unitaire**, la **Quantité** et le **Total**.
6.  **Action :** Cliquez sur **Valider** pour continuer.

### Étape 5 : Conditions de Garantie et Signature

1.  Consultez les **conditions de garantie** (Garantie de 3 ans, Exclusion mauvaise utilisation, Limitation à l'argile, Grilles supplémentaires gratuites, Certificats CO₂ propriété ADES).
2.  Cochez la case **« J’accepte de céder le droit de ce dossier »**.
3.  Le client doit signer dans le **signature pad**. Utilisez l'icône poubelle pour effacer.
4.  **Action Finale :** Cliquez sur **Enregistrer** pour finaliser la vente.

---

## 2️⃣ Processus de Vente Revendeur (Approvisionnement ADES) (`##`)

Ce processus est dédié à l'approvisionnement des revendeurs ADES (boutiques).

### Schéma du Flux

**Vente Revendeur** : `Page des Ventes` $\to$ `Sélection Facture` $\to$ `Sélection Revendeur` $\to$ `Scan Réchaud` $\to$ `Conditions & Signature` $\to$ **Enregistrer**.

### Étape 1 : Sélectionner le Numéro de Facture

- Le vendeur sélectionne un numéro de facture disponible dans la liste.
- **Action :** Cliquez sur **Valider**.

### Étape 2 : Sélectionner le Revendeur

- La liste des revendeurs liés au centre de vente est affichée.
- Le vendeur sélectionne le revendeur qui effectue l'approvisionnement.
- **Action :** Cliquez sur **Valider**.

### Étape 3 : Scanner le(s) Réchaud(s)

_(Cette étape est identique à l'étape 4 de la Vente Directe)._

1.  Scannez le **code-barres** du réchaud.
2.  Le réchaud doit être dans le stock local du vendeur.
3.  Chaque réchaud est associé à un prix et une zone (**riche, moyenne, LNOB**).
4.  Le tableau récapitulatif affiche le **Type**, le **Prix unitaire**, la **Quantité** et le **Total**.
5.  **Action :** Cliquez sur **Valider** pour continuer.

### Étape 4 : Conditions de Garantie et Signature

_(Cette étape est identique à l'étape 5 de la Vente Directe)._

1.  Lecture des conditions.
2.  Acceptation de la cession de droit via la case à cocher.
3.  Signature dans le **signature pad**.
4.  **Action Finale :** Cliquez sur **Enregistrer** pour finaliser la vente.

---

## 📊 Gestion de la Synchronisation et du Résultat (`##`)

### Résultat de la Vente

| Statut                           | Description                                                                                     | Indicateur                                                                                                |
| :------------------------------- | :---------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------- |
| **Vente Réussie (Synchronisée)** | Enregistrée localement et envoyée au serveur (Salesforce).                                      | Carte marquée **"Synchronisé"** (vert). Réchaud marqué **"vendu"** dans le stock.                         |
| **Vente Non Synchronisée**       | Enregistrée localement, mais **pas encore envoyée au serveur** (absence de connexion Internet). | Statut **"Non synchronisé"** (orange). Badge sur l'icône Ventes indiquant le nombre de ventes en attente. |

### Procédure de Synchronisation des Données (Ventes Hors Ligne)

- **Prérequis :** Une connexion Internet est requise pour la synchronisation.

1.  Accédez à la **page des ventes**.
2.  Vérifiez les cartes marquées **"Non synchronisé"** (orange).
3.  Cliquez sur les **trois points verticaux** dans l’en-tête de la page.
4.  Sélectionnez l'option **Synchroniser** pour envoyer les données au serveur Salesforce.

---

## 🚫 Annulation d'une Vente (`##`)

### Procédure d'Annulation

Pour annuler une vente enregistrée via l'application Lemadio, suivez les étapes ci-dessous :

1.  Accédez à la **Page des ventes**.
2.  Localisez la carte de la vente concernée.
3.  Cliquez sur le bouton **"Annuler"** sur la carte.
4.  L'application récupère automatiquement le numéro de réchaud et le numéro de facture associés.
5.  Entrez le **motif** précis de l'annulation de la vente.
6.  Cliquez sur le bouton **"Valider"** pour confirmer.

### ⚠️ Restriction d'Annulation

L'annulation d'une vente depuis l'application mobile est limitée dans le temps.

> **Condition :** L'annulation n'est valide que si elle est effectuée dans la **journée suivant la création** de la vente.
> **Après ce délai :** Le vendeur doit **contacter le responsable** ou l'administrateur pour procéder à l'annulation de la vente.

---

## 🔥 Types de Réchauds Commercialisés par ADES (`##`)

L'ADES commercialise plusieurs modèles de réchauds et poêles. Cette information est utile lors du remplissage du champ "Cluster" ou "Type de réchaud" pendant une vente.

| Type de Réchaud | Combustible   | Format / Description |
| :-------------- | :------------ | :------------------- |
| **OLI-c**       | Charbon       | Petit format         |
| **OLI-b**       | Bois          | Petit format         |
| **OLI-45c**     | Charbon       | Moyen format         |
| **OLI-45b**     | Bois          | Moyen format         |
| **OLI-60c**     | Charbon       | Grand format         |
| **OLI-60b**     | Bois          | Grand format         |
| **Box**         | Multifonction |                      |
| **Parabole**    | Solaire       | Réflecteur solaire   |

---
