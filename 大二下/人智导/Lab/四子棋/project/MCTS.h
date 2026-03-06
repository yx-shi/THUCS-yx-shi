#pragma once
#include "Point.h"
#include "Node.h"
#include <iostream>
using namespace std;

class MCTS
{
public:
    Node *root;
    int M;
    int N;
    int *mct_top;    // 存储搜索过程中的top;
    int **mct_board; // 存储搜索过程中的board;
    int lastX;
    int lastY;
    int noX;
    int noY;
    double timeLimit = 2.2; // 时间限制
    MCTS(const int M, const int N, const int *top, int **board, const int lastX, const int lastY, const int noX, const int noY);
    ~MCTS();
    Point getBestMove();
    Node *select(Node *root); // 需要在里面实现扩展和选择，就是treepolicy
    int simulate(Node *node);
    void backup(Node *node, int result);
};