(function () {
    var authFetchJson = window.ApiHttp.authFetchJson;

    function getPresignUrl(data) {
        var token = window.TokenStore.getAccessToken();
        if (!token) return Promise.reject(new Error("Не авторизован"));

        return authFetchJson("/api/v1/media/presign-url", {
            method: "POST",
            body: data,
        });
    }

    window.ApiMedia = {
        getPresignUrl: getPresignUrl,
    };
})();
