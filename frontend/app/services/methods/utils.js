(function () {
    window.AppMethodsUtils = {
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
    };
})();
