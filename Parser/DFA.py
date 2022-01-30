from collections import deque

import jsonpickle
from anytree import Node, RenderTree
from Parser import first_follow
import json

log = False
id_state_dict = dict()
states_stack = deque()
nterminal_first_dict = first_follow.first
nterminal_follow_dict = first_follow.follow
nterminal_first_state = dict()
# state_id_nterminal_dict = dict()
pars_tree = (0, [])
tree_heads_list = ["Program"]
first_node = Node(tree_heads_list[0])
tree_heads_Nodes_list = [first_node]
token_type = ''
token_main = ''


class State:
    id = 0
    nterminal_id = 0
    terminal_trans = dict()
    nterminal_trans = set()
    end_state = False

    # set((int(nterminal),dest_state))

    def __init__(self, state_id, nterminal_id, state_terminal_trans, state_nterminal_trans, end_state):
        self.id = state_id
        self.nterminal_id = nterminal_id
        self.terminal_trans = state_terminal_trans
        self.nterminal_trans = state_nterminal_trans
        self.end_state = end_state
        id_state_dict[state_id] = self

    def next_state(self, token, tuple_token, line_number):
        if log:
            print("token" + str(tuple_token))
            print(self.to_str())
        if self.end_state:
            states_stack.pop()
            tree_heads_list.pop()
            tree_heads_Nodes_list.pop()
            if log:
                print("end state, return")
            return False, None
        # if its terminal
        if self.terminal_trans.__contains__(token):
            state_id = self.terminal_trans[token]
            state = id_state_dict[state_id]
            try:
                Node(tuple_token, parent=tree_heads_Nodes_list[tree_heads_list.__len__() - 1])
            except:
                print(token)
            if state.end_state:
                states_stack.pop()
                tree_heads_list.pop()
                tree_heads_Nodes_list.pop()
            else:
                states_stack.pop()
                states_stack.append(state_id)
            if log:
                print("read token to " + str(state_id))
            return True, None
        #
        else:
            for nt_trans in self.nterminal_trans:
                normal_trans = nterminal_first_dict[nt_trans[0]].__contains__(token)
                epsilon_trans = nterminal_follow_dict[nt_trans[0]].__contains__(token) and \
                                nterminal_first_dict[nt_trans[0]].__contains__('')
                if normal_trans or epsilon_trans:
                    states_stack.pop()
                    states_stack.append(nt_trans[1])
                    states_stack.append(nterminal_first_state[nt_trans[0]])
                    tree_heads_Nodes_list.append(
                        Node(str(nt_trans[0]), parent=tree_heads_Nodes_list[tree_heads_list.__len__() - 1]))
                    tree_heads_list.append(str(nt_trans[0]))
                    if log:
                        print("read nterminal to " + str(nt_trans[1]))
                    return False, None
        # if epsilon
        if self.terminal_trans.__contains__(''):
            state_id = self.terminal_trans['']
            state = id_state_dict[state_id]
            try:
                Node('epsilon', parent=tree_heads_Nodes_list[tree_heads_list.__len__() - 1])
            except:
                print(token)
            if state.end_state:
                states_stack.pop()
                tree_heads_list.pop()
                tree_heads_Nodes_list.pop()
            else:
                states_stack.pop()
                states_stack.append(state_id)
            return False, None
        # if semantic routine
        # if self.nterminal_trans.__contains__('#'):
        #     state_id = self.terminal_trans[self.terminal_trans.keys[0]]
        #     state = id_state_dict[state_id]
        #     try:
        #         Node(tuple_token, parent=tree_heads_Nodes_list[tree_heads_list.__len__() - 1])
        #     except:
        #         print(token)
        #     # todo run semantic routine
        #     if state.end_state:
        #         states_stack.pop()
        #         tree_heads_list.pop()
        #         tree_heads_Nodes_list.pop()
        #     else:
        #         states_stack.pop()
        #         states_stack.append(state_id)
        #     if log:
        #         print("read token to " + str(state_id))
        #     return True, None
        # syntax-error
        if self.terminal_trans.keys().__len__() > 0:
            missing_token = list(self.terminal_trans.keys())[0]
            state_id = self.terminal_trans[missing_token]
            state = id_state_dict[state_id]
            # try:
            #     Node('epsilon', parent=tree_heads_Nodes_list[tree_heads_list.__len__() - 1])
            # except:
            #     print(token)
            if state.end_state:
                states_stack.pop()
                tree_heads_list.pop()
                tree_heads_Nodes_list.pop()
            else:
                states_stack.pop()
                states_stack.append(state_id)
            error = "#" + str(line_number) + " : " + "syntax error, missing " + missing_token
            return False, error
        try:
            missing_nterminal = list(self.nterminal_trans)[0][0]
            if nterminal_follow_dict[missing_nterminal].__contains__(token):
                error = "#" + str(line_number) + " : " + "syntax error, missing " + str(
                    missing_nterminal)
                state_id = list(self.nterminal_trans)[0][1]
                state = id_state_dict[state_id]
                # try:
                #     Node('epsilon', parent=tree_heads_Nodes_list[tree_heads_list.__len__() - 1])
                # except:
                #     print(token)
                if state.end_state:
                    states_stack.pop()
                    tree_heads_list.pop()
                    tree_heads_Nodes_list.pop()
                else:
                    states_stack.pop()
                    states_stack.append(state_id)
                if log:
                    print(error)
                return False, error
            # self.terminal_trans = dict()
        except:
            a = 1
        if token == '$':
            error = "#" + str(line_number) + " : " + "syntax error, Unexpected EOF"
        else:
            error = "#" + str(line_number) + " : " + "syntax error, illegal " + token
        if log:
            print(error)
        return True, error

    def to_str(self):
        print(self.id)
        print(self.nterminal_id)
        print(self.terminal_trans)
        print(self.nterminal_trans)
        print(self.end_state)


def save_states():
    global id_state_dict
    jsonpickle.unpickler.loadclass("Parser.DFA.State")
    nodes_json_pickled = jsonpickle.encode(id_state_dict, keys=False)
    nodes_json = json.dumps(nodes_json_pickled)
    nodes_json_pickled1 = jsonpickle.decode(nodes_json, keys=False)
    python_file = open("states.json", "w")
    python_file.write(nodes_json_pickled1)
    python_file.close()
    nodes_json_pickled = jsonpickle.encode(nterminal_first_state, keys=False)
    nodes_json = json.dumps(nodes_json_pickled)
    nodes_json_pickled1 = jsonpickle.decode(nodes_json, keys=False)
    python_file = open("nterminal_first_state.json", "w")
    python_file.write(nodes_json_pickled1)
    python_file.close()


def load_state():
    global id_state_dict
    global nterminal_first_state
    python_file = open("states.json", "r")
    state_dict_load = jsonpickle.unpickler.decode(python_file.read())
    id_state_dict = {int(k): v for k, v in state_dict_load.items()}
    id_state_dict
    python_file = open("nterminal_first_state.json", "r")
    nterminal_first_state = jsonpickle.unpickler.decode(python_file.read())
# nterminal_first_dict = {0: {'a'}, 1: {'b', 'x', 'w'}, 2: {'x', 'w'}, 3: {'z', 'a', ''}}
# nterminal_follow_dict = {0: {'$'}, 1: {'$'}, 2: {'$'}, 3: {'$'}}
# # s : 0 - A : 1 - B : 2 - C : 3
# s1 = State(1, 0, {'a': 2}, {}, False)
# s2 = State(2, 0, dict(), {(1, 3)}, False)
# s3 = State(3, 0, {'$': 12}, {}, False)
# s12 = State(12, 0, dict(), {}, True)
# s4 = State(4, 1, {'b': 5}, {(2, 6)}, False)
# s5 = State(5, 1, dict(), {(3, 6)}, False)
# s6 = State(6, 1, dict(), {}, True)
# s7 = State(7, 2, {'x': 8, 'w': 9}, set(), False)
# s8 = State(8, 2, {'y': 9}, set(), False)
# s9 = State(9, 2, dict(), {}, True)
# s10 = State(10, 3, {'z': 11, 'a': 11, '': 11}, set(), False)
# s11 = State(11, 3, dict(), {}, True)
# nterminal_first_state = {0: 1, 1: 4, 2: 7, 3: 10}
# states_stack.append(1)
# b = states_stack[states_stack.__len__() - 1]
#
# a = 1
# string = ['a', 'b', '$']
# while string.__len__() > 0:
#     last_state_id = states_stack[states_stack.__len__() - 1]
#     last_state = id_state_dict[last_state_id]
#     next_token = last_state.next_state(string[0])
#     if next_token:
#         string.pop(0)
# for pre, fill, node in RenderTree(first_node):
#     print("%s%s" % (pre, node.name))
