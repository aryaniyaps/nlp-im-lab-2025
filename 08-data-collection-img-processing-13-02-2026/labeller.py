import streamlit as st
import pandas as pd
import os
from pathlib import Path
from PIL import Image
import json
import re

# Expanded predefined options for fast labeling
INGREDIENT_OPTIONS = [
    'bread', 'rice', 'pasta', 'noodles', 'potato', 'sweet_potato', 'oats', 'corn', 
    'wheat', 'flour', 'couscous', 'quinoa', 'barley', 'polenta', 'tortilla',
    'chicken', 'beef', 'pork', 'lamb', 'fish', 'salmon', 'shrimp', 'tuna', 'egg', 
    'tofu', 'tempeh', 'lentils', 'chickpeas', 'black_beans', 'kidney_beans',
    'cheese', 'cheddar', 'mozzarella', 'parmesan', 'feta', 'butter', 'milk', 'yogurt', 'cream',
    'tomato', 'onion', 'garlic', 'carrot', 'celery', 'bell_pepper', 'zucchini', 
    'broccoli', 'cauliflower', 'spinach', 'lettuce', 'kale', 'mushroom', 'eggplant', 
    'cucumber', 'avocado', 'green_beans', 'peas', 'pumpkin', 'squash',
    'lemon', 'lime', 'apple', 'banana', 'orange', 'cilantro', 'parsley', 'basil', 
    'ginger', 'scallions', 'chili', 'jalapeno',
    'almonds', 'peanuts', 'walnuts', 'cashews', 'sesame_seeds', 'pine_nuts',
    'soy_sauce', 'olive_oil', 'coconut_milk', 'honey', 'vinegar', 'mustard',
    'none', 'multiple', 'other'
]

CUISINE_OPTIONS = [
    'indian', 'chinese', 'italian', 'mexican', 'thai', 'japanese', 'american',
    'french', 'greek', 'spanish', 'korean', 'vietnamese', 'indonesian',
    'mediterranean', 'middle_eastern', 'lebanese', 'moroccan', 'turkish',
    'persian', 'malaysian', 'filipino', 'singaporean', 'australian',
    'asian', 'european', 'latin_american', 'caribbean', 'african',
    'fusion', 'none', 'other'
]

# 🧠 SMART PRE-SELECTION RULES
LABEL_TO_INGREDIENTS = {
    r'(pizza|pasta|spaghetti|carbonara|gnocchi|ravio|lasagna|bolognese)': ['cheese', 'tomato', 'pasta'],
    r'(risotto|paella)': ['rice'],
    r'(chicken|wings|curry|nuggets)': ['chicken'],
    r'(beef|steak|burger|hamburger|carpaccio)': ['beef'],
    r'(pork|chop|pulled)': ['pork'],
    r'(lamb|curry)': ['lamb'],
    r'(fish|salmon|sashimi|tuna|trout|cod)': ['fish'],
    r'(shrimp|prawn|scampi)': ['shrimp'],
    r'(bread|sandwich|burger|hotdog|falafel|naan|roti|pita|bagel|pretzel|bruschetta)': ['bread'],
    r'(taco|burrito|quesadilla|enchilada|nachos)': ['tortilla'],
    r'(salad|caprese|caesar|guacamole|ceviche)': ['lettuce', 'tomato'],
    r'(sushi|roll|maki|nigiri)': ['rice', 'fish'],
    r'(pho|ramen|udon|soba|chow mein|pad thai)': ['noodles'],
    r'(fried rice|炒饭)': ['rice'],
    r'(dim sum|dumpling|gyoza|baozi|wonton)': ['dough'],
    r'(naan|roti|dosa|paratha|chapati)': ['bread'],
    r'(dal|dosa|idli|sambar)': ['lentils'],
    r'(omelette|eggs|scrambled|sunny[- ]?side|poached)': ['egg'],
    r'(pancake|waffle|french toast)': ['bread', 'egg'],
    r'(fondue|raclette|gratin|macaroni)': ['cheese'],
}

LABEL_TO_CUISINE = {
    r'(pizza|pasta|spaghetti|gnocchi|lasagna|risotto|tiramisu|carbonara|bolognese|ravioli|parmesan|mozzarella|bruschetta|gelato|macaroni|caprese)': 'italian',
    r'(fried rice|dim sum|dumpling|wonton|chow mein|spring roll|hot dog|fortune cookie|peking duck|mapo tofu)': 'chinese',
    r'(chicken curry|butter chicken|naan|roti|dosa|masala|paneer|samosa|biryani|dal|tikka|korma|vindaloo)': 'indian',
    r'(taco|burrito|quesadilla|enchilada|nachos|guacamole|ceviche|churros)': 'mexican',
    r'(sushi|sashimi|maki|nigiri|ramen|udon|soba|tempura|gyoza|onigiri|miso|teriyaki|donburi|takoyaki)': 'japanese',
    r'(pad thai|pho|spring roll|papaya salad|tom yum|curry)': 'thai',
    r'(croissant|crepe|escargots|fondue|ratatouille|quiche|macaron|beef bourguignon|coq au vin)': 'french',
    r'(hamburger|hot dog|chicken wings|macaroni|club sandwich|pulled pork|ribs|corn dog)': 'american',
    r'(falafel|hummus|gyro|baklava|halloumi|dolma|spanakopita|tzatziki|souvlaki)': 'mediterranean',
}

def smart_predict_labels(label):
    """🧠 Predict ingredients & cuisine from Food101 label"""
    label_lower = label.lower()
    predicted_ingredients = []
    
    for pattern, ingredients in LABEL_TO_INGREDIENTS.items():
        if re.search(pattern, label_lower):
            predicted_ingredients.extend(ingredients)
            predicted_ingredients = list(set(predicted_ingredients))
    
    predicted_cuisine = ''
    for pattern, cuisine in LABEL_TO_CUISINE.items():
        if re.search(pattern, label_lower):
            predicted_cuisine = cuisine
            break
    
    return predicted_ingredients, predicted_cuisine

@st.cache_data
def load_inventory(sample_dir):
    inventory_path = Path(sample_dir) / "image_inventory.csv"
    if not inventory_path.exists():
        st.error("Run Step 1 first to create image inventory!")
        st.stop()
    
    df = pd.read_csv(inventory_path)
    labels_path = Path(sample_dir) / "labels.json"
    
    existing_labels = {}
    if labels_path.exists():
        existing_labels = json.loads(labels_path.read_text())
    
    for col in ['ingredients', 'cuisine']:
        if col not in df.columns:
            df[col] = df['filename'].map({k: v.get(col, '') for k, v in existing_labels.items()}).fillna('')
    
    return df, existing_labels

def save_labels(df, sample_dir):
    labels = {}
    for _, row in df.iterrows():
        if row.get('ingredients') or row.get('cuisine'):
            labels[row['filename']] = {
                'label': row['label'],
                'ingredients': str(row['ingredients']) if pd.notna(row['ingredients']) else '',
                'cuisine': str(row['cuisine']) if pd.notna(row['cuisine']) else ''
            }
    
    labels_path = Path(sample_dir) / "labels.json"
    labels_path.write_text(json.dumps(labels, indent=2))
    
    output_csv = Path(sample_dir) / "final_labeled_data.csv"
    df.to_csv(output_csv, index=False)
    
    st.success(f"✅ Saved {len(labels)} labeled images")

def main():
    st.set_page_config(page_title="Food101 Smart Labeler", layout="wide")
    st.title("🤖 Food101 AI-Smart Multi-Label Image Labeler")
    st.markdown("**🧠 Auto-preselects ingredients & cuisine** based on original Food101 labels")
    
    sample_dir = "./food101_sample"
    df, existing_labels = load_inventory(sample_dir)
    
    # Progress tracking
    total = len(df)
    labeled_mask = (
        (df['ingredients'].notna() & (df['ingredients'] != '')) | 
        (df['cuisine'].notna() & (df['cuisine'] != ''))
    )
    labeled_count = len(df[labeled_mask])
    st.metric("Labeling Progress", f"{labeled_count}/{total}", f"{labeled_count/total*100:.1f}%")
    
    # Filter unlabeled images
    unlabeled_mask = ~labeled_mask
    unlabeled_df = df[unlabeled_mask].copy()
    
    if unlabeled_df.empty:
        st.success("🎉 All images labeled!")
        if st.button("🔄 Reset All Labels", type="secondary"):
            for col in ['ingredients', 'cuisine']:
                df[col] = ''
            save_labels(df, sample_dir)
            st.rerun()
        return
    
    # ✅ FIXED NAVIGATION - Use simple position index
    if 'image_position' not in st.session_state:
        st.session_state.image_position = 0
    
    image_options = unlabeled_df.index.tolist()
    position = st.session_state.image_position % len(image_options)
    idx = image_options[position]
    
    # Navigation buttons FIRST (before selectbox)
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    with col1:
        if st.button("⬅️ Previous", key="prev"):
            st.session_state.image_position -= 1
            st.rerun()
    with col2:
        if st.button("➡️ Next", key="next"):
            st.session_state.image_position += 1
            st.rerun()
    with col3:
        if st.button("🎲 Random", key="random"):
            st.session_state.image_position = len(image_options)
            import random
            st.session_state.image_position = random.randint(0, len(image_options)-1)
            st.rerun()
    with col4:
        st.metric("Position", f"{position+1}/{len(image_options)}")
    
    # 🧠 SMART PREDICTION
    predicted_ings, predicted_cuisine = smart_predict_labels(df.loc[idx, 'label'])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        img_path = Path(sample_dir) / df.loc[idx, 'label'] / df.loc[idx, 'filename']
        image = Image.open(img_path)
        st.image(image, caption=f"**Original: {df.loc[idx, 'label']}**", use_column_width=True)
        st.info(f"🤖 **AI Prediction:** {', '.join(predicted_ings)} | **{predicted_cuisine}**")
    
    with col2:
        st.write("### 🔖 **Smart Labeling** (AI-preselected)")
        
        # Ingredients
        default_ings = predicted_ings if predicted_ings else []
        current_ings = df.loc[idx, 'ingredients']
        if current_ings and current_ings != 'skipped':
            default_ings = [ing.strip() for ing in current_ings.split(',') if ing.strip()]
        
        selected_ingredients = st.multiselect("🥘 **Ingredients**", 
                                            INGREDIENT_OPTIONS,
                                            default=default_ings,
                                            key=f"ing_{idx}")
        ingredients_str = ','.join(selected_ingredients) if selected_ingredients else ''
        
        # Cuisine
        default_cuisine = predicted_cuisine
        current_cuisine = df.loc[idx, 'cuisine']
        if current_cuisine and current_cuisine != 'skipped':
            default_cuisine = current_cuisine
        
        cuisine_options = [''] + CUISINE_OPTIONS
        cuisine_idx = cuisine_options.index(default_cuisine) if default_cuisine in cuisine_options else 0
        cuisine = st.selectbox("🌍 **Cuisine**", 
                             cuisine_options,
                             index=cuisine_idx,
                             key=f"cuisine_{idx}")
        
        # Action buttons
        col1b, col2b, col3b = st.columns([1,1,1])
        if col1b.button("✅ Save", key=f"save_{idx}"):
            df.at[idx, 'ingredients'] = ingredients_str
            df.at[idx, 'cuisine'] = cuisine
            save_labels(df, sample_dir)
            st.success("✅ Saved!")
            st.rerun()
            
        if col2b.button("💾 Save & Next", key=f"save_next_{idx}"):
            df.at[idx, 'ingredients'] = ingredients_str
            df.at[idx, 'cuisine'] = cuisine
            save_labels(df, sample_dir)
            st.session_state.image_position += 1
            st.rerun()
            
        if col3b.button("⏭️ Skip", key=f"skip_{idx}"):
            df.at[idx, 'ingredients'] = 'skipped'
            df.at[idx, 'cuisine'] = 'skipped'
            save_labels(df, sample_dir)
            st.session_state.image_position += 1
            st.rerun()
    
    # Save all button
    if st.button("💾 Save Session", key="save_all"):
        save_labels(df, sample_dir)
    
    # Live stats
    col1s, col2s = st.columns(2)
    with col1s:
        if (df['ingredients'] != '').any():
            ing_counts = df[df['ingredients'] != '']['ingredients'].str.split(',').explode().str.strip().value_counts()
            st.subheader("🥘 Top Ingredients")
            st.bar_chart(ing_counts.head(10))
    with col2s:
        if (df['cuisine'] != '').any():
            st.subheader("🌍 Top Cuisines")
            st.bar_chart(df[df['cuisine'] != '']['cuisine'].value_counts().head(10))

if __name__ == "__main__":
    main()
