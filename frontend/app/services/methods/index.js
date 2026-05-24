(function () {
    window.AppMethods = Object.assign(
        {},
        window.AppMethodsRouting,
        window.AppMethodsAuth,
        window.AppMethodsGenres,
        window.AppMethodsMovies,
        window.AppMethodsMovieDetails,
        window.AppMethodsReviews,
        window.AppMethodsProfile,
        window.AppMethodsFavorites,
        window.AppMethodsWatchHistory,
        window.AppMethodsAdminGenres,
        window.AppMethodsAdminMovies,
        window.AppMethodsAdminGenresConfirm,
        window.AppMethodsUtils,
        window.AppMethodsUtilsToast
    );
})();
