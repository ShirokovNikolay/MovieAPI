(function () {
    window.AppMethodsAuth = {
        onLogin: function () {
            var self = this;
            this.error = "";
            this.loading = true;
            window.ApiAuth.loginUser(this.loginForm.username, this.loginForm.password)
                .then(function () {
                    window.location.hash = "#/";
                    window.location.reload();
                })
                .catch(function (e) {
                    self.error = e.message || "Не удалось войти";
                })
                .finally(function () {
                    self.loading = false;
                });
        },

        // ОТПРАВКА КОДА НА ПОЧТУ
        onSendCode: function () {
            var self = this;
            this.error = "";
            this.success = "";
            this.loading = true;

            // Сохраняем данные регистрации
            this.registrationData = {
                surname: this.registerForm.surname.trim(),
                name: this.registerForm.name.trim(),
                login: this.registerForm.login.trim(),
                email: this.registerForm.email.trim(),
                password: this.registerForm.password,
            };

            window.ApiAuth.sendConfirmationCode(this.registrationData.email)
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

        // ПОВТОРНАЯ ОТПРАВКА КОДА
        onResendCode: function () {
            var self = this;
            this.error = "";
            this.success = "";
            this.loading = true;

            window.ApiAuth.sendConfirmationCode(this.registrationData.email)
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

            // Валидация пароля
            if (this.registerForm.password.length < 8) {
                this.error = "Пароль должен быть минимум 8 символов";
                return;
            }

            // Валидация email
            var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(this.registerForm.email.trim())) {
                this.error = "Введите корректный email";
                return;
            }

            // Валидация логина
            if (this.registerForm.login.trim().length < 3) {
                this.error = "Логин должен быть минимум 3 символа";
                return;
            }

            // Отправляем код
            this.onSendCode();
        },

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

        // ТАЙМЕР ДЛЯ ПОВТОРНОЙ ОТПРАВКИ
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
    };
})();