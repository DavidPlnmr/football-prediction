# Journal de bord

Ce journal de bord a pour but de permettre de simplifier la rédaction du rapport final de stage de technicien. Le stage de technicien est un POC (proof of concept) du travail de diplôme de technicien. Il contiendra toutes les réflexions, les éléments techniques liés à votre travail, résumés des rencontres avec des enseignants, élèves, etc.

## Contenu

### 30.03.2021

Premier jour de stage. Début du POC

Contact par e-mail avec Monsieur Schmid pour être sûr du contenu du POC :

* Conception de la classe pour récupérer les données de l'API
* Design Pattern "Facade" qui permet de simplifier la communication entre l'API et le programme.
  * Permettra de garder la même façade si un jour l'API change

![Facade Analyse](./img/facadeAnalyse.jpg)

9h40 
Début de l'implémentation de la facade. Librairie requests python. Lorsqu'on appel le endpoint de l'API, on reçoit le contenu en byte ( ex : `b'Mon text'` ), il faut alors le convertir en string -> `content.decode("utf-8")`

10h00

Avancement dans les requêtes pour l'API. Création d'une classe ApiFacade qui contient une méthode `getAction(request_params)`. Les autres méthodes (comme par ex: `getH2H(first_team_name, second_team_name)`) appeleront la méthode `getAction` avec les paramètres spécifiques à chacune de ces méthodes.

```python
def getAction(self, request_params):
        response = requests.get('https://apiv2.apifootball.com/?APIkey={key}&{params}'.format(key=self.api_key, params=request_params))

        if response.status_code == 200: # Code 200 = OK. Healthy connection
            return response.content.decode('utf-8') # decode to get the content in string
        # TODO : VERIFICATION IF THE CODE IS NOT 200
```

Voici la méthode `getAction` en question.

```python
def getCountries(self):
        endpoint_action = "get_countries"
        return self.getAction('action={action}'.format(action=endpoint_action))
```

Et ce à quoi ressemble la méthode `getCountries()`. Cela permet de réduire considérablement le nombre de ligne de la façade et de rendre son code plus simple.

10h30

Ajout de la librairie `dotenv` au projet. Cela permet d'apporter une certaine sécurité sur la clé de mon API. Surtout lorsque l'on ne peut pas la réinitialiser.

