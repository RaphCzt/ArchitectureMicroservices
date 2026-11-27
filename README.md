# Todo API

API REST de gestion de tâches (todos), écrite en Python avec FastAPI.
Les données sont stockées en mémoire, donc elles sont perdues à chaque redémarrage.

## Structure

```
src/
├── src/
│   ├── main.py      # routes HTTP (FastAPI)
│   └── api.py       # modèles Pydantic et logique métier (stockage en mémoire)
├── openapi.yaml     # contrat de l'API
├── requirements.txt # dépendances figées
└── pyproject.toml   # projet uv
```

## Installation et lancement

Python 3.14 est requis.

Avec uv :

```bash
uv sync
uv run fastapi dev src/main.py
```

Avec pip :

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev src/main.py
```

L'API écoute sur http://127.0.0.1:8000. La documentation interactive est sur `/docs` (Swagger) et `/redoc`.

## Modèle Todo

| Champ         | Type                                     | Remarque                     |
|---------------|------------------------------------------|------------------------------|
| `id`          | UUID                                     | généré par le serveur        |
| `title`       | string (100 caractères max)              | obligatoire                  |
| `description` | string ou null                           |                              |
| `state`       | `"not done"`, `"in progress"`, `"done"`  | `"not done"` par défaut      |
| `tags`        | liste de strings                         | `[]` par défaut              |
| `created_at`  | datetime                                 | généré par le serveur        |

## Endpoints

| Méthode  | Route               | Rôle                                                  | Succès | Erreurs  |
|----------|---------------------|-------------------------------------------------------|--------|----------|
| `POST`   | `/todos`            | crée un todo                                          | 201    | 422      |
| `GET`    | `/todos`            | liste les todos, avec filtres `?tag=` et `?tags=a,b`  | 200    | -        |
| `GET`    | `/todos/search`     | recherche texte `?q=` dans le titre et la description, et filtre `?tag=` | 200 | - |
| `GET`    | `/todos/{id}`       | renvoie un todo                                       | 200    | 404, 422 |
| `PATCH`  | `/todos/{id}`       | modification partielle (champs envoyés seulement)     | 200    | 404, 422 |
| `PUT`    | `/todos/{id}`       | remplacement complet (`title` obligatoire)            | 200    | 404, 422 |
| `DELETE` | `/todos/{id}`       | supprime un todo, la réponse n'a pas de corps         | 204    | 404, 422 |

Les codes d'erreur :
- **404** : aucun todo ne porte cet id.
- **422** : la requête est invalide (id qui n'est pas un UUID, `title` absent ou trop long, `state` inconnu, `null` sur `title`, `state` ou `tags` dans un PATCH).

`?tag=x` garde les todos qui ont le tag `x`. `?tags=a,b` garde ceux qui ont **tous** les tags listés.

### Exemples

```bash
curl -X POST localhost:8000/todos -H 'content-type: application/json' \
     -d '{"title":"Courses","tags":["perso","urgent"]}'
curl "localhost:8000/todos?tags=perso,urgent"
curl "localhost:8000/todos/search?q=cours"
curl -X PATCH localhost:8000/todos/<id> -H 'content-type: application/json' -d '{"state":"done"}'
curl -X DELETE localhost:8000/todos/<id>
```

## Contrat OpenAPI

`openapi.yaml` est généré à partir du code. Si vous modifiez les routes, régénérez-le avec le serveur lancé :

```bash
curl -s localhost:8000/openapi.json | python -c "import sys,json,yaml; yaml.safe_dump(json.load(sys.stdin), sys.stdout, sort_keys=False, allow_unicode=True)" > openapi.yaml
```

Attention : cette commande écrase les réponses 404 et 204 qui ont été ajoutées à la main dans le fichier.

## Dépendances

`requirements.txt` fige les versions installées dans le venv. Pour le régénérer :

```bash
uv pip freeze | grep -v '^-e' > requirements.txt
```



