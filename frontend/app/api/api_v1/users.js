(function () {
    var authFetchJson = window.ApiHttp.authFetchJson;

    function getCurrentUserProfile() {
        return authFetchJson("/api/v1/users/me/", { method: "GET" });
    }

    function updateCurrentUserProfile(payload) {
        return authFetchJson("/api/v1/users/me/", { method: "PUT", body: payload });
    }

    function partialUpdateCurrentUserProfile(payload) {
        return authFetchJson("/api/v1/users/me/", { method: "PATCH", body: payload });
    }

    function deleteCurrentUserProfile() {
        return authFetchJson("/api/v1/users/me/", { method: "DELETE" });
    }

    window.ApiUsers = {
        getCurrentUserProfile: getCurrentUserProfile,
        updateCurrentUserProfile: updateCurrentUserProfile,
        partialUpdateCurrentUserProfile: partialUpdateCurrentUserProfile,
        deleteCurrentUserProfile: deleteCurrentUserProfile,
    };
})();
