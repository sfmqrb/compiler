from collections import deque

from anytree import Node, RenderTree
from Parser import first_follow
from SemanticLevel import Semantic

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
token_type = ""
token_main = ""


class State:
    id = 0
    nterminal_id = 0
    terminal_trans = dict()
    nterminal_trans = set()
    end_state = False

    # set((int(nterminal),dest_state))

    def __init__(
        self,
        state_id,
        nterminal_id,
        state_terminal_trans,
        state_nterminal_trans,
        end_state,
    ):
        self.id = state_id
        self.nterminal_id = nterminal_id
        self.terminal_trans = state_terminal_trans
        self.nterminal_trans = state_nterminal_trans
        self.end_state = end_state
        id_state_dict[state_id] = self

    def next_state(self, token, tuple_token, line_number, semantic):
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
                Node(
                    tuple_token,
                    parent=tree_heads_Nodes_list[tree_heads_list.__len__(
                    ) - 1],
                )
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
        # non terminal
        else:
            for nt_trans in self.nterminal_trans:
                normal_trans = nterminal_first_dict[nt_trans[0]].__contains__(
                    token)
                epsilon_trans = nterminal_follow_dict[nt_trans[0]].__contains__(
                    token
                ) and nterminal_first_dict[nt_trans[0]].__contains__("")
                if normal_trans or epsilon_trans:
                    states_stack.pop()
                    states_stack.append(nt_trans[1])
                    states_stack.append(nterminal_first_state[nt_trans[0]])
                    tree_heads_Nodes_list.append(
                        Node(
                            str(nt_trans[0]),
                            parent=tree_heads_Nodes_list[tree_heads_list.__len__(
                            ) - 1],
                        )
                    )
                    tree_heads_list.append(str(nt_trans[0]))
                    if log:
                        print("read nterminal to " + str(nt_trans[1]))
                    return False, None
        # if epsilon
        if self.nterminal_id == 'D':
            a = 23
        if self.terminal_trans.__contains__("") and nterminal_follow_dict[self.nterminal_id].__contains__(token):
            state_id = self.terminal_trans[""]
            state = id_state_dict[state_id]
            try:
                Node(
                    "epsilon",
                    parent=tree_heads_Nodes_list[tree_heads_list.__len__(
                    ) - 1],
                )
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
        terminal_semantic_transition_list = list()
        for t in self.terminal_trans.keys():
            if "#" in t:
                terminal_semantic_transition_list.append(t)
        for k in terminal_semantic_transition_list:
            semantic_trans = False
            if len(list(terminal_semantic_transition_list)) < 2:
                semantic_trans = True
            else:
                semantic_trans = nterminal_follow_dict[k].__contains__(token)
            if semantic_trans:
                state_id = self.terminal_trans[k]
                state = id_state_dict[state_id]
                try:
                    Node(
                        k,
                        parent=tree_heads_Nodes_list[tree_heads_list.__len__(
                        ) - 1],
                    )
                except:
                    print(token)
                if len(tuple_token) > 1:
                    current_token = tuple_token[1]
                else:
                    current_token = ""
                semantic.run(k, current_token)
                if state.end_state:
                    states_stack.pop()
                    tree_heads_list.pop()
                    tree_heads_Nodes_list.pop()
                else:
                    states_stack.pop()
                    states_stack.append(state_id)
                if log:
                    print("read token to " + str(state_id))
                return False, None
        # syntax-error
        print("syntax_errors")
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
            error = (
                "#"
                + str(line_number)
                + " : "
                + "syntax error, missing "
                + missing_token
            )
            return False, error
        try:
            missing_nterminal = list(self.nterminal_trans)[0][0]
            if nterminal_follow_dict[missing_nterminal].__contains__(token):
                error = (
                    "#"
                    + str(line_number)
                    + " : "
                    + "syntax error, missing "
                    + str(missing_nterminal)
                )
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
        if token == "$":
            error = "#" + str(line_number) + " : " + \
                "syntax error, Unexpected EOF"
        else:
            error = "#" + str(line_number) + " : " + \
                "syntax error, illegal " + token
        if log:
            print(error)
        return True, error

    def to_str(self):
        print(self.id)
        print(self.nterminal_id)
        print(self.terminal_trans)
        print(self.nterminal_trans)
        print(self.end_state)
