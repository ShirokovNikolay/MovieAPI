(function () {
    var IMAGE_TYPES = {
        "image/jpeg": "image/jpeg",
        "image/jpg": "image/jpg",
        "image/png": "image/png",
        "image/webp": "image/webp",
    };

    var VIDEO_TYPES = {
        "video/mp4": "video/mp4",
    };

    var EXT_TO_IMAGE = {
        jpg: "image/jpeg",
        jpeg: "image/jpeg",
        png: "image/png",
        webp: "image/webp",
    };

    var EXT_TO_VIDEO = {
        mp4: "video/mp4",
    };

    function extensionOf(fileName) {
        var parts = (fileName || "").split(".");
        if (parts.length < 2) return "";
        return parts.pop().toLowerCase();
    }

    function resolveContentType(file, kind) {
        var allowed = kind === "video" ? VIDEO_TYPES : IMAGE_TYPES;
        if (file.type && allowed[file.type]) {
            return allowed[file.type];
        }
        var extMap = kind === "video" ? EXT_TO_VIDEO : EXT_TO_IMAGE;
        var ext = extensionOf(file.name);
        if (extMap[ext]) {
            return extMap[ext];
        }
        return null;
    }

    var MINIO_HOST = "minio";

    function ensureMinioHost(presignedUrl) {
        try {
            var parsed = new URL(presignedUrl);
            if (parsed.hostname === "localhost" || parsed.hostname === "127.0.0.1") {
                parsed.hostname = MINIO_HOST;
                return parsed.toString();
            }
        } catch (e) {
            /* ignore */
        }
        return presignedUrl;
    }

    function uploadToPresignedUrl(presignedUrl, file, contentType) {
        return fetch(ensureMinioHost(presignedUrl), {
            method: "PUT",
            headers: { "Content-Type": contentType },
            body: file,
        }).then(function (res) {
            if (!res.ok) {
                throw new Error("Не удалось загрузить файл в хранилище (" + res.status + ")");
            }
        });
    }

    function uploadFile(bucketName, file, kind) {
        var contentType = resolveContentType(file, kind);
        if (!contentType) {
            var hint = kind === "video" ? "MP4" : "JPEG, PNG или WebP";
            return Promise.reject(new Error("Неподдерживаемый формат файла. Допустимо: " + hint));
        }

        return window.Api.getPresignUrl({
            bucket_name: bucketName,
            file_name: file.name,
            content_type: contentType,
        }).then(function (presign) {
            var uploadUrl = ensureMinioHost(presign.url);
            return uploadToPresignedUrl(uploadUrl, file, contentType).then(function () {
                return presign.path;
            });
        });
    }

    window.MediaUpload = {
        uploadGenrePoster: function (file) {
            return uploadFile("genre-posters", file, "image");
        },
        uploadMoviePoster: function (file) {
            return uploadFile("movie-posters", file, "image");
        },
        uploadMovieSource: function (file) {
            return uploadFile("movies", file, "video");
        },
        resolveContentType: resolveContentType,
    };
})();
