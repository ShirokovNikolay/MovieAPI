(function () {
    window.AppMethodsWatchHistory = {
            // ========== ИСТОРИЯ ПРОСМОТРОВ ==========
            loadWatchHistory: function () {
                console.log("loadWatchHistory ВЫЗВАН");
                var self = this;
                this.watchHistoryLoading = true;

                window.Api.getWatchHistory(this.watchHistoryPage, this.watchHistorySize)
                    .then(function (data) {
                        console.log("ДАННЫЕ ОТ API:", data);
                        var historyList = data.watch_history_list || [];
                        console.log("HISTORY_LIST:", historyList);
                        self.watchHistoryList = historyList.map(function(item) {
                            return {
                                id: item.id,
                                watched_at: item.watched_at,
                                movie: item.movie
                            };
                        });
                        console.log("ИТОГОВЫЙ watchHistoryList:", self.watchHistoryList);
                        console.log("ДЛИНА:", self.watchHistoryList.length);
                    })
                    .catch(function (e) {
                        console.error("Ошибка:", e);
                    })
                    .finally(function () {
                        self.watchHistoryLoading = false;
                    });

                window.Api.getWatchHistoryCount()
                    .then(function(data) {
                        console.log("Количество (сырые данные):", data);
                        // data может быть просто числом 24, а не объектом
                        self.watchHistoryCount = typeof data === 'number' ? data : (data.count || 0);
                        console.log("self.watchHistoryCount:", self.watchHistoryCount);
                    })
                    .catch(function(e) {
                        console.error("Ошибка загрузки количества:", e);
                    });
            },

            applyHistoryDateFilter: function () {
                    this.historyFilterApplied = true;
                    this.watchHistoryPage = 1;
                    this.loadWatchHistoryWithFilter();
                },

            clearHistoryDateFilter: function () {
                this.historyStartDate = "";
                this.historyEndDate = "";
                this.historyFilterApplied = false;
                this.watchHistoryPage = 1;
                this.loadWatchHistory();
            },

            loadWatchHistoryWithFilter: function () {
                var self = this;
                this.watchHistoryLoading = true;

                window.Api.getWatchHistoryByDateRange(
                    this.historyStartDate,
                    this.historyEndDate,
                    this.watchHistoryPage,
                    this.watchHistorySize
                )
                    .then(function (data) {
                        var historyList = data.watch_history_list || [];
                        self.watchHistoryList = historyList.map(function(item) {
                            return {
                                id: item.id,
                                watched_at: item.watched_at,
                                movie: item.movie
                            };
                        });
                        if (typeof data.page === "number") self.watchHistoryPage = data.page;
                        if (typeof data.size === "number") self.watchHistorySize = data.size;
                    })
                    .catch(function (e) {
                        self.error = e.message || "Не удалось загрузить историю";
                        self.watchHistoryList = [];
                    })
                    .finally(function () {
                        self.watchHistoryLoading = false;
                    });
            },

            goToMovieFromHistory: function (movieId) {
                window.location.hash = "#/movie/" + movieId;
            },

            goWatchHistoryPage: function (nextPage) {
                if (nextPage < 1) return;
                this.watchHistoryPage = nextPage;
                this.loadWatchHistory();
            },

            confirmDeleteHistoryItem: function (historyId, event) {
                event.stopPropagation();
                this.deletingHistoryId = historyId;
                var modalEl = document.getElementById("deleteHistoryItemModal");
                if (modalEl && typeof bootstrap !== "undefined") {
                    var modal = new bootstrap.Modal(modalEl);
                    modal.show();
                }
            },

            confirmDeleteHistoryItemConfirmed: function () {
                var self = this;
                window.Api.deleteWatchHistoryItem(this.deletingHistoryId)
                    .then(function() {
                        self.watchHistoryList = self.watchHistoryList.filter(function(item) {
                            return item.id !== self.deletingHistoryId;
                        });
                        self.watchHistoryCount--;
                        var modalEl = document.getElementById("deleteHistoryItemModal");
                        if (modalEl) {
                            var modal = bootstrap.Modal.getInstance(modalEl);
                            if (modal) modal.hide();
                        }
                    })
                    .catch(function(e) {
                        self.error = e.message || "Не удалось удалить запись";
                    });
            },

            confirmClearAllHistory: function () {
                var modalEl = document.getElementById("clearAllHistoryModal");
                if (modalEl && typeof bootstrap !== "undefined") {
                    var modal = new bootstrap.Modal(modalEl);
                    modal.show();
                }
            },

            confirmClearAllHistoryConfirmed: function () {
                var self = this;
                window.Api.clearAllWatchHistory()
                    .then(function() {
                        self.watchHistoryList = [];
                        self.watchHistoryCount = 0;
                        self.watchHistoryPage = 1;
                        var modalEl = document.getElementById("clearAllHistoryModal");
                        if (modalEl) {
                            var modal = bootstrap.Modal.getInstance(modalEl);
                            if (modal) modal.hide();
                        }
                    })
                    .catch(function(e) {
                        self.error = e.message || "Не удалось очистить историю";
                    });
            },
    };
})();
