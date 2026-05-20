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

                // Фильтры для фильмов
                movieFilters: {
                    search_query: "",
                    min_rating: null,
                    max_rating: null,
                    start_release_date: "",
                    end_release_date: "",
                    genre_id: null,
                    sort_by: null,
                    sorting_direction: "ASC"
                },
                showFilters: false,

                currentMovie: null,
                movieDetailsLoading: false,

                reviewsList: [],
                reviewsPage: 1,
                reviewsSize: 10,
                reviewsTotal: 0,
                reviewsLoading: false,
                deletingReviewSource: null,

                userReview: null,
                reviewRating: 5,
                reviewText: "",
                reviewSubmitting: false,
                showReviewForm: false,

                // Мои отзывы
                myReviewsList: [],
                myReviewsPage: 1,
                myReviewsSize: 10,
                myReviewsLoading: false,
                myReviewsTotal: 0,

                // Фильтры по жанру
                selectedGenreId: null,
                selectedGenreName: null,

                reviewsSortBy: "default",  // default, newest, oldest

                editingReview: null,
                editReviewRating: 5,
                editReviewText: "",

                deleteReviewId: null,

                favoritesCount: 0,
                isFavorite: false,
                favoriteToggling: false,

                favoritesList: [],
                favoritesPage: 1,
                favoritesSize: 12,
                favoritesLoading: false,

                watchHistoryList: [],
                watchHistoryPage: 1,
                watchHistorySize: 15,
                watchHistoryLoading: false,
                watchHistoryCount: 0,
                deletingHistoryId: null,
                // Фильтрация истории по датам
                historyStartDate: "",
                historyEndDate: "",
                historyFilterApplied: false,

                reviewsSortType: "default",
                reviewsSortOrder: "",
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

            favoritesHasNext: function () {
                return this.favoritesList.length === this.favoritesSize;
            },
            favoritesHasPrev: function () {
                return this.favoritesPage > 1;
            },

            reviewsHasNext: function () {
                return this.reviewsList.length === this.reviewsSize;
            },
            reviewsHasPrev: function () {
                return this.reviewsPage > 1;
            },
            userFullName: function () {
                if (this.profileData && this.profileData.surname && this.profileData.name) {
                    return this.profileData.surname + ' ' + this.profileData.name;
                }
                return this.displayLogin || 'Пользователь';
            },
            myReviewsHasNext: function () {
                return this.myReviewsList.length === this.myReviewsSize;
            },
            myReviewsHasPrev: function () {
                return this.myReviewsPage > 1;
            },
            watchHistoryHasNext: function () {
                return this.watchHistoryList.length === this.watchHistorySize;
            },
            watchHistoryHasPrev: function () {
                return this.watchHistoryPage > 1;
            },
        },
        mounted: function () {
            var self = this;
            this.syncRoute();
            this.loadGenres();
            window.addEventListener("hashchange", function () {
                self.syncRoute();
            });
        },
        methods: {
            syncRoute: function () {
                var hash = window.location.hash || "#/";
                if (hash === "#/" || hash === "#/home" || hash === "#/catalog") {
                    this.currentView = "catalog";
                    if (this.isAuthenticated && !this.profileData) {
                        this.loadProfile();
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
                if (hash.startsWith("#/movie/")) {
                    var movieId = parseInt(hash.split("/")[2]);
                    if (!isNaN(movieId)) {
                        this.currentView = "movieDetails";
                        this.error = "";
                        this.loadMovieDetails(movieId);
                        return;
                    }
                }
                if (hash === "#/favorites") {
                    if (!this.isAuthenticated) {
                        this.goLogin();
                        return;
                    }
                    this.currentView = "favorites";
                    this.loadFavorites();
                    return;
                }
                if (hash === "#/history") {
                    if (!this.isAuthenticated) {
                        this.goLogin();
                        return;
                    }
                    this.currentView = "history";
                    if (this.historyFilterApplied) {
                        this.loadWatchHistoryWithFilter();
                    } else {
                        this.loadWatchHistory();
                    }
                    return;
                }
                if (hash === "#/my-reviews") {
                    if (!this.isAuthenticated) {
                        this.goLogin();
                        return;
                    }
                    this.currentView = "myReviews";
                    this.loadMyReviews();
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
                        window.location.href = "#/";
                        window.location.reload();
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
                        window.location.href = "#/";
                        window.location.reload();
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

            toggleFilters: function () {
                this.showFilters = !this.showFilters;
            },

            applyFilters: function () {
                this.moviesPage = 1;
                this.loadMoviesWithFilters();
            },

            clearFilters: function () {
                this.movieFilters = {
                    search_query: "",
                    min_rating: null,
                    max_rating: null,
                    start_release_date: "",
                    end_release_date: "",
                    genre_id: null,
                    sort_by: null,
                    sorting_direction: "ASC"
                };
                this.movieSearchInput = "";
                this.movieActiveSearch = "";
                this.selectedGenreId = null;
                this.selectedGenreName = null;
                this.moviesPage = 1;
                this.loadMoviesWithFilters();
            },

            loadMoviesWithFilters: function () {
                var self = this;
                this.moviesLoading = true;
                this.error = "";

                var filters = {
                    search_query: this.movieFilters.search_query || null,
                    min_rating: this.movieFilters.min_rating,
                    max_rating: this.movieFilters.max_rating,
                    start_release_date: this.movieFilters.start_release_date || null,
                    end_release_date: this.movieFilters.end_release_date || null,
                    genre_id: this.selectedGenreId || this.movieFilters.genre_id,
                    sort_by: this.movieFilters.sort_by,
                    sorting_direction: this.movieFilters.sorting_direction
                };

                window.Api.searchMoviesWithFilters(filters, this.moviesPage, this.moviesSize)
                    .then(function (data) {
                        self.moviesList = (data.movie_list || []).map(function(movie) {
                            if (!movie.preview_url || movie.preview_url === "string") {
                                movie.preview_url = "https://via.placeholder.com/300x450?text=No+Poster";
                            }
                            return movie;
                        });
                        if (typeof data.page === "number") self.moviesPage = data.page;
                        if (typeof data.size === "number") self.moviesSize = data.size;
                    })
                    .catch(function (e) {
                        self.error = e.message || "Не удалось загрузить фильмы";
                        self.moviesList = [];
                    })
                    .finally(function () {
                        self.moviesLoading = false;
                    });
            },

            loadMovies: function () {
                var self = this;
                this.moviesLoading = true;
                this.error = "";

                var searchQuery = this.movieActiveSearch || "";
                var promise;

                if (this.selectedGenreId) {
                    // Если выбран жанр — грузим по жанру
                    promise = window.Api.getMoviesByGenre(this.selectedGenreId, this.moviesPage, this.moviesSize);
                } else if (searchQuery) {
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
            loadMoviesByGenre: function (genreId, genreName) {
                var self = this;
                this.moviesLoading = true;
                this.error = "";
                this.selectedGenreId = genreId;
                this.selectedGenreName = genreName;
                this.moviesPage = 1;
                this.movieActiveSearch = "";
                this.movieSearchInput = "";

                // Сбрасываем фильтры
                this.movieFilters = {
                    search_query: "",
                    min_rating: null,
                    max_rating: null,
                    start_release_date: "",
                    end_release_date: "",
                    genre_id: genreId,
                    sort_by: null,
                    sorting_direction: "ASC"
                };

                // Используем новый эндпоинт
                window.Api.searchMoviesWithFilters(this.movieFilters, this.moviesPage, this.moviesSize)
                    .then(function (data) {
                        self.moviesList = (data.movie_list || []).map(function(movie) {
                            if (!movie.preview_url || movie.preview_url === "string") {
                                movie.preview_url = "https://via.placeholder.com/300x450?text=No+Poster";
                            }
                            return movie;
                        });
                        if (typeof data.page === "number") self.moviesPage = data.page;
                        if (typeof data.size === "number") self.moviesSize = data.size;
                        self.currentView = "movies";
                    })
                    .catch(function (e) {
                        self.error = e.message || "Не удалось загрузить фильмы";
                        self.moviesList = [];
                    })
                    .finally(function () {
                        self.moviesLoading = false;
                    });
            },
            clearGenreFilter: function () {
                this.selectedGenreId = null;
                this.selectedGenreName = null;
                this.moviesPage = 1;
                this.movieActiveSearch = "";
                this.movieSearchInput = "";
                this.loadMovies();
            },

            loadMovieDetails: function (movieId) {
                var self = this;
                this.movieDetailsLoading = true;
                this.error = "";
                this.reviewsPage = 1;
                this.reviewsList = [];
                this.userReview = null;
                this.showReviewForm = false;

                window.Api.getMovieById(movieId)
                    .then(function (movie) {
                        self.currentMovie = movie;
                        self.currentView = "movieDetails";
                        self.loadReviewsWithSort(movie.id, self.reviewsSortBy);
                        self.loadUserReview(movie.id);
                        self.loadFavoritesData(movie.id);
                    })
                    .catch(function (e) {
                        self.error = e.message || "Не удалось загрузить детали фильма";
                    })
                    .finally(function () {
                        self.movieDetailsLoading = false;
                    });
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


            showMovieDetails: function (movieId) {
                var self = this;
                this.movieDetailsLoading = true;
                this.error = "";
                this.reviewsPage = 1;
                this.reviewsList = [];
                this.userReview = null;
                this.showReviewForm = false;

                window.Api.getMovieById(movieId)
                    .then(function (movie) {
                        self.currentMovie = movie;
                        self.currentView = "movieDetails";
                        self.loadReviewsWithSort(movie.id, self.reviewsSortType, self.reviewsSortOrder);
                        self.loadUserReview(movie.id);
                        console.log("showMovieDetails: вызов loadFavoritesData для movie.id =", movie.id);
                        self.loadFavoritesData(movie.id);
                    })
                    .catch(function (e) {
                        self.error = e.message || "Не удалось загрузить детали фильма";
                    })
                    .finally(function () {
                        self.movieDetailsLoading = false;
                    });
            },

            watchMovieNow: function () {
                var self = this;
                if (!this.isAuthenticated) {
                    this.error = "Для просмотра фильма необходимо войти в аккаунт";
                    return;
                }

                if (!this.currentMovie || !this.currentMovie.source_url) {
                    this.error = "Ссылка на источник не найдена";
                    return;
                }

                // Отправляем запрос для записи истории (фоном)
                window.Api.watchMovie(this.currentMovie.id);

                // Сразу открываем ссылку
                window.open(this.currentMovie.source_url, '_blank');
            },

            loadReviews: function (movieId) {
                var self = this;
                this.reviewsLoading = true;

                window.Api.getMovieReviews(movieId, this.reviewsPage, this.reviewsSize)
                    .then(function (data) {
                        self.reviewsList = data.review_list || [];
                        self.reviewsTotal = data.total || 0;
                        if (typeof data.page === "number") {
                            self.reviewsPage = data.page;
                        }
                        if (typeof data.size === "number") {
                            self.reviewsSize = data.size;
                        }
                    })
                    .catch(function (e) {
                        console.error("Ошибка загрузки отзывов:", e);
                        self.reviewsList = [];
                    })
                    .finally(function () {
                        self.reviewsLoading = false;
                    });
            },

            loadReviewsWithSort: function (movieId, sortType, sortOrder) {
                console.log("loadReviewsWithSort вызван", movieId, sortType, sortOrder);
                var self = this;
                this.reviewsLoading = true;

                var promise;

                if (sortType === "default") {
                    promise = window.Api.getMovieReviews(movieId, this.reviewsPage, this.reviewsSize);
                } else if (sortType === "date") {
                    if (sortOrder === "desc") {
                        console.log("Вызов getMovieReviewsNewest");
                        promise = window.Api.getMovieReviewsNewest(movieId, this.reviewsPage, this.reviewsSize);
                    } else {
                        console.log("Вызов getMovieReviewsOldest");
                        promise = window.Api.getMovieReviewsOldest(movieId, this.reviewsPage, this.reviewsSize);
                    }
                } else {
                    if (sortOrder === "desc") {
                        console.log("Вызов getMovieReviewsTopRated");
                        promise = window.Api.getMovieReviewsTopRated(movieId, this.reviewsPage, this.reviewsSize);
                    } else {
                        console.log("Вызов getMovieReviewsLowRated");
                        promise = window.Api.getMovieReviewsLowRated(movieId, this.reviewsPage, this.reviewsSize);
                    }
                }

                promise
                    .then(function (data) {
                        console.log("Данные получены:", data);
                        self.reviewsList = data.review_list || [];
                        if (typeof data.page === "number") self.reviewsPage = data.page;
                        if (typeof data.size === "number") self.reviewsSize = data.size;
                    })
                    .catch(function (e) {
                        console.error("Ошибка загрузки отзывов:", e);
                        self.reviewsList = [];
                    })
                    .finally(function () {
                        self.reviewsLoading = false;
                    });
            },

            changeReviewsSort: function (event) {
                if (event) event.stopPropagation();
                console.log("changeReviewsSort вызван", this.reviewsSortType, this.reviewsSortOrder);
                this.reviewsPage = 1;
                if (this.currentMovie) {
                    this.loadReviewsWithSort(this.currentMovie.id, this.reviewsSortType, this.reviewsSortOrder);
                }
            },

            changeReviewsSortWithValues: function (sortType, sortOrder) {
                console.log("changeReviewsSortWithValues", sortType, sortOrder);
                this.reviewsSortType = sortType;
                this.reviewsSortOrder = sortOrder;
                this.reviewsPage = 1;
                if (this.currentMovie) {
                    this.loadReviewsWithSort(this.currentMovie.id, sortType, sortOrder);
                }
            },

            startEditReview: function (review) {
                this.editingReview = review;
                this.editReviewRating = review.rating;
                this.editReviewText = review.review_text || "";
            },

            cancelEditReview: function () {
                this.editingReview = null;
                this.editReviewRating = 5;
                this.editReviewText = "";
            },

            submitEditReview: function () {
                var self = this;
                if (!this.editReviewText.trim()) {
                    this.error = "Введите текст отзыва";
                    return;
                }

                this.reviewSubmitting = true;

                window.Api.partialUpdateReview(this.editingReview.id, this.editReviewRating, this.editReviewText.trim())
                    .then(function (updatedReview) {
                        // Обновляем отзыв в списке
                        var index = self.reviewsList.findIndex(r => r.id === updatedReview.id);
                        if (index !== -1) {
                            self.reviewsList[index] = updatedReview;
                        }
                        // Если редактируем свой отзыв
                        if (self.userReview && self.userReview.id === updatedReview.id) {
                            self.userReview = updatedReview;
                            self.reviewRating = updatedReview.rating;
                            self.reviewText = updatedReview.review_text || "";
                        }
                        self.cancelEditReview();
                        // Перезагружаем список для обновления пагинации
                        self.loadReviewsWithSort(self.currentMovie.id, self.reviewsSortBy);
                    })
                    .catch(function (e) {
                        self.error = e.message || "Не удалось обновить отзыв";
                    })
                    .finally(function () {
                        self.reviewSubmitting = false;
                    });
            },

            confirmDeleteReview: function (reviewId) {
                this.deleteReviewId = reviewId;
                var modalEl = document.getElementById("deleteReviewModal");
                if (modalEl && typeof bootstrap !== "undefined") {
                    var modal = new bootstrap.Modal(modalEl);
                    modal.show();
                }
            },

            confirmDeleteReviewConfirmed: function () {
                var self = this;
                this.reviewSubmitting = true;

                window.Api.deleteReview(this.deletingReviewId)
                    .then(function () {
                        if (self.deletingReviewSource === "myReviews") {
                            // Удаляем из списка "Мои отзывы"
                            self.myReviewsList = self.myReviewsList.filter(function(r) {
                                return r.id !== self.deletingReviewId;
                            });
                            self.myReviewsTotal--;
                        } else {
                            // Удаляем из списка отзывов под фильмом
                            self.reviewsList = self.reviewsList.filter(function(r) {
                                return r.id !== self.deletingReviewId;
                            });
                            if (self.userReview && self.userReview.id === self.deletingReviewId) {
                                self.userReview = null;
                            }
                            self.loadReviewsWithSort(self.currentMovie.id, self.reviewsSortType, self.reviewsSortOrder);
                        }

                        var modalEl = document.getElementById("deleteReviewModal");
                        if (modalEl) {
                            var modal = bootstrap.Modal.getInstance(modalEl);
                            if (modal) modal.hide();
                        }
                        self.deletingReviewId = null;
                        self.deletingReviewSource = null;
                    })
                    .catch(function (e) {
                        self.error = e.message || "Не удалось удалить отзыв";
                    })
                    .finally(function () {
                        self.reviewSubmitting = false;
                    });
            },

            changeReviewsSort: function (sortOrder) {
                this.reviewsPage = 1;
                this.reviewsSortBy = sortOrder;
                if (this.currentMovie) {
                    this.loadReviewsWithSort(this.currentMovie.id, sortOrder);
                }
            },

            loadMyReviews: function () {
                var self = this;
                this.myReviewsLoading = true;

                window.Api.getMyReviews(this.myReviewsPage, this.myReviewsSize)
                    .then(function (data) {
                        self.myReviewsList = data.review_list || [];
                        self.myReviewsTotal = data.total || 0;
                        if (typeof data.page === "number") self.myReviewsPage = data.page;
                        if (typeof data.size === "number") self.myReviewsSize = data.size;
                    })
                    .catch(function (e) {
                        self.error = e.message || "Не удалось загрузить отзывы";
                        self.myReviewsList = [];
                    })
                    .finally(function () {
                        self.myReviewsLoading = false;
                    });
            },

            goMyReviewsPage: function (nextPage) {
                if (nextPage < 1) return;
                this.myReviewsPage = nextPage;
                this.loadMyReviews();
            },

            editReviewFromList: function (review) {
                // Открываем детальную страницу фильма с модалкой редактирования
                window.location.hash = "#/movie/" + review.movie.id;
                // Можно передать данные для открытия формы редактирования
                this.pendingEditReview = review;
            },

            deleteMyReview: function (reviewId) {
                this.deletingReviewId = reviewId;
                this.deletingReviewSource = "myReviews";
                var modalEl = document.getElementById("deleteReviewModal");
                if (modalEl && typeof bootstrap !== "undefined") {
                    var modal = new bootstrap.Modal(modalEl);
                    modal.show();
                }
            },

            goReviewsPage: function (nextPage) {
                if (nextPage < 1) return;
                this.reviewsPage = nextPage;
                if (this.currentMovie) {
                    this.loadReviews(this.currentMovie.id);
                }
            },

            backToMovies: function () {
                this.currentView = "movies";
                this.currentMovie = null;
                this.movieDetailsLoading = false;
                // Сбросить фильтры
                this.selectedGenreId = null;
                this.selectedGenreName = null;
                this.movieActiveSearch = "";
                this.movieSearchInput = "";
                this.moviesPage = 1;
                // Перезагрузить список фильмов
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

            loadUserReview: function (movieId) {
                var self = this;
                if (!this.isAuthenticated) {
                    this.userReview = null;
                    return;
                }

                window.Api.getUserReview(movieId)
                    .then(function (data) {
                        self.userReview = data;
                        if (data) {
                            self.reviewRating = data.rating;
                            self.reviewText = data.review_text || "";
                        }
                    })
                    .catch(function () {
                        self.userReview = null;
                    });
            },

            toggleReviewForm: function () {
                this.showReviewForm = !this.showReviewForm;
                if (!this.showReviewForm) {
                    this.reviewRating = 5;
                    this.reviewText = "";
                }
            },

            submitReview: function () {
                var self = this;
                if (!this.isAuthenticated) {
                    this.error = "Для написания отзыва необходимо войти";
                    return;
                }

                if (!this.reviewText.trim()) {
                    this.error = "Введите текст отзыва";
                    return;
                }

                this.reviewSubmitting = true;
                this.error = "";

                window.Api.createReview(this.currentMovie.id, this.reviewRating, this.reviewText.trim())
                    .then(function (newReview) {
                        self.userReview = newReview;
                        self.showReviewForm = false;
                        self.reviewRating = 5;
                        self.reviewText = "";
                        // Перезагружаем список отзывов
                        self.reviewsPage = 1;
                        self.loadReviews(self.currentMovie.id);
                    })
                    .catch(function (e) {
                        self.error = e.message || "Не удалось отправить отзыв";
                    })
                    .finally(function () {
                        self.reviewSubmitting = false;
                    });
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
            loadFavoritesData: function (movieId) {
                var self = this;
                console.log("loadFavoritesData: начало, movieId =", movieId);

                window.Api.getFavoritesCount(movieId)
                    .then(function(data) {
                        console.log("getFavoritesCount вернул:", data);
                        // data уже число 3, не нужно брать data.count
                        self.favoritesCount = data;
                        console.log("self.favoritesCount теперь =", self.favoritesCount);
                    })
                    .catch(function(e) {
                        console.error("Ошибка getFavoritesCount:", e);
                    });

                if (this.isAuthenticated) {
                    window.Api.checkFavorite(movieId)
                        .then(function(isFav) {
                            console.log("checkFavorite вернул:", isFav);
                            self.isFavorite = isFav;
                        });
                }
            },

            toggleFavorite: function () {
                var self = this;
                if (!this.isAuthenticated) {
                    this.error = "Для добавления в избранное необходимо войти";
                    return;
                }

                this.favoriteToggling = true;

                if (this.isFavorite) {
                    window.Api.removeFromFavorites(this.currentMovie.id)
                        .then(() => { self.isFavorite = false; self.favoritesCount--; })
                        .catch(e => console.error(e))
                        .finally(() => self.favoriteToggling = false);
                } else {
                    window.Api.addToFavorites(this.currentMovie.id)
                        .then(() => { self.isFavorite = true; self.favoritesCount++; })
                        .catch(e => console.error(e))
                        .finally(() => self.favoriteToggling = false);
                }
            },

            loadFavorites: function () {
                console.log("1. loadFavorites начал");
                var self = this;
                this.favoritesLoading = true;

                window.Api.getFavorites(this.favoritesPage, this.favoritesSize)
                    .then(function (data) {
                        console.log("2. getFavorites вернул:", data);
                        var favoriteList = data.favorite_movie_list || [];
                        console.log("3. favoriteList:", favoriteList);
                        self.favoritesList = favoriteList.map(function(item) {
                            var movie = item.movie;
                            movie.favorite_id = item.id;
                            return movie;
                        });
                        console.log("4. Итоговый favoritesList:", self.favoritesList);
                    })
                    .catch(function(e) {
                        console.error("Ошибка:", e);
                    })
                    .finally(function() {
                        self.favoritesLoading = false;
                    });
            },

            goFavoritesPage: function (nextPage) {
                if (nextPage < 1) return;
                this.favoritesPage = nextPage;
                this.loadFavorites();
            },

            goToMovieFromFavorites: function (movieId) {
                window.location.hash = "#/movie/" + movieId;
            },

            confirmDeleteFavorite: function (favoriteId, movieId, event) {
                console.log("Метод вызван, favoriteId:", favoriteId, "movieId:", movieId);
                event.stopPropagation();
                this.deletingFavoriteId = favoriteId;
                this.deletingFavoriteMovieId = movieId;

                // Показываем модальное окно через bootstrap
                var modalEl = document.getElementById('deleteFavoriteModal');
                if (modalEl) {
                    var modal = new bootstrap.Modal(modalEl);
                    modal.show();
                } else {
                    console.error("Модальное окно не найдено");
                    // Если модального окна нет, сразу удаляем
                    this.confirmDeleteFavoriteConfirmed();
                }
            },

            confirmDeleteFavoriteConfirmed: function () {
                var self = this;
                window.Api.removeFavoriteById(this.deletingFavoriteId)
                    .then(function() {
                        self.favoritesList = self.favoritesList.filter(function(m) {
                            return m.favorite_id !== self.deletingFavoriteId;
                        });
                        // Закрываем модальное окно
                        var modalEl = document.getElementById('deleteFavoriteModal');
                        if (modalEl) {
                            var modal = bootstrap.Modal.getInstance(modalEl);
                            if (modal) modal.hide();
                        }
                        console.log("Удалено, новый список:", self.favoritesList);
                    })
                    .catch(function(e) {
                        console.error("Ошибка удаления:", e);
                    });
            },

            // ========== ИСТОРИЯ ПРОСМОТРОВ ==========
            loadWatchHistory: function () {
                console.log("loadWatchHistory ВЫЗВАН");
                var self = this;
                this.watchHistoryLoading = true;

                window.Api.getWatchHistory(this.watchHistoryPage, this.watchHistorySize)
                    .then(function (data) {
                        console.log("ДАННЫЕ ОТ API:", data);
                        var historyList = data.watch_history_list || [];
                        console.log("HISTORY_LIST:", historyList);
                        self.watchHistoryList = historyList.map(function(item) {
                            return {
                                id: item.id,
                                watched_at: item.watched_at,
                                movie: item.movie
                            };
                        });
                        console.log("ИТОГОВЫЙ watchHistoryList:", self.watchHistoryList);
                        console.log("ДЛИНА:", self.watchHistoryList.length);
                    })
                    .catch(function (e) {
                        console.error("Ошибка:", e);
                    })
                    .finally(function () {
                        self.watchHistoryLoading = false;
                    });

                window.Api.getWatchHistoryCount()
                    .then(function(data) {
                        console.log("Количество (сырые данные):", data);
                        // data может быть просто числом 24, а не объектом
                        self.watchHistoryCount = typeof data === 'number' ? data : (data.count || 0);
                        console.log("self.watchHistoryCount:", self.watchHistoryCount);
                    })
                    .catch(function(e) {
                        console.error("Ошибка загрузки количества:", e);
                    });
            },

            applyHistoryDateFilter: function () {
                    this.historyFilterApplied = true;
                    this.watchHistoryPage = 1;
                    this.loadWatchHistoryWithFilter();
                },

            clearHistoryDateFilter: function () {
                this.historyStartDate = "";
                this.historyEndDate = "";
                this.historyFilterApplied = false;
                this.watchHistoryPage = 1;
                this.loadWatchHistory();
            },

            loadWatchHistoryWithFilter: function () {
                var self = this;
                this.watchHistoryLoading = true;

                window.Api.getWatchHistoryByDateRange(
                    this.historyStartDate,
                    this.historyEndDate,
                    this.watchHistoryPage,
                    this.watchHistorySize
                )
                    .then(function (data) {
                        var historyList = data.watch_history_list || [];
                        self.watchHistoryList = historyList.map(function(item) {
                            return {
                                id: item.id,
                                watched_at: item.watched_at,
                                movie: item.movie
                            };
                        });
                        if (typeof data.page === "number") self.watchHistoryPage = data.page;
                        if (typeof data.size === "number") self.watchHistorySize = data.size;
                    })
                    .catch(function (e) {
                        self.error = e.message || "Не удалось загрузить историю";
                        self.watchHistoryList = [];
                    })
                    .finally(function () {
                        self.watchHistoryLoading = false;
                    });
            },

            goToMovieFromHistory: function (movieId) {
                window.location.hash = "#/movie/" + movieId;
            },

            goWatchHistoryPage: function (nextPage) {
                if (nextPage < 1) return;
                this.watchHistoryPage = nextPage;
                this.loadWatchHistory();
            },

            confirmDeleteHistoryItem: function (historyId, event) {
                event.stopPropagation();
                this.deletingHistoryId = historyId;
                var modalEl = document.getElementById("deleteHistoryItemModal");
                if (modalEl && typeof bootstrap !== "undefined") {
                    var modal = new bootstrap.Modal(modalEl);
                    modal.show();
                }
            },

            confirmDeleteHistoryItemConfirmed: function () {
                var self = this;
                window.Api.deleteWatchHistoryItem(this.deletingHistoryId)
                    .then(function() {
                        self.watchHistoryList = self.watchHistoryList.filter(function(item) {
                            return item.id !== self.deletingHistoryId;
                        });
                        self.watchHistoryCount--;
                        var modalEl = document.getElementById("deleteHistoryItemModal");
                        if (modalEl) {
                            var modal = bootstrap.Modal.getInstance(modalEl);
                            if (modal) modal.hide();
                        }
                    })
                    .catch(function(e) {
                        self.error = e.message || "Не удалось удалить запись";
                    });
            },

            confirmClearAllHistory: function () {
                var modalEl = document.getElementById("clearAllHistoryModal");
                if (modalEl && typeof bootstrap !== "undefined") {
                    var modal = new bootstrap.Modal(modalEl);
                    modal.show();
                }
            },

            confirmClearAllHistoryConfirmed: function () {
                var self = this;
                window.Api.clearAllWatchHistory()
                    .then(function() {
                        self.watchHistoryList = [];
                        self.watchHistoryCount = 0;
                        self.watchHistoryPage = 1;
                        var modalEl = document.getElementById("clearAllHistoryModal");
                        if (modalEl) {
                            var modal = bootstrap.Modal.getInstance(modalEl);
                            if (modal) modal.hide();
                        }
                    })
                    .catch(function(e) {
                        self.error = e.message || "Не удалось очистить историю";
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
