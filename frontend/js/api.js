(function () {
    var base = function () {
        return typeof window.__API_BASE__ === "string" ? window.__API_BASE__ : "";
    };

    function apiUrl(path) {
        var b = base();
        if (!path.startsWith("/")) {
            path = "/" + path;
        }
        return b + path;
    }

    var refreshInFlight = null;

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

    function registerUser(payload) {
        return fetch(apiUrl("/api/v1/auth/register"), {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
            body: JSON.stringify(payload),
        }).then(function (res) {
            return parseResponseJson(res).then(function (data) {
                if (!res.ok) {
                    throw new Error(readErrorMessage(data));
                }
                return data;
            });
        });
    }

    function loginUser(username, password) {
        var body = new URLSearchParams();
        body.set("username", username);
        body.set("password", password);
        return fetch(apiUrl("/api/v1/auth/login"), {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                Accept: "application/json",
            },
            body: body.toString(),
        }).then(function (res) {
            return parseResponseJson(res).then(function (data) {
                if (!res.ok) {
                    throw new Error(readErrorMessage(data));
                }
                window.TokenStore.setTokens(data.access_token, data.refresh_token);
                return data;
            });
        });
    }

    function logout() {
        window.TokenStore.clearTokens();
    }

    function authFetchJson(path, options) {
        options = options || {};
        var headers = Object.assign({ Accept: "application/json" }, options.headers || {});
        var body = options.body;
        var method = options.method || "GET";
        if (
            body !== undefined &&
            body !== null &&
            typeof body === "object" &&
            !(body instanceof FormData)
        ) {
            body = JSON.stringify(body);
            headers["Content-Type"] = "application/json";
        }
        return authFetch(path, { method: method, headers: headers, body: body }).then(function (res) {
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

    function getCurrentUserProfile() {
        return authFetchJson("/api/v1/users/me/", { method: "GET" });
    }

    function updateCurrentUserProfile(payload) {
        return authFetchJson("/api/v1/users/me/", { method: "PUT", body: payload });
    }

    function partialUpdateCurrentUserProfile(payload) {
        return authFetchJson("/api/v1/users/me/", { method: "PATCH", body: payload });
    }

    function deleteCurrentUserProfile() {
        return authFetchJson("/api/v1/users/me/", { method: "DELETE" });
    }

    function publicGetJson(pathWithQuery) {
        return fetch(apiUrl(pathWithQuery), {
            method: "GET",
            headers: { Accept: "application/json" },
        }).then(function (res) {
            return parseResponseJson(res).then(function (data) {
                if (!res.ok) {
                    throw new Error(readErrorMessage(data));
                }
                return data;
            });
        });
    }

    function getGenres(page, size) {
        var p = page != null ? page : 1;
        var s = size != null ? size : 10;
        return publicGetJson(
            "/api/v1/genres/?page=" + encodeURIComponent(p) + "&size=" + encodeURIComponent(s)
        );
    }

    function searchGenresByName(name, page, size) {
        var p = page != null ? page : 1;
        var s = size != null ? size : 10;
        var q =
            "genre_name=" +
            encodeURIComponent(name) +
            "&page=" +
            encodeURIComponent(p) +
            "&size=" +
            encodeURIComponent(s);
        return publicGetJson("/api/v1/genres/search?" + q);
    }

    window.Api = {
        apiUrl: apiUrl,
        refreshAccessToken: refreshAccessToken,
        ensureValidAccessToken: ensureValidAccessToken,
        authFetch: authFetch,
        authFetchJson: authFetchJson,
        getCurrentUserProfile: getCurrentUserProfile,
        updateCurrentUserProfile: updateCurrentUserProfile,
        partialUpdateCurrentUserProfile: partialUpdateCurrentUserProfile,
        deleteCurrentUserProfile: deleteCurrentUserProfile,
        registerUser: registerUser,
        loginUser: loginUser,
        logout: logout,
        readErrorMessage: readErrorMessage,
        getGenres: getGenres,
        searchGenresByName: searchGenresByName,
    };
})();
