#include <bits/stdc++.h>
using namespace std;
int n, m;
double points[1010101][3];
int ans[330][330][330];
 
double dis(double x1, double y1, double z1, double x2, double y2, double z2) {
    return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2) + (z1 - z2) * (z1 - z2);
}
 
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    cin >> n >> m;
    for (int i = 1; i <= n; i++) {
        cin >> points[i][0] >> points[i][1] >> points[i][2];
    }
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= m; j++) {
            for (int k = 1; k <= m; k++) {
                double val = 1e9;
                int idx;
                for (int t = 1; t <= n; t++) {
                    if (val > dis(i, j, k, points[t][0], points[t][1], points[t][2])) {
                        val = dis(i, j, k, points[t][0], points[t][1], points[t][2]);
                        idx = t;
                    }
                }
                ans[i][j][k] = idx;
            }
        }
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
