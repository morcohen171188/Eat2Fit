import SemanticWordSimilarityCalculator


def calcDishesRates(userPreferences, ingredientsGroups, Dish):
    dish_results = {}
    meat_kosher_flag = 0;
    dairy_kosher_flag = 0;
    number_of_disliked = 0;
    dish_id = Dish['name']
    dish_results[dish_id] = 0
    for ingredient in Dish['ingredients']:
        if userPreferences["KOSHER"]:
            if (ingredient in ingredientsGroups["SEAFOOD"]):
                dish_results[dish_id] = -1000
                break
            else:
                if(ingredient in ingredientsGroups["MEAT"]):
                    meat_kosher_flag = 1;
                    if dairy_kosher_flag:
                        dish_results[dish_id] = -1000
                        break
                if(ingredient in ingredientsGroups["DAIRY"]):
                    dairy_kosher_flag = 1;
                    if meat_kosher_flag:
                        dish_results[dish_id] = -1000
                        break
        if userPreferences["VEGETARIAN"]:
            if (ingredient in ingredientsGroups["MEAT"])or \
                (ingredient in ingredientsGroups["SEAFOOD"]):
                    dish_results[dish_id] = -1000
                    break
        if userPreferences["VEGAN"]:
            if (ingredient in ingredientsGroups["MEAT"])or \
                (ingredient in ingredientsGroups["DAIRY"])or \
                (ingredient in ingredientsGroups["SEAFOOD"]):
                    dish_results[dish_id] = -1000
                    break
        if ingredient in userPreferences["LIKED"]:
            dish_results[dish_id] += 1
        else:
            if ingredient in userPreferences["DISLIKED"]:
                dish_results[dish_id] -= 1
                number_of_disliked += 1
            else:
                result_similarity = SemanticWordSimilarityCalculator.calculateSemanticWordSimilarity(ingredient, userPreferences["LIKED"])
                if result_similarity > 0.7:
                    dish_results[dish_id] += 1
                else:
                    number_of_disliked += 1
    return [dish_results,number_of_disliked]

def recalcRatesByPreviouslyLiked(dish_results, previouslyLiked, Dish):
    if "none" not in previouslyLiked:
        for dish in dish_results:
            dish_set = set(Dish['ingredients'])
            for perLikedDish in previouslyLiked:
                preLiked_set = set(perLikedDish['ingredients'])
                dish_results[dish] += len(dish_set.intersection(preLiked_set))