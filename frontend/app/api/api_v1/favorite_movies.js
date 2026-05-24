(function () {
    var apiUrl = window.ApiClient.apiUrl;
    var authFetchJson = window.ApiHttp.authFetchJson;
    var publicGetJson = window.ApiHttp.publicGetJson;

    function getFavorites(page, size) {
        var p = page != null ? page : 1;
        var s = size != null ? size : 12;
        return authFetchJson("/api/v1/favorite-movies/about-me?page=" + encodeURIComponent(p) + "&size=" + encodeURIComponent(s));
    }

    function getFavoritesCount(movieId) {
        console.log("Запрос count для movieId:", movieId);
        return publicGetJson("/api/v1/favorite-movies/count/" + encodeURIComponent(movieId))
            .then(function(data) {
                console.log("Ответ count:", data);
                return data.count || data || 0;
            });
    }

    function addToFavorites(movieId) {
        var token = window.TokenStore.getAccessToken();
        if (!token) {
            return Promise.reject(new Error("Не авторизован"));
        }

        return authFetchJson("/api/v1/favorite-movies/", {
            method: "POST",
            body: { movie_id: movieId }
        });
    }

    function removeFromFavorites(movieId) {
        var token = window.TokenStore.getAccessToken();
        if (!token) {
            return Promise.reject(new Error("Не авторизован"));
        }

        return authFetchJson("/api/v1/favorite-movies/movies/" + encodeURIComponent(movieId), {
            method: "DELETE"
        });
    }

    function removeFavoriteById(favoriteMovieId) {
        var token = window.TokenStore.getAccessToken();
        if (!token) {
            return Promise.reject(new Error("Не авторизован"));
        }

        return authFetchJson("/api/v1/favorite-movies/" + encodeURIComponent(favoriteMovieId), {
            method: "DELETE"
        });
    }

    function isFavorite(movieId) {
        // Проверяем, добавлен ли фильм в избранное текущим пользователем
        var token = window.TokenStore.getAccessToken();
        if (!token) {
            return Promise.resolve(false);
        }

        return authFetchJson("/api/v1/favorite-movies/count/" + encodeURIComponent(movieId))
            .then(function(data) {
                return data.is_favorite === true;
            })
            .catch(function() {
                return false;
            });
    }

    function checkFavorite(movieId) {
        var token = window.TokenStore.getAccessToken();
        if (!token) return Promise.resolve(false);

        return fetch(apiUrl("/api/v1/favorite-movies/check/" + encodeURIComponent(movieId)), {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + token,
                "Accept": "application/json"
            }
        })
        .then(function(res) {
            return res.json();
        })
        .then(function(data) {
            // data может быть просто true, а не объектом
            return data === true || data.is_favorite === true;
        })
        .catch(function() {
            return false;
        });
    }

    window.ApiFavoriteMovies = {
        getFavorites: getFavorites,
        getFavoritesCount: getFavoritesCount,
        addToFavorites: addToFavorites,
        removeFromFavorites: removeFromFavorites,
        removeFavoriteById: removeFavoriteById,
        isFavorite: isFavorite,
        checkFavorite: checkFavorite,
    };
})();
