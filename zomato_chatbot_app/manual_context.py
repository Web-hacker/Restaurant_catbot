import json

# Load the knowledge base
with open("data/knowledge_base.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def give_custom_context(dish_query):
    results = []

    if "restaurant-list" in dish_query.lower():

        for restaurant in data:
            results.append({
                "restaurant_name":restaurant["restaurant_name"]
            })

        if results:
            context = "\n\n".join([
            f"{match['restaurant_name']}"
            for match in results
            ])
        return context
    
    elif "menu-list" in dish_query.lower():
        restaurant_name = None
        for restaurant in data:
            if restaurant["restaurant_name"].lower() in dish_query.lower():
                restaurant_name = restaurant["restaurant_name"]
                for dish in restaurant.get("restaurant_menu", []):
                    results.append({
                        "dish_name": dish["dish_name"],
                        "price": dish.get("price")
                    })
            else:
                continue
        
        if results:
            context = "\n".join([
            f"{restaurant_name} serves {match['dish_name']} at price {match['price']}"
            for match in results
            ])
            return context
        else:
            return "Not found"
    
    elif "serves-dish-item" in dish_query.lower():
        for restaurant in data:
            for dish in restaurant.get("restaurant_menu", []):
                if dish["dish_name"].lower() in dish_query.lower():
                    results.append({
                    "restaurant_name": restaurant["restaurant_name"],
                    "dish_name": dish["dish_name"]
                    })

        if results:
            context = "\n".join([
            f"{match['restaurant_name']} serves {match['dish_name']}"
            for match in results
            ])
            return context
        else:
            return "Not Found"


