class Activity(object):

    #activityLimit: string -> int
    # retorna el limite de la actividad
    #activityMembers:string -> array string
    #retorna los miembros de la actividad
    def __init__(self):
        self.activityLimit = {}
        self.activityMembers = {}

    #addActivity: string, int -> void
    #agrega nueva actividad necesita de un nombre y un limite de personas
    def addActivity(self, activityName, limit):
        self.activityLimit[activityName] = limit
        self.activityMembers[activityName] = []

    #addMemberToActivity: string,string -> void
    #agrega un nuevo miembro a la actividad sino imprime que no se puede
    def addMemberToActivity(self, actName, memberName):
        if len(self.activityMembers[actName]) < self.activityLimit[actName]:
            self.activityMembers[actName].append(memberName)
        else:
            print "Exceded size of activity"

    #getMembersOfactivity: string -> array string
    #obtiene una lista con los miembros de la actividad pedida
    def getMembersOfActivity(self, actName):
        return self.activityMembers[actName]

    #getMembersExceptUser: string, string -> array string
    # obtiene una lista con los miembros de la actividad pedida excepto por el user dado
    def getMembersExceptUser(self, actName, userName):
        members = self.getMembersOfActivity(actName)
        ans = []
        for user in members:
            if (user != userName):
                ans.append(user)
        return ans
