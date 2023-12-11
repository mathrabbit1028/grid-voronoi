#include <bits/stdc++.h>
using namespace std;
typedef pair<double, double> pdd;
int n, m;
vector< pair<pdd, int> > points;
int cnt[5050][5050];
int ans[5050][5050];
vector<int> idx[5050][5050];
 
double dis(double x1, double y1, double x2, double y2) {
    return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2);
}

int get(int s, int e, int l, int r) {
    s = max(s, 0);
    e = min(e, m);
    l = max(l, 0);
    r = min(r, m);
    return cnt[e][r] - cnt[e][l] - cnt[s][r] + cnt[s][l];
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    cin >> n >> m;
    for (int i = 1; i <= n; i++) {
        double a, b;
        cin >> a >> b;
        points.push_back({{a, b}, i});
    }

    sort(points.begin(), points.end());

    for (int i = 0; i < n; i++) {
        cnt[(int)ceil(points[i].first.first)][(int)ceil(points[i].first.second)] += 1;
        idx[(int)ceil(points[i].first.first)][(int)ceil(points[i].first.second)].push_back(i);
    }

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= m; j++) {
            cnt[i][j] += cnt[i][j - 1];
        }
    }
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= m; j++) {
            cnt[i][j] += cnt[i - 1][j];
        }
    }

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= m; j++) {
            int st = 1, ed = m;
            while (st < ed) {
                int mid = (st + ed) / 2;
                if (get(i - mid, i + mid, j - mid, j + mid) == 0) st = mid + 1;
                else ed = mid; 
            }
            int d = st;
            d = (int)ceil((double)d * sqrt(2));
            vector<int> plist;
            for (int x = max(1, i - d); x <= min(m, i + d); x++) {
                for (int y = max(1, j - d); y <= min(m, j + d); y++) {
                    for (int t = 0; t < idx[x][y].size(); t++) plist.push_back(idx[x][y][t]);
                }
            }
            double val = 1e18;
            for (int t = 0; t < plist.size(); t++) {
                if (val > dis(i, j, points[plist[t]].first.first, points[plist[t]].first.second)) {
                    val = dis(i, j, points[plist[t]].first.first, points[plist[t]].first.second);
                    ans[i][j] = points[plist[t]].second;
                }
            }
        }
    }

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= m; j++) cout << (ans[i][j] - 1) % 10000 << " ";
        cout << "\n";
    }
    return 0;
}
