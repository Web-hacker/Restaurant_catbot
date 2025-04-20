# Fixing the AttributeError: If 'description' is None, default to "No description"

import json

# Load the scraped JSON data
with open("knowledge_base.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

optimized_corpus = []
metadata_list = []

for entry in raw_data:
    restaurant = entry.get("restaurant_name", "Unknown")
    location = entry.get("restaurant_location", "Unknown")
    city = entry.get("city", "Unknown")
    rating = entry.get("restaurant_rating", "N/A")
    cuisine = entry.get("available_cuisine", "N/A")
    delivery = entry.get("delivery_time", "N/A")

    for dish in entry.get("restaurant_menu", []):
        name = dish.get("dish_name", "Unknown")
        if name is None:
            name = "Unknown"
        name = name.strip()

        description = dish.get("description") or "No description"
        description = description.strip()

        price = f"{dish.get('price', 'N/A')}"
        tags = dish.get("tags", [])
        if tags is None:
            tags = []
        tags_str = ", ".join(tag.capitalize() for tag in tags if isinstance(tag, str))
        dish_type = dish.get("dish_type", "Unknown")
        dish_rating = dish.get("rating", "N/A")
        reviews = dish.get("num_reviews", "0")

        # Build optimized text chunk
        text = (
            f"Dish: {name}\n"
            f"Description: {description}\n"
            f"Price: {price}\n"
            f"Type: {dish_type}, {tags_str}\n"
            f"Restaurant: {restaurant}\n"
            f"Location: {location}, {city}\n"
            f"Restaurant Rating: {rating} ({reviews} reviews)\n"
            f"Cuisine: {cuisine}\n"
            f"Delivery Time: {delivery}"
        )

        optimized_corpus.append(text)
        metadata_list.append({
            "restaurant_name": restaurant,
            "location": location,
            "city": city,
            "dish_name": name,
            "dish_type": dish_type,
            "tags": tags_str,
            "dish_rating": dish_rating,
            "restaurant_rating": rating,
            "price": dish.get("price"),
        })

# Save optimized output
output_path = "optimized_corpus.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump({"documents": optimized_corpus, "metadata": metadata_list}, f, indent=2)

output_path
