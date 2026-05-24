(function () {
    window.AppMethodsFavorites = {
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
    };
})();
