"""
This code comes from an assignment in an advanced "learning to code" Python course, and it was completed while I was still a student.
The goal of this code is to practice sorting objects in different ways.
In this case, this program stores information about different climbing areas and their lengths and difficulties.

The console outputs the different climbing areas in the desired string format, sorted in the desired order.
"""

# Class that is used to store information about a specific climbing route
class ClimbingRoute:
    # Initializes new object with route name, length, and grade
    def __init__(self, name: str, length: int, grade: str):
        self.name = name
        self.length = length
        self.grade = grade
 
    def __str__(self):
        return f"Climbing area: {self.name} -> Length: {self.length} metres | Grade: {self.grade}"
 
# Class that represents a climbing area and allows users to add climbing routes to it
class ClimbingArea:
    def __init__(self, name: str):
        self.name = name
        self.__routes = []
 
    # Adds a climbing route to the area
    def add_route(self, route: ClimbingRoute): # Inherits ClimbingRoute object
        if isinstance(route, ClimbingRoute): # Ensures only instances of ClimbingRoute are added
            self.__routes.append(route)
            self.__routes.sort(key=lambda x: x.grade) # Sorting the routes by difficulty
 
    # Returns the number of routes in the area
    def routes(self):
        return len(self.__routes)
 
    # Returns the hardest route in the area
    def hardest_route(self):
        def by_difficulty(route):
            return route.grade
        return self.__routes[-1] # Routes have been sorted by difficulty so the last route is the hardest
 
    def __str__(self):
        if not self.__routes:
            return f"Climbing area: {self.name} -> 0 routes" # Incase there are no routes
        return f"Climbing area: {self.name} -> {self.routes()} routes | Hardest route: {self.hardest_route().grade}"

# Returns the climbing area with the greatest number of routes first 
def sort_by_number_of_routes(areas:list):
    return sorted(areas, key=lambda area: area.routes(), reverse=True)

# Returns the most difficult climbing areas first 
def sort_by_most_difficult(areas:list):
    return sorted(areas, key=lambda area: area.hardest_route().grade, reverse=True)
        
if __name__ == "__main__":
    # Creating climbing areas, routes, and difficulties
    ca_1 = ClimbingArea("Olhava")
    ca_1.add_route(ClimbingRoute("Edge", 38, "6A+"))
    ca_1.add_route(ClimbingRoute("Great cut", 36, "6B"))
    ca_1.add_route(ClimbingRoute("Swedish route", 42, "5+"))
 
    ca_2 = ClimbingArea("Nummi")
    ca_2.add_route(ClimbingRoute("Synchro", 14, "8C+"))
 
    ca_3 = ClimbingArea("Nalkkila slab")
    ca_3.add_route(ClimbingRoute("Small steps", 12, "6A+"))
    ca_3.add_route(ClimbingRoute("Smooth operator", 11, "7A"))
    ca_3.add_route(ClimbingRoute("Piggy not likey", 12 , "6B+"))
    ca_3.add_route(ClimbingRoute("Orchard", 8, "6A"))
 
    print(ca_1)
    print(ca_3.hardest_route())
    
    areas = [ca_1, ca_2, ca_3]
    print(f"\nMost difficult:\n")
    for area in sort_by_most_difficult(areas):
        print(area)
    print(f"\nGreatest number of routes:\n")    
    for area in sort_by_number_of_routes(areas):
        print(area)
