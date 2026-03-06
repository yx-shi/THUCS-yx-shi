#pragma once
#include <vector>
using namespace std;
class Node{
public:
    int M;
    int N;
    int noX,noY;//不可落子点
    int x,y;//记录该节点的落子位置，便于回溯
    int *node_top;//存储了当前结点的top数组，表示每一列的顶部位置
    int visitCount;
    int winCount;
    Node* parent;
    vector<Node*> children; // 存储子节点
    int childrenCount;
    bool is_my_turn;//1表示我方落子，0表示对方落子
    bool isend=false;
    /*
    其实一共有两种办法，一是在节点中存储整个棋盘的状态，这样的话就不需要记录是谁落子，因为根据父子节点的
    棋盘状态不同就可以判断是谁落子，但是这样的话每个结点都需要拷贝一次棋盘状态
    另一种办法就是通过记录落子顺序和top数组，也能推断出棋盘的状态。是谁落子其实并不重要，重要的是在UCT的simulate步骤中，我要能够得到
    模拟结点对应的棋盘状态
    */
    Node(int M, int N, int *top,int noX,int noY,bool is_my_turn=1,int x=0,int y=0);
    ~Node();
    int  can_expand();
    Node* expand();
    double getUctValue();
};