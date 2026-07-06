(function () {
    var publicGetJson = window.ApiHttp.publicGetJson;
    var authFetchJson = window.ApiHttp.authFetchJson;

    function getGenres(page, size) {
        var p = page != null ? page : 1;
        var s = size != null ? size : 10;
        return publicGetJson(
            "/api/v1/genres/?page=" + encodeURIComponent(p) + "&size=" + encodeURIComponent(s)
        );
    }

    function searchGenresByName(name, page, size) {
        var p = page != null ? page : 1;
        var s = size != null ? size : 10;
        var q =
            "search_query=" +
            encodeURIComponent(name) +
            "&page=" +
            encodeURIComponent(p) +
            "&size=" +
            encodeURIComponent(s);
        return publicGetJson("/api/v1/genres/search?" + q);
    }

    function createGenre(data) {
        var token = window.TokenStore.getAccessToken();
        if (!token) return Promise.reject(new Error("Не авторизован"));

        return authFetchJson("/api/v1/genres/", {
            method: "POST",
            body: data
        });
    }

    function updateGenre(genreId, data) {
        var token = window.TokenStore.getAccessToken();
        if (!token) return Promise.reject(new Error("Не авторизован"));

        return authFetchJson("/api/v1/genres/" + encodeURIComponent(genreId) + "/", {
            method: "PUT",
            body: data
        });
    }

    function partialUpdateGenre(genreId, data) {
        var token = window.TokenStore.getAccessToken();
        if (!token) return Promise.reject(new Error("Не авторизован"));

        return authFetchJson("/api/v1/genres/" + encodeURIComponent(genreId) + "/", {
            method: "PATCH",
            body: data
        });
    }

    function deleteGenre(genreId) {
        var token = window.TokenStore.getAccessToken();
        if (!token) return Promise.reject(new Error("Не авторизован"));

        return authFetchJson("/api/v1/genres/" + encodeURIComponent(genreId) + "/", {
            method: "DELETE"
        });
    }

    window.ApiGenres = {
        getGenres: getGenres,
        searchGenresByName: searchGenresByName,
        createGenre: createGenre,
        updateGenre: updateGenre,
        partialUpdateGenre: partialUpdateGenre,
        deleteGenre: deleteGenre,
    };
})();
