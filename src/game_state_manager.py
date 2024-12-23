class GameStateManager:
    def __init__(self):
        self.states = {}
        self.current_state = None

    def register_state(self, state_name, state_instance):
        self.states[state_name] = state_instance

    def switch_state(self, state_name):
        if state_name in self.states:
            self.current_state = self.states[state_name]
            self.current_state.on_enter()

    def handle_events(self, event_list):
        if self.current_state and hasattr(self.current_state, 'handle_events'):
            self.current_state.handle_events(event_list)

    def update(self):
        if self.current_state and hasattr(self.current_state, 'update'):
            self.current_state.update()

    def render(self, screen):
        if self.current_state and hasattr(self.current_state, 'render'):
            self.current_state.render(screen)
