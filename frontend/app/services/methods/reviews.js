(function () {
    window.AppMethodsReviews = {
            loadReviews: function (movieId) {
                var self = this;
                this.reviewsLoading = true;

                window.Api.getMovieReviews(movieId, this.reviewsPage, this.reviewsSize)
                    .then(function (data) {
                        self.reviewsList = data.review_list || [];
                        self.reviewsTotal = data.total || 0;
                        if (typeof data.page === "number") {
                            self.reviewsPage = data.page;
                        }
                        if (typeof data.size === "number") {
                            self.reviewsSize = data.size;
                        }
                    })
                    .catch(function (e) {
                        console.error("Ошибка загрузки отзывов:", e);
                        self.reviewsList = [];
                    })
                    .finally(function () {
                        self.reviewsLoading = false;
                    });
            },

            loadReviewsWithSort: function (movieId, sortType, sortOrder) {
                console.log("loadReviewsWithSort вызван", movieId, sortType, sortOrder);
                var self = this;
                this.reviewsLoading = true;

                var promise;

                if (sortType === "default") {
                    promise = window.Api.getMovieReviews(movieId, this.reviewsPage, this.reviewsSize);
                } else if (sortType === "date") {
                    if (sortOrder === "desc") {
                        console.log("Вызов getMovieReviewsNewest");
                        promise = window.Api.getMovieReviewsNewest(movieId, this.reviewsPage, this.reviewsSize);
                    } else {
                        console.log("Вызов getMovieReviewsOldest");
                        promise = window.Api.getMovieReviewsOldest(movieId, this.reviewsPage, this.reviewsSize);
                    }
                } else {
                    if (sortOrder === "desc") {
                        console.log("Вызов getMovieReviewsTopRated");
                        promise = window.Api.getMovieReviewsTopRated(movieId, this.reviewsPage, this.reviewsSize);
                    } else {
                        console.log("Вызов getMovieReviewsLowRated");
                        promise = window.Api.getMovieReviewsLowRated(movieId, this.reviewsPage, this.reviewsSize);
                    }
                }

                promise
                    .then(function (data) {
                        console.log("Данные получены:", data);
                        self.reviewsList = data.review_list || [];
                        if (typeof data.page === "number") self.reviewsPage = data.page;
                        if (typeof data.size === "number") self.reviewsSize = data.size;
                    })
                    .catch(function (e) {
                        console.error("Ошибка загрузки отзывов:", e);
                        self.reviewsList = [];
                    })
                    .finally(function () {
                        self.reviewsLoading = false;
                    });
            },

            changeReviewsSort: function (event) {
                if (event) event.stopPropagation();
                console.log("changeReviewsSort вызван", this.reviewsSortType, this.reviewsSortOrder);
                this.reviewsPage = 1;
                if (this.currentMovie) {
                    this.loadReviewsWithSort(this.currentMovie.id, this.reviewsSortType, this.reviewsSortOrder);
                }
            },

            changeReviewsSortWithValues: function (sortType, sortOrder) {
                console.log("changeReviewsSortWithValues", sortType, sortOrder);
                this.reviewsSortType = sortType;
                this.reviewsSortOrder = sortOrder;
                this.reviewsPage = 1;
                if (this.currentMovie) {
                    this.loadReviewsWithSort(this.currentMovie.id, sortType, sortOrder);
                }
            },

            startEditReview: function (review) {
                this.editingReview = review;
                this.editReviewRating = review.rating;
                this.editReviewText = review.review_text || "";
            },

            cancelEditReview: function () {
                this.editingReview = null;
                this.editReviewRating = 5;
                this.editReviewText = "";
            },

            submitEditReview: function () {
                var self = this;
                if (!this.editReviewText.trim()) {
                    this.error = "Введите текст отзыва";
                    return;
                }

                this.reviewSubmitting = true;

                window.Api.partialUpdateReview(this.editingReview.id, this.editReviewRating, this.editReviewText.trim())
                    .then(function (updatedReview) {
                        // Обновляем отзыв в списке
                        var index = self.reviewsList.findIndex(r => r.id === updatedReview.id);
                        if (index !== -1) {
                            self.reviewsList[index] = updatedReview;
                        }
                        // Если редактируем свой отзыв
                        if (self.userReview && self.userReview.id === updatedReview.id) {
                            self.userReview = updatedReview;
                            self.reviewRating = updatedReview.rating;
                            self.reviewText = updatedReview.review_text || "";
                        }
                        self.cancelEditReview();
                        // Перезагружаем список для обновления пагинации
                        self.loadReviewsWithSort(self.currentMovie.id, self.reviewsSortBy);
                    })
                    .catch(function (e) {
                        self.error = e.message || "Не удалось обновить отзыв";
                    })
                    .finally(function () {
                        self.reviewSubmitting = false;
                    });
            },

            confirmDeleteReview: function (reviewId) {
                var id = Number(reviewId);
                this.deletingReviewId = id;
                var modalEl = document.getElementById("deleteReviewModal");
                if (modalEl && typeof bootstrap !== "undefined") {
                    var modal = new bootstrap.Modal(modalEl);
                    modal.show();
                }
            },

            confirmDeleteReviewConfirmed: function () {
                var self = this;
                this.reviewSubmitting = true;

                window.Api.deleteReview(this.deletingReviewId)
                    .then(function () {
                        if (self.deletingReviewSource === "myReviews") {
                            // Удаляем из списка "Мои отзывы"
                            self.myReviewsList = self.myReviewsList.filter(function(r) {
                                return r.id !== self.deletingReviewId;
                            });
                            self.myReviewsTotal--;
                        } else {
                            // Удаляем из списка отзывов под фильмом
                            self.reviewsList = self.reviewsList.filter(function(r) {
                                return r.id !== self.deletingReviewId;
                            });
                            if (self.userReview && self.userReview.id === self.deletingReviewId) {
                                self.userReview = null;
                            }
                            self.loadReviewsWithSort(self.currentMovie.id, self.reviewsSortType, self.reviewsSortOrder);
                        }

                        var modalEl = document.getElementById("deleteReviewModal");
                        if (modalEl) {
                            var modal = bootstrap.Modal.getInstance(modalEl);
                            if (modal) modal.hide();
                        }
                        self.deletingReviewId = null;
                        self.deletingReviewSource = null;
                    })
                    .catch(function (e) {
                        self.error = e.message || "Не удалось удалить отзыв";
                    })
                    .finally(function () {
                        self.reviewSubmitting = false;
                    });
            },

            changeReviewsSort: function (sortOrder) {
                this.reviewsPage = 1;
                this.reviewsSortBy = sortOrder;
                if (this.currentMovie) {
                    this.loadReviewsWithSort(this.currentMovie.id, sortOrder);
                }
            },

            loadMyReviews: function () {
                var self = this;
                this.myReviewsLoading = true;

                window.Api.getMyReviews(this.myReviewsPage, this.myReviewsSize)
                    .then(function (data) {
                        self.myReviewsList = data.review_list || [];
                        self.myReviewsTotal = data.total || 0;
                        if (typeof data.page === "number") self.myReviewsPage = data.page;
                        if (typeof data.size === "number") self.myReviewsSize = data.size;
                    })
                    .catch(function (e) {
                        self.error = e.message || "Не удалось загрузить отзывы";
                        self.myReviewsList = [];
                    })
                    .finally(function () {
                        self.myReviewsLoading = false;
                    });
            },

            goMyReviewsPage: function (nextPage) {
                if (nextPage < 1) return;
                this.myReviewsPage = nextPage;
                this.loadMyReviews();
            },

            editReviewFromList: function (review) {
                // Открываем детальную страницу фильма с модалкой редактирования
                window.location.hash = "#/movie/" + review.movie.id;
                // Можно передать данные для открытия формы редактирования
                this.pendingEditReview = review;
            },

            deleteMyReview: function (reviewId) {
                this.deletingReviewId = reviewId;
                this.deletingReviewSource = "myReviews";
                var modalEl = document.getElementById("deleteReviewModal");
                if (modalEl && typeof bootstrap !== "undefined") {
                    var modal = new bootstrap.Modal(modalEl);
                    modal.show();
                }
            },

            goReviewsPage: function (nextPage) {
                if (nextPage < 1) return;
                this.reviewsPage = nextPage;
                if (this.currentMovie) {
                    this.loadReviews(this.currentMovie.id);
                }
            },

            backToMovies: function () {
                this.currentView = "movies";
                this.currentMovie = null;
                this.movieDetailsLoading = false;
                // Сбросить фильтры
                this.selectedGenreId = null;
                this.selectedGenreName = null;
                this.movieActiveSearch = "";
                this.movieSearchInput = "";
                this.moviesPage = 1;
                // Перезагрузить список фильмов
                this.loadMovies();
            },

            clearMovieSearch: function () {
                this.movieSearchInput = "";
                this.movieActiveSearch = "";
                this.moviesPage = 1;
                this.loadMovies();
            },
            formatDate: function (dateString) {
                if (!dateString) return "—";
                try {
                    var date = new Date(dateString);
                    return date.toLocaleDateString("ru-RU");
                } catch (e) {
                    return dateString;
                }
            },
            truncateText: function (text, maxLength) {
                if (!text) return "";
                if (text.length <= maxLength) return text;
                return text.substring(0, maxLength) + "...";
            },

            loadUserReview: function (movieId) {
                var self = this;
                if (!this.isAuthenticated) {
                    this.userReview = null;
                    return;
                }

                window.Api.getUserReview(movieId)
                    .then(function (data) {
                        self.userReview = data;
                        if (data) {
                            self.reviewRating = data.rating;
                            self.reviewText = data.review_text || "";
                        }
                    })
                    .catch(function () {
                        self.userReview = null;
                    });
            },

            toggleReviewForm: function () {
                this.showReviewForm = !this.showReviewForm;
                if (!this.showReviewForm) {
                    this.reviewRating = 5;
                    this.reviewText = "";
                }
            },

            submitReview: function () {
                var self = this;
                if (!this.isAuthenticated) {
                    this.error = "Для написания отзыва необходимо войти";
                    return;
                }

                if (!this.reviewText.trim()) {
                    this.error = "Введите текст отзыва";
                    return;
                }

                this.reviewSubmitting = true;
                this.error = "";

                window.Api.createReview(this.currentMovie.id, this.reviewRating, this.reviewText.trim())
                    .then(function (newReview) {
                        self.userReview = newReview;
                        self.showReviewForm = false;
                        self.reviewRating = 5;
                        self.reviewText = "";
                        // Перезагружаем список отзывов
                        self.reviewsPage = 1;
                        self.loadReviews(self.currentMovie.id);
                    })
                    .catch(function (e) {
                        self.error = e.message || "Не удалось отправить отзыв";
                    })
                    .finally(function () {
                        self.reviewSubmitting = false;
                    });
            },
    };
})();
