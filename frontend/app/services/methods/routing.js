(function () {
    window.AppMethodsRouting = {
            syncRoute: function () {
                var hash = window.location.hash || "#/";
                if (hash === "#/" || hash === "#/home" || hash === "#/catalog") {
                    this.currentView = "catalog";
                    if (this.isAuthenticated && !this.profileData) {
                        this.loadProfile();
                    }
                    this.error = "";
                    return;
                }
                if (hash === "#/genres") {
                    this.currentView = "genres";
                    this.error = "";
                    this.loadGenres();
                    return;
                }
                if (hash === "#/movies") {
                    this.currentView = "movies";
                    this.error = "";
                    this.loadMovies();
                    return;
                }
                if (hash === "#/register") {
                    this.currentView = "register";
                    this.error = "";
                    this.success = "";
                    return;
                }
                if (hash === "#/login") {
                    this.currentView = "login";
                    this.error = "";
                    return;
                }
                if (hash === "#/profile") {
                    if (!this.isAuthenticated) {
                        this.goLogin();
                        return;
                    }
                    this.currentView = "profile";
                    this.error = "";
                    this.profileSuccess = "";
                    this.profileTab = "view";
                    this.loadProfile();
                    return;
                }
                if (hash.startsWith("#/movie/")) {
                    var movieId = parseInt(hash.split("/")[2]);
                    if (!isNaN(movieId)) {
                        this.currentView = "movieDetails";
                        this.error = "";
                        this.loadMovieDetails(movieId);
                        return;
                    }
                }
                if (hash === "#/favorites") {
                    if (!this.isAuthenticated) {
                        this.goLogin();
                        return;
                    }
                    this.currentView = "favorites";
                    this.loadFavorites();
                    return;
                }
                if (hash === "#/history") {
                    if (!this.isAuthenticated) {
                        this.goLogin();
                        return;
                    }
                    this.currentView = "history";
                    if (this.historyFilterApplied) {
                        this.loadWatchHistoryWithFilter();
                    } else {
                        this.loadWatchHistory();
                    }
                    return;
                }
                if (hash === "#/my-reviews") {
                    if (!this.isAuthenticated) {
                        this.goLogin();
                        return;
                    }
                    this.currentView = "myReviews";
                    this.loadMyReviews();
                    return;
                }
                if (hash === "#/admin") {
                    if (!this.isAuthenticated || !this.isAdmin) {
                        this.goLogin();
                        return;
                    }
                    this.currentView = "admin";
                    return;
                }
                if (hash === "#/admin/genres") {
                    if (!this.isAuthenticated) {
                        this.goLogin();
                        return;
                    }

                    if (!this.profileData) {
                        this.loadProfile();
                        var self = this;
                        var interval = setInterval(function() {
                            if (self.profileData) {
                                clearInterval(interval);
                                if (self.profileData.role === "admin") {
                                    self.currentView = "adminGenres";
                                    self.loadAdminGenres();
                                } else {
                                    self.goCatalog();
                                    self.error = "Нет доступа";
                                }
                            }
                        }, 100);
                        return;
                    }

                    if (this.profileData.role !== "admin") {
                        this.goCatalog();
                        this.error = "Нет доступа";
                        return;
                    }

                    this.currentView = "adminGenres";
                    this.loadAdminGenres();
                    return;
                }
                if (hash === "#/admin/movies") {
                    if (!this.isAuthenticated) {
                        this.goLogin();
                        return;
                    }

                    if (!this.profileData) {
                        this.loadProfile();
                        var self = this;
                        var interval = setInterval(function() {
                            if (self.profileData) {
                                clearInterval(interval);
                                if (self.profileData.role === "admin") {
                                    self.currentView = "adminMovies";
                                    self.loadAdminMovies();
                                } else {
                                    self.goCatalog();
                                    self.error = "Нет доступа";
                                }
                            }
                        }, 100);
                        return;
                    }

                    if (this.profileData.role !== "admin") {
                        this.goCatalog();
                        this.error = "Нет доступа";
                        return;
                    }

                    this.currentView = "adminMovies";
                    this.loadAdminMovies();
                    return;
                }
                window.location.hash = "#/";
            },
            goCatalog: function () {
                window.location.hash = "#/";
            },
            goLogin: function () {
                window.location.hash = "#/login";
            },
            goRegister: function () {
                window.location.hash = "#/register";
            },
    };
})();
