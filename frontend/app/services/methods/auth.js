(function () {
    window.AppMethodsAuth = {
        // ==================== ЛОГИН С 2FA ====================
        onLogin: function () {
            var self = this;
            this.error = "";
            this.loading = true;

            // Передаем username и password отдельно (не JSON)
            window.ApiAuth.loginUser(
                this.loginForm.username.trim(),
                this.loginForm.password
            )
            .then(function (data) {
                self.loginToken = data.token;
                self.loginStep = 'verify';
                self.success = "Код подтверждения отправлен на почту";
                self.startLoginResendTimer(60);
            })
            .catch(function (e) {
                self.error = e.message || "Не удалось войти";
            })
            .finally(function () {
                self.loading = false;
            });
        },

        // ПОДТВЕРЖДЕНИЕ 2FA КОДА
        onVerifyLoginCode: function () {
            var self = this;
            this.error = "";
            this.loading = true;

            if (this.loginCode.trim().length !== 6) {
                this.error = "Введите 6-значный код";
                this.loading = false;
                return;
            }

            if (!this.loginToken) {
                this.error = "Ошибка: токен не найден. Попробуйте войти заново.";
                this.loading = false;
                return;
            }

            window.ApiAuth.verifyLogin(
                this.loginToken,
                this.loginCode.trim()
            )
                .then(function (data) {
                    // Сохраняем токены доступа
                    window.TokenStore.setTokens(data.access_token, data.refresh_token);
                    window.location.hash = "#/";
                    window.location.reload();
                })
                .catch(function (e) {
                    self.error = e.message || "Неверный код подтверждения";
                })
                .finally(function () {
                    self.loading = false;
                });
        },

        // ПОВТОРНАЯ ОТПРАВКА 2FA КОДА
        onResendLoginCode: function () {
            var self = this;
            this.error = "";
            this.success = "";
            this.loading = true;

            if (!this.loginToken) {
                this.error = "Ошибка: токен не найден. Попробуйте войти заново.";
                this.loading = false;
                return;
            }

            window.ApiAuth.resendLoginCode(this.loginToken)
                .then(function () {
                    self.success = "Новый код отправлен на почту";
                    self.startLoginResendTimer(60);
                })
                .catch(function (e) {
                    self.error = e.message || "Не удалось отправить код";
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
            this.error = "";
            this.success = "";

            // Валидация
            if (this.registerForm.password.length < 8) {
                this.error = "Пароль должен быть минимум 8 символов";
                return;
            }

            var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(this.registerForm.email.trim())) {
                this.error = "Введите корректный email";
                return;
            }

            if (this.registerForm.login.trim().length < 3) {
                this.error = "Логин должен быть минимум 3 символа";
                return;
            }

            if (this.registerForm.surname.trim().length < 2) {
                this.error = "Фамилия должна быть минимум 2 символа";
                return;
            }

            if (this.registerForm.name.trim().length < 2) {
                this.error = "Имя должно быть минимум 2 символа";
                return;
            }

            // Отправляем запрос на регистрацию
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
                    // Сохраняем временный токен
                    self.registrationToken = data.token;
                    // Сохраняем email для отображения
                    self.registrationData.email = payload.email;
                    // Переключаем на шаг подтверждения
                    self.registerStep = 'verify';
                    self.success = "Код подтверждения отправлен на почту";
                    self.startResendTimer(60);
                })
                .catch(function (e) {
                    self.error = e.message || "Ошибка регистрации";
                })
                .finally(function () {
                    self.loading = false;
                });
        },

        // ПОДТВЕРЖДЕНИЕ КОДА РЕГИСТРАЦИИ (ШАГ 2)
        onVerifyCode: function () {
            var self = this;
            this.error = "";
            this.success = "";
            this.loading = true;

            if (this.confirmationCode.trim().length !== 6) {
                this.error = "Введите 6-значный код";
                this.loading = false;
                return;
            }

            if (!this.registrationToken) {
                this.error = "Ошибка: токен не найден. Попробуйте зарегистрироваться заново.";
                this.loading = false;
                return;
            }

            window.ApiAuth.verifyRegistration(
                this.registrationToken,
                this.confirmationCode.trim()
            )
                .then(function () {
                // Мгновенный редирект без задержки
                window.location.hash = "#/login";
                window.location.reload();
            })
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
                    self.success = "Новый код отправлен на почту";
                    self.startResendTimer(60);
                })
                .catch(function (e) {
                    self.error = e.message || "Не удалось отправить код";
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
            this.error = "";
            this.success = "";
            this.loading = true;

            var email = this.resetEmail.trim();
            var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                this.error = "Введите корректный email";
                this.loading = false;
                return;
            }

            window.ApiAuth.recoverAccount(email)
                .then(function (data) {
                    // Сохраняем временный токен
                    self.resetToken = data.token;
                    // Сохраняем email для отображения
                    self.resetEmail = email;
                    // Переключаем на шаг подтверждения
                    self.resetStep = 'verify';
                    self.success = "Код восстановления отправлен на почту";
                    self.startResetResendTimer(60);
                })
                .catch(function (e) {
                    self.error = e.message || "Не удалось отправить код";
                })
                .finally(function () {
                    self.loading = false;
                });
        },

        // ШАГ 2: Подтверждение кода восстановления
        onVerifyResetCode: function () {
            var self = this;
            this.error = "";
            this.success = "";
            this.loading = true;

            if (this.resetCode.trim().length !== 6) {
                this.error = "Введите 6-значный код";
                this.loading = false;
                return;
            }

            if (!this.resetToken) {
                this.error = "Ошибка: токен не найден. Попробуйте начать заново.";
                this.loading = false;
                return;
            }

            window.ApiAuth.verifyRecovery(
                this.resetToken,
                this.resetCode.trim()
            )
                .then(function (data) {
                    // Сохраняем новый токен для смены пароля
                    self.resetPasswordToken = data.token;
                    // Переключаем на шаг смены пароля
                    self.resetStep = 'change';
                })
                .catch(function (e) {
                    self.error = e.message || "Неверный код подтверждения";
                })
                .finally(function () {
                    self.loading = false;
                });
        },

        // ШАГ 3: Смена пароля
        onChangePassword: function () {
            var self = this;
            this.error = "";
            this.success = "";
            this.loading = true;

            if (this.resetNewPassword.length < 8) {
                this.error = "Пароль должен быть минимум 8 символов";
                this.loading = false;
                return;
            }

            if (this.resetNewPassword !== this.resetConfirmPassword) {
                this.error = "Пароли не совпадают";
                this.loading = false;
                return;
            }

            if (!this.resetPasswordToken) {
                this.error = "Ошибка: токен не найден. Попробуйте начать заново.";
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
                    self.success = "Пароль успешно изменен! Теперь вы можете войти.";
                    self.resetStep = 'done';
                })
                .catch(function (e) {
                    self.error = e.message || "Не удалось изменить пароль";
                })
                .finally(function () {
                    self.loading = false;
                });
        },

        // ПОВТОРНАЯ ОТПРАВКА КОДА ВОССТАНОВЛЕНИЯ
        onResendResetCode: function () {
            var self = this;
            this.error = "";
            this.success = "";
            this.loading = true;

            if (!this.resetToken) {
                this.error = "Ошибка: токен не найден. Попробуйте начать заново.";
                this.loading = false;
                return;
            }

            window.ApiAuth.resendRecoveryCode(this.resetToken)
                .then(function () {
                    self.success = "Новый код отправлен на почту";
                    self.startResetResendTimer(60);
                })
                .catch(function (e) {
                    self.error = e.message || "Не удалось отправить код";
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
            this.error = '';
            this.success = '';
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