(function () {
    window.AppMethodsAdminGenres = {
            // Загрузка жанров для админки
            loadAdminGenres: function () {
                var self = this;
                this.adminGenresLoading = true;

                window.Api.getGenres(this.adminGenresPage, this.adminGenresSize)
                    .then(function (data) {
                        self.adminGenresList = data.genre_list || [];
                        self.adminGenresTotal = data.total || 0;
                        if (typeof data.page === "number") self.adminGenresPage = data.page;
                        if (typeof data.size === "number") self.adminGenresSize = data.size;
                    })
                    .catch(function (e) {
                        self.error = e.message || "Не удалось загрузить жанры";
                    })
                    .finally(function () {
                        self.adminGenresLoading = false;
                    });
            },

            goAdminGenresPage: function (nextPage) {
                if (nextPage < 1) return;
                this.adminGenresPage = nextPage;
                this.loadAdminGenres();
            },

            // Форма для жанра
            openCreateGenreForm: function () {
                this.editingGenre = null;
                this.genreForm = { name: "", description: "", preview_url: "" };
                this.showGenreForm = true;
            },

            openEditGenreForm: function (genre) {
                this.editingGenre = genre;
                this.genreForm = {
                    name: genre.name,
                    description: genre.description,
                    preview_url: genre.preview_url || ""
                };
                this.showGenreForm = true;
            },

            closeGenreForm: function () {
                this.showGenreForm = false;
                this.editingGenre = null;
                this.genreForm = { name: "", description: "", preview_url: "" };
            },

            submitGenreForm: function () {
                var self = this;
                if (!this.genreForm.name.trim()) {
                    this.error = "Название жанра обязательно";
                    return;
                }

                this.genreFormSubmitting = true;

                var promise;
                if (this.editingGenre) {
                    promise = window.Api.updateGenre(this.editingGenre.id, this.genreForm);
                } else {
                    promise = window.Api.createGenre(this.genreForm);
                }

                promise
                    .then(function () {
                        self.closeGenreForm();
                        self.loadAdminGenres();
                        self.loadGenres(); // обновляем список жанров на главной
                    })
                    .catch(function (e) {
                        self.error = e.message || "Ошибка сохранения жанра";
                    })
                    .finally(function () {
                        self.genreFormSubmitting = false;
                    });
            },

            confirmDeleteGenre: function (genre) {
                var self = this;
                if (confirm("Удалить жанр \"" + genre.name + "\"? Все фильмы этого жанра останутся без жанра.")) {
                    window.Api.deleteGenre(genre.id)
                        .then(function () {
                            self.loadAdminGenres();
                            self.loadGenres();
                        })
                        .catch(function (e) {
                            self.error = e.message || "Не удалось удалить жанр";
                        });
                }
            },
    };
})();
