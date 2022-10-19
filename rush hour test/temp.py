# async def solve(self):
#         """
#         Get best path to solution
#         """
#         open_nodes = [self.root]
#         nodes = [str(self.root[1])]

#         while True:
#             node = open_nodes.pop(0)

#             if test_win(node[1]):
#                 print("SOLVED")
#                 self.solution = self.calculate_solution(get_path(node))
#                 return

#             for new_node in get_new_nodes(node, self.size):
#                 if str(new_node[1]) not in nodes:
#                     nodes.append(str(new_node[1]))
#                     open_nodes.append(new_node)
