"""Top-level package for """

# create skeleton for a cli appication FOR weather app
__app_name__ = "Weather App"
__version__ = "0.1.0"

# define a series of return assign integer numbers to them using range()
(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(7)

ERROR ={
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    DB_READ_ERROR: "database read error",
    DB_WRITE_ERROR: "database write error",
    ID_ERROR: "to-do id error",
}