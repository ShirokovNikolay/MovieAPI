(function () {
    var base = function () {
        return typeof window.__API_BASE__ === "string" ? window.__API_BASE__ : "";
    };

    function apiUrl(path) {
        var b = base();
        if (!path.startsWith("/")) {
            path = "/" + path;
        }
        return b + path;
    }

    var refreshInFlight = null;

    function parseResponseJson(res) {
        return res.text().then(function (text) {
            if (!text) {
                return null;
            }
            try {
                return JSON.parse(text);
            } catch (e) {
                return { message: text || res.statusText };
            }
        });
    }

    function readErrorMessage(data) {
        if (!data) {
            return "Ошибка запроса";
        }
        // Обработка ошибки 429
        if (data.detail && data.detail.includes("Too Many Requests")) {
            return "⚠️ Слишком много запросов. Пожалуйста, подождите немного.";
        }
        if (typeof data.message === "string") {
            return data.message;
        }
        if (Array.isArray(data.detail)) {
            return data.detail
                .map(function (d) {
                    if (typeof d === "string") {
                        return d;
                    }
                    if (d && d.msg) {
                        return d.msg;
                    }
                    return JSON.stringify(d);
                })
                .join("; ");
        }
        if (typeof data.detail === "string") {
            return data.detail;
        }
        return "Ошибка запроса";
    }

    /**
     * Обновляет access по refresh. Ответ refresh может не содержать новый refresh — сохраняем старый.
     */
    function refreshAccessToken() {
        var refresh = window.TokenStore.getRefreshToken();
        if (!refresh || window.TokenStore.isTokenExpired(refresh, 30)) {
            window.TokenStore.clearTokens();
            return Promise.reject(new Error("REFRESH_EXPIRED"));
        }
        if (refreshInFlight) {
            return refreshInFlight;
        }
        refreshInFlight = fetch(apiUrl("/api/v1/auth/refresh"), {
            method: "POST",
            headers: {
                Authorization: "Bearer " + refresh,
                Accept: "application/json",
            },
        })
            .then(function (res) {
                return parseResponseJson(res).then(function (data) {
                    if (!res.ok) {
                        window.TokenStore.clearTokens();
                        throw new Error(readErrorMessage(data));
                    }
                    var newAccess = data.access_token;
                    var newRefresh = data.refresh_token;
                    window.TokenStore.setTokens(newAccess, newRefresh || refresh);
                    return newAccess;
                });
            })
            .finally(function () {
                refreshInFlight = null;
            });
        return refreshInFlight;
    }

    /**
     * Гарантирует актуальный access: при истечении срока вызывает refresh_access_token.
     */
    function ensureValidAccessToken() {
        var access = window.TokenStore.getAccessToken();
        var refresh = window.TokenStore.getRefreshToken();
        if (!refresh || window.TokenStore.isTokenExpired(refresh, 30)) {
            window.TokenStore.clearTokens();
            return Promise.reject(new Error("REFRESH_EXPIRED"));
        }
        if (!access || window.TokenStore.isTokenExpired(access, 30)) {
            return refreshAccessToken();
        }
        return Promise.resolve(access);
    }

    /**
     * fetch с Bearer access; при 401 один раз пробует refresh и повторяет запрос.
     */
    function authFetch(path, options) {
        options = options || {};
        var tryOnce = function (afterRefresh) {
            return ensureValidAccessToken()
                .then(function (token) {
                    var headers = Object.assign({}, options.headers || {}, {
                        Authorization: "Bearer " + token,
                    });
                    return fetch(apiUrl(path), Object.assign({}, options, { headers: headers }));
                })
                .then(function (res) {
                    if (res.status === 401 && !afterRefresh) {
                        return refreshAccessToken().then(function () {
                            return tryOnce(true);
                        });
                    }
                    return res;
                });
        };
        return tryOnce(false);
    }

    function registerUser(payload) {
        return fetch(apiUrl("/api/v1/auth/register"), {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
            body: JSON.stringify(payload),
        }).then(function (res) {
            return parseResponseJson(res).then(function (data) {
                if (!res.ok) {
                    throw new Error(readErrorMessage(data));
                }
                return data;
            });
        });
    }

    function loginUser(username, password) {
        var body = new URLSearchParams();
        body.set("username", username);
        body.set("password", password);
        return fetch(apiUrl("/api/v1/auth/login"), {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                Accept: "application/json",
            },
            body: body.toString(),
        }).then(function (res) {
            return parseResponseJson(res).then(function (data) {
                if (!res.ok) {
                    throw new Error(readErrorMessage(data));
                }
                window.TokenStore.setTokens(data.access_token, data.refresh_token);
                return data;
            });
        });
    }

    function logout() {
        window.TokenStore.clearTokens();
    }

    function authFetchJson(path, options) {
        options = options || {};
        var headers = Object.assign({ Accept: "application/json" }, options.headers || {});
        var body = options.body;
        var method = options.method || "GET";
        if (body !== undefined && body !== null && typeof body === "object" && !(body instanceof FormData)) {
            body = JSON.stringify(body);
            headers["Content-Type"] = "application/json";
        }
        return authFetch(path, { method: method, headers: headers, body: body }).then(function (res) {
            if (res.status === 429) {
                throw new Error("⚠️ Слишком много запросов. Подождите немного.");
            }
            if (res.status === 204) {
                if (!res.ok) {
                    return parseResponseJson(res).then(function (data) {
                        throw new Error(readErrorMessage(data));
                    });
                }
                return null;
            }
            return parseResponseJson(res).then(function (data) {
                if (!res.ok) {
                    throw new Error(readErrorMessage(data));
                }
                return data;
            });
        });
    }

    function getCurrentUserProfile() {
        return authFetchJson("/api/v1/users/me/", { method: "GET" });
    }

    function updateCurrentUserProfile(payload) {
        return authFetchJson("/api/v1/users/me/", { method: "PUT", body: payload });
    }

    function partialUpdateCurrentUserProfile(payload) {
        return authFetchJson("/api/v1/users/me/", { method: "PATCH", body: payload });
    }

    function deleteCurrentUserProfile() {
        return authFetchJson("/api/v1/users/me/", { method: "DELETE" });
    }

    function publicGetJson(pathWithQuery) {
        return fetch(apiUrl(pathWithQuery), {
            method: "GET",
            headers: { Accept: "application/json" },
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
            "genre_name=" +
            encodeURIComponent(name) +
            "&page=" +
            encodeURIComponent(p) +
            "&size=" +
            encodeURIComponent(s);
        return publicGetJson("/api/v1/genres/search?" + q);
    }

    // ========== ФИЛЬМЫ ==========
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

    function getMovieReviewsNewest(movieId, page, size) {
        var p = page != null ? page : 1;
        var s = size != null ? size : 10;
        return publicGetJson("/api/v1/reviews/movie/" + encodeURIComponent(movieId) + "/top-newest?page=" + encodeURIComponent(p) + "&size=" + encodeURIComponent(s));
    }

    function getMovieReviewsOldest(movieId, page, size) {
        var p = page != null ? page : 1;
        var s = size != null ? size : 10;
        return publicGetJson("/api/v1/reviews/movie/" + encodeURIComponent(movieId) + "/top-oldest?page=" + encodeURIComponent(p) + "&size=" + encodeURIComponent(s));
    }

    function getMovieReviewsTopRated(movieId, page, size) {
        var p = page != null ? page : 1;
        var s = size != null ? size : 10;
        return publicGetJson("/api/v1/reviews/movie/" + encodeURIComponent(movieId) + "/top-rated?page=" + encodeURIComponent(p) + "&size=" + encodeURIComponent(s));
    }

    function getMovieReviewsLowRated(movieId, page, size) {
        var p = page != null ? page : 1;
        var s = size != null ? size : 10;
        return publicGetJson("/api/v1/reviews/movie/" + encodeURIComponent(movieId) + "/low-rated?page=" + encodeURIComponent(p) + "&size=" + encodeURIComponent(s));
    }

    function searchMoviesByName(name, page, size) {
    var p = page != null ? page : 1;
    var s = size != null ? size : 9;
    var q = encodeURIComponent(name.trim());
    return publicGetJson("/api/v1/movies/search?movie_name=" + q + "&page=" + encodeURIComponent(p) + "&size=" + encodeURIComponent(s));
    }

    // ========== ФИЛЬМЫ ПО ЖАНРУ ==========
    function getMoviesByGenre(genreId, page, size) {
        var p = page != null ? page : 1;
        var s = size != null ? size : 9;
        return publicGetJson("/api/v1/movies/genre/" + encodeURIComponent(genreId) + "?page=" + encodeURIComponent(p) + "&size=" + encodeURIComponent(s));
    }

    // ========== ДЕТАЛИ ФИЛЬМА ==========
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

    // ========== ОТЗЫВЫ ==========
    function getMovieReviews(movieId, page, size) {
        var p = page != null ? page : 1;
        var s = size != null ? size : 10;
        return publicGetJson("/api/v1/reviews/movie/" + encodeURIComponent(movieId) + "/?page=" + encodeURIComponent(p) + "&size=" + encodeURIComponent(s));
    }

    function getUserReview(movieId) {
        var token = window.TokenStore.getAccessToken();
        if (!token) {
            return Promise.reject(new Error("Не авторизован"));
        }

        return authFetchJson("/api/v1/reviews/about-me/movie/" + encodeURIComponent(movieId));
    }

    function createReview(movieId, rating, reviewText) {
        var token = window.TokenStore.getAccessToken();
        if (!token) {
            return Promise.reject(new Error("Не авторизован"));
        }

        return authFetchJson("/api/v1/reviews/", {
            method: "POST",
            body: {
                movie_id: movieId,
                rating: rating,
                review_text: reviewText
            }
        });
    }

    function getMyReviews(page, size) {
        var p = page != null ? page : 1;
        var s = size != null ? size : 10;
        var token = window.TokenStore.getAccessToken();
        if (!token) {
            return Promise.reject(new Error("Не авторизован"));
        }

        return authFetchJson("/api/v1/reviews/about-me/?page=" + encodeURIComponent(p) + "&size=" + encodeURIComponent(s));
    }

    // ========== РЕДАКТИРОВАНИЕ И УДАЛЕНИЕ ОТЗЫВА ==========
    function partialUpdateReview(reviewId, rating, reviewText) {
        var token = window.TokenStore.getAccessToken();
        if (!token) {
            return Promise.reject(new Error("Не авторизован"));
        }

        var body = {};
        if (rating !== undefined) body.rating = rating;
        if (reviewText !== undefined) body.review_text = reviewText;

        return fetch(apiUrl("/api/v1/reviews/" + encodeURIComponent(reviewId) + "/"), {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
                "Accept": "application/json"
            },
            body: JSON.stringify(body)
        }).then(function(res) {
            return parseResponseJson(res).then(function(data) {
                if (!res.ok) {
                    throw new Error(readErrorMessage(data));
                }
                return data;
            });
        });
    }

    function deleteReview(reviewId) {
        var token = window.TokenStore.getAccessToken();
        if (!token) {
            return Promise.reject(new Error("Не авторизован"));
        }

        return fetch(apiUrl("/api/v1/reviews/" + encodeURIComponent(reviewId) + "/"), {
            method: "DELETE",
            headers: {
                "Authorization": "Bearer " + token,
                "Accept": "application/json"
            }
        }).then(function(res) {
            if (res.status === 204) {
                return { success: true };
            }
            return parseResponseJson(res).then(function(data) {
                if (!res.ok) {
                    throw new Error(readErrorMessage(data));
                }
                return data;
            });
        });
    }

    // ========== ИЗБРАННОЕ ==========
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

    // ========== ИСТОРИЯ ПРОСМОТРОВ ==========
    function getWatchHistory(page, size) {
        var p = page != null ? page : 1;
        var s = size != null ? size : 10;
        return authFetchJson("/api/v1/watch-history/about-me/?page=" + encodeURIComponent(p) + "&size=" + encodeURIComponent(s));
    }

    function getWatchHistoryByDateRange(startDate, endDate, page, size) {
        var p = page != null ? page : 1;
        var s = size != null ? size : 20;
        var token = window.TokenStore.getAccessToken();
        if (!token) {
            return Promise.reject(new Error("Не авторизован"));
        }

        var url = "/api/v1/watch-history/about-me/by-date-range?page=" + encodeURIComponent(p) + "&size=" + encodeURIComponent(s);
        if (startDate) url += "&start_date=" + encodeURIComponent(startDate);
        if (endDate) url += "&end_date=" + encodeURIComponent(endDate);

        return authFetchJson(url);
    }

    function getWatchHistoryCount() {
        return authFetchJson("/api/v1/watch-history/about-me/count");
    }

    function clearAllWatchHistory() {
        return authFetchJson("/api/v1/watch-history/about-me/", { method: "DELETE" });
    }
    function deleteWatchHistoryItem(historyId) {
        return authFetchJson("/api/v1/watch-history/" + encodeURIComponent(historyId) + "/", { method: "DELETE" });
    }

    // ========== АДМИН: УПРАВЛЕНИЕ ЖАНРАМИ ==========
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

    // ========== АДМИН: УПРАВЛЕНИЕ ФИЛЬМАМИ ==========
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

    window.Api = {
        apiUrl: apiUrl,
        refreshAccessToken: refreshAccessToken,
        ensureValidAccessToken: ensureValidAccessToken,
        authFetch: authFetch,
        authFetchJson: authFetchJson,
        getCurrentUserProfile: getCurrentUserProfile,
        updateCurrentUserProfile: updateCurrentUserProfile,
        partialUpdateCurrentUserProfile: partialUpdateCurrentUserProfile,
        deleteCurrentUserProfile: deleteCurrentUserProfile,
        registerUser: registerUser,
        loginUser: loginUser,
        logout: logout,
        readErrorMessage: readErrorMessage,
        getGenres: getGenres,
        searchGenresByName: searchGenresByName,
        getMovies: getMovies,
        searchMoviesWithFilters: searchMoviesWithFilters,
        searchMoviesByName: searchMoviesByName,
        getMovieById: getMovieById,
        watchMovie: watchMovie,
        getMovieReviews: getMovieReviews,
        getUserReview: getUserReview,
        createReview: createReview,
        getMoviesByGenre: getMoviesByGenre,
        getMovieReviewsNewest: getMovieReviewsNewest,
        getMovieReviewsOldest: getMovieReviewsOldest,

        partialUpdateReview: partialUpdateReview,
        deleteReview: deleteReview,

        getMyReviews: getMyReviews,

        getFavoritesCount: getFavoritesCount,
        addToFavorites: addToFavorites,
        removeFromFavorites: removeFromFavorites,
        removeFavoriteById: removeFavoriteById,
        isFavorite: isFavorite,
        checkFavorite: checkFavorite,
        getFavorites: getFavorites,

        getWatchHistory: getWatchHistory,
        getWatchHistoryCount: getWatchHistoryCount,
        clearAllWatchHistory: clearAllWatchHistory,
        deleteWatchHistoryItem: deleteWatchHistoryItem,
        getWatchHistoryByDateRange: getWatchHistoryByDateRange,

        getMovieReviewsTopRated: getMovieReviewsTopRated,
        getMovieReviewsLowRated: getMovieReviewsLowRated,

        createGenre: createGenre,
        updateGenre: updateGenre,
        partialUpdateGenre: partialUpdateGenre,
        deleteGenre: deleteGenre,

        createMovie: createMovie,
        updateMovie: updateMovie,
        partialUpdateMovie: partialUpdateMovie,
        deleteMovie: deleteMovie,
    };
})();
