(function () {
    window.AppComputed = {
        isAdmin: function () {
            return this.profileData && this.profileData.role === "admin";
        },
        isAuthenticated: function () {
            var access = window.TokenStore.getAccessToken();
            var refresh = window.TokenStore.getRefreshToken();
            if (!access || !refresh) {
                return false;
            }
            if (window.TokenStore.isTokenExpired(refresh, 0)) {
                return false;
            }
            return true;
        },
        genreHasNext: function () {
            return this.genreList.length === this.genreSize && this.genreSize >= 1;
        },
        genreHasPrev: function () {
            return this.genrePage > 1;
        },
        moviesHasNext: function () {
            return this.moviesList.length === this.moviesSize;
        },
        moviesHasPrev: function () {
            return this.moviesPage > 1;
        },

        favoritesHasNext: function () {
            return this.favoritesList.length === this.favoritesSize;
        },
        favoritesHasPrev: function () {
            return this.favoritesPage > 1;
        },

        reviewsHasNext: function () {
            return this.reviewsList.length === this.reviewsSize;
        },
        reviewsHasPrev: function () {
            return this.reviewsPage > 1;
        },
        userFullName: function () {
            if (this.profileData && this.profileData.surname && this.profileData.name) {
                return this.profileData.surname + ' ' + this.profileData.name;
            }
            return this.displayLogin || 'Пользователь';
        },
        myReviewsHasNext: function () {
            return this.myReviewsList.length === this.myReviewsSize;
        },
        myReviewsHasPrev: function () {
            return this.myReviewsPage > 1;
        },
        watchHistoryHasNext: function () {
            return this.watchHistoryList.length === this.watchHistorySize;
        },
        watchHistoryHasPrev: function () {
            return this.watchHistoryPage > 1;
        },
        adminGenresHasNext: function () {
            return this.adminGenresList.length === this.adminGenresSize;
        },
        adminGenresHasPrev: function () {
            return this.adminGenresPage > 1;
        },
        adminMoviesHasNext: function () {
            return this.adminMoviesList.length === this.adminMoviesSize;
        },
        adminMoviesHasPrev: function () {
            return this.adminMoviesPage > 1;
        },
    };
})();
