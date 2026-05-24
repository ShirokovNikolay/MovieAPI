(function () {
    window.AppMethodsUtilsToast = {
            showErrorToast: function (message) {
                this.toastMessage = message;
                this.toastVisible = true;
                setTimeout(() => { this.toastVisible = false; }, 5000);
            },
    };
})();
