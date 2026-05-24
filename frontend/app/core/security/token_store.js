(function () {
    var ACCESS_KEY = "movie_catalog_access_token";
    var REFRESH_KEY = "movie_catalog_refresh_token";

    function parseJwtPayload(token) {
        if (!token || typeof token !== "string") {
            return null;
        }
        var parts = token.split(".");
        if (parts.length < 2) {
            return null;
        }
        try {
            var base64Url = parts[1];
            var base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
            var json = decodeURIComponent(
                atob(base64)
                    .split("")
                    .map(function (c) {
                        return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
                    })
                    .join("")
            );
            return JSON.parse(json);
        } catch (e) {
            return null;
        }
    }

    function isTokenExpired(token, skewSeconds) {
        skewSeconds = skewSeconds == null ? 60 : skewSeconds;
        var p = parseJwtPayload(token);
        if (!p || !p.exp) {
            return true;
        }
        return Date.now() / 1000 >= p.exp - skewSeconds;
    }

    function getAccessToken() {
        return localStorage.getItem(ACCESS_KEY);
    }

    function getRefreshToken() {
        return localStorage.getItem(REFRESH_KEY);
    }

    function setTokens(accessToken, refreshToken) {
        if (accessToken) {
            localStorage.setItem(ACCESS_KEY, accessToken);
        }
        if (refreshToken) {
            localStorage.setItem(REFRESH_KEY, refreshToken);
        }
    }

    function clearTokens() {
        localStorage.removeItem(ACCESS_KEY);
        localStorage.removeItem(REFRESH_KEY);
    }

    function getLoginFromAccess() {
        var t = getAccessToken();
        var p = parseJwtPayload(t);
        return p && p.login ? p.login : null;
    }

    window.TokenStore = {
        ACCESS_KEY: ACCESS_KEY,
        REFRESH_KEY: REFRESH_KEY,
        parseJwtPayload: parseJwtPayload,
        isTokenExpired: isTokenExpired,
        getAccessToken: getAccessToken,
        getRefreshToken: getRefreshToken,
        setTokens: setTokens,
        clearTokens: clearTokens,
        getLoginFromAccess: getLoginFromAccess,
    };
})();
