class Node {
  constructor(i){
    this.index = i;
    this.id = 'n' + i;
    this.label = 'Node ' + i;
    this.x =  Math.random();
    this.y = Math.random();
    this.size = Math.random();
    this.color = '#666';
  }
}

let i,
    s,
    N = 10000,    // Number of nodes
    E = 50000,    // Number of edges
    g = {       // The graph
      nodes: [],
      edges: []
    },
    Adj = [];


// Generate random nodes
for (i = 0; i < N; i++){
  g.nodes.push(new Node(i));
  Adj[i] = [];
}

// Generate random edges
for (i = 0; i < E; i++){
  let node1 = Math.floor(Math.random() * N);
  let node2 = Math.floor(Math.random() * N);
  // Add to adjacency list
  Adj[node1].push(node2);
  Adj[node2].push(node1);
}

// Add all edges to the graph and color them grey
let current_edge = 0;
for (i = 0; i < N; i++){
  for (j = 0; j < Adj[i].length; j++){
    g.edges.push({
      id: 'e' + current_edge,
      source: 'n' + (i | 0),
      target: 'n' + (Adj[i][j] | 0),
      size: 0.5,
      color: '#ccc'
    });
    current_edge++;
  }
}

// Instantiate sigma
s = new sigma({
  graph: g,
  container: 'graph-container'
});

s.settings({
  minEdgeSize: 0.5,
  maxEdgeSize: 3,
});

s.refresh();
