(function () {
    window.AppMethodsAuth = {
        // ==================== УПРАВЛЕНИЕ СООБЩЕНИЯМИ ====================

        // Показать сообщение об ошибке (заменяет success)
        showError: function (message, autoClear = true) {
            this.error = message;
            this.success = ''; // Очищаем успешное сообщение
            if (autoClear) {
                this.clearMessagesAfterDelay(5000);
            }
        },

        // Показать сообщение об успехе (заменяет error)
        showSuccess: function (message, autoClear = true) {
            this.success = message;
            this.error = ''; // Очищаем сообщение об ошибке
            if (autoClear) {
                this.clearMessagesAfterDelay(5000);
            }
        },

        // Очистить все сообщения
        clearMessages: function () {
            this.error = '';
            this.success = '';
            if (this.messageTimeout) {
                clearTimeout(this.messageTimeout);
                this.messageTimeout = null;
            }
        },

        // Автоматическая очистка через заданное время
        clearMessagesAfterDelay: function (delay) {
            var self = this;
            if (this.messageTimeout) {
                clearTimeout(this.messageTimeout);
            }
            this.messageTimeout = setTimeout(function () {
                self.error = '';
                self.success = '';
                self.messageTimeout = null;
            }, delay);
        },

        // ==================== ЛОГИН С 2FA ====================
        onLogin: function () {
            var self = this;
            this.clearMessages();
            this.loading = true;

            window.ApiAuth.loginUser(
                this.loginForm.username.trim(),
                this.loginForm.password
            )
            .then(function (data) {
                self.loginToken = data.token;
                self.loginStep = 'verify';
                self.showSuccess("✅ Код подтверждения отправлен на почту");
                self.startLoginResendTimer(60);
            })
            .catch(function (e) {
                var message = e.message || "Не удалось войти";
                var lowerMessage = message.toLowerCase();
                var errorText = "";

                // 🔥 ОБРАБОТКА ОШИБОК ЛОГИНА
                if (lowerMessage.includes("invalid") ||
                    lowerMessage.includes("неверн") ||
                    lowerMessage.includes("не правильн") ||
                    lowerMessage.includes("incorrect")) {
                    if (lowerMessage.includes("password") || lowerMessage.includes("парол")) {
                        errorText = "❌ Неверный пароль. Пожалуйста, проверьте правильность введенного пароля.";
                        self.loginForm.password = '';
                        setTimeout(function () {
                            var input = document.getElementById('login-password');
                            if (input) {
                                input.focus();
                                input.select();
                            }
                        }, 100);
                    } else if (lowerMessage.includes("login") || lowerMessage.includes("логин") || lowerMessage.includes("username")) {
                        errorText = "❌ Неверный логин. Пожалуйста, проверьте правильность введенного логина.";
                        self.loginForm.username = '';
                        setTimeout(function () {
                            var input = document.getElementById('login-username');
                            if (input) {
                                input.focus();
                                input.select();
                            }
                        }, 100);
                    } else {
                        errorText = "❌ Неверный логин или пароль. Попробуйте еще раз.";
                    }
                } else if (lowerMessage.includes("not found") ||
                           lowerMessage.includes("не найден") ||
                           lowerMessage.includes("does not exist")) {
                    errorText = "❌ Пользователь с таким логином не найден. Проверьте правильность введенного логина.";
                    self.loginForm.username = '';
                    setTimeout(function () {
                        var input = document.getElementById('login-username');
                        if (input) {
                            input.focus();
                            input.select();
                        }
                    }, 100);
                } else {
                    errorText = "❌ " + message;
                }

                self.showError(errorText);
            })
            .finally(function () {
                self.loading = false;
            });
        },

        // ПОДТВЕРЖДЕНИЕ 2FA КОДА
        onVerifyLoginCode: function () {
            var self = this;
            this.clearMessages();
            this.loading = true;

            if (this.loginCode.trim().length !== 6) {
                this.showError("Введите 6-значный код");
                this.loading = false;
                return;
            }

            if (!this.loginToken) {
                this.showError("❌ Ошибка: токен не найден. Попробуйте войти заново.");
                this.loading = false;
                return;
            }

            window.ApiAuth.verifyLogin(
                this.loginToken,
                this.loginCode.trim()
            )
                .then(function (data) {
                    window.TokenStore.setTokens(data.access_token, data.refresh_token);
                    window.location.hash = "#/";
                    window.location.reload();
                })
                .catch(function (e) {
                    var message = e.message || "Неверный код подтверждения";
                    var lowerMessage = message.toLowerCase();
                    var errorText = "";

                    if (lowerMessage.includes("does not exist") ||
                        lowerMessage.includes("не существует") ||
                        lowerMessage.includes("not found") ||
                        lowerMessage.includes("не найден")) {
                        errorText = "❌ Код подтверждения не найден. Возможно, он уже был использован или истек. Запросите новый код.";
                        self.loginCode = '';
                        setTimeout(function () {
                            var input = document.getElementById('login-code-input');
                            if (input) {
                                input.focus();
                                input.select();
                            }
                        }, 100);
                    } else if (lowerMessage.includes("expired") ||
                               lowerMessage.includes("истек") ||
                               lowerMessage.includes("timeout") ||
                               lowerMessage.includes("не действителен") ||
                               lowerMessage.includes("срок действия") ||
                               lowerMessage.includes("устарел")) {
                        errorText = "⏰ Срок действия кода истек. Запросите новый код.";
                        self.loginCode = '';
                        setTimeout(function () {
                            self.onResendLoginCode();
                        }, 2000);
                    } else if (lowerMessage.includes("not valid") ||
                               lowerMessage.includes("недействителен") ||
                               lowerMessage.includes("invalid") ||
                               lowerMessage.includes("неверн") ||
                               lowerMessage.includes("не правильн")) {
                        errorText = "❌ Неверный код подтверждения. Проверьте правильность введенных цифр.";
                        self.loginCode = '';
                        setTimeout(function () {
                            var input = document.getElementById('login-code-input');
                            if (input) {
                                input.focus();
                                input.select();
                            }
                        }, 100);
                    } else if (lowerMessage.includes("attempt") ||
                               lowerMessage.includes("попытк") ||
                               lowerMessage.includes("blocked") ||
                               lowerMessage.includes("заблокирован") ||
                               lowerMessage.includes("too many")) {
                        errorText = "⚠️ Слишком много неудачных попыток. Доступ временно заблокирован.";
                        self.loginBlocked = true;
                        setTimeout(function () {
                            self.loginBlocked = false;
                            self.onResendLoginCode();
                        }, 5000);
                    } else {
                        errorText = "❌ " + message;
                    }

                    self.showError(errorText);
                })
                .finally(function () {
                    self.loading = false;
                });
        },


        // ПОВТОРНАЯ ОТПРАВКА 2FA КОДА
        onResendLoginCode: function () {
            var self = this;
            this.clearMessages();
            this.loading = true;

            if (!this.loginToken) {
                this.showError("❌ Ошибка: токен не найден. Попробуйте войти заново.");
                this.loading = false;
                return;
            }

            window.ApiAuth.resendLoginCode(this.loginToken)
                .then(function () {
                    self.showSuccess("✅ Новый код отправлен на почту");
                    self.startLoginResendTimer(60);
                    self.loginCode = '';
                    self.loginBlocked = false;
                    setTimeout(function () {
                        var input = document.getElementById('login-code-input');
                        if (input) input.focus();
                    }, 100);
                })
                .catch(function (e) {
                    var message = e.message || "Не удалось отправить код";
                    var lowerMessage = message.toLowerCase();

                    if (lowerMessage.includes("expired") ||
                        lowerMessage.includes("истек") ||
                        lowerMessage.includes("timeout")) {
                        self.showError("⏰ Срок действия сессии истек. Пожалуйста, войдите заново.");
                        setTimeout(function () {
                            self.onBackToLogin();
                        }, 2000);
                    } else if (lowerMessage.includes("too many") ||
                               lowerMessage.includes("много")) {
                        self.showError("⚠️ Слишком много запросов. Подождите немного.");
                    } else {
                        self.showError("❌ " + message);
                    }
                })
                .finally(function () {
                    self.loading = false;
                });
        },


        // ВОЗВРАТ К ФОРМЕ ЛОГИНА
        onBackToLogin: function () {
            this.loginStep = 'form';
            this.loginCode = '';
            this.loginToken = '';
            this.error = '';
            this.success = '';
            if (this.loginTimerInterval) {
                clearInterval(this.loginTimerInterval);
                this.loginTimerInterval = null;
            }
        },

        // ТАЙМЕР ДЛЯ 2FA
        startLoginResendTimer: function (seconds) {
            var self = this;
            this.loginResendTimer = seconds;
            this.loginCanResend = false;

            if (this.loginTimerInterval) {
                clearInterval(this.loginTimerInterval);
            }

            this.loginTimerInterval = setInterval(function () {
                self.loginResendTimer--;
                if (self.loginResendTimer <= 0) {
                    clearInterval(self.loginTimerInterval);
                    self.loginTimerInterval = null;
                    self.loginCanResend = true;
                }
            }, 1000);
        },

        // ==================== РЕГИСТРАЦИЯ ====================
        // ОБНОВЛЕННАЯ РЕГИСТРАЦИЯ (ШАГ 1)
        onRegister: function () {
            var self = this;
            this.clearMessages();

            // Валидация
            if (this.registerForm.password.length < 8) {
                this.showError("Пароль должен быть минимум 8 символов");
                return;
            }

            var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(this.registerForm.email.trim())) {
                this.showError("Введите корректный email");
                return;
            }

            if (this.registerForm.login.trim().length < 3) {
                this.showError("Логин должен быть минимум 3 символа");
                return;
            }

            if (this.registerForm.surname.trim().length < 2) {
                this.showError("Фамилия должна быть минимум 2 символа");
                return;
            }

            if (this.registerForm.name.trim().length < 2) {
                this.showError("Имя должно быть минимум 2 символа");
                return;
            }

            this.loading = true;
            var payload = {
                surname: this.registerForm.surname.trim(),
                name: this.registerForm.name.trim(),
                login: this.registerForm.login.trim(),
                email: this.registerForm.email.trim(),
                password: this.registerForm.password,
            };

            window.ApiAuth.registerUser(payload)
                .then(function (data) {
                    self.registrationToken = data.token;
                    self.registrationData.email = payload.email;
                    self.registerStep = 'verify';
                    self.showSuccess("✅ Код подтверждения отправлен на почту");
                    self.startResendTimer(60);
                })
                .catch(function (e) {
                    var message = e.message || "Ошибка регистрации";
                    var lowerMessage = message.toLowerCase();
                    var errorText = "";

                    // 🔥 ОБРАБОТКА ОШИБОК УНИКАЛЬНОСТИ
                    if (lowerMessage.includes("login") &&
                        (lowerMessage.includes("already exists") ||
                         lowerMessage.includes("already taken") ||
                         lowerMessage.includes("существует") ||
                         lowerMessage.includes("занят") ||
                         lowerMessage.includes("используется"))) {
                        errorText = "❌ Логин уже занят. Пожалуйста, выберите другой логин.";
                        // Очищаем поле логина и ставим фокус
                        self.registerForm.login = '';
                        setTimeout(function () {
                            var input = document.getElementById('reg-login');
                            if (input) {
                                input.focus();
                                input.select();
                            }
                        }, 100);
                    } else if (lowerMessage.includes("email") &&
                               (lowerMessage.includes("already exists") ||
                                lowerMessage.includes("already taken") ||
                                lowerMessage.includes("существует") ||
                                lowerMessage.includes("занят") ||
                                lowerMessage.includes("используется"))) {
                        errorText = "❌ Email уже используется. Пожалуйста, используйте другой email.";
                        // Очищаем поле email и ставим фокус
                        self.registerForm.email = '';
                        setTimeout(function () {
                            var input = document.getElementById('reg-email');
                            if (input) {
                                input.focus();
                                input.select();
                            }
                        }, 100);
                    } else if (lowerMessage.includes("already exists") ||
                               lowerMessage.includes("существует") ||
                               lowerMessage.includes("already registered") ||
                               lowerMessage.includes("already taken")) {
                        errorText = "❌ Пользователь с таким email или логином уже существует.";
                    } else {
                        errorText = "❌ " + message;
                    }

                    self.showError(errorText);
                })
                .finally(function () {
                    self.loading = false;
                });
        },


        // ПОДТВЕРЖДЕНИЕ КОДА РЕГИСТРАЦИИ (ШАГ 2)
        onVerifyCode: function () {
            var self = this;
            this.clearMessages();
            this.loading = true;

            if (this.confirmationCode.trim().length !== 6) {
                this.showError("Введите 6-значный код");
                this.loading = false;
                return;
            }

            if (!this.registrationToken) {
                this.showError("❌ Ошибка: токен не найден. Попробуйте зарегистрироваться заново.");
                this.loading = false;
                return;
            }

            window.ApiAuth.verifyRegistration(
                this.registrationToken,
                this.confirmationCode.trim()
            )
                .then(function (data) {
                    if (data.access_token) {
                        window.TokenStore.setTokens(data.access_token, data.refresh_token);
                        self.showSuccess("✅ Регистрация успешна! Добро пожаловать!");
                        setTimeout(function () {
                            window.location.hash = "#/";
                            window.location.reload();
                        }, 1000);
                    } else {
                        self.showSuccess("✅ Регистрация успешна! Теперь вы можете войти.");
                        setTimeout(function () {
                            window.location.hash = "#/login";
                            window.location.reload();
                        }, 1500);
                    }
                })
                .catch(function (e) {
                    var message = e.message || "Неверный код подтверждения";
                    var lowerMessage = message.toLowerCase();
                    var errorText = "";

                    if (lowerMessage.includes("does not exist") ||
                        lowerMessage.includes("не существует") ||
                        lowerMessage.includes("not found") ||
                        lowerMessage.includes("не найден")) {
                        errorText = "❌ Код подтверждения не найден. Возможно, он уже был использован или истек. Запросите новый код.";
                        self.confirmationCode = '';
                        setTimeout(function () {
                            var input = document.getElementById('code-input');
                            if (input) {
                                input.focus();
                                input.select();
                            }
                        }, 100);
                    } else if (lowerMessage.includes("expired") ||
                               lowerMessage.includes("истек") ||
                               lowerMessage.includes("timeout")) {
                        errorText = "⏰ Срок действия кода истек. Отправляем новый код...";
                        setTimeout(function () {
                            self.onResendCode();
                        }, 1500);
                    } else if (lowerMessage.includes("not valid") ||
                               lowerMessage.includes("недействителен") ||
                               lowerMessage.includes("invalid")) {
                        errorText = "❌ Неверный код. Проверьте правильность введенных цифр.";
                        self.confirmationCode = '';
                        setTimeout(function () {
                            var input = document.getElementById('code-input');
                            if (input) {
                                input.focus();
                                input.select();
                            }
                        }, 100);
                    } else if (lowerMessage.includes("already exists") ||
                               lowerMessage.includes("существует") ||
                               lowerMessage.includes("already registered")) {
                        errorText = "❌ Пользователь с таким email или логином уже существует.";
                        setTimeout(function () {
                            self.onBackToRegister();
                        }, 2000);
                    } else if (lowerMessage.includes("attempt") ||
                               lowerMessage.includes("попытк")) {
                        errorText = "⚠️ Слишком много неудачных попыток. Попробуйте позже.";
                    } else {
                        errorText = "❌ " + message;
                    }

                    self.showError(errorText);
                })
                .finally(function () {
                    self.loading = false;
                });
        },



        // ПОВТОРНАЯ ОТПРАВКА КОДА РЕГИСТРАЦИИ
        onResendCode: function () {
            var self = this;
            this.error = "";
            this.success = "";
            this.loading = true;

            if (!this.registrationToken) {
                this.error = "Ошибка: токен не найден. Попробуйте зарегистрироваться заново.";
                this.loading = false;
                return;
            }

            window.ApiAuth.resendRegistrationCode(this.registrationToken)
                .then(function () {
                    self.success = "✅ Новый код отправлен на почту";
                    self.startResendTimer(60);
                })
                .catch(function (e) {
                    var message = e.message || "Не удалось отправить код";
                    var lowerMessage = message.toLowerCase();

                    if (lowerMessage.includes("expired") ||
                        lowerMessage.includes("истек") ||
                        lowerMessage.includes("timeout")) {
                        self.error = "⏰ Срок действия сессии истек. Пожалуйста, начните регистрацию заново.";
                        setTimeout(function () {
                            self.onBackToRegister();
                        }, 2000);
                    } else {
                        self.error = "❌ " + message;
                    }
                })
                .finally(function () {
                    self.loading = false;
                });
        },

        // ВОЗВРАТ К ФОРМЕ РЕГИСТРАЦИИ
        onBackToRegister: function () {
            this.registerStep = 'form';
            this.confirmationCode = '';
            this.registrationToken = '';
            this.error = '';
            this.success = '';
            if (this.timerInterval) {
                clearInterval(this.timerInterval);
                this.timerInterval = null;
            }
        },

        // ТАЙМЕР ДЛЯ РЕГИСТРАЦИИ
        startResendTimer: function (seconds) {
            var self = this;
            this.resendTimer = seconds;
            this.canResend = false;

            if (this.timerInterval) {
                clearInterval(this.timerInterval);
            }

            this.timerInterval = setInterval(function () {
                self.resendTimer--;
                if (self.resendTimer <= 0) {
                    clearInterval(self.timerInterval);
                    self.timerInterval = null;
                    self.canResend = true;
                }
            }, 1000);
        },

        // ==================== ВОССТАНОВЛЕНИЕ ПАРОЛЯ ====================

        // ШАГ 1: Отправка email для восстановления
        onSendResetCode: function () {
            var self = this;
            this.clearMessages();
            this.loading = true;

            var email = this.resetEmail.trim();
            var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                this.showError("Введите корректный email");
                this.loading = false;
                return;
            }

            window.ApiAuth.recoverAccount(email)
                .then(function (data) {
                    self.resetToken = data.token;
                    self.resetEmail = email;
                    self.resetStep = 'verify';
                    self.showSuccess("✅ Код восстановления отправлен на почту");
                    self.startResetResendTimer(60);
                })
                .catch(function (e) {
                    var message = e.message || "Не удалось отправить код";
                    var lowerMessage = message.toLowerCase();
                    var errorText = "";

                    // 🔥 ОБРАБОТКА ОШИБКИ - EMAIL НЕ НАЙДЕН
                    if (lowerMessage.includes("not found") ||
                        lowerMessage.includes("не найден") ||
                        lowerMessage.includes("does not exist") ||
                        lowerMessage.includes("не существует")) {
                        errorText = "❌ Пользователь с таким email не найден. Проверьте правильность введенного адреса.";
                        self.resetEmail = '';
                        setTimeout(function () {
                            var input = document.getElementById('reset-email');
                            if (input) {
                                input.focus();
                                input.select();
                            }
                        }, 100);
                    } else {
                        errorText = "❌ " + message;
                    }

                    self.showError(errorText);
                })
                .finally(function () {
                    self.loading = false;
                });
        },


        // ШАГ 2: Подтверждение кода восстановления
        onVerifyResetCode: function () {
            var self = this;
            this.clearMessages();
            this.loading = true;

            if (this.resetCode.trim().length !== 6) {
                this.showError("Введите 6-значный код");
                this.loading = false;
                return;
            }

            if (!this.resetToken) {
                this.showError("❌ Ошибка: токен не найден. Попробуйте начать заново.");
                this.loading = false;
                return;
            }

            window.ApiAuth.verifyRecovery(
                this.resetToken,
                this.resetCode.trim()
            )
                .then(function (data) {
                    self.resetPasswordToken = data.token;
                    self.showSuccess("✅ Код подтвержден! Теперь вы можете установить новый пароль.");
                    setTimeout(function () {
                        self.resetStep = 'change';
                    }, 1000);
                })
                .catch(function (e) {
                    var message = e.message || "Неверный код подтверждения";
                    var lowerMessage = message.toLowerCase();
                    var errorText = "";

                    if (lowerMessage.includes("does not exist") ||
                        lowerMessage.includes("не существует") ||
                        lowerMessage.includes("not found") ||
                        lowerMessage.includes("не найден")) {
                        errorText = "❌ Код подтверждения не найден. Возможно, он уже был использован или истек. Запросите новый код.";
                        self.resetCode = '';
                        setTimeout(function () {
                            var input = document.getElementById('reset-code-input');
                            if (input) {
                                input.focus();
                                input.select();
                            }
                        }, 100);
                    } else if (lowerMessage.includes("expired") ||
                               lowerMessage.includes("истек") ||
                               lowerMessage.includes("timeout") ||
                               lowerMessage.includes("не действителен") ||
                               lowerMessage.includes("срок действия") ||
                               lowerMessage.includes("устарел")) {
                        errorText = "⏰ Срок действия кода истек. Пожалуйста, запросите новый код.";
                        self.resetCode = '';
                        setTimeout(function () {
                            self.onResendResetCode();
                        }, 2000);
                    } else if (lowerMessage.includes("not valid") ||
                               lowerMessage.includes("недействителен") ||
                               lowerMessage.includes("invalid") ||
                               lowerMessage.includes("неверн") ||
                               lowerMessage.includes("не правильн")) {
                        errorText = "❌ Неверный код подтверждения. Проверьте правильность введенных цифр.";
                        self.resetCode = '';
                        setTimeout(function () {
                            var input = document.getElementById('reset-code-input');
                            if (input) {
                                input.focus();
                                input.select();
                            }
                        }, 100);
                    } else if (lowerMessage.includes("not found") ||
                               lowerMessage.includes("не найден")) {
                        errorText = "❌ Пользователь с таким email не найден.";
                        setTimeout(function () {
                            self.onResetBackToLogin();
                        }, 2000);
                    } else if (lowerMessage.includes("attempt") ||
                               lowerMessage.includes("попытк") ||
                               lowerMessage.includes("too many")) {
                        errorText = "⚠️ Слишком много неудачных попыток. Попробуйте позже.";
                    } else {
                        errorText = "❌ " + message;
                    }

                    self.showError(errorText);
                })
                .finally(function () {
                    self.loading = false;
                });
        },

        // ШАГ 3: Смена пароля
        onChangePassword: function () {
            var self = this;
            this.clearMessages();
            this.loading = true;

            if (this.resetNewPassword.length < 8) {
                this.showError("Пароль должен быть минимум 8 символов");
                this.loading = false;
                return;
            }

            if (this.resetNewPassword !== this.resetConfirmPassword) {
                this.showError("Пароли не совпадают");
                this.loading = false;
                return;
            }

            if (!this.resetPasswordToken) {
                this.showError("❌ Ошибка: токен не найден. Попробуйте начать заново.");
                this.loading = false;
                return;
            }

            var payload = {
                reset_password_token: this.resetPasswordToken,
                password: this.resetNewPassword,
                password_confirmation: this.resetConfirmPassword,
            };

            window.ApiAuth.resetPassword(payload)
                .then(function () {
                    self.showSuccess("✅ Пароль успешно изменен! Теперь вы можете войти.");
                    self.resetStep = 'done';
                })
                .catch(function (e) {
                    self.showError(e.message || "❌ Не удалось изменить пароль");
                })
                .finally(function () {
                    self.loading = false;
                });
        },

        // ПОВТОРНАЯ ОТПРАВКА КОДА ВОССТАНОВЛЕНИЯ
        onResendResetCode: function () {
            var self = this;
            this.clearMessages();
            this.loading = true;

            if (!this.resetToken) {
                this.showError("❌ Ошибка: токен не найден. Попробуйте начать заново.");
                this.loading = false;
                return;
            }

            window.ApiAuth.resendRecoveryCode(this.resetToken)
                .then(function () {
                    self.showSuccess("✅ Новый код отправлен на почту");
                    self.startResetResendTimer(60);
                })
                .catch(function (e) {
                    var message = e.message || "Не удалось отправить код";
                    var lowerMessage = message.toLowerCase();

                    if (lowerMessage.includes("expired") ||
                        lowerMessage.includes("истек") ||
                        lowerMessage.includes("timeout")) {
                        self.showError("⏰ Срок действия сессии истек. Начните восстановление заново.");
                        setTimeout(function () {
                            self.onResetBackToLogin();
                        }, 2000);
                    } else {
                        self.showError("❌ " + message);
                    }
                })
                .finally(function () {
                    self.loading = false;
                });
        },

        // ВОЗВРАТ К ФОРМЕ ВОССТАНОВЛЕНИЯ
        onResetBackToLogin: function () {
            this.resetStep = 'form';
            this.resetEmail = '';
            this.resetCode = '';
            this.resetNewPassword = '';
            this.resetConfirmPassword = '';
            this.resetToken = '';
            this.resetPasswordToken = '';
            this.clearMessages(); // ← используем общий метод
            if (this.resetTimerInterval) {
                clearInterval(this.resetTimerInterval);
                this.resetTimerInterval = null;
            }
            this.currentView = 'login';
        },

        // ТАЙМЕР ДЛЯ ВОССТАНОВЛЕНИЯ
        startResetResendTimer: function (seconds) {
            var self = this;
            this.resetResendTimer = seconds;
            this.resetCanResend = false;

            if (this.resetTimerInterval) {
                clearInterval(this.resetTimerInterval);
            }

            this.resetTimerInterval = setInterval(function () {
                self.resetResendTimer--;
                if (self.resetResendTimer <= 0) {
                    clearInterval(self.resetTimerInterval);
                    self.resetTimerInterval = null;
                    self.resetCanResend = true;
                }
            }, 1000);
        },

        // ==================== ОБЩИЕ МЕТОДЫ ====================
        onLogout: function () {
            window.ApiAuth.logout();
            window.location.reload();
        },

        formatRegistrationDate: function (iso) {
            if (!iso) {
                return "—";
            }
            try {
                return new Date(iso).toLocaleString("ru-RU");
            } catch (e) {
                return iso;
            }
        },
    };
})();