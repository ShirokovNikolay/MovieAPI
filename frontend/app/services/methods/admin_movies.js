(function () {
    window.AppMethodsAdminMovies = {
            // Загрузка фильмов для админки
            loadAdminMovies: function () {
                var self = this;
                this.adminMoviesLoading = true;

                window.Api.getMovies(this.adminMoviesPage, this.adminMoviesSize)
                    .then(function (data) {
                        self.adminMoviesList = data.movie_list || [];
                        self.adminMoviesTotal = data.total || 0;
                        if (typeof data.page === "number") self.adminMoviesPage = data.page;
                        if (typeof data.size === "number") self.adminMoviesSize = data.size;
                    })
                    .catch(function (e) {
                        self.error = e.message || "Не удалось загрузить фильмы";
                    })
                    .finally(function () {
                        self.adminMoviesLoading = false;
                    });
            },

            goAdminMoviesPage: function (nextPage) {
                if (nextPage < 1) return;
                this.adminMoviesPage = nextPage;
                this.loadAdminMovies();
            },

            // Форма для фильма
            openCreateMovieForm: function () {
                this.editingMovie = null;
                this.movieForm = {
                    name: "",
                    description: "",
                    rating: 5,
                    preview_url: "",
                    source_url: "",
                    genre_id: null,
                    release_date: new Date().toISOString().split('T')[0]
                };
                this.showMovieForm = true;
            },

            openEditMovieForm: function (movie) {
                this.editingMovie = movie;
                this.movieForm = {
                    name: movie.name,
                    description: movie.description,
                    rating: movie.rating,
                    preview_url: movie.preview_url || "",
                    source_url: movie.source_url || "",
                    genre_id: movie.genre_id,
                    release_date: movie.release_date ? movie.release_date.split('T')[0] : ""
                };
                this.showMovieForm = true;
            },

            closeMovieForm: function () {
                this.showMovieForm = false;
                this.editingMovie = null;
            },

            submitMovieForm: function () {
                var self = this;
                if (!this.movieForm.name.trim()) {
                    this.error = "Название фильма обязательно";
                    return;
                }
                if (!this.movieForm.genre_id) {
                    this.error = "Выберите жанр";
                    return;
                }

                this.movieFormSubmitting = true;

                var data = {
                    name: this.movieForm.name,
                    description: this.movieForm.description,
                    rating: parseFloat(this.movieForm.rating),
                    preview_url: this.movieForm.preview_url,
                    source_url: this.movieForm.source_url,
                    genre_id: this.movieForm.genre_id,
                    release_date: this.movieForm.release_date
                };

                var promise;
                if (this.editingMovie) {
                    promise = window.Api.updateMovie(this.editingMovie.id, data);
                } else {
                    promise = window.Api.createMovie(data);
                }

                promise
                    .then(function () {
                        self.closeMovieForm();
                        self.loadAdminMovies();
                        self.loadMovies(); // обновляем список на главной
                    })
                    .catch(function (e) {
                        self.error = e.message || "Ошибка сохранения фильма";
                    })
                    .finally(function () {
                        self.movieFormSubmitting = false;
                    });
            },

            confirmDeleteGenre: function (genre) {
                this.deletingGenreId = genre.id;
                this.deletingGenreName = genre.name;
                var modalEl = document.getElementById("deleteGenreModal");
                if (modalEl && typeof bootstrap !== "undefined") {
                    var modal = new bootstrap.Modal(modalEl);
                    modal.show();
                }
            },

            confirmDeleteGenreConfirmed: function () {
                var self = this;
                this.genreDeleting = true;

                window.Api.deleteGenre(this.deletingGenreId)
                    .then(function () {
                        self.loadAdminGenres();
                        self.loadGenres();
                        var modalEl = document.getElementById("deleteGenreModal");
                        if (modalEl) {
                            var modal = bootstrap.Modal.getInstance(modalEl);
                            if (modal) modal.hide();
                        }
                    })
                    .catch(function (e) {
                        self.error = e.message || "Не удалось удалить жанр";
                    })
                    .finally(function () {
                        self.genreDeleting = false;
                        self.deletingGenreId = null;
                        self.deletingGenreName = null;
                    });
            },

            confirmDeleteMovie: function (movie) {
                console.log("confirmDeleteMovie, movie.id:", movie.id, "тип:", typeof movie.id);
                this.deletingMovieId = Number(movie.id);
                this.deletingMovieName = movie.name;
                if (isNaN(this.deletingMovieId)) {
                    console.error("Невалидный ID фильма");
                    this.error = "Ошибка ID фильма";
                    return;
                }
                var modalEl = document.getElementById("deleteMovieModal");
                if (modalEl && typeof bootstrap !== "undefined") {
                    var modal = new bootstrap.Modal(modalEl);
                    modal.show();
                }
            },

            confirmDeleteMovieConfirmed: function () {
                var self = this;
                this.movieDeleting = true;

                window.Api.deleteMovie(this.deletingMovieId)
                    .then(function () {
                        self.loadAdminMovies();
                        self.loadMovies();
                        var modalEl = document.getElementById("deleteMovieModal");
                        if (modalEl) {
                            var modal = bootstrap.Modal.getInstance(modalEl);
                            if (modal) modal.hide();
                        }
                    })
                    .catch(function (e) {
                        self.error = e.message || "Не удалось удалить фильм";
                    })
                    .finally(function () {
                        self.movieDeleting = false;
                        self.deletingMovieId = null;
                        self.deletingMovieName = null;
                    });
            },
    };
})();
