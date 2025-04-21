"""
manual_context.py
-----------------
Provides structured context for specific hardcoded queries (fallback logic)
using the prebuilt knowledge base JSON.

Supported query types:
- restaurant-list: List all restaurants in the knowledge base
- menu-list: List menu items (with prices) of a specific restaurant
- serves-dish-item: Return restaurants that serve a specific dish

Usage:
    from manual_context import give_custom_context
    response = give_custom_context("menu-list Anandeshwar Dhaba")


"""

import json

# -------------------------------
# Load structured knowledge base
# -------------------------------
with open("../Structured_data/knowledge_base.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# -------------------------------
# Main Custom Context Handler
# -------------------------------
def give_custom_context(dish_query: str) -> str:
    """
    Manually search the structured knowledge base for predefined keywords.

    Parameters:
        dish_query (str): The user query

    Returns:
        str: Context string to feed to the language model
    """
    results = []

    # --- Case 1: List all restaurants ---
    if "restaurant-list" in dish_query.lower():
        results = [r["restaurant_name"] for r in data]
        if results:
            return ", ".join(results)
        return "No restaurants found in the knowledge base."

    # --- Case 2: Get menu of a specific restaurant ---
    elif "menu-list" in dish_query.lower():
        restaurant_name = None
        for restaurant in data:
            if restaurant["restaurant_name"].lower() in dish_query.lower():
                restaurant_name = restaurant["restaurant_name"]
                for dish in restaurant.get("restaurant_menu", []):
                    results.append({
                        "dish_name": dish["dish_name"],
                        "price": dish.get("price", "N/A")
                    })
                break  # Stop after first match

        if results and restaurant_name:
            return "  :;  ".join([
                f"{restaurant_name} serves {dish['dish_name']} at price {dish['price']}"
                for dish in results
            ])
        return "No matching restaurant or menu found."

    # --- Case 3: Find all restaurants serving a particular dish ---
    elif "serves-dish-item" in dish_query.lower():
        for restaurant in data:
            for dish in restaurant.get("restaurant_menu", []):
                if dish["dish_name"].lower() in dish_query.lower():
                    results.append({
                        "restaurant_name": restaurant["restaurant_name"],
                        "dish_name": dish["dish_name"]
                    })
                    break

        if results:
            return " , ".join([
                f"{match['restaurant_name']} serves {match['dish_name']}"
                for match in results
            ])
        return "No restaurants found serving this dish."

    # --- Fallback ---
    return "Unsupported custom query format."
