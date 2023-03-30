# Voici la procédure pour lancer la pipeline dans Azure DevOps :

## Pré-requis :

    Un accès au repository DevOps "Brief-8"
    Un accès au pipeline "Brief-8" dans l'organisation "nicolasmarty" sur Azure DevOps avec un compte Azure

## Première étape : Lancement de la pipeline
Lorsqu'un push est effectué sur le repository, la pipeline de déploiement de l'application de vote se lance automatiquement. Il est cependant important de vérifier que le numéro de version dans le code de l'application a été modifié, car si ce n'est pas le cas, la pipeline ne mettra pas à jour le container, ni sur le registry ni sur l'AKS.

## Deuxième étape : Validation manuelle
Une fois que tous les tests ont été effectués par la pipeline, un email est envoyé au responsable de la pipeline (Nicolas MARTY) pour une validation manuelle afin de finaliser le déploiement en production.

Voici les étapes à suivre pour valider la pipeline manuellement :

    Ouvrir un navigateur web de votre choix et accéder à l'adresse https://dev.azure.com/nicolasmarty
    Se connecter avec votre compte Azure
    Cliquer sur le projet "Brief-8"
    Dans le menu de gauche, cliquer sur "Pipelines", puis sur "Pipelines" juste en dessous
    Cliquer sur le pipeline "recently run pipelines" avec le symbole bleu tournant
    Dans la présentation suivante, cliquer sur le pipeline avec le symbole bleu et la description "Update main.py"

Une fois la validation manuelle effectuée, la pipeline déploiera automatiquement l'application de vote en production.


---
page_type: sample
languages:
  - python
products:
  - azure
  - azure-redis-cache
description: "This sample creates a multi-container application in an Azure Kubernetes Service (AKS) cluster."
---

# Azure Voting App

This sample creates a multi-container application in an Azure Kubernetes Service (AKS) cluster. The application interface has been built using Python / Flask. The data component is using Redis.

To walk through a quick deployment of this application, see the AKS [quick start](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough?WT.mc_id=none-github-nepeters).

To walk through a complete experience where this code is packaged into container images, uploaded to Azure Container Registry, and then run in and AKS cluster, see the [AKS tutorials](https://docs.microsoft.com/en-us/azure/aks/tutorial-kubernetes-prepare-app?WT.mc_id=none-github-nepeters).

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
---
# Explications de fonctionnement du pipeline

Ce pipeline Azure DevOps est configuré pour déployer une application sur un cluster Kubernetes. Il est composé de plusieurs étapes pour construire et déployer l'application, effectuer des tests de performance, et potentiellement effectuer un rollback en cas d'échec des tests.

    Étape "docker" : Cette étape construit et pousse une image Docker contenant l'application vers un registre Docker. Elle récupère les versions actuelles et précédentes de l'image, met à jour le fichier de manifeste Kubernetes avec la nouvelle version, puis construit et pousse l'image si la nouvelle version est différente de l'ancienne.

    Étape "QAL_Deployment" : Cette étape déploie l'application sur un environnement de qualité (QAL). Elle vérifie le déploiement, effectue des tests de charge et compte le nombre de pods déployés. Si le nombre de pods n'est pas égal à 2, le déploiement QAL est supprimé.

    Étape "Deploy_canary" : Cette étape déploie une version Canary de l'application dans l'environnement de production (Prod) avec 30 % du trafic dirigé vers cette version. Cette étape permet de vérifier que la nouvelle version fonctionne correctement avec un sous-ensemble d'utilisateurs avant de la déployer complètement.

    Étape "ManualIntervention" : Cette étape attend une validation manuelle avant de poursuivre. Un utilisateur doit confirmer que la configuration est correcte et que le pipeline peut continuer.

    Étape "DeployOnProd" : Cette étape déploie l'application sur l'environnement de production et supprime la version Canary. Si le déploiement réussit, un message indiquant que le déploiement en production est OK est affiché.

    Étape "PerformanceTest" : Cette étape effectue des tests de performance sur l'environnement de production. Elle vérifie le nombre de pods de production, attend les résultats des tests de charge et affiche un message indiquant que les tests de performance sont terminés.

    Étape "Rollback" : Cette étape est exécutée uniquement si les tests de performance échouent. Elle effectue un rollback du déploiement en production à la version précédente et affiche un message indiquant que le rollback est terminé.

Le pipeline utilise plusieurs tâches pour interagir avec Kubernetes, gérer les images Docker, exécuter des scripts Bash et des commandes en ligne, et attendre une intervention manuelle. 
