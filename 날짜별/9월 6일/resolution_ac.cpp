#include <bits/stdc++.h>
using namespace std;
 
int n, m;
double points[1010101][2];
int ans[5050][5050];
 
double get_dis(double x1, double y1, double x2, double y2) {
    return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2);
}
 
int closest(int x, int y) {
    int ret = -1;
    double dis = 1e9;
    for (int i = 1; i <= n; i++) {
        if (dis > get_dis(x, y, points[i][0], points[i][1])) {
            dis = get_dis(x, y, points[i][0], points[i][1]);
            ret = i;
        }
    }
    return ret;
}
 
void solve(int s, int e, int l, int r) {
    if (s > e || l > r) return;
    if (s == e && l == r) {
        ans[s][l] = closest(s, l);
    }
    int clo[4];
    clo[0] = closest(s, l);
    clo[1] = closest(s, r);
    clo[2] = closest(e, l);
    clo[3] = closest(e, r);
    if (clo[0] == clo[1] && clo[1] == clo[2] && clo[2] == clo[3]) {
        for (int i = s; i <= e; i++) {
            for (int j = l; j <= r; j++) {
                ans[i][j] = clo[0];
            }
        }
        return;
    }
    int m1 = (s + e) / 2, m2 = (l + r) / 2;
    solve(s, m1, l, m2);
    solve(s, m1, m2+1, r);
    solve(m1+1, e, l, m2);
    solve(m1+1, e, m2+1, r);
}
 
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);
 
    cin >> n >> m;
    for (int i = 1; i <= n; i++) {
        cin >> points[i][0] >> points[i][1];
    }
 
    solve(1, m, 1, m);
 
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= m; j++) {
            cout << (ans[i][j] - 1) % 10000 << " ";
        }
        cout << "\n";
    }
 
    return 0;
}
