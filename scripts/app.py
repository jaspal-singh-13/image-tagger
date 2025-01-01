import streamlit as st
import tempfile
import json
from pathlib import Path
from PIL import Image
from tagger import ImageTagger, ConfigurationError
from constants import CONFIG_PATH, DEFAULT_TEMPERATURE

def load_tags_config():
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading tags configuration: {str(e)}")
        return {"whitelist_tags": [], "blacklist_tags": []}

def save_tags_config(config):
    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Error saving tags configuration: {str(e)}")
        return False

st.set_page_config(
    page_title="Image Tagger",
    page_icon="🏷️",
    layout="wide"
)
logo_image = r".\oxima ai logo\black-transparent.png"
st.logo(logo_image, icon_image = logo_image, size="large")

# Add custom CSS for tag management
st.markdown("""
    <style>
        .tag-item {
            padding: 8px 16px;
            margin: 4px 0;
            border-radius: 4px;
            background-color: #f0f2f6;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .tag-group {
            margin: 20px 0;
            padding: 15px;
            border-radius: 8px;
            background-color: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for tag management
with st.sidebar:
    st.title("Tag Management")
    
    # Load current configuration
    tags_config = load_tags_config()
    
    # Search box at the top
    search = st.text_input("🔍 Search tags", placeholder="Type to filter tags...")
    
    # Whitelist tags section
    with st.container():
        st.subheader("📋 Whitelist Tags")
        
        # Add new whitelist tag
        new_tag_col1, new_tag_col2 = st.columns([3, 1])
        with new_tag_col1:
            new_whitelist = st.text_input("Add new whitelist tag", 
                                        placeholder="Enter tag",
                                        key="new_whitelist")
        with new_tag_col2:
            if st.button("Add", key="add_whitelist", type="primary"):
                if new_whitelist and new_whitelist.lower() not in tags_config["whitelist_tags"]:
                    tags_config["whitelist_tags"].append(new_whitelist.lower())
                    save_tags_config(tags_config)
                    st.rerun()
        
        # Display whitelist tags
        filtered_whitelist = [tag for tag in sorted(tags_config["whitelist_tags"]) 
                            if not search or search.lower() in tag.lower()]
        for tag in filtered_whitelist:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.text(tag)
            with col2:
                if st.button("×", key=f"del_{tag}", help=f"Remove {tag}"):
                    tags_config["whitelist_tags"].remove(tag)
                    save_tags_config(tags_config)
                    st.rerun()
    
    # Blacklist tags section
    with st.container():
        st.subheader("⛔ Blacklist Tags")
        
        # Add new blacklist tag
        new_tag_col1, new_tag_col2 = st.columns([3, 1])
        with new_tag_col1:
            new_blacklist = st.text_input("Add new blacklist tag", 
                                        placeholder="Enter tag",
                                        key="new_blacklist")
        with new_tag_col2:
            if st.button("Add", key="add_blacklist", type="primary"):
                if new_blacklist and new_blacklist.lower() not in tags_config["blacklist_tags"]:
                    tags_config["blacklist_tags"].append(new_blacklist.lower())
                    save_tags_config(tags_config)
                    st.rerun()
        
        # Display blacklist tags
        filtered_blacklist = [tag for tag in sorted(tags_config["blacklist_tags"]) 
                            if not search or search.lower() in tag.lower()]
        for tag in filtered_blacklist:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.text(tag)
            with col2:
                if st.button("×", key=f"del_black_{tag}", help=f"Remove {tag}"):
                    tags_config["blacklist_tags"].remove(tag)
                    save_tags_config(tags_config)
                    st.rerun()

def save_uploaded_file(uploaded_file) -> Path:
    """Save uploaded file to temporary location and return path"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        return Path(tmp_file.name)

def main():
    st.subheader("🏷️ Image Tagger")
    st.write("Upload an image to generate relevant tags")

    # Add temperature slider
    temperature = st.slider(
        "Temperature (0.0 = more focused, 1.0 = more creative)",
        min_value=0.0,
        max_value=1.0,
        value=DEFAULT_TEMPERATURE,
        step=0.1,
        help="Controls randomness in tag generation. Lower values give more focused results."
    )

    # Initialize tagger with temperature
    try:
        tagger = ImageTagger(temperature=temperature)
    except ConfigurationError as e:
        st.error(f"Configuration Error: {str(e)}")
        return
    except Exception as e:
        st.error(f"Initialization Error: {str(e)}")
        return

    # File upload
    uploaded_file = st.file_uploader("Choose an image", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        try:
            # Display image
            col1, col2 = st.columns(2)
            with col1:
                st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
            
            # Generate tags
            with st.spinner("Generating tags..."):
                # Save uploaded file temporarily
                tmp_path = save_uploaded_file(uploaded_file)
                tags = tagger.generate_tags(tmp_path)
                print("Generated Tags:", tags)
                
                # Clean up temp file
                tmp_path.unlink()
            
            # Display tags
            with col2:
                st.subheader("Generated Tags:")
                # Create a clean tag display with markdown
                tag_html = " ".join([
                    f"<span style='background-color: #e6e6e6; padding: 0.2rem 0.6rem; "
                    f"border-radius: 1rem; margin: 0.2rem; display: inline-block;'>{tag}</span>"
                    for tag in tags
                ])
                st.markdown(tag_html, unsafe_allow_html=True)
                
                # Display total count
                st.write(f"Total tags generated: {len(tags)}")
                
                # Download tags as text
                if tags:
                    tags_text = ", ".join(tags)
                    st.download_button(
                        label="Download Tags",
                        data=tags_text,
                        file_name="generated_tags.txt",
                        mime="text/plain"
                    )
                
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")

if __name__ == "__main__":
    main()
