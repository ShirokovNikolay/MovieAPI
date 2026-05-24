(function () {
    var authFetchJson = window.ApiHttp.authFetchJson;

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

    window.ApiWatchHistory = {
        getWatchHistory: getWatchHistory,
        getWatchHistoryByDateRange: getWatchHistoryByDateRange,
        getWatchHistoryCount: getWatchHistoryCount,
        clearAllWatchHistory: clearAllWatchHistory,
        deleteWatchHistoryItem: deleteWatchHistoryItem,
    };
})();
