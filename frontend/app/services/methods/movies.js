(function () {
    window.AppMethodsMovies = {
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
                    genre_id: this.movieFilters.genre_id,
                    sort_by: this.movieFilters.sort_by,
                    sorting_direction: this.movieFilters.sorting_direction
                };

                console.log("Отправляемые фильтры:", filters);

                window.Api.searchMoviesWithFilters(filters, this.moviesPage, this.moviesSize)
                    .then(function (data) {
                        console.log("Ответ:", data);  // ← добавить
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
                console.log("loadMoviesByGenre, genreId:", genreId);
                var self = this;
                this.moviesLoading = true;
                this.error = "";
                this.selectedGenreId = genreId;
                this.selectedGenreName = genreName;
                this.moviesPage = 1;
                this.movieActiveSearch = "";
                this.movieSearchInput = "";

                // ОБНОВЛЯЕМ ФИЛЬТРЫ
                this.movieFilters.genre_id = genreId;
                console.log("movieFilters.genre_id после установки:", this.movieFilters.genre_id);
                this.movieFilters.search_query = "";

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
    };
})();
