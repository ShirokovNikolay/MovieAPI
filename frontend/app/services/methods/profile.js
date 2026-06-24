(function () {
    window.AppMethodsProfile = {
            loadProfile: function () {
                var self = this;
                this.profileLoading = true;
                this.profileSuccess = "";
                this.error = "";
                window.Api.getCurrentUserProfile()
                    .then(function (data) {
                        self.profileData = data;
                        self.isAdmin = data.role === "admin";
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
                        window.location.reload();
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
    };
})();
