### Rapport de Débogage

---

#### Présentation de l'application

L'application développée est une API de traduction basée sur FastAPI, destinée à traduire du texte entre plusieurs langues en utilisant des modèles de traduction fournis par la bibliothèque `transformers` de Hugging Face. L'application permet aux utilisateurs de soumettre du texte via des requêtes HTTP POST, spécifiant la langue source et cible. En fonction de la version de la traduction spécifiée, l'API retourne le texte traduit. L'API est conçue pour être extensible, et prend actuellement en charge les traductions de `français` vers `anglais` et de `anglais` vers `français`.

#### Présentation de l'incident technique

Lors de l'utilisation de l'API, une exception de type `UnboundLocalError` a été rencontrée. Cet incident est survenu lors de la tentative de traduction d'un texte de l'anglais vers le français. L'erreur a interrompu l'exécution du programme, rendant l'API incapable de traiter les requêtes et de renvoyer les traductions attendues.

#### Présentez le message d'erreur en console et expliquez-le

Le message d'erreur observé était le suivant :

```
UnboundLocalError: local variable 'translator' referenced before assignment
```

Ce message indique que la variable `translator` a été référencée avant d'avoir été initialisée. Dans le contexte du code, cette erreur se produit lorsque le chemin d'exécution du code ne rencontre pas la condition qui initialiserait la variable `translator`. Par conséquent, lorsqu'il essaie de l'utiliser, la variable n'a pas encore été définie, ce qui provoque l'erreur.

#### Expliquez les recherches faites pour résoudre l'incident technique

Pour résoudre l'incident, une analyse approfondie du flux du programme a été réalisée. Le code a été débogué en utilisant Visual Studio Code (VSCode). Des points d'arrêt ont été placés à des endroits stratégiques pour suivre l'exécution du code. En examinant les valeurs des variables au moment où l'erreur se produisait, il est apparu que la condition d'initialisation de la variable `translator` ne couvrait pas tous les cas d'utilisation, notamment le cas où la traduction était demandée de l'anglais vers le français (`en >> fr`).

#### Expliquez la correction apportée et le test de validation

La correction a consisté à :

1. **Initialiser la variable `translator` à `None`** au début de la fonction `traduire` pour éviter toute référence avant assignation.
2. **Ajouter une condition pour gérer la version `en >> fr`** en utilisant le modèle approprié, déjà défini dans la variable `VERSIONS` du fichier `parametres.py`.
3. **Ajouter un contrôle d'erreur** pour lever une exception explicite si aucune version de traduction valide n'était trouvée.

Voici la correction apportée au code :

```python
def traduire(prompt: Prompt):
    translator = None  # Initialisation à None

    if prompt.version == VERSIONS[0]:  # Cas de la traduction 'fr >> en'
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")
    elif prompt.version == VERSIONS[1]:  # Cas de la traduction 'en >> fr'
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")

    if translator is not None:
        prompt.traduction = translator(prompt.atraduire)
    else:
        raise ValueError(f"Aucun modèle trouvé pour la version: {prompt.version}")
    
    return prompt
```

Après la correction, le code a été testé en utilisant le débogueur de VSCode. Les tests ont confirmé que les traductions fonctionnaient correctement pour les deux versions spécifiées dans `VERSIONS`, à savoir `fr >> en` et `en >> fr`.

#### Expliquez le versionnage de la correction dans Git et le déploiement sur GitHub

Une fois la correction validée, le code a été versionné en utilisant Git. Les étapes suivantes ont été suivies pour gérer le versionnage et le déploiement sur GitHub :

1. **Création d'une nouvelle branche** pour la correction :
   ```bash
   git checkout -b fix/translation-unboundlocalerror
   ```

2. **Ajout des modifications** à l'index :
   ```bash
   git add src/model/nlp.py
   ```

3. **Validation des modifications** avec un message descriptif :
   ```bash
   git commit -m "Fix UnboundLocalError in translation function by initializing translator for all versions"
   ```

4. **Fusion de la branche de correction** dans la branche principale après revue de code :
   ```bash
   git checkout main
   git merge fix/translation-unboundlocalerror
   ```

5. **Déploiement des modifications** sur GitHub :
   ```bash
   git push origin main
   ```

#### Documentation sur le dashboard

Pour le suivi des performances et la surveillance de l'API, un dashboard a été conçu pour fournir des métriques clés. Ce dashboard utilise des technologies comme **Grafana** et **Prometheus** pour collecter, stocker et visualiser les données.

- **Choix des métriques** : Les métriques surveillées incluent le temps de réponse de l'API, le taux d'erreur, l'utilisation de la mémoire et du CPU, ainsi que les débits de requêtes par seconde. Ces métriques sont essentielles pour s'assurer que l'API fonctionne correctement et pour détecter toute dégradation de performance.

- **Choix de la technologie** : Grafana a été choisi pour sa flexibilité et son intégration facile avec Prometheus. Prometheus est utilisé pour collecter et agréger les données, tandis que Grafana est utilisé pour créer des visualisations en temps réel.

- **Mise à jour des indicateurs** : Les indicateurs sont mis à jour en temps réel grâce à Prometheus qui scrute l'API à intervalles réguliers. Les alertes sont configurées pour notifier l'équipe DevOps en cas d'anomalies, comme une augmentation du taux d'erreur ou une latence excessive.

- **Alertes** : Des alertes ont été configurées dans Grafana pour déclencher des notifications via Slack et email en cas de dépassement des seuils définis pour chaque métrique critique. Cela garantit une réponse rapide aux incidents potentiels.

---

Ce rapport présente un aperçu complet du processus de débogage, de la correction, du test, du versionnage et du déploiement de l'application, ainsi que de la mise en place du monitoring pour assurer un suivi continu des performances.

-------------------------------------------------------------------------------


# Rapport de Correction d'un Incident Technique dans une Application FastAPI

## Présentation de l'application

L'application développée est une API de traduction utilisant **FastAPI** pour la gestion du backend et **Streamlit** pour l'interface utilisateur. L'API permet aux utilisateurs de soumettre des textes à traduire, d'obtenir les traductions et de gérer les utilisateurs. Le projet est structuré en plusieurs modules, comprenant la gestion des connexions à la base de données, les opérations CRUD (Create, Read, Update, Delete) sur les données de traduction, et l'authentification des utilisateurs.

L'interface Streamlit interagit avec l'API FastAPI, affichant les résultats des traductions, permettant aux utilisateurs de se connecter, et affichant divers tableaux de bord liés aux opérations de traduction.

## Présentation de l'incident technique

Un incident technique est survenu lors de l'appel de l'API pour sauvegarder un prompt de traduction. Lors de l'exécution de la méthode `sauvegarder_prompt`, un message d'erreur a été retourné en console, empêchant l'enregistrement des données dans la base de données MySQL.

### Message d'erreur en console

Le message d'erreur suivant a été affiché :

```
MySQLInterfaceError: Python type list cannot be converted
```

Cette erreur se produisait dans la méthode `sauvegarder_prompt` de la classe `Service_Traducteur` lorsque le script tentait d'insérer un enregistrement dans la table `prompts` de la base de données.

### Explication du message d'erreur

L'erreur `MySQLInterfaceError: Python type list cannot be converted` indique que l'application tentait de passer une liste Python à une requête SQL, alors que MySQL s'attendait à des types de données scalaires (tels que des chaînes de caractères ou des entiers). En Python, les paramètres d'une requête SQL doivent être passés sous forme de tuple, mais dans ce cas, une liste avait été utilisée à la place.

## Recherches faites pour résoudre l'incident technique

Pour résoudre cet incident, plusieurs étapes de débogage ont été entreprises :

1. **Inspection du Code Source :** Le code source de la méthode `sauvegarder_prompt` a été examiné pour identifier la manière dont les données étaient passées à la requête SQL.
2. **Recherche sur la Gestion des Paramètres MySQL en Python :** Des recherches ont été effectuées sur les bonnes pratiques de passage de paramètres aux requêtes SQL dans MySQL à l'aide de Python, confirmant que les tuples devaient être utilisés au lieu des listes.
3. **Utilisation du Débogueur de VSCode :** Le débogueur intégré de VSCode a été utilisé pour inspecter les valeurs contenues dans la variable `values` avant l'exécution de la requête SQL, permettant ainsi de confirmer la nature de l'erreur.

## Correction apportée et test de validation

### Correction apportée

Les corrections suivantes ont été appliquées au code :

- **Changement des Listes en Tuples :** Les listes utilisées pour passer les paramètres des requêtes SQL ont été remplacées par des tuples, comme suit :

  **Ancienne version :**
  ```python
  values = [prompt.atraduire, prompt.traduction, prompt.version, prompt.utilisateur]
  ```

  **Nouvelle version :**
  ```python
  values = (prompt.atraduire, prompt.traduction, prompt.version, prompt.utilisateur)
  ```

- **Gestion des Erreurs :** La méthode a été modifiée pour inclure un bloc `try-except-finally`, garantissant que les erreurs sont capturées et gérées proprement, et que la transaction est annulée en cas de problème :

  ```python
  try:
      cls.cursor.execute(query, values)
      cls.bdd.commit()
  except Exception as e:
      print(f"Erreur lors de l'insertion du prompt : {e}")
      cls.bdd.rollback()
  finally:
      cls.fermer_connexion()
  ```

### Test de validation

Après la correction, l'application a été redémarrée et les tests suivants ont été effectués :

1. **Soumission d'un prompt de traduction via l'API FastAPI :** L'appel à la méthode `sauvegarder_prompt` a été réessayé avec succès, confirmant que le prompt est bien enregistré dans la base de données.
2. **Validation des données dans MySQL :** Une vérification dans la base de données a confirmé que les données sont correctement enregistrées dans la table `prompts`.
3. **Test complet de l'application Streamlit :** L'interface utilisateur a également été testée pour s'assurer qu'elle interagit correctement avec l'API, sans générer d'erreurs.

## Versionnage de la correction dans Git et déploiement sur GitHub

### Versionnage de la correction

Les modifications apportées au code ont été versionnées en suivant les étapes suivantes :

1. **Commit des changements :** Tous les fichiers modifiés ont été ajoutés à un nouveau commit avec un message explicite décrivant la nature de la correction.
   ```bash
   git add .
   git commit -m "Correction du bug MySQLInterfaceError en remplaçant les listes par des tuples pour les valeurs SQL"
   ```

2. **Push vers le dépôt GitHub :** Le commit a été poussé vers le dépôt GitHub.
   ```bash
   git push origin main
   ```

### Déploiement sur GitHub

Après avoir poussé les changements sur GitHub, le projet a été déployé en utilisant un workflow CI/CD (par exemple, GitHub Actions). Ce processus assure que les modifications sont automatiquement testées et déployées sur l'environnement de production, garantissant que l'application est à jour avec les dernières corrections.

## Documentation sur le Dashboard

### Choix des métriques

Le dashboard de l'application, développé avec Streamlit, inclut plusieurs métriques importantes pour surveiller les performances et l'usage de l'API, telles que :

- **Nombre de traductions effectuées** : Mesure l'activité principale de l'application.
- **Temps moyen de réponse de l'API** : Indicateur clé des performances.
- **Taux de réussite des traductions** : Pour surveiller les erreurs dans le processus de traduction.

### Choix de la technologie

**Streamlit** a été choisi pour sa simplicité et sa rapidité de développement. Il permet de créer des interfaces interactives pour les utilisateurs sans nécessiter de compétences avancées en front-end. De plus, il s'intègre bien avec Python, facilitant l'accès aux données directement depuis l'application backend.

### Mise à jour des indicateurs et alertes

Les indicateurs sont mis à jour en temps réel en utilisant des appels API à FastAPI pour récupérer les dernières données. Les alertes sont configurées pour notifier les administrateurs en cas d'anomalies, telles qu'un temps de réponse élevé ou une baisse du taux de réussite des traductions.

Ces fonctionnalités assurent une surveillance continue de l'application et permettent une réaction rapide en cas de problème, garantissant ainsi une qualité de service optimale pour les utilisateurs.