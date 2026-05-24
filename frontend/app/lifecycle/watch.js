(function () {
    window.AppWatch = {
        isAuthenticated: function (val) {
            if (!val && this.currentView === "profile") {
                this.error = "Сессия истекла. Войдите снова.";
                this.goLogin();
            }
        },
    };
})();
