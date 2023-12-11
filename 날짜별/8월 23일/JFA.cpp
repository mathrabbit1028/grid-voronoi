#include <bits/stdc++.h>
using namespace std;
int n, m;
double points[1010101][3];
int ans[330][330][330], temp[330][330][330];
 
double dis(double x1, double y1, double z1, double x2, double y2, double z2) {
    return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2) + (z1 - z2) * (z1 - z2);
}
 
void update(int i, int j, int k, int t) {
    if (temp[i][j][k] == 0) {
        temp[i][j][k] = t;
        return;
    }
    int s = temp[i][j][k];
    if (dis(i, j, k, points[s][0], points[s][1], points[s][2]) 
        > dis(i, j, k, points[t][0], points[t][1], points[t][2])) temp[i][j][k] = t;
    if (dis(i, j, k, points[s][0], points[s][1], points[s][2]) 
        == dis(i, j, k, points[t][0], points[t][1], points[t][2])) temp[i][j][k] = min(temp[i][j][k], t);
}
 
void spread(int x, int y, int z, int step) {
    if (ans[x][y][z] == 0) return;
    int delta[3] = {-step, 0, step};
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            for (int k = 0; k < 3; k++) {
                int xx = x + delta[i], yy = y + delta[j], zz = z + delta[k];
                if (xx < 0 || xx > m) continue;
                if (yy < 0 || yy > m) continue;
                if (zz < 0 || zz > m) continue;
                update(xx, yy, zz, ans[x][y][z]);
            }
        }
    }
}
 
void paste() {
    for (int i = 0; i <= m; i++) {
        for (int j = 0; j <= m; j++) {
            for (int k = 0; k <= m; k++) {
                ans[i][j][k] = temp[i][j][k];
            }
        }
    }
}
 
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    cin >> n >> m;
    for (int i = 1; i <= n; i++) {
        cin >> points[i][0] >> points[i][1] >> points[i][2];
    }
 
    for (int i = 1; i <= n; i++) {
        for (int j = 0; j < 8; j++) {
            int x = (j & 1) ? ceil(points[i][0]) : floor(points[i][0]);
            int y = (j & 2) ? ceil(points[i][1]) : floor(points[i][1]);
            int z = (j & 4) ? ceil(points[i][2]) : floor(points[i][2]);
            update(x, y, z, i);
        }
    }
    paste();
 
    int step = 1<<((int)log2(m));
    while (step > 0) {
        for (int i = 0; i <= m; i++) {
            for (int j = 0; j <= m; j++) {
                for (int k = 0; k <= m; k++) {
                    spread(i, j, k, step);
                }
            }
        }
        paste();
        step /= 2;
    }
 
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= m; j++) {
            for (int k = 1; k <= m; k++) cout << (ans[i][j][k] - 1) % 10000 << " ";
            cout << "\n";
        }
        cout << "\n";
    }
    return 0;
}
