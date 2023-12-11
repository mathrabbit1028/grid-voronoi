#include <bits/stdc++.h>
using namespace std;
const int dx[8] = {-1, -1, -1, 0, 0, 1, 1, 1};
const int dy[8] = {-1, 0, 1, -1, 1, -1, 0, 1};

int n, m;
double points[1010101][2];
int ans[5050][5050][2];

double get_dis(double x, double y, int i) {
    if (i == -1) return 1e9;
    return (x - points[i][0]) * (x - points[i][0]) + (y - points[i][1]) * (y - points[i][1]);
}

int update(int x, int y, int i) {
    if (ans[x][y][0] == i) return -1;
    if (get_dis(x, y, i) + 1e-9 < get_dis(x, y, ans[x][y][0])) {
        ans[x][y][1] = ans[x][y][0];
        ans[x][y][0] = i;
        return 0;
    }
    else if (get_dis(x, y, i) + 1e-9 < get_dis(x, y, ans[x][y][1])) {
        ans[x][y][1] = i;
        return 1;
    }
    return -1;
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
            ans[i][j][0] = -1;
            ans[i][j][1] = -1;
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
                int r = update(x, y, i);
                if (r == 0) 
                    pq.push({-get_dis(x, y, ans[x][y][0]), x + (m+1) * y});
                if (r == 1) 
                    pq.push({-get_dis(x, y, ans[x][y][1]), x + (m+1) * y});
            }
        }
    }

    while (!pq.empty()) {
        int i = pq.top().second % (m+1), j = pq.top().second / (m+1);
        double d = -pq.top().first; int t = -1;
        pq.pop();
        if (d > get_dis(i, j, ans[i][j][1]) + 1e-9) continue;
        if (d < get_dis(i, j, ans[i][j][0]) + 1e-9) t = 0;
        else t = 1;
        for (int k = 0; k < 8; k++) {
            int x = i + dx[k], y = j + dy[k];
            if (x < 0 || x > m || y < 0 || y > m) continue;
            int r = update(x, y, ans[i][j][t]);
            if (r == 0) pq.push({-get_dis(x, y, ans[x][y][0]), x + (m+1) * y});
            if (r == 1) pq.push({-get_dis(x, y, ans[x][y][1]), x + (m+1) * y});
        }
    }

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= m; j++) cout << (ans[i][j][0] - 1) % 10000 << " ";
        cout << "\n";
    }

    return 0;
}