(function () {
    var apiUrl = window.ApiClient.apiUrl;
    var parseResponseJson = window.ApiClient.parseResponseJson;
    var readErrorMessage = window.ApiClient.readErrorMessage;
    var publicGetJson = window.ApiHttp.publicGetJson;
    var authFetchJson = window.ApiHttp.authFetchJson;

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

    window.ApiReviews = {
        getMovieReviewsNewest: getMovieReviewsNewest,
        getMovieReviewsOldest: getMovieReviewsOldest,
        getMovieReviewsTopRated: getMovieReviewsTopRated,
        getMovieReviewsLowRated: getMovieReviewsLowRated,
        getMovieReviews: getMovieReviews,
        getUserReview: getUserReview,
        createReview: createReview,
        getMyReviews: getMyReviews,
        partialUpdateReview: partialUpdateReview,
        deleteReview: deleteReview,
    };
})();
