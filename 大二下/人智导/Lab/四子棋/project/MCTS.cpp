#include "MCTS.h"
#include "Node.h"
#include "Point.h"
#include "Judge.h"
#include <ctime>

using namespace std;

MCTS::MCTS(const int M, const int N, const int *top, int **board, const int lastX, const int lastY, const int noX, const int noY)
{
    this->M = M;
    this->N = N;
    this->mct_top = new int[N];
    for (int i = 0; i < N; i++)
    {
        this->mct_top[i] = top[i];
    }
    this->mct_board = new int *[M];
    for (int i = 0; i < M; i++)
    {
        this->mct_board[i] = new int[N];
        for (int j = 0; j < N; j++)
        {
            this->mct_board[i][j] = board[i][j];
        }
    }
    // cerr << "初始化根节点..." << endl;
    this->root = new Node(M, N, mct_top, noX, noY, false); // 根节点总是对方落子
    // cerr << "根节点初始化完成" << root->x << "," << root->y << endl;
    this->lastX = lastX;
    this->lastY = lastY;
    this->noX = noX;
    this->noY = noY;
    // cerr<< "MCTS初始化完成，根节点的落子位置：" << root->x << "," << root->y << endl;
}

MCTS::~MCTS()
{
    if (root)
    {
        delete root;
    }
    delete[] mct_top;
    for (int i = 0; i < M; i++)
    {
        delete[] mct_board[i];
    }
    delete[] mct_board;
}

// 使用UCT算法求最优落点
Point MCTS::getBestMove()
{
    clock_t start_time = clock();
    int y = 0;
    double bestWinRate = -1e9;
    long times=0;
    // cerr << "开始求解..." << endl;
    // 一次求解时长不能超过timeLimit秒
    while ((clock() - start_time) < timeLimit * CLOCKS_PER_SEC)
    {
        // cerr<<"进行一次搜索"<<endl;
        Node *now_node = select(root); // select要找到最适合且仍可以探索的结点
        // if (now_node != nullptr)
        // {
        //     // cerr << "选择完成，当前选择的结点的落子位置：" << now_node->x << "," << now_node->y << endl;
        // }
        // cerr<<now_node->visitCount<<endl;
        int result = simulate(now_node);
        // cerr << "模拟完成，结果为：" << result << endl;
        backup(now_node, result);
        // cerr << "回溯完成" << endl;
        times++;
    }
    for (int i = 0; i < N; i++)
    {
        if (root->children[i] != nullptr)
        {
            double winRate = (double)root->children[i]->winCount / root->children[i]->visitCount;
            // cerr << "列 " << i << " 的结点胜率为: " << winRate << endl;
            // cerr << "列 " << i << " 的结点访问次数为: " << root->children[i]->visitCount << endl;
            if (winRate > bestWinRate)
            {
                bestWinRate = winRate;
                y = i;
            }
        }
    }
    Node *bestNode = root->children[y];
    Point bestMove(bestNode->x, bestNode->y);
    // cerr << "落子点为: (" << bestMove.x << ", " << bestMove.y << ")" << endl;
    // cerr<<"当前结点胜率为："<<bestWinRate<<endl;
    // cerr<<"当前结点访问次数为：" << bestNode->visitCount << endl;
    // cerr<<"总搜索次数：" << times << endl;
    // cerr<<"根节点访问次数：" << root->visitCount << endl;
    return bestMove;
}

void printBoard(int **board, int M, int N)
{
    for (int i = 0; i < M; i++)
    {
        for (int j = 0; j < N; j++)
        {
            cerr << board[i][j] << " ";
        }
        cerr << endl;
    }
}

// select要找到最适合且仍可以探索的结点进行扩展，返回扩展的结点
Node *MCTS::select(Node *root)
{
    Node *now_node = root;
    // cerr << "还没进入循环" << endl;
    while (now_node->can_expand()==-1&&now_node->isend==false) // 如果没有未扩展的子节点
    {
        // cerr << "正在选择结点..." << endl;
        // 根据UCT公式选择最优子节点
        double bestValue = -1e9;
        int bestChildIdx = -1;
        for (int i = 0; i < N; ++i)
        {
            Node *child = now_node->children[i];
            if (child != nullptr)
            {
                double uctValue = child->getUctValue();
                if (uctValue > bestValue)
                {
                    bestValue = uctValue;
                    bestChildIdx = i;
                }
            }
        }

        if (bestChildIdx == -1)
        {
            cerr << "抛出异常1" << endl;
        }
        if (bestChildIdx != -1)
        {

            now_node = now_node->children[bestChildIdx];
        }
        // cerr<<"test"<<endl;
        mct_board[now_node->node_top[bestChildIdx]][bestChildIdx] = now_node->is_my_turn ? 2 : 1;
        // cerr<<"运行完了"<<endl;
    }
    // 扩展结点
    if(now_node->isend==true){ // 如果是叶节点，直接返回
        mct_board[now_node->x][now_node->y] = now_node->is_my_turn? 2 : 1;
        return now_node;
    }
    else{
        // cerr << "扩展结点..." << endl;
        Node *expandedNode = now_node->expand();
        // cerr << "扩展完成..." << endl;
        if(expandedNode== nullptr){
            cerr << "抛出异常2" << endl;
        }
        mct_board[expandedNode->x][expandedNode->y] = expandedNode->is_my_turn ? 2 : 1;

        // cerr<<"扩展结点的落子位置：" << expandedNode->x << "," << expandedNode->y << endl;
        return expandedNode;
    }

}

int MCTS::simulate(Node *node)
{
    // std::cerr << "开始模拟..." << std::endl;
    int x, y;
    x = node->x; // 获取当前结点的落子位置
    y = node->y;
    bool turn = node->is_my_turn;
    if(turn&& machineWin(x, y, M, N, mct_board)) {
        node->isend = true; // 机器赢了，不能再扩展
        return 1; // 我方是指机器赢
    }
    else if(!turn && userWin(x, y, M, N, mct_board)) {
        node->isend = true; // 用户赢了，不能再扩展
        return -1; // 对方赢
    }
    else if (isTie(N, node->node_top)) {
        node->isend = true; // 平局，不能再扩展
        return 0; // 平局
    }

    int **now_board = new int *[M];
    for (int i = 0; i < M; i++)
    {
        now_board[i] = new int[N];
        for (int j = 0; j < N; j++)
        {
            now_board[i][j] = mct_board[i][j];
        }
    }
    
    int *top = new int[N];
    for (int i = 0; i < N; i++)
    {
        top[i] = node->node_top[i];
    }

    // cerr << "模拟开始前，当前结点的棋盘状态：" << endl;
    // printBoard(now_board, M, N);
    while (1)
    {
        turn = !turn;
        // 随机落子

        int col = rand() % N;
        while (top[col] <= 0)
        {
            col = rand() % N;
        }
        x = top[col] - 1;
        y = col;

        // 按理说Node的实现已经处理了不可落子点了
        if (x == noX && y == noY) // 防止落到不可落子点
        {
            if (x == 0)
            {
                continue;
            }
            else
            {
                x--;
            }
        }
        // if (turn)
        // {
        //     cerr << "机器落子：" << x << "," << y << endl;
        // }
        // else
        // {
        //     cerr << "用户落子：" << x << "," << y << endl;
        // }
        now_board[x][y] = turn ? 2 : 1;
        // printBoard(now_board, M, N);
        // cerr<<endl;
        top[col] = x; // top顶端也就是现在落子的x
        if (turn && machineWin(x, y, M, N, now_board))
        {
            // 释放
            for (int i = 0; i < M; i++)
            {
                delete[] now_board[i];
            }
            delete[] now_board;
            delete[] top;
            // cerr << "机器赢了" << endl;
            return 1; // 我方是指机器赢
        }
        else if (!turn && userWin(x, y, M, N, now_board))
        {
            // 释放
            for (int i = 0; i < M; i++)
            {
                delete[] now_board[i];
            }
            delete[] now_board;
            delete[] top;
            // cerr << "用户赢了" << endl;
            return -1; // 对方赢
        }
        else if (isTie(N, top))
        {
            // 释放
            for (int i = 0; i < M; i++)
            {
                delete[] now_board[i];
            }
            delete[] now_board;
            delete[] top;
            // cerr << "平局" << endl;
            return 0; // 平局
        }
    }
}

// 回溯
void MCTS::backup(Node *node, int result)
{
    // 回溯，注意回溯时还需要借助Node类中存储的x,y，把棋盘状态也一并回溯
    while (node != root)
    {
        node->visitCount++;
        if (mct_board[node->x][node->y] != 0)
        {
            mct_board[node->x][node->y] = 0;
        }
        if (result == 1)
        {
            if (node->is_my_turn)
            {
                node->winCount += 1; // 如果是我方落子，赢了就加1
            }
            else
            {
                node->winCount -= 1; // 如果是对方落子，赢了就减1
            }
        }
        else if (result == -1)
        {
            if (node->is_my_turn)
            {
                node->winCount -= 1; // 如果是我方落子，赢了就加1
            }
            else
            {
                node->winCount += 1; // 如果是对方落子，赢了就减1
            }
        }
        node = node->parent;
    }
    node->visitCount++; // 根节点也要加1
}
