(function () {
    window.AppMounted = function () {
        var self = this;
        this.syncRoute();
        if (this.isAuthenticated) {
            this.loadProfile();
        }
        // Загружаем жанры для всех форм
        this.loadGenres();
        window.addEventListener("hashchange", function () {
            self.syncRoute();
        });

        // Глобальный перехват ошибок 429
        window.addEventListener('unhandledrejection', function(event) {
            var error = event.reason;
            if (error && error.message && error.message.includes("⚠️")) {
                event.preventDefault();
                self.showErrorToast(error.message);
            }
        });
    };
})();
