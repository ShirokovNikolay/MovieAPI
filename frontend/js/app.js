(function () {
    var mountEl = document.getElementById("app");
    var tplEl = document.getElementById("app-template");

    if (typeof Vue === "undefined") {
        if (mountEl) {
            mountEl.innerHTML =
                '<div class="container py-5 text-light"><p class="alert alert-danger">Не удалось загрузить Vue.js. Проверьте доступ к сети и к CDN (cdn.jsdelivr.net).</p></div>';
        }
        return;
    }
    if (!tplEl || !mountEl) {
        if (mountEl) {
            mountEl.innerHTML =
                '<div class="container py-5 text-light"><p class="alert alert-danger">Не найден шаблон приложения (#app-template) или корень (#app).</p></div>';
        }
        return;
    }

    var tpl = tplEl.innerHTML;
    if (!tpl || !String(tpl).trim()) {
        mountEl.innerHTML =
            '<div class="container py-5 text-light"><p class="alert alert-danger">Шаблон приложения пуст.</p></div>';
        return;
    }

    var createApp = Vue.createApp;

    try {
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
                profileLoading: false,
                profileData: null,
                profileTab: "view",
                profileSuccess: "",
                fullUpdateForm: {
                    surname: "",
                    name: "",
                    login: "",
                    email: "",
                    password: "",
                },
                partialFlags: {
                    surname: false,
                    name: false,
                    login: false,
                    email: false,
                    password: false,
                },
                partialForm: {
                    surname: "",
                    name: "",
                    login: "",
                    email: "",
                    password: "",
                },
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
                if (hash === "#/profile") {
                    if (!this.isAuthenticated) {
                        this.goLogin();
                        return;
                    }
                    this.currentView = "profile";
                    this.error = "";
                    this.profileSuccess = "";
                    this.profileTab = "view";
                    this.loadProfile();
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
            loadProfile: function () {
                var self = this;
                this.profileLoading = true;
                this.profileSuccess = "";
                this.error = "";
                window.Api.getCurrentUserProfile()
                    .then(function (data) {
                        self.profileData = data;
                        self.fullUpdateForm = {
                            surname: data.surname,
                            name: data.name,
                            login: data.login,
                            email: data.email,
                            password: "",
                        };
                        self.partialForm = {
                            surname: "",
                            name: "",
                            login: "",
                            email: "",
                            password: "",
                        };
                        self.partialFlags = {
                            surname: false,
                            name: false,
                            login: false,
                            email: false,
                            password: false,
                        };
                    })
                    .catch(function (e) {
                        if (e.message === "REFRESH_EXPIRED") {
                            self.goLogin();
                            return;
                        }
                        self.error = e.message || "Не удалось загрузить профиль";
                    })
                    .finally(function () {
                        self.profileLoading = false;
                    });
            },
            onFullProfileUpdate: function () {
                var self = this;
                this.error = "";
                this.profileSuccess = "";
                this.loading = true;
                window.Api.updateCurrentUserProfile({
                    surname: self.fullUpdateForm.surname.trim(),
                    name: self.fullUpdateForm.name.trim(),
                    login: self.fullUpdateForm.login.trim(),
                    email: self.fullUpdateForm.email.trim(),
                    password: self.fullUpdateForm.password,
                })
                    .then(function (data) {
                        self.profileData = data;
                        self.fullUpdateForm = {
                            surname: data.surname,
                            name: data.name,
                            login: data.login,
                            email: data.email,
                            password: "",
                        };
                        self.profileSuccess = "Профиль полностью обновлён.";
                        return window.Api.refreshAccessToken().catch(function () {});
                    })
                    .then(function () {
                        self.displayLogin =
                            window.TokenStore.getLoginFromAccess() || self.profileData.login;
                    })
                    .catch(function (e) {
                        if (e.message === "REFRESH_EXPIRED") {
                            self.goLogin();
                            return;
                        }
                        self.error = e.message || "Ошибка полного обновления";
                    })
                    .finally(function () {
                        self.loading = false;
                    });
            },
            onPartialProfileUpdate: function () {
                var self = this;
                this.error = "";
                this.profileSuccess = "";
                var body = {};
                var flags = this.partialFlags;
                var form = this.partialForm;
                var labels = {
                    surname: "фамилия",
                    name: "имя",
                    login: "логин",
                    email: "email",
                    password: "пароль",
                };
                var keys = ["surname", "name", "login", "email", "password"];
                for (var i = 0; i < keys.length; i++) {
                    var k = keys[i];
                    if (!flags[k]) {
                        continue;
                    }
                    if (k === "password") {
                        if (!form.password) {
                            this.error = "Введите новый пароль для выбранного поля.";
                            return;
                        }
                        body.password = form.password;
                    } else {
                        var v = (form[k] || "").trim();
                        if (!v) {
                            this.error = "Заполните поле «" + labels[k] + "» или снимите галочку.";
                            return;
                        }
                        body[k] = v;
                    }
                }
                if (Object.keys(body).length === 0) {
                    this.error = "Отметьте поля, которые нужно изменить, и введите новые значения.";
                    return;
                }
                this.loading = true;
                window.Api.partialUpdateCurrentUserProfile(body)
                    .then(function (data) {
                        self.profileData = data;
                        self.fullUpdateForm = {
                            surname: data.surname,
                            name: data.name,
                            login: data.login,
                            email: data.email,
                            password: "",
                        };
                        self.profileSuccess = "Профиль частично обновлён.";
                        self.partialForm.password = "";
                        return window.Api.refreshAccessToken().catch(function () {});
                    })
                    .then(function () {
                        self.displayLogin =
                            window.TokenStore.getLoginFromAccess() || self.profileData.login;
                    })
                    .catch(function (e) {
                        if (e.message === "REFRESH_EXPIRED") {
                            self.goLogin();
                            return;
                        }
                        self.error = e.message || "Ошибка частичного обновления";
                    })
                    .finally(function () {
                        self.loading = false;
                    });
            },
            confirmDeleteProfile: function () {
                var self = this;
                this.error = "";
                this.loading = true;
                window.Api.deleteCurrentUserProfile()
                    .then(function () {
                        var el = document.getElementById("deleteProfileModal");
                        if (el && typeof bootstrap !== "undefined") {
                            var Modal = bootstrap.Modal;
                            var inst = Modal.getInstance(el) || Modal.getOrCreateInstance(el);
                            inst.hide();
                        }
                        window.Api.logout();
                        self.profileData = null;
                        self.goLogin();
                    })
                    .catch(function (e) {
                        if (e.message === "REFRESH_EXPIRED") {
                            self.goLogin();
                            return;
                        }
                        self.error = e.message || "Не удалось удалить профиль";
                    })
                    .finally(function () {
                        self.loading = false;
                    });
            },
        },
        watch: {
            isAuthenticated: function (val) {
                if (!val && (this.currentView === "home" || this.currentView === "profile")) {
                    this.error = "Сессия истекла. Войдите снова.";
                    this.goLogin();
                }
            },
        },
        template: tpl,
    }).mount("#app");
    } catch (err) {
        var msg = err && err.message ? err.message : String(err);
        mountEl.innerHTML =
            '<div class="container py-5 text-light"><p class="alert alert-danger">Ошибка запуска интерфейса: ' +
            msg.replace(/</g, "&lt;") +
            "</p></div>";
    }
})();
