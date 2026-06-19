(function () {
    var apiUrl = window.ApiClient.apiUrl;
    var parseResponseJson = window.ApiClient.parseResponseJson;
    var readErrorMessage = window.ApiClient.readErrorMessage;

    // ОТПРАВКА КОДА (универсальный метод с message_type)
    function sendConfirmationCode(email, messageType) {
        var payload = {
            email: email,
            message_type: messageType, // "verify_email" | "two_factor_auth" | "reset_password"
        };

        return fetch(apiUrl("/api/v1/auth/send-confirmation-code"), {
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

    // ПОДТВЕРЖДЕНИЕ 2FA КОДА
    function confirmEmail(payload) {
        return fetch(apiUrl("/api/v1/auth/confirm-email"), {
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

    // СТАРАЯ РЕГИСТРАЦИЯ (для совместимости)
    function registerUser(payload) {
        console.warn("registerUser is deprecated, use registerUserWithCode");
        return registerUserWithCode(payload);
    }

    // ЛОГИН (возвращает email)
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
                // data - это строка с email
                return data;
            });
        });
    }

    // СБРОС ПАРОЛЯ
    function resetPassword(payload) {
        return fetch(apiUrl("/api/v1/auth/reset-password"), {
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

    function logout() {
        window.TokenStore.clearTokens();
    }

    window.ApiAuth = {
        registerUser: registerUser, // для обратной совместимости
        registerUserWithCode: registerUserWithCode,
        sendConfirmationCode: sendConfirmationCode, // универсальный метод
        confirmEmail: confirmEmail,
        loginUser: loginUser,
        resetPassword: resetPassword,
        logout: logout,
    };
})();