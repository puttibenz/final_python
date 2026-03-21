import streamlit as st

class CampCard:
    """
    A class representing a single camping trip card.
    Encapsulates data and UI rendering logic.
    """
    def __init__(self, data):
        self.name = data.get('name', 'Unnamed Trip')
        self.start_date = data.get('start_date', 'TBA')
        self.duration = data.get('duration', 0)
        self.location = data.get('location', 'Unknown')
        self.price = data.get('price', 0)
        self.slots = data.get('slots', 0)
        self.contact = data.get('contact', 'N/A')
        self.link = data.get('link', '#')
        self.image = data.get('image', 'https://via.placeholder.com/400x250')

    def _get_style(self):
        """Returns the CSS styling for the card."""
        return """
        <style>
        .camp-card-container {
            border-radius: 15px;
            border: 1px solid #e1e4e8;
            padding: 0px;
            margin-bottom: 25px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            background-color: white;
            overflow: hidden;
            height: 100%;
        }
        .camp-card-container:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.15);
        }
        .camp-card-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
        }
        .camp-card-content {
            padding: 20px;
        }
        .camp-card-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 10px;
            line-height: 1.3;
            height: 3.4em; /* Approx 2 lines */
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        .camp-card-meta {
            font-size: 0.85rem;
            color: #666;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .camp-card-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 15px;
        }
        .camp-card-tag {
            background-color: #FFF3E0;
            color: #E65100;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 500;
        }
        .camp-card-price {
            font-size: 1.4rem;
            font-weight: 800;
            color: #FF8C42;
        }
        </style>
        """

    def render(self):
        """Renders the HTML/CSS card in the Streamlit app."""
        st.markdown(self._get_style(), unsafe_allow_html=True)
        
        # HTML structure
        card_html = f"""
        <div class="camp-card-container">
            <img src="{self.image}" class="camp-card-image">
            <div class="camp-card-content">
                <div class="camp-card-title">{self.name}</div>
                <div class="camp-card-meta">
                    <span>📍 {self.location}</span>
                    <span>📅 {self.start_date}</span>
                </div>
                <div class="camp-card-tags">
                    <span class="camp-card-tag">⏱️ {self.duration} Days</span>
                    <span class="camp-card-tag">👤 {self.slots} Slots left</span>
                </div>
                <div class="camp-card-price">฿{self.price:,}</div>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Add Streamlit native buttons for interactivity
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Details", key=f"btn_details_{self.name}", use_container_width=True):
                st.toast(f"Contact: {self.contact}", icon="ℹ️")
        with col2:
            st.link_button("View Post", self.link, use_container_width=True)
