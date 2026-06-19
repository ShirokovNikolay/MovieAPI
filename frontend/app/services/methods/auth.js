(function () {
    window.AppMethodsAuth = {
        // ==================== ЛОГИН С 2FA ====================
        onLogin: function () {
            var self = this;
            this.error = "";
            this.loading = true;

            window.ApiAuth.loginUser(this.loginForm.username, this.loginForm.password)
                .then(function (email) {
                    self.loginEmail = email;
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

            window.ApiAuth.confirmEmail({
                email: this.loginEmail,
                confirmation_code: this.loginCode.trim(),
            })
                .then(function (data) {
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

            window.ApiAuth.sendConfirmationCode(this.loginEmail, "two_factor_auth")
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
        // ОТПРАВКА КОДА НА ПОЧТУ (регистрация)
        onSendCode: function () {
            var self = this;
            this.error = "";
            this.success = "";
            this.loading = true;

            this.registrationData = {
                surname: this.registerForm.surname.trim(),
                name: this.registerForm.name.trim(),
                login: this.registerForm.login.trim(),
                email: this.registerForm.email.trim(),
                password: this.registerForm.password,
            };

            window.ApiAuth.sendConfirmationCode(this.registrationData.email, "verify_email")
                .then(function () {
                    self.registerStep = 'verify';
                    self.success = "Код подтверждения отправлен на почту";
                    self.startResendTimer(60);
                })
                .catch(function (e) {
                    self.error = e.message || "Не удалось отправить код";
                })
                .finally(function () {
                    self.loading = false;
                });
        },

        // ПОДТВЕРЖДЕНИЕ КОДА И РЕГИСТРАЦИЯ
        onVerifyCode: function () {
            var self = this;
            this.error = "";
            this.success = "";
            this.loading = true;

            var payload = {
                surname: this.registrationData.surname,
                name: this.registrationData.name,
                login: this.registrationData.login,
                email: this.registrationData.email,
                password: this.registrationData.password,
                confirmation_code: this.confirmationCode.trim(),
            };

            window.ApiAuth.registerUserWithCode(payload)
                .then(function () {
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

        // ПОВТОРНАЯ ОТПРАВКА КОДА (регистрация)
        onResendCode: function () {
            var self = this;
            this.error = "";
            this.success = "";
            this.loading = true;

            window.ApiAuth.sendConfirmationCode(this.registrationData.email, "verify_email")
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
            this.error = '';
            this.success = '';
            if (this.timerInterval) {
                clearInterval(this.timerInterval);
                this.timerInterval = null;
            }
        },

        // ОБНОВЛЕННАЯ РЕГИСТРАЦИЯ
        onRegister: function () {
            var self = this;
            this.error = "";
            this.success = "";

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

            this.onSendCode();
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
        // ШАГ 1: Отправка кода для восстановления
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

            window.ApiAuth.sendConfirmationCode(email, "reset_password")
                .then(function () {
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

        // ШАГ 2: Подтверждение кода и переход к смене пароля
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

            // Проверяем код через бэкенд
            // Для проверки кода используем тот же confirmEmail?
            // Если есть отдельный эндпоинт для проверки - используйте его
            // Пока просто переходим к шагу смены пароля
            self.resetStep = 'change';
            self.loading = false;
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

            var payload = {
                email: this.resetEmail,
                password: this.resetNewPassword,
                password_confirmation: this.resetConfirmPassword,
                confirmation_code: this.resetCode.trim(),
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

        // СБРОС ВОССТАНОВЛЕНИЯ (возврат к логину)
        onResetBackToLogin: function () {
            this.resetStep = 'form';
            this.resetEmail = '';
            this.resetCode = '';
            this.resetNewPassword = '';
            this.resetConfirmPassword = '';
            this.error = '';
            this.success = '';
            if (this.resetTimerInterval) {
                clearInterval(this.resetTimerInterval);
                this.resetTimerInterval = null;
            }
            this.currentView = 'login';
        },

        // ПОВТОРНАЯ ОТПРАВКА КОДА ДЛЯ ВОССТАНОВЛЕНИЯ
        onResendResetCode: function () {
            var self = this;
            this.error = "";
            this.success = "";
            this.loading = true;

            window.ApiAuth.sendConfirmationCode(this.resetEmail, "reset_password")
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