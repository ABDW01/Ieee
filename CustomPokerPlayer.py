from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
from pypokerengine.engine.hand_evaluator import HandEvaluator
class CustomPokerPlayer(BasePokerPlayer): 

    
        
    
    def declare_action(self, valid_actions, hole_card, round_state):
        # valid_actions format => [raise_action_info, call_action_info, fold_action_info]
        community_card = round_state['community_card']
        ran=HandEvaluator.eval_hand(self.hole_card, community_card)
        call_action_info =valid_actions[1]
        action, amount = call_action_info["action"], call_action_info["amount"]
        pot_amount = round_state['pot']['main']['amount']
        player_stack = round_state['seats'][self.uuid]['stack']
        win_rate = self.estimate_hole_card_win_rate(hole_card, round_state)
        raise_amount_percent = win_rate -(win_rate/pot_amount)
        amount_to_raise = int(raise_amount_percent * pot_amount)
        max_raise_amount = min(player_stack, amount_to_raise)
        action_histories = round_state['action_histories']
        opponent_actions = [action['action'] for actions in action_histories.values() for action in actions if action['uuid'] != self.uuid]
        aggressive_actions = ['raise', 'bet']
        opponents_aggressive = any(action in aggressive_actions for action in opponent_actions)
        
        
        action_map = {0: 'fold', 1: 'call', 2: 'raise'}
        if win_rate >= 1.5 / self.nb_player:
            chosen_action=action_map[2]
        elif win_rate >=1.0 / self.nb_player:
            chosen_action=action_map[1]
        else:
            chosen_action=action_map[0]
        
        if chosen_action == 'raise':
            chosen_action_info = valid_actions[2]
            chosen_action_amount = min(chosen_action_info["amount"], max_raise_amount)
        else:
            chosen_action_amount = 0
        if opponents_aggressive and chosen_action == 'call':
            bluff_probability = 0.3  # Setting the probability of bluffing
            if np.random.rand() < bluff_probability:
              
              chosen_action = 'raise'  # Blufffing by raising
              chosen_action_amount = max_raise_amount
            else:
              chosen_action = 'fold'
              chosen_action_amount = 0
        if ran > (1>>10):           
            chosen_action = 'raise'
            chosen_action_amount = max_raise_amount
              
        return chosen_action, chosen_action_amount



        

    def receive_game_start_message(self, game_info):
        self.nb_player = game_info['player_num']
        

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass
         

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

