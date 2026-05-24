(function () {
    function base() {
        return typeof window.__API_BASE__ === "string" ? window.__API_BASE__ : "";
    }

    function apiUrl(path) {
        var b = base();
        if (!path.startsWith("/")) {
            path = "/" + path;
        }
        return b + path;
    }

    function parseResponseJson(res) {
        return res.text().then(function (text) {
            if (!text) {
                return null;
            }
            try {
                return JSON.parse(text);
            } catch (e) {
                return { message: text || res.statusText };
            }
        });
    }

    function readErrorMessage(data) {
        if (!data) {
            return "Ошибка запроса";
        }
        // Обработка ошибки 429
        if (data.detail && data.detail.includes("Too Many Requests")) {
            return "⚠️ Слишком много запросов. Пожалуйста, подождите немного.";
        }
        if (typeof data.message === "string") {
            return data.message;
        }
        if (Array.isArray(data.detail)) {
            return data.detail
                .map(function (d) {
                    if (typeof d === "string") {
                        return d;
                    }
                    if (d && d.msg) {
                        return d.msg;
                    }
                    return JSON.stringify(d);
                })
                .join("; ");
        }
        if (typeof data.detail === "string") {
            return data.detail;
        }
        return "Ошибка запроса";
    }

    window.ApiClient = {
        apiUrl: apiUrl,
        parseResponseJson: parseResponseJson,
        readErrorMessage: readErrorMessage,
    };
})();
