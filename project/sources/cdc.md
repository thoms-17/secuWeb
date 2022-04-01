# Cahier des charges mybank.io

---

## Avant de commencer le projet

- Le projet est à réaliser par groupe de 1 ou 2
- La première étape du projet est de créer un dépot GitHub pour votre rendu et ajouter les droits en lecture à l'utilisateur github.com/lp1dev 
- Le rendu devra se faire sous forme de fichier docker-compose.yml et de conteneurs Docker fonctionnels

---

## Liste des tâches à réaliser

- Création d'un conteneur pour l'application basé sur alpine
- Intégration dans docker-compose
- Ajout de HTTPS via un reverse proxy NGINX
- Mise en place d'un pare-feu type fail2ban
- Audit des vulnérabilités de l'applicatif (manuel et automatisé)
- Reporting des vulnérabilités de l'application (cf section vulnérabilités)
- Fix des soucis de sécurité via NGINX et fail2ban

---

## Vulnérabilités

### Exemple

| Vulnérabilité | Injection SQL |
|:-----:|:------------:|
| Description | Le paramètre GET post_id de l'URL https://website.com/blog est utilisé par le back-end sans vérification de la preśence de caractères pouvant causer une injection SQL. | 
| Criticité | Critique |
| Exploitation | https://website.com/blog?id=1 UNION SELECT * FROM users |
| Remédiation | Ajouter une règle dans le pare-feu pour bloquer les requêtes contenant le mot clé UNION |
