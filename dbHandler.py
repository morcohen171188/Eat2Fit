from firebase.firebase import FirebaseApplication
from firebase.firebase import FirebaseAuthentication
from string import Template
import rateCalculation, json

class dbHandler:

    def __init__(self):
        self.firebaseClient = None
        self.DBConnection()
        self.ingredients = self.GetIngredientsGroups()

    def DBConnection(self):
        self.firebaseClient = FirebaseApplication('https://eat2fit-adcd2.firebaseio.com', authentication=None)
        authentication = FirebaseAuthentication('JQxgwXKOwoBa5piS5cphXoc0ToiJaq2qDwAkPzPo',
                                            'mor171188@gmail.com',
                                            extra={'id': 'kRZ84YKZXPS9ZIIULOVOV8pXUQt2'})
        self.firebaseClient.authentication = authentication
        user = authentication.get_user()

    def GetNewUserId(self):
        result_stractured_data = self.firebaseClient.get('/users', None)
        return len(result_stractured_data)

    def GetUsers(self):
        result_stractured_data = self.firebaseClient.get('/users', None)
        return result_stractured_data

    def GetAllRestaurants(self):
        result_stractured_data =  self.firebaseClient.get('/restaurants', None)
        return result_stractured_data

    def GetAllDishesFromRestaurant(self, restaurantName):
        restaurant_id = 0
        restaurants_list = self.GetAllRestaurants()
        for restaurant in restaurants_list:
            if restaurant['restName'] == restaurantName:
                restaurant_id = restaurant['restId']
                break
        result_stractured_data = self.firebaseClient.get('/restaurants/{0}/Dishes'.format(restaurant_id), None)
        return result_stractured_data

    def GetIngredientsGroups(self):
        result_stractured_data = self.firebaseClient.get('/ingredientsGroups', None)
        return result_stractured_data

    def GetUserPreferences(self, user_id):
        result_stractured_data = self.firebaseClient.get('/users/{0}/userPreferences'.format(user_id), None)
        return result_stractured_data

    def updateUserPreferences(self, user_id, preferences):
        self.firebaseClient.put('/users/{0}/userPreferences'.format(user_id),'VEGETARIAN',preferences['VEGETARIAN'])
        self.firebaseClient.put('/users/{0}/userPreferences'.format(user_id),'VEGAN',preferences['VEGAN'])
        self.firebaseClient.put('/users/{0}/userPreferences'.format(user_id),'KOSHER',preferences['KOSHER'])
        self.firebaseClient.put('/users/{0}/userPreferences'.format(user_id),'LIKED',preferences['LIKED'])
        self.firebaseClient.put('/users/{0}/userPreferences'.format(user_id),'DISLIKED',preferences['DISLIKED'])

    def GetUserPreviouslyLiked(self, user_id):
        result_stractured_data = self.firebaseClient.get('/users/{0}/previouslyLiked'.format(user_id), None)
        if result_stractured_data is None:
            result_stractured_data = []
        return result_stractured_data

    def UpdateUserPreviouslyLiked(self, user_id, Dish):
        result_stractured_data = self.firebaseClient.get('/users/{0}/previouslyLiked'.format(user_id), None)
        if result_stractured_data is None:
            result_stractured_data = []
        result_stractured_data.append(Dish)
        self.firebaseClient.put('/users/{0}'.format(user_id),'previouslyLiked',result_stractured_data)

    def UpdateUserLikedPreferences(self, user_id, likedIngredients):
        result_stractured_data = self.firebaseClient.get('/users/{0}/userPreferences/LIKED'.format(user_id), None)
        if result_stractured_data is None:
            result_stractured_data = []
        for ingredient in likedIngredients:
            result_stractured_data.append(ingredient)
        self.firebaseClient.put('/users/{0}/userPreferences'.format(user_id),'LIKED',result_stractured_data)

    def UpdateUserDislikedPreferences(self, user_id, dislikedIngredients):
        result_stractured_data = self.firebaseClient.get('/users/{0}/userPreferences/DISLIKED'.format(user_id), None)
        if result_stractured_data is None:
            result_stractured_data = []
        old_dislikedlist = set(result_stractured_data)
        add_unliked_items_only_list = list(set(dislikedIngredients)-set(self.GetUserPreferences(user_id)['LIKED']))
        new_disliked_list = list(old_dislikedlist | add_unliked_items_only_list)

        self.firebaseClient.put('/users/{0}/userPreferences'.format(user_id),'DISLIKED',new_disliked_list)

    def SaveNewUserPreferences(self, user_data):
        new_user_id = self.GetNewUserId()
        user_data["userId"] = new_user_id
        self.firebaseClient.patch('/users/{0}'.format(new_user_id),user_data)
        return str(new_user_id)

    # maybe we dont need it
    def get_recommended_dishes(self, restName):
        pref = self.GetUserPreferences(0)
        dishes = self.GetAllDishesFromRestaurant(restName)
        pref = rateCalculation.PreProcessUserPreferences(pref, self.ingredients)
        return rateCalculation.CalculateBestMatchDishes(pref,dishes,self.ingredients)

if __name__ == "__main__":
    db = dbHandler()
    db.SaveNewUserPreferences('{"userId":${user_id},"userName":"test","userPreferences":{"KOSHER":1,"VEGETARIAN":0,"VEGAN":0,"LIKED":["MEAT"],"DISLIKED":["DAIRY"]},"previouslyLiked":[]}')