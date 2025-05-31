def treeVC(tree, root):
    """
    tree: diccionario {nodo: [hijos]}
    root: nodo raíz del árbol
    Retorna el tamaño de la cobertura mínima de vértices
    """
    from collections import defaultdict
    dp = defaultdict(lambda: [0, 0])  # dp[node] = [sin_node, con_node]

    def dfs(u, parent):
        dp[u][0] = 0  # no incluye u
        dp[u][1] = 1  # incluye u

        for v in tree[u]:
            if v == parent:
                continue
            dfs(v, u)
            dp[u][0] += dp[v][1]  # si no incluimos u, debemos incluir todos los hijos
            dp[u][1] += min(dp[v][0], dp[v][1])  # si incluimos u, elegimos el mínimo de los hijos

    dfs(root, None)
    return min(dp[root][0], dp[root][1])

"""
Note que la complejidad es O(n), ya que cada nodo y arista se visita una sola vez.
"""