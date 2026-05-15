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
                currentView: "catalog",
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
                genreList: [],
                genrePage: 1,
                genreSize: 10,
                genreLoading: false,
                genreSearchInput: "",
                genreActiveSearch: "",

                // Фильмы
                moviesList: [],
                moviesPage: 1,
                moviesSize: 9,
                moviesLoading: false,

                movieSearchInput: "",
                movieActiveSearch: "",
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
            genreHasNext: function () {
                return this.genreList.length === this.genreSize && this.genreSize >= 1;
            },
            genreHasPrev: function () {
                return this.genrePage > 1;
            },
            moviesHasNext: function () {
                return this.moviesList.length === this.moviesSize;
            },
            moviesHasPrev: function () {
                return this.moviesPage > 1;
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
                if (hash === "#/" || hash === "#/home" || hash === "#/catalog") {
                    this.currentView = "catalog";
                    if (this.isAuthenticated) {
                        this.displayLogin =
                            window.TokenStore.getLoginFromAccess() || this.loginForm.username;
                    }
                    this.error = "";
                    return;
                }
                if (hash === "#/genres") {
                    this.currentView = "genres";
                    this.error = "";
                    this.loadGenres();
                    return;
                }
                if (hash === "#/movies") {
                    this.currentView = "movies";
                    this.error = "";
                    this.loadMovies();
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
                window.location.hash = "#/";
            },
            goCatalog: function () {
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
                        self.goCatalog();
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
                this.goCatalog();
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
            loadGenres: function () {
                var self = this;
                this.genreLoading = true;
                this.error = "";
                var p = this.genrePage;
                var s = this.genreSize;
                var q = (this.genreActiveSearch || "").trim();
                var req = q
                    ? window.Api.searchGenresByName(q, p, s)
                    : window.Api.getGenres(p, s);
                req.then(function (data) {
                    self.genreList = data.genre_list || [];
                    if (typeof data.page === "number") {
                        self.genrePage = data.page;
                    }
                    if (typeof data.size === "number") {
                        self.genreSize = data.size;
                    }
                })
                    .catch(function (e) {
                        self.error = e.message || "Не удалось загрузить жанры";
                        self.genreList = [];
                    })
                    .finally(function () {
                        self.genreLoading = false;
                    });
            },
            applyGenreSearch: function () {
                this.genreActiveSearch = (this.genreSearchInput || "").trim();
                this.genrePage = 1;
                this.loadGenres();
            },
            clearGenreSearch: function () {
                this.genreSearchInput = "";
                this.genreActiveSearch = "";
                this.genrePage = 1;
                this.loadGenres();
            },
            goGenrePage: function (nextPage) {
                if (nextPage < 1) {
                    return;
                }
                this.genrePage = nextPage;
                this.loadGenres();
            },

            loadMovies: function () {
                var self = this;
                this.moviesLoading = true;
                this.error = "";

                var searchQuery = this.movieActiveSearch || "";
                var promise;

                if (searchQuery) {
                    promise = window.Api.searchMoviesByName(searchQuery, this.moviesPage, this.moviesSize);
                } else {
                    promise = window.Api.getMovies(this.moviesPage, this.moviesSize);
                }

                promise.then(function (data) {
                    self.moviesList = (data.movie_list || []).map(function(movie) {
                        if (!movie.preview_url || movie.preview_url === "string") {
                            movie.preview_url = "https://via.placeholder.com/300x450?text=No+Poster";
                        }
                        return movie;
                    });
                    console.log("Загружено фильмов:", self.moviesList.length);
                    if (typeof data.page === "number") {
                        self.moviesPage = data.page;
                    }
                    if (typeof data.size === "number") {
                        self.moviesSize = data.size;
                    }
                })
                .catch(function (e) {
                    self.error = e.message || "Не удалось загрузить фильмы";
                    self.moviesList = [];
                })
                .finally(function () {
                    self.moviesLoading = false;
                });
            },

            showMovieDetails: function (movieId) {
                console.log("Клик по фильму ID:", movieId);
                // Позже можно добавить модальное окно или отдельную страницу
            },

            goMoviesPage: function (nextPage) {
                if (nextPage < 1) return;
                this.moviesPage = nextPage;
                this.loadMovies();
            },
            applyMovieSearch: function () {
                this.movieActiveSearch = (this.movieSearchInput || "").trim();
                this.moviesPage = 1;
                this.loadMovies();
            },

            clearMovieSearch: function () {
                this.movieSearchInput = "";
                this.movieActiveSearch = "";
                this.moviesPage = 1;
                this.loadMovies();
            },
            formatDate: function (dateString) {
                if (!dateString) return "—";
                try {
                    var date = new Date(dateString);
                    return date.toLocaleDateString("ru-RU");
                } catch (e) {
                    return dateString;
                }
            },
            truncateText: function (text, maxLength) {
                if (!text) return "";
                if (text.length <= maxLength) return text;
                return text.substring(0, maxLength) + "...";
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
                if (!val && this.currentView === "profile") {
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
