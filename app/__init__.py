__app_name__ = "mypytimer"
__version__ = "0.1.0"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    CREATE_SESSION_ERROR,
    STOP_SESSION_ERROR,
) = range(7)

ERRORS = {
    CREATE_SESSION_ERROR: "session already in progress, please stop the current session and try again.",
    STOP_SESSION_ERROR: "no current session in progress",
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config directory error",
    DB_READ_ERROR: "config directory error",
    DB_WRITE_ERROR: "config directory error",
}