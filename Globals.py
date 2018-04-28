import dbHandler

class Globals():
    def __init__(self, user_id):
        self.db = dbHandler.dbHandler()
        self.userPreferences = self.db.GetUserPreferences(user_id)
        self.ingredientsGroups = self.db.ingredients
    def getDb(self):
        return self.db
    def getUserPreferences(self):
        return self.userPreferences

    def setUserPreferences(self,value):
        self.userPreferences = value

    def getIngredientsGroups(self):
        return self.ingredientsGroups