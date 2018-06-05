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

    def GetRestaurants(self):
        result_stractured_data = self.firebaseClient.get('/restaurants', None)
        return result_stractured_data

    def GetAllRestaurants(self):
        result_stractured_data =  self.firebaseClient.get('/restaurants', None)
        return result_stractured_data

    def GetAllDishesFromRestaurant(self, restaurantName):
        restaurant_id = None
        restaurants_list = self.GetAllRestaurants()
        for restaurant in restaurants_list:
            if restaurant['restName'] == restaurantName:
                restaurant_id = restaurant['restId']
                break
        if restaurant_id is None:
            return []

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

    def GetUserPreviouslyDisliked(self, user_id):
        result_stractured_data = self.firebaseClient.get('/users/{0}/previouslyDisliked'.format(user_id), None)
        if result_stractured_data is None:
            result_stractured_data = []
        return result_stractured_data

    def UpdateUserPreviouslyLikedDisliked(self, user_id, Dishes):

        result_stractured_data = self.firebaseClient.get('/users/{0}/previouslyLiked'.format(user_id), None)
        if result_stractured_data is None or "none" in result_stractured_data:
            result_stractured_data = []

        for dish in Dishes["LIKED"]:
            restName, dishName = dish.split(":")
            allDishesFromRest = self.GetAllDishesFromRestaurant(restName)
            for rest_dish in allDishesFromRest:
                if rest_dish['name'] == dishName:
                    result_stractured_data.append(rest_dish)
        self.firebaseClient.put('/users/{0}'.format(user_id),'previouslyLiked',result_stractured_data)

        result_stractured_data = []

        for dish in Dishes["DISLIKED"]:
            restName, dishName = dish.split(":")
            allDishesFromRest = self.GetAllDishesFromRestaurant(restName)
            for rest_dish in allDishesFromRest:
                if rest_dish['name'] == dishName:
                    result_stractured_data.append(rest_dish)
        self.firebaseClient.put('/users/{0}'.format(user_id),'previouslyDisliked',result_stractured_data)

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
        if user_data['userPreferences']['DISLIKED'] == []:
            user_data['userPreferences']['DISLIKED'] = ["none"]
        if user_data['userPreferences']['LIKED'] == []:
            user_data['userPreferences']['LIKED'] = ["none"]
        if user_data['previouslyLiked'] == []:
            user_data['previouslyLiked'] = ["none"]
        if user_data['previouslyDisliked'] == []:
            user_data['previouslyDisliked'] = ["none"]

        self.firebaseClient.patch('/users/{0}'.format(new_user_id),user_data)
        return str(new_user_id)


if __name__ == "__main__":
    db = dbHandler()
    db.SaveNewUserPreferences('{"userId":${user_id},"userName":"test","userPreferences":{"KOSHER":1,"VEGETARIAN":0,"VEGAN":0,"LIKED":["MEAT"],"DISLIKED":["DAIRY"]},"previouslyLiked":[]}')