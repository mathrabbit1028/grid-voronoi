#include <bits/stdc++.h>

using namespace std;

typedef pair<int,int> pii;
typedef pair<double, double> pdd;

const double EPS = 1e-9;
int dcmp(double x){ return x < -EPS? -1 : x > EPS ? 1 : 0; }

double operator / (pdd a,    pdd b){ return a.first * b.second - a.second * b.first; }
pdd    operator * (double b, pdd a){ return pdd(b * a.first, b * a.second); }
pdd    operator + (pdd a,    pdd b){ return pdd(a.first + b.first, a.second + b.second); }
pdd    operator - (pdd a,    pdd b){ return pdd(a.first - b.first, a.second - b.second); }

double sq(double x){ return x*x; }
double size(pdd p){ return hypot(p.first, p.second); }
double sz2(pdd p){ return sq(p.first) + sq(p.second); }
pdd r90(pdd p){ return pdd(-p.second, p.first); }

pdd line_intersect(pdd a, pdd b, pdd u, pdd v){ return u + (((a-u)/b) / (v/b))*v; }
pdd get_circumcenter(pdd p0, pdd p1, pdd p2){
	return line_intersect(0.5 * (p0+p1), r90(p0-p1), 0.5 * (p1+p2), r90(p1-p2));
}

// https://www.youtube.com/watch?v=h_vvP4ah6Ck
double parabola_intersect(pdd left, pdd right, double sweepline){
	/*
	if(dcmp(left.second - right.second) == 0) return (left.first + right.first) / 2.0; /*/
	auto f2 = [](pdd left, pdd right, double sweepline){
		int sign = left.first < right.first ? 1 : -1;
		pdd m = 0.5 * (left+right);
		pdd v = line_intersect(m, r90(right-left), pdd(0, sweepline), pdd(1, 0));
		pdd w = line_intersect(m, r90(left-v), v, left-v);
		double l1 = size(v-w), l2 = sqrt(sq(sweepline-m.second) - sz2(m-w)), l3 = size(left-v);
		return v.first + (m.first - v.first) * l3 / (l1 + sign * l2);
	};
	if(fabs(left.second - right.second) < fabs(left.first - right.first) * EPS) return f2(left, right, sweepline);// */
	int sign = left.second < right.second ? -1 : 1;
	pdd v = line_intersect(left, right-left, pdd(0, sweepline), pdd(1, 0));
	double d1 = sz2(0.5 * (left+right) - v), d2 = sz2(0.5 * (left-right));
	return v.first + sign * sqrt(max(0.0, d1 - d2));
}

class Beachline{
	public:
		struct node{
			node(){}
			node(pdd point, int idx):point(point), idx(idx), end(0), 
				link{0, 0}, par(0), prv(0), nxt(0) {}
			pdd point; int idx; int end;
			node *link[2], *par, *prv, *nxt;
		};
		node *root;
		double sweepline;

		Beachline() : sweepline(-1e20), root(NULL){ }
		inline int dir(node *x){ return x->par->link[0] != x; }

		//     p        n          p            n
		//    / \      / \        / \          / \
		//   n   d => a   p   or a   n   =>   p   d
		//  / \          / \        / \      / \
		// a   b        b   d      c   d    a   c

		void rotate(node *n){
			node *p = n->par;         int d = dir(n);
			p->link[d] = n->link[!d]; if(n->link[!d]) n->link[!d]->par = p;
			n->par = p->par;          if(p->par) p->par->link[dir(p)] = n;
			n->link[!d] = p;          p->par = n;
		}

		void splay(node *x, node *f = NULL){
			while(x->par != f){
				if(x->par->par == f);
				else if(dir(x) == dir(x->par)) rotate(x->par);
				else rotate(x);
				rotate(x);
			}
			if(f == NULL) root = x;
		}

		void insert(node *n, node *p, int d){
			splay(p); node* c = p->link[d];
			n->link[d] = c; if(c) c->par = n;
			p->link[d] = n; n->par = p;

			node *prv = !d?p->prv:p, *nxt = !d?p:p->nxt;
			n->prv = prv;   if(prv) prv->nxt = n;
			n->nxt = nxt;   if(nxt) nxt->prv = n;
		}

		void erase(node* n){
			node *prv = n->prv, *nxt = n->nxt;
			if(!prv && !nxt){ if(n == root) root = NULL; return; }
			n->prv = NULL;   if(prv) prv->nxt = nxt;
			n->nxt = NULL;   if(nxt) nxt->prv = prv;
			splay(n);
			if(!nxt){
				root->par = NULL; n->link[0] = NULL;
				root = prv;
			}
			else{
				splay(nxt, n);     node* c = n->link[0];
				nxt->link[0] = c;  c->par = nxt;         n->link[0] = NULL;
				n->link[1] = NULL; nxt->par = NULL;
				root = nxt;
			}
		}
		bool get_event(node* cur, double &next_sweep){
			if(!cur->prv || !cur->nxt) return false;
			pdd u = r90(cur->point - cur->prv->point);
			pdd v = r90(cur->nxt->point - cur->point);
			if(dcmp(u/v) != 1) return false;
			pdd p = get_circumcenter(cur->point, cur->prv->point, cur->nxt->point);
			next_sweep = p.second + size(p - cur->point);
			return true;
		}
		node* find_beachline(double x){
			node* cur = root;
			while(cur){
				double left = cur->prv ? parabola_intersect(cur->prv->point, cur->point, sweepline) : -1e30;
				double right = cur->nxt ? parabola_intersect(cur->point, cur->nxt->point, sweepline) : 1e30;
				if(left <= x && x <= right){ splay(cur); return cur; }
				cur = cur->link[x > right];
			}
		}
}; using BeachNode = Beachline::node;

static BeachNode* arr;
static int sz;
static BeachNode* new_node(pdd point, int idx){
	arr[sz] = BeachNode(point, idx);
	return arr + (sz++);
}

struct event{
	event(double sweep, int idx):type(0), sweep(sweep), idx(idx){}
	event(double sweep, BeachNode* cur):type(1), sweep(sweep), prv(cur->prv->idx), cur(cur), nxt(cur->nxt->idx){}
	int type, idx, prv, nxt;
	BeachNode* cur;
	double sweep;
	bool operator>(const event &l)const{ return sweep > l.sweep; }
};

void VoronoiDiagram(vector<pdd> &input, vector<pdd> &vertex, vector<pii> &edge, vector<pii> &area){
	Beachline beachline = Beachline();
	priority_queue<event, vector<event>, greater<event>> events;

	auto add_edge = [&](int u, int v, int a, int b, BeachNode* c1, BeachNode* c2){
		if(c1) c1->end = edge.size()*2;
		if(c2) c2->end = edge.size()*2 + 1;
		edge.emplace_back(u, v);
		area.emplace_back(a, b);
	};
	auto write_edge = [&](int idx, int v){ idx%2 == 0 ? edge[idx/2].first = v : edge[idx/2].second = v; };
	auto add_event = [&](BeachNode* cur){ double nxt; if(beachline.get_event(cur, nxt)) events.emplace(nxt, cur); };

	int n = input.size(), cnt = 0;
	arr = new BeachNode[n*4]; sz = 0;
	sort(input.begin(), input.end(), [](const pdd &l, const pdd &r){
			return l.second != r.second ? l.second < r.second : l.first < r.first;
			});

	BeachNode* tmp = beachline.root = new_node(input[0], 0), *t2;
	for(int i = 1; i < n; i++){
		if(dcmp(input[i].second - input[0].second) == 0){
			add_edge(-1, -1, i-1, i, 0, tmp);
			beachline.insert(t2 = new_node(input[i], i), tmp, 1);
			tmp = t2;
		}
		else events.emplace(input[i].second, i);
	}
	while(events.size()){
		event q = events.top(); events.pop();
		BeachNode *prv, *cur, *nxt, *site;
		int v = vertex.size(), idx = q.idx;
		beachline.sweepline = q.sweep;
		if(q.type == 0){
			pdd point = input[idx];
			cur = beachline.find_beachline(point.first);
			beachline.insert(site = new_node(point, idx), cur, 0);
			beachline.insert(prv = new_node(cur->point, cur->idx), site, 0);
			add_edge(-1, -1, cur->idx, idx, site, prv);
			add_event(prv); add_event(cur);
		}
		else{
			cur = q.cur, prv = cur->prv, nxt = cur->nxt;
			if(!prv || !nxt || prv->idx != q.prv || nxt->idx != q.nxt) continue;
			vertex.push_back(get_circumcenter(prv->point, nxt->point, cur->point));
			write_edge(prv->end, v); write_edge(cur->end, v);
			add_edge(v, -1, prv->idx, nxt->idx, 0, prv);
			beachline.erase(cur);
			add_event(prv); add_event(nxt);
		}
	}
	delete arr;
}

static double dx = 0, dy = 0, scale = 1e-8;
std::vector<pdd> input;
std::vector<pdd> vertex;
std::vector<pii> edge;
std::vector<pii> area;

void printinfo() {
	cout << "vertex : \n";
	for (pdd c : vertex) cout << c.first << " " << c.second << "\n";
	cout << "edge : \n";
	for (int i = 0; i < edge.size(); i++) {
		cout << edge[i].first << " " << edge[i].second << ", " 
			<< area[i].first << " " << area[i].second << "\n";
	}
	cout << "\n";
}

int grid[5050][5050];
double mindis[5050][5050];
int ch[5050][5050];
queue<pii> q, q1;
vector< pair<double, int> > reorder;

void bound(int x, int y, int can) {
	double val = (x - input[can].first) * (x - input[can].first) 
		+ (y - input[can].second) * (y - input[can].second);
	if (val < mindis[x][y]) { 
		grid[x][y] = reorder[can].second;
		mindis[x][y] = val;
		return; 
	}
	if (val == mindis[x][y]) { 
		grid[x][y] = min(grid[x][y], reorder[can].second); 
		return; 
	}
}

int main() {
	int n, m;
	double lx = 1e10, rx = -1e10, ly = 1e10, ry = -1e10;
	cin >> n >> m;
	for(int i = 0; i < n; i++){
		double a, b;
		cin >> a >> b;
		input.emplace_back(a, b);
		lx = std::min(lx, a);
		rx = std::max(rx, a);
		ly = std::min(ly, b);
		ry = std::max(ry, b);
	}
	dx = -(rx+lx)/2;
	dy = (ry+ly)/2;
	scale = 1. / std::max(rx-lx, ry-ly);
	for (int i = 0; i < n; i++) reorder.emplace_back(input[i].second, i);
	sort(input.begin(), input.end());
	sort(reorder.begin(), reorder.end());
	input.resize(unique(input.begin(), input.end()) - input.begin());
	VoronoiDiagram(input, vertex, edge, area);
	//cout << "\n";
	//for (int i = 0; i < n; i++) cout << input[i].first << " " << input[i].second << "\n";

	//printinfo();

	for (int i = 1; i <= m; i++) for (int j = 1; j <= m; j++) grid[i][j] = n;
	for (int i = 1; i <= m; i++) for (int j = 1; j <= m; j++) mindis[i][j] = 1e9;

	for (int i = 0; i < n; i++) {
		pii coor = input[i];
		q1.push({(int)ceil(coor.first), (int)ceil(coor.second)});
		ch[(int)ceil(coor.first)][(int)ceil(coor.second)] = 1;
		bound((int)ceil(coor.first), (int)ceil(coor.second), i);

		q1.push({(int)ceil(coor.first), (int)floor(coor.second)});
		ch[(int)ceil(coor.first)][(int)floor(coor.second)] = 1;
		bound((int)ceil(coor.first), (int)floor(coor.second), i);

		q1.push({(int)floor(coor.first), (int)ceil(coor.second)});
		ch[(int)floor(coor.first)][(int)ceil(coor.second)] = 1;
		bound((int)floor(coor.first), (int)ceil(coor.second), i);

		q1.push({(int)floor(coor.first), (int)floor(coor.second)});
		ch[(int)floor(coor.first)][(int)floor(coor.second)] = 1;
		bound((int)floor(coor.first), (int)floor(coor.second), i);
	}

	for (int i = 0; i < edge.size(); i++) {
		if (edge[i].first == -1) {
			swap(edge[i].first, edge[i].second);
			swap(area[i].first, area[i].second);
		}
		pdd p1, p2, own1, own2, use;
		p1 = vertex[edge[i].first]; p2 = vertex[edge[i].second];
		use = vertex[edge[i].first];
		own1 = input[area[i].first]; own2 = input[area[i].second];
		double a = (own2.first - own1.first) / (own1.second - own2.second);
		double inva = 1 / a;

		if (edge[i].second == -1) {
			if (own1.second > a * (own1.first - p1.first) + p1.second) {
				if (a > 0) p2 = {p1.first + 2 * (double)m, p1.second + 2 * (double)m};
				else p2 = {p1.first + 2 * (double)m, p1.second - 2 * (double)m};
			}
			else {
				if (a > 0) p2 = {p1.first - 2 * (double)m, p1.second - 2 * (double)m};
				else p2 = {p1.first - 2 * (double)m, p1.second + 2 * (double)m};
			}
		}

		//cout << p1.first << " " << p1.second << " " << p2.first << " " << p2.second << " " << a << "\n";

		if (p1.first > p2.first) swap(p1, p2);
		for (int x = max(1, (int)ceil(p1.first)); x <= min(m, (int)floor(p2.first)); x++) {
			double y = a * ((double)x - use.first) + use.second;
			if (y < 0 || y > m + 1) continue;
			//cout << x << " " << y << " " << area[i].first << " " << area[i].second << "\n";
			bound(x, floor(y), area[i].first);
			bound(x, floor(y), area[i].second);
			q.push({x, (int)floor(y)});
			ch[x][(int)floor(y)] = 1;

			bound(x, ceil(y), area[i].first);
			bound(x, ceil(y), area[i].second);
			q.push({x, (int)ceil(y)});
			ch[x][(int)ceil(y)] = 1;
		}
		
		if (p1.second > p2.second) swap(p1, p2);
		for (int y = max(1, (int)ceil(p1.second)); y <= min(m, (int)floor(p2.second)); y++) {
			double x = inva * ((double)y - use.second) + use.first;
			if (x < 0 || x > m + 1) continue;
			//cout << x << " " << y << " " << area[i].first << " " << area[i].second << "\n";
			bound(floor(x), y, area[i].first);
			bound(floor(x), y, area[i].second);
			q.push({(int)floor(x), y});
			ch[(int)floor(x)][y] = 1;

			bound(ceil(x), y, area[i].first);
			bound(ceil(x), y, area[i].second);
			q.push({(int)ceil(x), y});
			ch[(int)ceil(x)][y] = 1;
		}
		//cout << "\n";
	}
/*
	for (int i = m; i >= 1; i--) {
		for (int j = 1; j <= m; j++) cout << grid[j][i] << " ";
		cout << "\n";
	}
	cout << "\n";
	for (int i = 1; i <= m; i++) {
		for (int j = 1; j <= m; j++) cout << ch[i][j] << " ";
		cout << "\n";
	}
	cout << "\n";
	for (int i = 1; i <= m; i++) {
		for (int j = 1; j <= m; j++) cout << grid[i][j] << " ";
		cout << "\n";
	}
	cout << "\n";
*/

	const int dx[4] = {-1, 0, 1, 0}, dy[4] = {0, -1, 0, 1};
	while (!q1.empty()) {
		pii now = q1.front();
		q1.pop();
		if (now.first < 1 || now.first > m || now.second < 1 || now.second > m) continue;
		for (int k = 0; k < 4; k++) {
			pii next = {now.first + dx[k], now.second + dy[k]};
			if (next.first < 1 || next.first > m || next.second < 1 || next.second > m) continue;
			if (ch[next.first][next.second] == 0) {
				grid[next.first][next.second] = grid[now.first][now.second];
				ch[next.first][next.second] = 1;
				q1.push(next);
			}
		}
	}

	while (!q.empty()) {
		pii now = q.front();
		q.pop();
		if (now.first < 1 || now.first > m || now.second < 1 || now.second > m) continue;
		for (int k = 0; k < 4; k++) {
			pii next = {now.first + dx[k], now.second + dy[k]};
			if (next.first < 1 || next.first > m || next.second < 1 || next.second > m) continue;
			if (ch[next.first][next.second] == 0) {
				grid[next.first][next.second] = grid[now.first][now.second];
				ch[next.first][next.second] = 1;
				q.push(next);
			}
		}
	}

	for (int i = 1; i <= m; i++) {
		for (int j = 1; j <= m; j++) {
			cout << grid[i][j] % 10000 << " ";
		}
		cout << "\n";
	}

	return 0;
}