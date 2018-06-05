import multiprocessing
import multiprocessing.pool
import sys
import Globals
import restLogic
import util

userPreferences = []
Dishes = []
ingredientsGroups = []
globals = None
ingredientsGroups = None


class CalcBestMatchDishes(object):

    def __init__(self, ingredientsGroups, userPreferences, previouslyLiked, previouslyDisliked):
        self._ingredientsGroups, self._userPreferences, \
            self._previouslyLiked, self._previouslyDisliked = ingredientsGroups, userPreferences, previouslyLiked, previouslyDisliked


    def calculate(self, Dish):
        dish_results = restLogic.calcDishesRates(self._userPreferences, self._ingredientsGroups, Dish)
        number_of_disliked = dish_results[1] if dish_results[1] != 0 else 1
        dish_rate = dish_results[0]
        restLogic.recalcRatesByPreviouslyLikedDisliked(dish_rate, self._previouslyLiked, self._previouslyDisliked, Dish)
        dish_score = dish_rate[Dish['name']]

        if dish_score > 0:
            dish_score_perc = dish_score / (dish_score + number_of_disliked)
        else:
            dish_score_perc = 0
        dish_rate[Dish['name']] = int(dish_score_perc*100)
        return dish_rate

def PreProcessUserPreferences(userPreferences, ingredientsGroups):
    some_list = []

    if 'LIKED' in userPreferences:
        for liked_ingredient in userPreferences['LIKED']:
            if liked_ingredient in ingredientsGroups:
                some_list.extend(ingredientsGroups[liked_ingredient])
            else:
                some_list.extend(liked_ingredient)

        userPreferences['LIKED'].clear()
        userPreferences['LIKED'].extend(some_list)

    if 'DISLIKED' in userPreferences:
        some_list = []
        for disliked_ingredient in userPreferences['DISLIKED']:
            if disliked_ingredient in ingredientsGroups:
                some_list.extend(ingredientsGroups[disliked_ingredient])
            else:
                some_list.extend(disliked_ingredient)

        userPreferences['DISLIKED'].clear()
        userPreferences['DISLIKED'].extend(some_list)

    return userPreferences

def main(data):
    pool_outputs = []
    (rest_name, user_id) = util.parse_url_data(data)
    rest_name.replace("%20", " ")
    rest_name = rest_name.lower()
    globals = Globals.Globals(user_id)
    Dishes = globals.getDb().GetAllDishesFromRestaurant(rest_name)
    if Dishes == []:
        return []

    ingredientsGroups = globals.getIngredientsGroups()
    userPreferences = (PreProcessUserPreferences(globals.getUserPreferences(), ingredientsGroups))
    previouslyLiked = globals.getDb().GetUserPreviouslyLiked(user_id)
    previouslyDisliked = globals.getDb().GetUserPreviouslyDisliked(user_id)
    worker = CalcBestMatchDishes(ingredientsGroups, userPreferences, previouslyLiked, previouslyDisliked)
    for dish in Dishes:
        pool_outputs.append(worker.calculate(dish))
    top5 = sorted(pool_outputs, key=lambda x: list(x.values())[0], reverse=True)[:5]
    return top5
