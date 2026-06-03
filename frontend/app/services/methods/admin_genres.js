(function () {
    window.AppMethodsAdminGenres = {
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

            resetGenrePosterInput: function () {
                this.genrePosterFile = null;
                this.genrePosterFileName = "";
                var input = document.getElementById("genre-poster-file");
                if (input) input.value = "";
            },

            onGenrePosterSelected: function (event) {
                var file = event.target.files && event.target.files[0];
                this.genrePosterFile = file || null;
                this.genrePosterFileName = file ? file.name : "";
            },

            openCreateGenreForm: function () {
                this.editingGenre = null;
                this.genreForm = { name: "", description: "", preview_url: "" };
                this.resetGenrePosterInput();
                this.showGenreForm = true;
            },

            openEditGenreForm: function (genre) {
                this.editingGenre = genre;

                // Извлекаем ВЕСЬ ключ после genre-posters/
                var fullUrl = genre.preview_url || "";
                var key = "";

                if (fullUrl) {
                    var parts = fullUrl.split('/');
                    var bucketIndex = parts.indexOf('genre-posters');
                    if (bucketIndex !== -1) {
                        // Берем всё после genre-posters
                        key = parts.slice(bucketIndex + 1).join('/');
                    } else {
                        key = parts[parts.length - 1];
                    }
                }

                this.genreForm = {
                    name: genre.name,
                    description: genre.description,
                    preview_url: key,
                };
                this.resetGenrePosterInput();
                this.showGenreForm = true;
            },

            closeGenreForm: function () {
                this.showGenreForm = false;
                this.editingGenre = null;
                this.genreForm = { name: "", description: "", preview_url: "" };
                this.resetGenrePosterInput();
            },

            submitGenreForm: function () {
                var self = this;
                if (!this.genreForm.name.trim()) {
                    this.error = "Название жанра обязательно";
                    return;
                }

                if (!this.editingGenre && !this.genrePosterFile) {
                    this.error = "Выберите файл постера";
                    return;
                }

                this.genreFormSubmitting = true;
                this.error = "";

                var saveGenre = function (posterValue) {
                    var payload = {
                        name: self.genreForm.name.trim(),
                        description: self.genreForm.description,
                        preview_url: posterValue
                    };

                    var promise;
                    if (self.editingGenre) {
                        promise = window.Api.updateGenre(self.editingGenre.id, payload);
                    } else {
                        promise = window.Api.createGenre(payload);
                    }

                    return promise
                        .then(function () {
                            self.closeGenreForm();
                            self.loadAdminGenres();
                            self.loadGenres();
                        })
                        .catch(function (e) {
                            self.error = e.message || "Ошибка сохранения жанра";
                        });
                };

                if (this.genrePosterFile) {
                    window.MediaUpload.uploadGenrePoster(this.genrePosterFile)
                        .then(saveGenre)
                        .catch(function (e) {
                            self.error = e.message || "Ошибка загрузки постера";
                        })
                        .finally(function () {
                            self.genreFormSubmitting = false;
                        });
                } else if (this.editingGenre) {
                    var oldPosterValue = this.genreForm.preview_url || "";
                    saveGenre(oldPosterValue).finally(function () {
                        self.genreFormSubmitting = false;
                    });
                } else {
                    saveGenre("").finally(function () {
                        self.genreFormSubmitting = false;
                    });
                }
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
