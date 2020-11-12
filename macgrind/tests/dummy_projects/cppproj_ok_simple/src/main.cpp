#include <iostream>
#include <vector>


using std::cout;
using std::endl;
using std::vector;


int main (void)
{
    cout << "Hello, World!" << endl;

    vector<int> v;

    v.push_back(10);

    int * my_int = new int(10);
    delete my_int;

    return 0;
}
