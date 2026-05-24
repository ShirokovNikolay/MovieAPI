(function () {
    window.AppMethodsGenres = {
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
    };
})();
