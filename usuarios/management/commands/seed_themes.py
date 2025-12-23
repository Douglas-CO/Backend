import json
from pathlib import Path
from django.core.management.base import BaseCommand
from usuarios.models.theme_models import Theme
from usuarios.repository.theme_repository import ThemeRepository


class Command(BaseCommand):
    help = "Seed inicial de Themes desde theme_seed.jsonc"

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        file_path = base_dir / "seed" / "usuarios" / "theme_seed.jsonc"

        self.stdout.write(f"Cargando seed desde: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            # Ignorar comentarios en JSONC
            content = f.read()
            # Quitar líneas que empiezan con // para comentarios
            json_content = "\n".join(
                [line for line in content.splitlines() if not line.strip().startswith("//")])
            data = json.loads(json_content)

        for theme_data in data:
            code = theme_data["code"]
            # Verificar si ya existe
            existing = Theme.objects.filter(code=code).first()
            if existing:
                self.stdout.write(f"Theme {code} ya existe, saltando...")
                continue

            # Crear theme
            ThemeRepository.crear_theme(
                name=theme_data["name"],
                code=theme_data["code"],
                description=theme_data["description"],
                state=theme_data.get("state", True),
                palette=theme_data["pallete"]
            )
            self.stdout.write(f"Theme {code} creado correctamente.")

        self.stdout.write(self.style.SUCCESS("Seed de Themes completado!"))
