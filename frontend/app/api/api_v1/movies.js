(function () {
    var apiUrl = window.ApiClient.apiUrl;
    var parseResponseJson = window.ApiClient.parseResponseJson;
    var readErrorMessage = window.ApiClient.readErrorMessage;
    var publicGetJson = window.ApiHttp.publicGetJson;
    var authFetchJson = window.ApiHttp.authFetchJson;

    function getMovies(page, size) {
        var p = page != null ? page : 1;
        var s = size != null ? size : 9;
        return publicGetJson("/api/v1/movies/?page=" + encodeURIComponent(p) + "&size=" + encodeURIComponent(s));
    }

    function searchMoviesWithFilters(filters, page, size) {
        var p = page != null ? page : 1;
        var s = size != null ? size : 9;

        var body = {
            search_query: filters.search_query || null,
            min_rating: filters.min_rating || null,
            max_rating: filters.max_rating || null,
            start_release_date: filters.start_release_date || null,
            end_release_date: filters.end_release_date || null,
            genre_id: filters.genre_id || null,
            sort_by: filters.sort_by || null,
            sorting_direction: filters.sorting_direction || "ASC"
        };

        Object.keys(body).forEach(key => {
            if (body[key] === null || body[key] === undefined) {
                delete body[key];
            }
        });

        return fetch(apiUrl("/api/v1/movies/search?page=" + encodeURIComponent(p) + "&size=" + encodeURIComponent(s)), {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify(body)
        }).then(function (res) {
            if (res.status === 429) {
                throw new Error("⚠️ Слишком много запросов. Подождите немного.");
            }
            return parseResponseJson(res).then(function (data) {
                if (!res.ok) {
                    throw new Error(readErrorMessage(data));
                }
                return data;
            });
        });
    }

    function searchMoviesByName(name, page, size) {
    var p = page != null ? page : 1;
    var s = size != null ? size : 9;
    var q = encodeURIComponent(name.trim());
    return publicGetJson("/api/v1/movies/search?movie_name=" + q + "&page=" + encodeURIComponent(p) + "&size=" + encodeURIComponent(s));
    }

    function getMoviesByGenre(genreId, page, size) {
        var p = page != null ? page : 1;
        var s = size != null ? size : 9;
        return publicGetJson("/api/v1/movies/genre/" + encodeURIComponent(genreId) + "?page=" + encodeURIComponent(p) + "&size=" + encodeURIComponent(s));
    }

    function getMovieById(movieId) {
        return publicGetJson("/api/v1/movies/" + encodeURIComponent(movieId) + "/");
    }

    function watchMovie(movieId) {
        var token = window.TokenStore.getAccessToken();
        if (!token) {
            return Promise.reject(new Error("Не авторизован"));
        }

        return authFetchJson("/api/v1/movies/watch", {
            method: "POST",
            body: { movie_id: movieId }
        });
    }

    function createMovie(data) {
        var token = window.TokenStore.getAccessToken();
        if (!token) return Promise.reject(new Error("Не авторизован"));

        return authFetchJson("/api/v1/movies/", {
            method: "POST",
            body: data
        });
    }

    function updateMovie(movieId, data) {
        var token = window.TokenStore.getAccessToken();
        if (!token) return Promise.reject(new Error("Не авторизован"));

        return authFetchJson("/api/v1/movies/" + encodeURIComponent(movieId) + "/", {
            method: "PUT",
            body: data
        });
    }

    function partialUpdateMovie(movieId, data) {
        var token = window.TokenStore.getAccessToken();
        if (!token) return Promise.reject(new Error("Не авторизован"));

        return authFetchJson("/api/v1/movies/" + encodeURIComponent(movieId) + "/", {
            method: "PATCH",
            body: data
        });
    }

    function deleteMovie(movieId) {
        var token = window.TokenStore.getAccessToken();
        if (!token) return Promise.reject(new Error("Не авторизован"));

        return authFetchJson("/api/v1/movies/" + encodeURIComponent(movieId) + "/", {
            method: "DELETE"
        });
    }

    window.ApiMovies = {
        getMovies: getMovies,
        searchMoviesWithFilters: searchMoviesWithFilters,
        searchMoviesByName: searchMoviesByName,
        getMoviesByGenre: getMoviesByGenre,
        getMovieById: getMovieById,
        watchMovie: watchMovie,
        createMovie: createMovie,
        updateMovie: updateMovie,
        partialUpdateMovie: partialUpdateMovie,
        deleteMovie: deleteMovie,
    };
})();
