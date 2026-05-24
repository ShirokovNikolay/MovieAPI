(function () {
    var mountEl = document.getElementById("app");

    function showBootError(html) {
        if (mountEl) {
            mountEl.innerHTML = html;
        }
    }

    if (typeof Vue === "undefined") {
        showBootError(
            '<div class="container py-5 text-light"><p class="alert alert-danger">Не удалось загрузить Vue.js. Проверьте доступ к сети и к CDN (cdn.jsdelivr.net).</p></div>'
        );
        return;
    }
    if (!mountEl) {
        showBootError(
            '<div class="container py-5 text-light"><p class="alert alert-danger">Не найден корень приложения (#app).</p></div>'
        );
        return;
    }

    var createApp = Vue.createApp;

    function loadTemplate() {
        var parts = window.AppTemplateParts || [];
        if (!parts.length) {
            var legacy = document.getElementById("app-template");
            if (legacy && String(legacy.innerHTML).trim()) {
                return Promise.resolve(legacy.innerHTML);
            }
            return Promise.reject(new Error("Шаблоны не найдены"));
        }
        return Promise.all(
            parts.map(function (name) {
                return fetch("/app/ui/templates/" + name).then(function (res) {
                    if (!res.ok) {
                        throw new Error("Не удалось загрузить шаблон: " + name);
                    }
                    return res.text();
                });
            })
        ).then(function (chunks) {
            return chunks.join("");
        });
    }

    function startApp(tpl) {
        if (!tpl || !String(tpl).trim()) {
            showBootError(
                '<div class="container py-5 text-light"><p class="alert alert-danger">Шаблон приложения пуст.</p></div>'
            );
            return;
        }

        try {
            createApp({
                data: window.AppData,
                computed: window.AppComputed,
                methods: window.AppMethods,
                mounted: window.AppMounted,
                watch: window.AppWatch,
                template: tpl,
            }).mount("#app");
        } catch (err) {
            var msg = err && err.message ? err.message : String(err);
            showBootError(
                '<div class="container py-5 text-light"><p class="alert alert-danger">Ошибка запуска интерфейса: ' +
                    msg.replace(/</g, "&lt;") +
                    "</p></div>"
            );
        }
    }

    loadTemplate()
        .then(startApp)
        .catch(function (err) {
            var msg = err && err.message ? err.message : String(err);
            showBootError(
                '<div class="container py-5 text-light"><p class="alert alert-danger">Ошибка загрузки шаблона: ' +
                    msg.replace(/</g, "&lt;") +
                    "</p></div>"
            );
        });
})();
