function(
    name = "get_meal_by_area",
    description = "Returns meal suggestions in JSON Format; the JSON is an array, with one meal per item.",
    params = types(string("area", "The area the meal should be from, like 'Canadian'"))
) { (area) ->
    println(area)
    val result = httpGet("https://www.themealdb.com/api/json/v1/1/filter.php?a=$area")
    println(result)
    result
}