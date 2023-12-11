#include <bits/stdc++.h>
using namespace std;
const int dx[4] = {-1, 0, 1, 0}, dy[4] = {0, -1, 0, 1};

int n, m;
double points[1010101][2];
int ans[5050][5050];
double dis[5050][5050];

double get_dis(double x1, double y1, double x2, double y2) {
    return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2);
}

bool update(int x, int y, int i) {
    if (get_dis(x, y, points[i][0], points[i][1]) + 1e-9 < dis[x][y]) {
        ans[x][y] = i;
        dis[x][y] = get_dis(x, y, points[i][0], points[i][1]);
        return true;
    }
    else if (abs(get_dis(x, y, points[i][0], points[i][1]) - dis[x][y]) < 1e-9) {
        if (ans[x][y] > i) {
            ans[x][y] = i;
            return true;
        }
    }
    return false;
}


int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);

    cin >> n >> m;
    for (int i = 1; i <= n; i++) {
        cin >> points[i][0] >> points[i][1];
    }

    for (int i = 0; i <= m; i++) {
        for (int j = 0; j <= m; j++) {
            ans[i][j] = -1;
            dis[i][j] = 1e9;
        }
    }

    priority_queue< pair<double, int> > pq;
    for (int i = 1; i <= n; i++) {
        int s[2] = {ceil(points[i][0]), floor(points[i][0])};
        int t[2] = {ceil(points[i][1]), floor(points[i][1])};
        for (int a = 0; a < 2; a++) {
            for (int b = 0; b < 2; b++) {
                int x = s[a], y = t[b];
                if (x < 0 || x > m || y < 0 || y > m) continue;
                if (update(x, y, i)) pq.push({-dis[x][y], x + (m+1) * y});
            }
        }
    }

    while (!pq.empty()) {
        int x = pq.top().second % (m+1), y = pq.top().second / (m+1);
        double d = -pq.top().first;
        pq.pop();
        if (d > dis[x][y] + 1e-9) continue;
        for (int k = 0; k < 4; k++) {
            int i = x + dx[k], j = y + dy[k];
            if (i < 0 || i > m || j < 0 || j > m) continue;
            if (update(i, j, ans[x][y])) {
                pq.push({-dis[i][j], i + (m+1) * j});
            }
        }
    }

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= m; j++) cout << (ans[i][j] - 1) % 10000 << " ";
        cout << "\n";
    }

    return 0;
}