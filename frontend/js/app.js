(function () {
    var createApp = Vue.createApp;

    createApp({
        data: function () {
            return {
                currentView: "login",
                loginForm: { username: "", password: "" },
                registerForm: {
                    surname: "",
                    name: "",
                    login: "",
                    email: "",
                    password: "",
                },
                error: "",
                success: "",
                loading: false,
                displayLogin: null,
            };
        },
        computed: {
            isAuthenticated: function () {
                var access = window.TokenStore.getAccessToken();
                var refresh = window.TokenStore.getRefreshToken();
                if (!access || !refresh) {
                    return false;
                }
                if (window.TokenStore.isTokenExpired(refresh, 0)) {
                    return false;
                }
                return true;
            },
        },
        mounted: function () {
            var self = this;
            this.syncRoute();
            window.addEventListener("hashchange", function () {
                self.syncRoute();
            });
        },
        methods: {
            syncRoute: function () {
                var hash = window.location.hash || "#/";
                if (hash === "#/" || hash === "#/home") {
                    if (this.isAuthenticated) {
                        this.currentView = "home";
                        this.displayLogin =
                            window.TokenStore.getLoginFromAccess() || this.loginForm.username;
                        this.error = "";
                    } else {
                        this.goLogin();
                    }
                    return;
                }
                if (hash === "#/register") {
                    this.currentView = "register";
                    this.error = "";
                    this.success = "";
                    return;
                }
                if (hash === "#/login") {
                    this.currentView = "login";
                    this.error = "";
                    return;
                }
                this.currentView = "login";
            },
            goHome: function () {
                window.location.hash = "#/";
            },
            goLogin: function () {
                window.location.hash = "#/login";
            },
            goRegister: function () {
                window.location.hash = "#/register";
            },
            onLogin: function () {
                var self = this;
                this.error = "";
                this.loading = true;
                window.Api.loginUser(this.loginForm.username, this.loginForm.password)
                    .then(function () {
                        self.displayLogin =
                            window.TokenStore.getLoginFromAccess() || self.loginForm.username;
                        self.goHome();
                    })
                    .catch(function (e) {
                        self.error = e.message || "Не удалось войти";
                    })
                    .finally(function () {
                        self.loading = false;
                    });
            },
            onRegister: function () {
                var self = this;
                this.error = "";
                this.success = "";
                this.loading = true;
                window.Api.registerUser({
                    surname: this.registerForm.surname.trim(),
                    name: this.registerForm.name.trim(),
                    login: this.registerForm.login.trim(),
                    email: this.registerForm.email.trim(),
                    password: this.registerForm.password,
                })
                    .then(function () {
                        self.success =
                            "Регистрация прошла успешно. Теперь можно войти, используя логин и пароль.";
                        self.registerForm.password = "";
                    })
                    .catch(function (e) {
                        self.error = e.message || "Ошибка регистрации";
                    })
                    .finally(function () {
                        self.loading = false;
                    });
            },
            onLogout: function () {
                window.Api.logout();
                this.loginForm.password = "";
                this.goLogin();
            },
            /**
             * Демонстрация: принудительно обновить access (как при истечении срока).
             */
            demoRefresh: function () {
                var self = this;
                this.error = "";
                window.Api.refreshAccessToken().catch(function (e) {
                    self.error = e.message || "Сессия истекла, войдите снова";
                    if (e.message === "REFRESH_EXPIRED" || !window.TokenStore.getRefreshToken()) {
                        self.goLogin();
                    }
                });
            },
            /**
             * Проверка ensureValidAccessToken (например, перед вызовами защищённого API).
             */
            demoEnsureAccess: function () {
                var self = this;
                this.error = "";
                window.Api.ensureValidAccessToken().catch(function (e) {
                    self.error = "Нужен повторный вход";
                    self.goLogin();
                });
            },
        },
        watch: {
            isAuthenticated: function (val) {
                if (!val && (this.currentView === "home")) {
                    this.error = "Сессия истекла. Войдите снова.";
                    this.goLogin();
                }
            },
        },
        template: document.getElementById("app-template").innerHTML,
    }).mount("#app");
})();
