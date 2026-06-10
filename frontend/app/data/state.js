(function () {
    window.AppData = function () {
            return {
                currentView: "catalog",
                loginForm: { username: "", password: "" },
                registerForm: {
                    surname: "",
                    name: "",
                    login: "",
                    email: "",
                    password: "",
                },
                error: "",
                success: "",
                loading: false,
                displayLogin: null,
                profileLoading: false,
                profileData: null,
                profileTab: "view",
                profileSuccess: "",
                fullUpdateForm: {
                    surname: "",
                    name: "",
                    login: "",
                    email: "",
                    password: "",
                },
                // isAdmin: false,
                partialFlags: {
                    surname: false,
                    name: false,
                    login: false,
                    email: false,
                    password: false,
                },
                partialForm: {
                    surname: "",
                    name: "",
                    login: "",
                    email: "",
                    password: "",
                },
                genreList: [],
                genrePage: 1,
                genreSize: 10,
                genreLoading: false,
                genreSearchInput: "",
                genreActiveSearch: "",

                // Фильмы
                moviesList: [],
                moviesPage: 1,
                moviesSize: 9,
                moviesLoading: false,

                movieSearchInput: "",
                movieActiveSearch: "",

                // Фильтры для фильмов
                movieFilters: {
                    search_query: "",
                    min_rating: null,
                    max_rating: null,
                    start_release_date: "",
                    end_release_date: "",
                    genre_id: null,
                    sort_by: null,
                    sorting_direction: "ASC"
                },
                showFilters: false,

                currentMovie: null,
                movieDetailsLoading: false,

                reviewsList: [],
                reviewsPage: 1,
                reviewsSize: 10,
                reviewsTotal: 0,
                reviewsLoading: false,
                deletingReviewSource: null,

                userReview: null,
                reviewRating: 5,
                reviewText: "",
                reviewSubmitting: false,
                showReviewForm: false,

                // Мои отзывы
                myReviewsList: [],
                myReviewsPage: 1,
                myReviewsSize: 10,
                myReviewsLoading: false,
                myReviewsTotal: 0,

                // Фильтры по жанру
                selectedGenreId: null,
                selectedGenreName: null,

                reviewsSortBy: "default",  // default, newest, oldest

                editingReview: null,
                editReviewRating: 5,
                editReviewText: "",

                deleteReviewId: null,

                favoritesCount: 0,
                isFavorite: false,
                favoriteToggling: false,

                favoritesList: [],
                favoritesPage: 1,
                favoritesSize: 12,
                favoritesLoading: false,

                watchHistoryList: [],
                watchHistoryPage: 1,
                watchHistorySize: 15,
                watchHistoryLoading: false,
                watchHistoryCount: 0,
                deletingHistoryId: null,
                // Фильтрация истории по датам
                historyStartDate: "",
                historyEndDate: "",
                historyFilterApplied: false,

                reviewsSortType: "default",
                reviewsSortOrder: "",

                // Админ панель - жанры
                adminGenres: [],
                adminGenresPage: 1,
                adminGenresSize: 16,
                adminGenresLoading: false,
                adminGenresTotal: 0,

                // Форма для жанра
                editingGenre: null,
                genreForm: {
                    name: "",
                    description: "",
                    preview_url: ""
                },
                genreFormSubmitting: false,
                showGenreForm: false,
                genrePosterFile: null,
                genrePosterFileName: "",

                // Админ панель - фильмы
                adminMoviesList: [],
                adminMoviesPage: 1,
                adminMoviesSize: 16,
                adminMoviesLoading: false,
                adminMoviesTotal: 0,

                // Форма для фильма
                editingMovie: null,
                showMovieForm: false,
                movieFormSubmitting: false,
                movieForm: {
                    name: "",
                    description: "",
                    rating: 5,
                    preview_url: "",
                    source_url: "",
                    genre_id: null,
                    release_date: ""
                },
                moviePosterFile: null,
                moviePosterFileName: "",
                movieSourceFile: null,
                movieSourceFileName: "",

                deletingGenreId: null,
                deletingGenreName: null,
                genreDeleting: false,

                deletingMovieId: null,
                deletingMovieName: null,
                movieDeleting: false,

                toastMessage: "",
                toastVisible: false,
            };
    };
})();
