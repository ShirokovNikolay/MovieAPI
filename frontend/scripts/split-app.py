import os

ROOT = os.path.join(os.path.dirname(__file__), "..")
SRC = os.path.join(ROOT, "js", "app.js")

with open(SRC, encoding="utf-8") as f:
    lines = f.readlines()


def write(rel_path, content):
    path = os.path.join(ROOT, rel_path.replace("/", os.sep))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


write(
    "app/data/state.js",
    "(function () {\n    window.AppData = function () {\n"
    + "".join(lines[31:206])
    + "    };\n})();\n",
)

computed = "".join(
    line.replace("            ", "        ", 1) for line in lines[209:279]
)
write(
    "app/computed/index.js",
    "(function () {\n    window.AppComputed = {\n" + computed + "    };\n})();\n",
)

mounted = "".join(
    line.replace("            ", "        ", 1) for line in lines[281:300]
)
write(
    "app/lifecycle/mounted.js",
    "(function () {\n    window.AppMounted = function () {\n" + mounted + "    };\n})();\n",
)

watch = "".join(
    line.replace("            ", "        ", 1) for line in lines[1880:1887]
)
write(
    "app/lifecycle/watch.js",
    "(function () {\n    window.AppWatch = {\n" + watch + "    };\n})();\n",
)

method_ranges = [
    ("routing", 303, 474),
    ("auth", 475, 528),
    ("genres", 529, 573),
    ("movies", 575, 735),
    ("movie_details", 737, 820),
    ("reviews", 822, 1156),
    ("profile", 1159, 1335),
    ("favorites", 1336, 1453),
    ("watch_history", 1455, 1603),
    ("admin_genres", 1605, 1696),
    ("admin_movies", 1698, 1874),
    ("admin_genres_confirm", 1802, 1834),
    ("utils", 1082, 1095),
    ("utils_toast", 1875, 1879),
]


def to_global(name):
    parts = name.split("_")
    return "AppMethods" + "".join(p.capitalize() for p in parts)


globals_list = []
for name, start, end in method_ranges:
    global_name = to_global(name)
    globals_list.append(f"window.{global_name}")
    body = "".join(lines[start - 1 : end])
    write(
        f"app/services/methods/{name}.js",
        f"(function () {{\n    window.{global_name} = {{\n{body}    }};\n}})();\n",
    )

assign = ",\n        ".join(globals_list)
write(
    "app/services/methods/index.js",
    f"(function () {{\n    window.AppMethods = Object.assign(\n        {{}},\n        {assign}\n    );\n}})();\n",
)

print("Split complete")
