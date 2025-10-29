# 🔒 Authentification de l'Application Lemadio

Ce document décrit le processus de connexion, d'obtention et de réinitialisation des identifiants pour l'application mobile "Lemadio".

---

## 🔑 Fonctionnement de la Connexion (`##`)

### Connexion Initiale (Nécessite Internet)

La **toute première connexion** à l'application Lemadio nécessite obligatoirement une **connexion Internet** active.

- **Action :** L'application valide le Nom d'utilisateur et le Mot de passe auprès du serveur.
- **Résultat :** Une fois réussie, le nom d'utilisateur est enregistré localement sur l'appareil.

### Connexions Ultérieures (Mode Hors-Ligne Possible)

Après la première authentification réussie en ligne, les connexions suivantes peuvent être effectuées **hors ligne**.

- **Saisie :** Le vendeur doit saisir uniquement son **Mot de passe**. Le Nom d'utilisateur est pré-rempli.
- **Restriction :** Chaque instance de l'application est **liée à un seul compte vendeur**. Toute tentative de connexion avec un autre compte après la première connexion réussie est **bloquée** localement.

---

## 🆔 Gestion des Identifiants (`##`)

### Qui fournit mon Nom d'utilisateur et mon Mot de passe ?

Vos identifiants de connexion (Nom d'utilisateur et Mot de passe) sont fournis par l'**équipe IT** de l'administrateur.

### Quel est mon format de Nom d'utilisateur ?

Le Nom d'utilisateur correspond généralement au nom de votre centre de vente.

- **Exemple :** Pour le centre de vente de Fianarantsoa, le Nom d'utilisateur est `Vente Fianarantsoa`.

---

## 🔄 Procédure de Mot de Passe Oublié (`##`)

### Comment réinitialiser mon mot de passe Lemadio ?

En cas d'oubli de mot de passe, suivez la procédure de réinitialisation :

1.  Sur la page d'authentification, cliquez sur le lien **« Mot de passe oublié ? »**.
2.  Dans la fenêtre contextuelle qui s'ouvre :
    - Sélectionnez votre **centre de vente**.
    - Saisissez votre **nouveau mot de passe** souhaité.
3.  Validez la demande.
4.  Le système envoie automatiquement un **code de confirmation** à l'administrateur (équipe IT) par e-mail.
5.  **Action requise :** **Contactez l'administrateur (équipe IT)** pour obtenir rapidement ce code de confirmation.
6.  L'application vous dirigera vers une nouvelle fenêtre pour **saisir le code** et finaliser la modification du mot de passe.

> **⚠️ AVERTISSEMENT :** Le code de confirmation n'est valide que pendant **10 minutes**.

---

## 🔍 Éléments de la Page d'Authentification (Référence) (`##`)

Pour vous orienter sur la page de connexion, voici les éléments clés :

- **Logo ADES :** Sert d'identification visuelle de l'application (en haut de la page).
- **Champ « Nom d’utilisateur » :** Sert à entrer votre identifiant (ex: `Vente Fianarantsoa`).
- **Champ « Mot de passe » :** Champ sécurisé. Une icône **œil** à droite permet d'afficher/masquer le texte saisi.
- **Bouton « Se connecter » :** Lance le processus d'authentification.
- **Lien « Mot de passe oublié ? » :** Lance la procédure de réinitialisation du mot de passe (voir section précédente).

---

## ✅ Étapes Simples pour se Connecter (`##`)

Pour une connexion standard :

1.  **Saisir le Nom d'utilisateur :** Entrez l'identifiant de votre centre de vente (seulement lors de la première connexion en ligne ou après une déconnexion complète).
2.  **Saisir le Mot de passe :** Entrez votre mot de passe personnel dans le champ sécurisé.
3.  **Cliquer :** Cliquez sur le bouton **« Se connecter »**.

---

## 🚪 Déconnexion de l'Application (`##`)

### Comment se Déconnecter du Compte Lemadio ?

Pour quitter votre session de vendeur de l'application :

1.  Localisez et cliquez sur l'icône des **trois points verticaux** (le menu) en haut à droite de l'entête (près de votre Nom d'utilisateur).
2.  Dans le menu déroulant, cliquez sur l'option **"Déconnexion"**.
3.  Une fenêtre de confirmation apparaît. Cliquez sur **"Oui"** pour valider la déconnexion.
4.  Vous serez immédiatement redirigé vers la **page d'authentification** (login).

---
