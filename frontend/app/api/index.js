(function () {
    window.Api = Object.assign(
        {
            apiUrl: window.ApiClient.apiUrl,
            readErrorMessage: window.ApiClient.readErrorMessage,
            refreshAccessToken: window.ApiHttp.refreshAccessToken,
            ensureValidAccessToken: window.ApiHttp.ensureValidAccessToken,
            authFetch: window.ApiHttp.authFetch,
            authFetchJson: window.ApiHttp.authFetchJson,
        },
        window.ApiAuth,
        window.ApiUsers,
        window.ApiMedia,
        window.ApiGenres,
        window.ApiMovies,
        window.ApiReviews,
        window.ApiFavoriteMovies,
        window.ApiWatchHistory
    );
})();
