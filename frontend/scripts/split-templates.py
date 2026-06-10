import os

ROOT = os.path.join(os.path.dirname(__file__), "..")
TPL_DIR = os.path.join(ROOT, "app", "ui", "templates")

# Порядок сборки шаблона (имена отражают содержимое секций)
TEMPLATE_PARTS = [
    "layout_navbar_auth_catalog_genres.html",
    "view_genres_movies_list.html",
    "view_movie_details.html",
    "view_movie_reviews_favorites_history.html",
    "view_history_my_reviews_admin_genres.html",
    "view_admin_movies_profile.html",
    "profile_modals_confirmations.html",
    "modals_admin_toast.html",
]


def write_manifest():
    manifest = "window.AppTemplateParts = " + repr(TEMPLATE_PARTS) + ";\n"
    with open(
        os.path.join(ROOT, "app", "ui", "template_manifest.js"), "w", encoding="utf-8"
    ) as f:
        f.write(manifest)


def split_from_monolithic(source_path, start_line=19, end_line=1479, chunk_size=200):
    """Разбивает монолитный HTML-шаблон на части (для повторной генерации)."""
    with open(source_path, encoding="utf-8") as f:
        lines = f.readlines()

    template_lines = lines[start_line - 1 : end_line - 1]
    os.makedirs(TPL_DIR, exist_ok=True)

    if len(TEMPLATE_PARTS) * chunk_size < len(template_lines):
        raise SystemExit(
            f"Нужно {len(template_lines) // chunk_size + 1} частей, в TEMPLATE_PARTS — {len(TEMPLATE_PARTS)}"
        )

    for i, name in enumerate(TEMPLATE_PARTS):
        chunk = template_lines[i * chunk_size : (i + 1) * chunk_size]
        with open(os.path.join(TPL_DIR, name), "w", encoding="utf-8") as f:
            f.writelines(chunk)

    write_manifest()
    print(f"Created {len(TEMPLATE_PARTS)} template parts")


if __name__ == "__main__":
    monolith = os.path.join(ROOT, "_template_monolith.html")
    if os.path.isfile(monolith):
        split_from_monolithic(monolith)
    else:
        write_manifest()
        print("Manifest updated (no _template_monolith.html to split)")
