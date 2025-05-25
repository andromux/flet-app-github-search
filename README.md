
### Flet en Python crea un Apk android una interfaz moderna, responsiva y funcional

para buscar repositorios de GitHub relacionados con "Termux", y está pensado para ser una guía educativa para que los usuarios puedan crear su propia app. Vamos a desglosarlo por secciones para entender su funcionalidad y cómo podrías replicarla o modificarla.

## ¿Te gustó este repositorio?
_______________


<div align="center">

  <h3>¿Te gustó este repositorio?</h3>
  <p>¡Regálame una estrella o haz un fork si quieres contribuir!</p>

  <a href="https://github.com/andromux/flet-app-github-search/stargazers">
    <img src="https://img.shields.io/github/stars/andromux/flet-app-github-search?style=social" alt="GitHub Stars"/>
  </a>

  <a href="https://github.com/andromux/flet-app-github-search/fork">
    <img src="https://img.shields.io/github/forks/andromux/flet-app-github-search?style=social" alt="GitHub Forks"/>
  </a>

</div>

_______________
1. Estructura General

```bash
import flet as ft
import httpx
from datetime import datetime
```

`flet`: librería para crear interfaces gráficas responsivas con Python.

`httpx`: cliente HTTP para hacer peticiones a la API de GitHub.

`datetime`: para convertir y formatear fechas.



---

2. Clase GitHubRepo

```
class GitHubRepo:
    def __init__(self, repo_data):
```

Esta clase convierte los datos crudos del JSON de GitHub en un objeto organizado. Esto ayuda a manejar la información más fácilmente cuando se crea la UI.


---

3. Configuración de la página

```
page.title = "Termux GitHub Hunter"
page.theme_mode = ft.ThemeMode.DARK
```

Establece título, modo oscuro, color de fondo, scroll automático, y padding.

Esta sección define la base visual de la app.



---

4. AppBar personalizada con botones sociales

```
def setup_appbar():
```

Usa `ft.AppBar` para mostrar el nombre de la app y botones que abren redes sociales en el navegador.

Los íconos se cargan desde imágenes locales `(assets_dir="assets")`.



---

5. Contenedor de resultados con diseño responsive

```
repos_container = ft.ResponsiveRow(...)
```

Usa `ResponsiveRow`, que adapta el número de columnas en función del tamaño de pantalla.

Cada tarjeta de repositorio se adapta usando col={"xs": 12, "md": 6, "lg": 4}.



---

6. Formato de fecha y tamaño

```
def format_date(date_str):
def format_size(size_kb):
```

Convierte datos como "2023-11-24T23:00:00Z" a "24/11/2023".

Convierte KB a MB si es mayor de 1024.



---

7. Tarjeta interactiva de repositorio

```
def create_repo_card(repo: GitHubRepo): ...
```

Cada tarjeta tiene vista resumida y vista detallada.

Usa `AnimatedSwitcher` para cambiar entre ambas con animación SCALE.



---

8. Buscar repositorios en GitHub

```
def search_repos(term="termux", append=False):
```
Hace una petición a `https://api.github.com/search/repositories`.

Usa paginación (`page=1, 2...`) para cargar más resultados.

Controla si borra los resultados previos (append=False) o agrega más (append=True).



---

9. Buscador

```
search_field = ft.TextField(...)
search_btn = ft.ElevatedButton(...)
```

`Input` para que el usuario escriba su búsqueda.

El botón lanza `search_repos()` con el término ingresado.



---

10. Diseño responsive

```
ft.ResponsiveRow([search_field, search_btn], spacing=10)
```

Hace que los elementos se acomoden según el ancho de pantalla.

Gracias a las propiedades `col={"xs": 12, "md": 9}`, funciona perfecto en móviles y escritorio.

---

11. Ejecución

```
ft.app(target=main, assets_dir="assets")
```

Lanza la app y carga las imágenes sociales desde la carpeta assets.

---

¿Cómo puedes crear la tuya?

Paso a paso:

1. Piensa en una fuente de datos pública: usa una API como GitHub, YouTube, Reddit, etc.


2. Crea una clase que modele esos datos (GitHubRepo).


3. Diseña la interfaz con Flet:

Usa `TextField`, `ElevatedButton`, `Container`, `ResponsiveRow`.

Añade animaciones (`AnimatedSwitcher`) para interactividad.



4. Haz tu diseño responsive:

Usa `col={"xs": 12, "md": 6, "lg": 4}` en contenedores.



5. Agrega eventos con `on_click`, `on_submit`, y actualiza con `page.update()`.
