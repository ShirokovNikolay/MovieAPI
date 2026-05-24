(function () {
    window.AppMethodsAdminGenresConfirm = {
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
    };
})();
