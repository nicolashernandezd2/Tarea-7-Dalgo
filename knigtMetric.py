from collections import deque, defaultdict
import heapq

def knightMetric(p, q):
    """
    Retorna el mínimo número de movimientos de caballo para ir del punto p al punto q.
    """
    if p == q:
        return 0

    moves = [
        (2, 1), (1, 2), (-1, 2), (-2, 1),
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]
    
    visited = set()
    queue = deque([(p[0], p[1], 0)])
    visited.add(p)
    
    while queue:
        x, y, dist = queue.popleft()
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if (nx, ny) == q:
                return dist + 1
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny, dist + 1))
    return -1  # En teoría nunca pasa porque un caballo puede llegar a cualquier casilla

def build_complete_graph(points):
    """
    Construye un grafo completo ponderado usando la métrica del caballo.
    """
    n = len(points)
    graph = defaultdict(list)
    for i in range(n):
        for j in range(i + 1, n):
            d = knightMetric(points[i], points[j])
            graph[i].append((j, d))
            graph[j].append((i, d))
    return graph

def prim_mst(graph, n):
    """
    Construye un árbol de expansión mínima (MST) usando el algoritmo de Prim.
    """
    mst = defaultdict(list)
    visited = set()
    min_heap = [(0, 0, -1)]  # (costo, nodo, padre)

    while len(visited) < n:
        cost, u, parent = heapq.heappop(min_heap)
        if u in visited:
            continue
        visited.add(u)
        if parent != -1:
            mst[parent].append(u)
            mst[u].append(parent)
        for v, w in graph[u]:
            if v not in visited:
                heapq.heappush(min_heap, (w, v, u))
    return mst

def dfs_mst(mst, start, visited, path):
    """
    Recorrido DFS sobre el MST para construir el ciclo TSP.
    """
    visited.add(start)
    path.append(start)
    for neighbor in mst[start]:
        if neighbor not in visited:
            dfs_mst(mst, neighbor, visited, path)

def approxMTSP(points):
    """
    Algoritmo aproximado para el problema del TSP múltiple (MTSP),
    usando MST + DFS con la métrica del caballo.
    """
    n = len(points)
    graph = build_complete_graph(points)
    mst = prim_mst(graph, n)

    visited = set()
    path = []
    dfs_mst(mst, 0, visited, path)

    return [points[i] for i in path + [path[0]]]  # ciclo en coordenadas

# ---------------------------
# Ejemplo de uso
# ---------------------------

if __name__ == "__main__":
    puntos = [(0, 0), (1, 2), (3, 3), (2, 1), (-1, -1)]
    ciclo = approxMTSP(puntos)
    
    print("Recorrido MTSP aproximado (coordenadas):")
    for punto in ciclo:
        print(punto)