(function () {
    var apiUrl = window.ApiClient.apiUrl;
    var parseResponseJson = window.ApiClient.parseResponseJson;
    var readErrorMessage = window.ApiClient.readErrorMessage;

    // ============ РЕГИСТРАЦИЯ (НОВАЯ ЛОГИКА) ============

    // ШАГ 1: Регистрация (получаем временный токен)
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
                return data; // { token: "...", token_type: "bearer" }
            });
        });
    }

    // ШАГ 2: Подтверждение кода регистрации
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

    // ПОВТОРНАЯ ОТПРАВКА КОДА РЕГИСТРАЦИИ
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

    // ============ 2FA (двухфакторная аутентификация) ============

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
                return data; // { access_token, refresh_token, token_type }
            });
        });
    }

    // ПОВТОРНАЯ ОТПРАВКА 2FA КОДА
    function sendConfirmationCode(email, messageType) {
        var payload = {
            email: email,
            message_type: messageType, // "two_factor_auth"
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

    // ============ ВОССТАНОВЛЕНИЕ ПАРОЛЯ ============

    // ОТПРАВКА КОДА ДЛЯ ВОССТАНОВЛЕНИЯ
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

    // СБРОС ПАРОЛЯ (с новым паролем)
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

        // 2FA
        loginUser: loginUser,
        confirmEmail: confirmEmail,
        sendConfirmationCode: sendConfirmationCode, // для повторной отправки 2FA

        // Восстановление
        sendResetCode: sendResetCode,
        resetPassword: resetPassword,

        // Общее
        logout: logout,
    };
})();