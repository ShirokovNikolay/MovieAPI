(function () {
    var apiUrl = window.ApiClient.apiUrl;
    var parseResponseJson = window.ApiClient.parseResponseJson;
    var readErrorMessage = window.ApiClient.readErrorMessage;

    // ОТПРАВКА КОДА НА ПОЧТУ
    function sendConfirmationCode(email) {
        return fetch(apiUrl("/api/v1/auth/confirmation_code?email=" + encodeURIComponent(email)), {
            method: "POST",
            headers: {
                Accept: "application/json",
            },
        }).then(function (res) {
            return parseResponseJson(res).then(function (data) {
                if (!res.ok) {
                    throw new Error(readErrorMessage(data));
                }
                return data;
            });
        });
    }

    // РЕГИСТРАЦИЯ С КОДОМ
    function registerUserWithCode(payload) {
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

    // СТАРАЯ РЕГИСТРАЦИЯ (оставляем для совместимости, но не используем)
    function registerUser(payload) {
        // Можно оставить или удалить
        console.warn("registerUser is deprecated, use registerUserWithCode");
        return registerUserWithCode(payload);
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

    window.ApiAuth = {
        registerUser: registerUser, // оставляем для обратной совместимости
        registerUserWithCode: registerUserWithCode,
        sendConfirmationCode: sendConfirmationCode,
        loginUser: loginUser,
        logout: logout,
    };
})();