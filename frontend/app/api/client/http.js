(function () {
    var apiUrl = window.ApiClient.apiUrl;
    var parseResponseJson = window.ApiClient.parseResponseJson;
    var readErrorMessage = window.ApiClient.readErrorMessage;

    var refreshInFlight = null;

    /**
     * Обновляет access по refresh. Ответ refresh может не содержать новый refresh — сохраняем старый.
     */
    function refreshAccessToken() {
        var refresh = window.TokenStore.getRefreshToken();
        if (!refresh || window.TokenStore.isTokenExpired(refresh, 30)) {
            window.TokenStore.clearTokens();
            return Promise.reject(new Error("REFRESH_EXPIRED"));
        }
        if (refreshInFlight) {
            return refreshInFlight;
        }
        refreshInFlight = fetch(apiUrl("/api/v1/auth/refresh"), {
            method: "POST",
            headers: {
                Authorization: "Bearer " + refresh,
                Accept: "application/json",
            },
        })
            .then(function (res) {
                return parseResponseJson(res).then(function (data) {
                    if (!res.ok) {
                        window.TokenStore.clearTokens();
                        throw new Error(readErrorMessage(data));
                    }
                    var newAccess = data.access_token;
                    var newRefresh = data.refresh_token;
                    window.TokenStore.setTokens(newAccess, newRefresh || refresh);
                    return newAccess;
                });
            })
            .finally(function () {
                refreshInFlight = null;
            });
        return refreshInFlight;
    }

    /**
     * Гарантирует актуальный access: при истечении срока вызывает refresh_access_token.
     */
    function ensureValidAccessToken() {
        var access = window.TokenStore.getAccessToken();
        var refresh = window.TokenStore.getRefreshToken();
        if (!refresh || window.TokenStore.isTokenExpired(refresh, 30)) {
            window.TokenStore.clearTokens();
            return Promise.reject(new Error("REFRESH_EXPIRED"));
        }
        if (!access || window.TokenStore.isTokenExpired(access, 30)) {
            return refreshAccessToken();
        }
        return Promise.resolve(access);
    }

    /**
     * fetch с Bearer access; при 401 один раз пробует refresh и повторяет запрос.
     */
    function authFetch(path, options) {
        options = options || {};
        var tryOnce = function (afterRefresh) {
            return ensureValidAccessToken()
                .then(function (token) {
                    var headers = Object.assign({}, options.headers || {}, {
                        Authorization: "Bearer " + token,
                    });
                    return fetch(apiUrl(path), Object.assign({}, options, { headers: headers }));
                })
                .then(function (res) {
                    if (res.status === 401 && !afterRefresh) {
                        return refreshAccessToken().then(function () {
                            return tryOnce(true);
                        });
                    }
                    return res;
                });
        };
        return tryOnce(false);
    }

    function authFetchJson(path, options) {
        options = options || {};
        var headers = Object.assign({ Accept: "application/json" }, options.headers || {});
        var body = options.body;
        var method = options.method || "GET";
        if (body !== undefined && body !== null && typeof body === "object" && !(body instanceof FormData)) {
            body = JSON.stringify(body);
            headers["Content-Type"] = "application/json";
        }
        return authFetch(path, { method: method, headers: headers, body: body }).then(function (res) {
            if (res.status === 429) {
                throw new Error("⚠️ Слишком много запросов. Подождите немного.");
            }
            if (res.status === 204) {
                if (!res.ok) {
                    return parseResponseJson(res).then(function (data) {
                        throw new Error(readErrorMessage(data));
                    });
                }
                return null;
            }
            return parseResponseJson(res).then(function (data) {
                if (!res.ok) {
                    throw new Error(readErrorMessage(data));
                }
                return data;
            });
        });
    }

    function publicGetJson(pathWithQuery) {
        return fetch(apiUrl(pathWithQuery), {
            method: "GET",
            headers: { Accept: "application/json" },
        }).then(function (res) {
            if (res.status === 429) {
                throw new Error("⚠️ Слишком много запросов. Подождите немного.");
            }
            return parseResponseJson(res).then(function (data) {
                if (!res.ok) {
                    throw new Error(readErrorMessage(data));
                }
                return data;
            });
        });
    }

    window.ApiHttp = {
        refreshAccessToken: refreshAccessToken,
        ensureValidAccessToken: ensureValidAccessToken,
        authFetch: authFetch,
        authFetchJson: authFetchJson,
        publicGetJson: publicGetJson,
    };
})();
