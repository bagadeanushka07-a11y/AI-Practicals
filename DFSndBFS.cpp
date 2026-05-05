#include <iostream>
#include <vector>//create dynamic arrays (adjacency list)
#include <queue>
using namespace std;

class Graph{
    int V; // number of vertices
    vector<vector<int>> adj; //adjacency list

public:
//Constructor
    Graph(int V){
        this->V = V;//stores number of vertices
        adj.resize(V);//creates V empty lists
    }
     // Add edge (undirected)
    void addEdge(int u, int v){//Adds connection both ways:
        adj[u].push_back(v);//add element at the end of the vector
        adj[v].push_back(u);

    }
    // DFS Utility (Recursive)
    void DFSUtil(int v, vector<bool> &visited){//& pass by reference
// changes will reflect everywhere
        visited[v] = true;//Prevents infinite loops
        cout << v << " ";//DFS traversal output

        for(int neighbor : adj[v]){//Loop through all neighbors of node
            if(!visited[neighbor]){//Only visit neighbor if it is NOT visited
                DFSUtil(neighbor, visited);
            }
        }
    }
     // DFS Traversal
    void DFS(){
        vector<bool> visited(V, false);

        for(int i = 0; i<V;i++){
            if(!visited[i]){
                DFSUtil(i, visited);

            }
        }
    }
     // BFS Traversal
    void BFS(int start){
        vector<bool>visited(V,false);
        queue<int> q;
//Start from given node:

// Mark it visited
// Push into queue
        visited[start] = true;
        q.push(start);

        while(!q.empty()){//Run until queue becomes empty
            int v = q.front();//Take front element from queue
//  Remove it
            q.pop();
            cout<< v <<" ";


            for (int neighbor : adj[v]) {
                if (!visited[neighbor]) {//process unvisited nodes
                    visited[neighbor] = true;//mark visited
                    q.push(neighbor);//add to q
                }
            }
        }
    }
};

int main(){
    int V,E;
    cout<< "Enter number of vertices:";
    cin>>V;

    Graph g(V);

    cout << "Enter number of edges: ";
    cin >> E;

    cout << "Enter edges (u v):\n";
     for (int i = 0; i < E; i++) {
        int u, v;
        cin >> u >> v;
        g.addEdge(u, v);
    }

     cout << "\nDFS Traversal: ";
    g.DFS();

    int start;
    cout << "\nEnter starting node for BFS: ";
    cin >> start;
       
    cout << "BFS Traversal: ";
    g.BFS(start);

    return 0;

}


// ▶ Start: DFSUtil(0)
// Step 1:
// Visit 0 → print 0
// Step 2:
// Go to neighbor 1 → call DFSUtil(1)
// ▶ DFSUtil(1)
// Visit 1 → print 1
// Go to 3 → call DFSUtil(3)
// ▶ DFSUtil(3)
// Visit 3 → print 3
// Go to 2 → call DFSUtil(2)
// ▶ DFSUtil(2)
// Visit 2 → print 2
// All neighbors visited → return
