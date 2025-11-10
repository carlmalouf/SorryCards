import streamlit as st
import random

# Card definitions based on the official Sorry! game
CARD_TYPES = {
    '1': {'count': 5, 'color': '#FF6B6B', 'description': 'Move from Start or move 1 space forward'},
    '2': {'count': 4, 'color': '#4ECDC4', 'description': 'Move from Start or move 2 spaces forward'},
    '3': {'count': 4, 'color': '#45B7D1', 'description': 'Move 3 spaces forward'},
    '4': {'count': 4, 'color': '#96CEB4', 'description': 'Move 4 spaces backward'},
    '5': {'count': 4, 'color': '#FFEAA7', 'description': 'Move 5 spaces forward'},
    '7': {'count': 4, 'color': '#DFE6E9', 'description': 'Move 7 spaces forward or split between two pawns'},
    '8': {'count': 4, 'color': '#A29BFE', 'description': 'Move 8 spaces forward'},
    '10': {'count': 4, 'color': '#FD79A8', 'description': 'Move 10 spaces forward or 1 space backward'},
    '11': {'count': 4, 'color': '#FDCB6E', 'description': 'Move 11 spaces forward or switch with opponent'},
    '12': {'count': 4, 'color': '#6C5CE7', 'description': 'Move 12 spaces forward'},
    'Sorry!': {'count': 4, 'color': '#E17055', 'description': 'Move from Start and bump opponent back to their Start'}
}

def create_card_html(card_value, size='large'):
    """Create an HTML/CSS representation of a Sorry! card"""
    card_info = CARD_TYPES[card_value]
    color = card_info['color']
    description = card_info['description']
    
    if size == 'large':
        card_style = "width: 300px; height: 420px; font-size: 60px;"
        desc_style = "font-size: 16px; padding: 20px;"
    else:  # small
        card_style = "width: 150px; height: 210px; font-size: 30px;"
        desc_style = "font-size: 10px; padding: 10px; display: none;"
    
    card_html = f"""
    <div style="
        {card_style}
        background: white;
        border: 8px solid {color};
        border-radius: 15px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 0 auto;
    ">
        <div style="
            background: {color};
            width: 100%;
            padding: 20px;
            text-align: center;
            border-radius: 7px 7px 0 0;
            color: white;
            font-weight: bold;
            font-size: inherit;
        ">
            {card_value}
        </div>
        <div style="
            {desc_style}
            text-align: center;
            color: #333;
            flex-grow: 1;
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            {description if size == 'large' else ''}
        </div>
    </div>
    """
    return card_html

def initialize_deck():
    """Create a deck with the correct distribution of cards"""
    deck = []
    for card_type, info in CARD_TYPES.items():
        deck.extend([card_type] * info['count'])
    random.shuffle(deck)
    return deck

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'deck' not in st.session_state:
        st.session_state.deck = initialize_deck()
    
    if 'drawn_cards' not in st.session_state:
        st.session_state.drawn_cards = []
    
    if 'players' not in st.session_state:
        st.session_state.players = []
    
    if 'current_player_index' not in st.session_state:
        st.session_state.current_player_index = 0
    
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False

def draw_card():
    """Draw a card from the deck"""
    if not st.session_state.deck:
        # Reshuffle if deck is empty
        st.session_state.deck = initialize_deck()
        st.toast("Deck reshuffled! 🔄")
    
    card = st.session_state.deck.pop()
    st.session_state.drawn_cards.append(card)
    
    # Move to next player
    if st.session_state.players:
        st.session_state.current_player_index = (
            st.session_state.current_player_index + 1
        ) % len(st.session_state.players)
    
    return card

def main():
    st.set_page_config(
        page_title="Sorry! Card Game",
        page_icon="🎴",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .big-font {
            font-size: 30px !important;
            font-weight: bold;
        }
        .player-turn {
            font-size: 24px;
            color: #E17055;
            font-weight: bold;
            padding: 10px;
            background-color: #FFF5F5;
            border-radius: 10px;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    initialize_session_state()
    
    # Title
    st.title("🎴 Sorry! Card Game")
    st.markdown("---")
    
    # Sidebar for game setup
    with st.sidebar:
        st.header("⚙️ Game Setup")
        
        if not st.session_state.game_started:
            st.subheader("Add Players")
            
            num_players = st.number_input(
                "Number of players:",
                min_value=2,
                max_value=4,
                value=2,
                step=1
            )
            
            player_names = []
            for i in range(num_players):
                name = st.text_input(
                    f"Player {i+1} name:",
                    value=f"Player {i+1}",
                    key=f"player_{i}"
                )
                player_names.append(name)
            
            if st.button("🎮 Start Game", type="primary"):
                st.session_state.players = player_names
                st.session_state.game_started = True
                st.rerun()
        else:
            st.success("✅ Game in progress!")
            st.write("**Players:**")
            for i, player in enumerate(st.session_state.players):
                if i == st.session_state.current_player_index:
                    st.write(f"👉 **{player}** (Current)")
                else:
                    st.write(f"   {player}")
            
            st.markdown("---")
            
            if st.button("🔄 New Game"):
                st.session_state.clear()
                st.rerun()
        
        st.markdown("---")
        st.subheader("📊 Deck Info")
        st.write(f"Cards remaining: **{len(st.session_state.deck)}** / 45")
        st.write(f"Cards drawn: **{len(st.session_state.drawn_cards)}**")
    
    # Main content
    if not st.session_state.game_started:
        st.info("👈 Please set up the game in the sidebar to begin!")
        
        # Show card type reference
        st.subheader("📋 Card Types Reference")
        cols = st.columns(3)
        card_list = list(CARD_TYPES.keys())
        
        for idx, card_type in enumerate(card_list):
            with cols[idx % 3]:
                info = CARD_TYPES[card_type]
                st.markdown(f"**{card_type}** ({info['count']}x)")
                st.caption(info['description'])
    else:
        # Show current player
        current_player = st.session_state.players[st.session_state.current_player_index]
        st.markdown(
            f'<div class="player-turn">🎯 Current Turn: {current_player}</div>',
            unsafe_allow_html=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Draw card button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎴 Draw Card", type="primary", use_container_width=True):
                drawn_card = draw_card()
                st.session_state.last_drawn = drawn_card
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display last drawn card
        if st.session_state.drawn_cards:
            st.subheader("🎴 Last Card Drawn")
            last_card = st.session_state.drawn_cards[-1]
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                card_html = create_card_html(last_card, size='large')
                st.markdown(card_html, unsafe_allow_html=True)
            
            # Show description
            st.info(f"**{last_card}**: {CARD_TYPES[last_card]['description']}")
        
        st.markdown("---")
        
        # Show card history
        if len(st.session_state.drawn_cards) > 1:
            st.subheader("📜 Recent Cards (Last 5)")
            
            # Get last 5 cards (excluding the current one)
            recent_cards = st.session_state.drawn_cards[-6:-1] if len(st.session_state.drawn_cards) > 5 else st.session_state.drawn_cards[:-1]
            recent_cards.reverse()  # Show most recent first
            
            if recent_cards:
                cols = st.columns(min(5, len(recent_cards)))
                for idx, card in enumerate(recent_cards[:5]):
                    with cols[idx]:
                        card_html = create_card_html(card, size='small')
                        st.markdown(card_html, unsafe_allow_html=True)
                        st.caption(card)

if __name__ == "__main__":
    main()
