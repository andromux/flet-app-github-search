import flet as ft
import httpx
import threading
from datetime import datetime

class GitHubRepo:
    def __init__(self, repo_data):
        self.name = repo_data.get('name', 'N/A')
        self.full_name = repo_data.get('full_name', 'N/A')
        self.description = repo_data.get('description', 'No description available')
        self.stars = repo_data.get('stargazers_count', 0)
        self.forks = repo_data.get('forks_count', 0)
        self.language = repo_data.get('language', 'Unknown')
        self.html_url = repo_data.get('html_url', '')
        self.updated_at = repo_data.get('updated_at', '')
        self.size = repo_data.get('size', 0)

def main(page: ft.Page):
    page.title = "Termux GitHub Hunter"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.BLACK
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    current_query = "termux hacking"
    PER_PAGE = 5
    current_page = [1]  # lista para acceso desde el hilo

    def setup_appbar():
        def social_button(image, tooltip, url):
            return ft.IconButton(
                content=ft.Image(src=image, width=24, height=24),
                tooltip=tooltip,
                on_click=lambda e: page.launch_url(url),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                    side=ft.BorderSide(1, ft.Colors.BLUE),
                    bgcolor=ft.Colors.TRANSPARENT,
                )
            )

        page.appbar = ft.AppBar(
            title=ft.Text("Termux GitHub Hunter", color=ft.Colors.GREEN_400),
            center_title=True,
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            actions=[
                social_button("youtube.png", "YouTube", "https://youtube.com/@Retired64"),
                social_button("github.png", "GitHub", "https://github.com/Retired64"),
                social_button("telegram.png", "Telegram", "https://t.me/yourchannel"),
                social_button("web.png", "Web", "https://www.andromux.org"),
            ]
        )

    setup_appbar()

    repos_container = ft.ResponsiveRow(run_spacing=20, spacing=20)
    load_more_container = ft.Container()
    repos_container.controls.append(load_more_container)

    def format_date(date_str):
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00')).strftime('%d/%m/%Y')
        except:
            return 'N/A'

    def format_size(size_kb):
        return f"{size_kb} KB" if size_kb < 1024 else f"{size_kb // 1024:.1f} MB"

    def create_repo_card(repo: GitHubRepo):
        summary = ft.Column([
            ft.Text(repo.name, size=16, weight="bold", color=ft.Colors.GREEN_400),
            ft.Text(repo.description or "No description", color=ft.Colors.WHITE70, max_lines=2),
            ft.Row([
                ft.Icon(ft.Icons.STAR, color=ft.Colors.YELLOW),
                ft.Text(str(repo.stars), color=ft.Colors.YELLOW),
                ft.Icon(ft.Icons.CALL_SPLIT, color=ft.Colors.BLUE),
                ft.Text(str(repo.forks), color=ft.Colors.BLUE),
            ], spacing=5),
        ])

        details = ft.Column([
            ft.Text(f"📂 Full name: {repo.full_name}", size=12, color=ft.Colors.WHITE),
            ft.Text(f"🌐 Lenguaje: {repo.language}", size=12, color=ft.Colors.WHITE),
            ft.Text(f"🕒 Última actualización: {format_date(repo.updated_at)}", size=12, color=ft.Colors.WHITE),
            ft.Text(f"🗃️ Tamaño: {format_size(repo.size)}", size=12, color=ft.Colors.WHITE),
            ft.ElevatedButton("Ver en GitHub", url=repo.html_url, icon=ft.Icons.OPEN_IN_NEW, style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN_800, color=ft.Colors.WHITE))
        ])

        switcher = ft.AnimatedSwitcher(
            content=summary,
            transition=ft.AnimatedSwitcherTransition.SCALE,
            duration=500
        )

        def toggle_info(e):
            switcher.content = details if switcher.content == summary else summary
            switcher.update()

        return ft.Container(
            content=ft.Column([
                switcher,
                ft.ElevatedButton("🧪 + info", on_click=toggle_info, style=ft.ButtonStyle(
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE), color=ft.Colors.GREEN_400))
            ]),
            padding=15,
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
            border_radius=15,
            col={"xs": 12, "md": 6, "lg": 4}
        )

    def load_more():
        load_more_container.content = ft.Container(
            content=ft.Image(src="loading.gif", width=80, height=80),
            alignment=ft.alignment.center,
        )
        load_more_container.update()

        def thread_job():
            url = "https://api.github.com/search/repositories"
            params = {
                'q': current_query,
                'sort': 'stars',
                'order': 'desc',
                'per_page': PER_PAGE,
                'page': current_page[0]
            }

            try:
                with httpx.Client(timeout=15.0) as client:
                    res = client.get(url, params=params)
                    items = res.json().get('items', [])

                    for repo_data in items:
                        repo = GitHubRepo(repo_data)
                        repos_container.controls.insert(-1, create_repo_card(repo))

                    current_page[0] += 1

                    if len(items) < PER_PAGE:
                        load_more_container.content = None
                        page.snack_bar = ft.SnackBar(
                            content=ft.Text("🚫 No hay más resultados."),
                            bgcolor=ft.Colors.RED_900
                        )
                        page.snack_bar.open = True
                    else:
                        load_more_container.content = ft.ElevatedButton(
                            "🔽 Cargar más",
                            icon=ft.Icons.MORE_HORIZ,
                            on_click=lambda e: load_more(),
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.BLUE_700,
                                color=ft.Colors.WHITE,
                                elevation=5,
                                shape=ft.RoundedRectangleBorder(radius=8),
                                padding=ft.padding.symmetric(horizontal=20, vertical=12)
                            )
                        )

                    page.update()

            except Exception as e:
                load_more_container.content = ft.Text(f"Error: {str(e)}", color=ft.Colors.RED)
                page.update()

        threading.Thread(target=thread_job).start()

    def reset_search(term):
        current_query = term
        current_page[0] = 1
        repos_container.controls.clear()
        repos_container.controls.append(load_more_container)
        load_more()

    search_field = ft.TextField(
        label="🔍 Buscar en GitHub",
        hint_text="termux hacking, shell, tools...",
        on_submit=lambda e: reset_search(search_field.value),
        border_radius=10,
        col={"xs": 12, "md": 9}
    )

    search_btn = ft.ElevatedButton(
        "Buscar", icon=ft.Icons.SEARCH,
        on_click=lambda e: reset_search(search_field.value),
        style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_900, color=ft.Colors.WHITE),
        col={"xs": 12, "md": 3}
    )

    page.add(
        ft.Column([
            ft.ResponsiveRow([search_field, search_btn], spacing=10),
            repos_container
        ])
    )

    reset_search(current_query)

ft.app(target=main, assets_dir="assets")
