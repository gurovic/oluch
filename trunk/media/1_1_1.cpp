#include <iostream>

using namespace std;

int main()
{
    int n, i, mass_first[n], k, j, mass_second[k], klicks;
    cin >> n;
    n = j = 0;
    int i = 1;
    while(i < n)
    {
        cin >> mass_first[i];
        i++;
    }
    cin >> k;
    while(j < k)
    {
        cin >> mass_second[j];
        j++;
    }
    i = j = 0;
    
    
    int onemorek;
    onemorek = 1;
    while(i != n-1)
    {
    while(j != k-1)
    {
    while(onemorek != j-2)
    {
        if(mass_second[j] = mass_second[onemorek])
        {
            klicks++;
        }
        else
        {
            onemorek++;
        }
    }
    j++;
    }
    if(klicks > mass_first[i])
    {
        cout << "yes";
    }
    else
    {
        cout << "no";
    }
    i++;
    }
    
}






