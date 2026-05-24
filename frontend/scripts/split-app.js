const fs = require("fs");
const path = require("path");

const src = fs.readFileSync(path.join(__dirname, "../js/app.js"), "utf8");
const lines = src.split("\n");

function write(filePath, content) {
    fs.mkdirSync(path.dirname(filePath), { recursive: true });
    fs.writeFileSync(filePath, content);
}

const root = path.join(__dirname, "..");

write(
    path.join(root, "app/data/state.js"),
    "(function () {\n    window.AppData = function () {\n" +
        lines.slice(31, 206).join("\n") +
        "\n    };\n})();\n"
);

write(
    path.join(root, "app/computed/index.js"),
    "(function () {\n    window.AppComputed = {\n" +
        lines
            .slice(210, 279)
            .map(function (l) {
                return l.replace(/^            /, "        ");
            })
            .join("\n") +
        "\n    };\n})();\n"
);

write(
    path.join(root, "app/lifecycle/mounted.js"),
    "(function () {\n    window.AppMounted = function () {\n" +
        lines
            .slice(282, 300)
            .map(function (l) {
                return l.replace(/^            /, "        ");
            })
            .join("\n") +
        "\n    };\n})();\n"
);

write(
    path.join(root, "app/lifecycle/watch.js"),
    "(function () {\n    window.AppWatch = {\n" +
        lines
            .slice(1882, 1887)
            .map(function (l) {
                return l.replace(/^            /, "        ");
            })
            .join("\n") +
        "\n    };\n})();\n"
);

const methodRanges = [
    ["routing", 303, 474],
    ["auth", 475, 528],
    ["genres", 529, 573],
    ["movies", 575, 735],
    ["movie_details", 737, 820],
    ["reviews", 822, 1156],
    ["profile", 1159, 1335],
    ["favorites", 1336, 1453],
    ["watch_history", 1455, 1603],
    ["admin_genres", 1605, 1696],
    ["admin_movies", 1698, 1874],
    ["admin_genres_confirm", 1802, 1834],
    ["utils", 1082, 1095],
    ["utils_toast", 1875, 1879],
];

function toGlobal(name) {
    return (
        "AppMethods" +
        name
            .split("_")
            .map(function (p) {
                return p.charAt(0).toUpperCase() + p.slice(1);
            })
            .join("")
    );
}

const globals = [];
methodRanges.forEach(function ([name, start, end]) {
    const globalName = toGlobal(name);
    globals.push("window." + globalName);
    const body = lines.slice(start - 1, end).join("\n");
    write(
        path.join(root, "app/services/methods", name + ".js"),
        "(function () {\n    window." + globalName + " = {\n" + body + "\n    };\n})();\n"
    );
});

write(
    path.join(root, "app/services/methods/index.js"),
    "(function () {\n    window.AppMethods = Object.assign(\n        {},\n        " +
        globals.join(",\n        ") +
        "\n    );\n})();\n"
);

console.log("Split complete");
