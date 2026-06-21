(function () {
    var apiUrl = window.ApiClient.apiUrl;
    var parseResponseJson = window.ApiClient.parseResponseJson;
    var readErrorMessage = window.ApiClient.readErrorMessage;

    // ============ РЕГИСТРАЦИЯ ============
    function registerUser(payload) {
        return fetch(apiUrl("/api/v1/auth/register/"), {
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

    function verifyRegistration(token, confirmationCode) {
        return fetch(apiUrl("/api/v1/auth/register/verify"), {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
            body: JSON.stringify({
                token: token,
                confirmation_code: confirmationCode,
            }),
        }).then(function (res) {
            return parseResponseJson(res).then(function (data) {
                if (!res.ok) {
                    throw new Error(readErrorMessage(data));
                }
                return data;
            });
        });
    }

    function resendRegistrationCode(token) {
        return fetch(apiUrl("/api/v1/auth/register/resend-confirmation-code"), {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
            body: JSON.stringify({
                token: token,
            }),
        }).then(function (res) {
            return parseResponseJson(res).then(function (data) {
                if (!res.ok) {
                    throw new Error(readErrorMessage(data));
                }
                return data;
            });
        });
    }

    // ============ ВХОД (2FA) ============

    // ШАГ 1: Логин (получаем временный токен)
    function loginUser(username, password) {
        var body = new URLSearchParams();
        body.set("username", username);
        body.set("password", password);

        return fetch(apiUrl("/api/v1/auth/login/"), {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",  // ← form-data
                Accept: "application/json",
            },
            body: body.toString(),  // ← form-data, не JSON
        }).then(function (res) {
            return parseResponseJson(res).then(function (data) {
                if (!res.ok) {
                    throw new Error(readErrorMessage(data));
                }
                return data; // { token: "...", token_type: "bearer" }
            });
        });
    }

    // ШАГ 2: Подтверждение 2FA кода
    function verifyLogin(token, confirmationCode) {
        return fetch(apiUrl("/api/v1/auth/login/verify"), {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
            body: JSON.stringify({
                token: token,
                confirmation_code: confirmationCode,
            }),
        }).then(function (res) {
            return parseResponseJson(res).then(function (data) {
                if (!res.ok) {
                    throw new Error(readErrorMessage(data));
                }
                return data; // { access_token, refresh_token, token_type }
            });
        });
    }

    // ПОВТОРНАЯ ОТПРАВКА 2FA КОДА
    function resendLoginCode(token) {
        return fetch(apiUrl("/api/v1/auth/login/resend-confirmation-code"), {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
            body: JSON.stringify({
                token: token,
            }),
        }).then(function (res) {
            return parseResponseJson(res).then(function (data) {
                if (!res.ok) {
                    throw new Error(readErrorMessage(data));
                }
                return data;
            });
        });
    }

    // ============ ВОССТАНОВЛЕНИЕ ПАРОЛЯ ============

    function sendResetCode(email) {
        var payload = {
            email: email,
            message_type: "reset_password",
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

    // ============ ОБЩИЕ МЕТОДЫ ============

    function logout() {
        window.TokenStore.clearTokens();
    }

    // ============ ЭКСПОРТ ============

    window.ApiAuth = {
        // Регистрация
        registerUser: registerUser,
        verifyRegistration: verifyRegistration,
        resendRegistrationCode: resendRegistrationCode,

        // Вход (2FA)
        loginUser: loginUser,
        verifyLogin: verifyLogin,
        resendLoginCode: resendLoginCode,

        // Восстановление
        sendResetCode: sendResetCode,
        resetPassword: resetPassword,

        // Общее
        logout: logout,
    };
})();