(function () {
    window.AppMethodsMovieDetails = {
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
                console.log("applyFilters, movieFilters.genre_id:", this.movieFilters.genre_id);
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
    };
})();
