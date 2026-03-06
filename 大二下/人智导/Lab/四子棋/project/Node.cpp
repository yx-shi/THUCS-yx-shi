#include "Node.h"
#include <iostream>
#include <math.h>
using namespace std;

Node::Node(int M, int N, int *top, int noX, int noY, bool is_my_turn, int x, int y)
{
    this->M = M;
    this->N = N;
    this->noX = noX;
    this->noY = noY;
    this->x = x;
    this->y = y;
    this->is_my_turn = is_my_turn;
    this->node_top = new int[N];
    for (int i = 0; i < N; i++)
    {
        this->node_top[i] = top[i];
    }
    this->visitCount = 0;
    this->winCount = 0;
    // cerr<<"初始化孩子..."<<endl;
    this->childrenCount = 0;
    this->children = vector<Node *>(N, nullptr); // 初始化子节点数组为nullptr

}

Node::~Node()
{
    delete[] node_top;
    for (int i = 0; i < N; i++)
    {
        if (children[i] != nullptr)
        {
            delete children[i];
        }
    }
    // delete[] children;
}

int Node::can_expand()
{
    // cerr << "can_expand" << endl;
    for (int i = 0; i < N; i++)
    {
        if (children[i] == nullptr)
        { // 如果有未扩展的子节点
            if (node_top[i] == 1 && noX == 0 && noY == i)
            {             
                continue; // 跳过不可落子点所在的列
            }
            if(node_top[i] == 0) // 如果该列已经满了
            {
                continue; // 跳过该列
            }
            return i; // 返回第一个未扩展的子节点的索引
        }
    }
    return -1; // 如果没有未扩展的子节点，返回-1
}

Node *Node::expand()
{
    int index = can_expand(); // 获取可以扩展的子节点索引
    if (index == -1)
    {
        return nullptr; // 如果没有可以扩展的子节点，返回nullptr
    }

    int temp = node_top[index];
    int child_x = node_top[index] - 1;
    int child_y = index;

    if (child_x < 0)
    { // 如果落子位置不合法
        return nullptr;
    }

    if (child_x == noX && child_y == noY)
    { // 防止落到不可落子点
        if (child_x == 0)
        {
            return nullptr; // 如果是第一行，不能落子
        }
        else
        {
            child_x--; // 否则就往下移一行
        }
    }

    node_top[index] = child_x; // 更新顶部位置
    Node *childNode = new Node(M, N, node_top, noX, noY, !is_my_turn, child_x, child_y);
    childNode->parent = this;    // 设置父节点
    children[index] = childNode; // 将新节点添加到子节点数组中
    childrenCount++;             // 子节点数量增加

    node_top[index] = temp; // 恢复顶部位置

    return childNode; // 返回新扩展的子节点
}

double Node::getUctValue()
{
    if (visitCount == 0)
    {
        return 1e9; // 如果没有访问过，返回一个很大的值
    }
    return (double)winCount / visitCount + 0.5 * sqrt(2 * log(parent->visitCount) / visitCount);
}
