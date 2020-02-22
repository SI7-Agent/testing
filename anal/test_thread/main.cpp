#include <iostream>
#include <thread>
#include <vector>
#include <ctime>
#include <memory>

unsigned long long tick(void)
{
    unsigned long long d;
    __asm__ __volatile__ ("rdtsc" : "=A" (d));
    return d;
}

class Imatrix
{
public:
    virtual int get_rows() = 0;
    virtual int get_cols() = 0;
    virtual std::vector<std::vector<int>> get_mat() = 0;
};

class matrix:Imatrix
{
private:
    std::vector<std::vector<int>> mat;
    int rows;
    int cols;

public:
    matrix():
    rows(0), cols(0)
    {}

    matrix(int n):
    rows(n), cols(n)
    {
        std::vector<std::vector<int>> tmp;
        srand(time(0));
        for (int i = 0; i < n; ++i)
        {
            std::vector<int> row;
            for (int j = 0; j < n; ++j)
                if (j == i)
                {
                    row.push_back(1);
                }
                else
                {
                    row.push_back(0);
                }
            tmp.push_back(row);
        }
        mat = tmp;
    }

    matrix(int n, int m):
    rows(n), cols(m)
    {
        std::vector<std::vector<int>> tmp;
        srand(time(0));
        for (int i = 0; i < n; ++i)
        {
            std::vector<int> row;
            for (int j = 0; j < m; ++j)
                row.push_back(rand() % 10 + 1);
            tmp.push_back(row);
        }
        mat = tmp;
    }

    matrix(matrix *m1)
    {
        if (this != m1)
        {
            mat = m1->get_mat();
            rows = m1->get_rows();
            cols = m1->get_cols();
        }
    }

    void zero_matrix()
    {
        std::vector<std::vector<int>> tmp;

        for (int i = 0; i < this->get_rows(); ++i)
        {
            std::vector<int> row;
            for (int j = 0; j < this->get_cols(); ++j)
                row.push_back(0);
            tmp.push_back(row);
        }

        this->set_mat(tmp);
    }

    std::vector<std::vector<int>> get_mat() override
    {
        return mat;
    }

    int get_rows() override
    {
        return rows;
    }

    int get_cols() override
    {
        return cols;
    }

    void set_mat(std::vector<std::vector<int>> m1)
    {
        mat = m1;
    }

    void set_rows(int r)
    {
        rows = r;
    }

    void set_cols(int c)
    {
        cols = c;
    }
};

class Imultiplicator
{
    virtual matrix *based() = 0;
};

class multiplicator:Imultiplicator
{
private:
    matrix *m1;
    matrix *m2;
    unsigned long int time;

public:
    multiplicator(matrix *m1, matrix *m2):
        time(int(0))
    {
        this->m1 = m1;
        this->m2 = m2;
    }

    multiplicator():
        m1(nullptr), m2(nullptr), time(0)
    {

    }

    matrix *based() override
    {
        int m = m1->get_rows();
        int n = m1->get_cols();
        int q = m2->get_cols();

        auto *tmp = new matrix();
        tmp->set_rows(m);
        tmp->set_cols(q);

        tmp->zero_matrix();
        std::vector<std::vector<int>> res = tmp->get_mat();
        std::vector<std::vector<int>> mat1 = m1->get_mat();
        std::vector<std::vector<int>> mat2 = m2->get_mat();


        for (int i = 0; i < m; ++i)
        {
            for (int j = 0; j < q; ++j)
            {
                for (int k = 0; k < n; ++k)
                    res[i][j] = res[i][j] + mat1[i][k]*mat2[k][j];
            }
        }
        tmp->set_mat(res);
        return tmp;
    }

    matrix *wino_sequence()
    {
        int m = m1->get_rows();
        int n = m1->get_cols();
        int q = m2->get_cols();
        int _2n = n/2;

        auto *result = new matrix();
        result->set_rows(m);
        result->set_cols(q);

        result->zero_matrix();
        std::vector<std::vector<int>> res = result->get_mat();
        std::vector<std::vector<int>> mat1 = m1->get_mat();
        std::vector<std::vector<int>> mat2 = m2->get_mat();

        auto *row_factor = new int[m];
        auto *column_factor = new int[q];

        for (int i = 0; i < m; ++i)
            row_factor[i] = 0;

        for (int i = 0; i < m; ++i)
            for (int j = 0; j < _2n; ++j)
                row_factor[i] += mat1[i][2*j]*mat1[i][2*j+1];

        for (int i = 0; i < q; ++i)
            column_factor[i] = 0;

        for (int i = 0; i < q; ++i)
            for (int j = 0; j < _2n; ++j)
                column_factor[i] += mat2[2*j][i]*mat2[2*j+1][i];

        for (int i = 0; i < m; ++i)
        {
            for (int j = 0; j < q; ++j)
            {
                res[i][j] = -row_factor[i] - column_factor[j];
                for (int k = 0; k < _2n; ++k)
                {
                    res[i][j] += (mat1[i][2*k+1] + mat2[2*k][j]) *
                            (mat1[i][2*k] + mat2[2*k+1][j]);
                }
            }
        }

        if (n % 2)
        {
            for (int i = 0; i < m; ++i)
            {
                for (int j = 0; j < q; j++)
                {
                    res[i][j] += mat1[i][n-1] *
                            mat2[n-1][j];
                }
            }
        }

        result->set_mat(res);
        return result;
    }

    matrix *wino_paral(int num_thread = 1)
    {
        int m = m1->get_rows();
        int n = m1->get_cols();
        int q = m2->get_cols();
        int _2n = n/2;

        auto *result = new matrix();
        result->set_rows(m);
        result->set_cols(q);

        result->zero_matrix();
        std::vector<std::vector<int>> res = result->get_mat();
        std::vector<std::vector<int>> mat1 = m1->get_mat();
        std::vector<std::vector<int>> mat2 = m2->get_mat();

        std::unique_ptr<int> row_factor(new int[m]);
        std::unique_ptr<int> column_factor(new int[q]);

        auto rows_func_thread = [](std::vector<std::vector<int>> m1, int* row_factor, int _2n)
        {
            int r = m1.size();

            for (int i = 0; i < r; ++i)
                row_factor[i] = 0;

            for (int i = 0; i < r; ++i)
                for (int j = 0; j < _2n; ++j)
                    row_factor[i] += m1[i][2*j]*m1[i][2*j+1];
        };
        std::thread rows_thread(rows_func_thread, mat1, row_factor.get(), _2n);

        auto cols_func_thread = [](std::vector<std::vector<int>> m2, int* column_factor, int _2n)
        {
            int c = m2[0].size();

            for (int i = 0; i < c; ++i)
                column_factor[i] = 0;

            for (int i = 0; i < c; ++i)
                for (int j = 0; j < _2n; ++j)
                    column_factor[i] += m2[2*j][i]*m2[2*j+1][i];
        };
        std::thread cols_thread(cols_func_thread, mat2, column_factor.get(), _2n);

        rows_thread.join();
        cols_thread.join();

        auto thread_counter = num_thread;
        std::thread threads[thread_counter];

        auto winograd_thread = [](std::vector<std::vector<int>> mat1,
                std::vector<std::vector<int>> mat2, std::vector<std::vector<int>> &res,
                int* row_factor, int* column_factor, int number, int count)
        {
            int d = mat2.size()/2;
            for (unsigned int i = number; i < mat1.size(); i += count)
            {
                for (unsigned int j = 0; j < mat2[0].size(); ++j)
                {
                    res[i][j] = -row_factor[i] - column_factor[j];
                    for (int k = 0; k < d; ++k)
                    {
                        res[i][j] += (mat1[i][2*k+1] + mat2[2*k][j]) *
                                (mat1[i][2*k] + mat2[2*k+1][j]);
                    }
                }
            }
        };

        for (int i = 0; i < thread_counter; ++i)
            threads[i] = std::thread(winograd_thread, mat1, mat2, std::ref(res),
                    row_factor.get(), column_factor.get(), i, thread_counter);

        for (int i = 0; i < thread_counter; ++i)
            if (threads[i].joinable())
                threads[i].join();

        if (n % 2)
        {
            for (int i = 0; i < m; ++i)
            {
                for (int j = 0; j < q; j++)
                {
                    res[i][j] += mat1[i][n-1] *
                            mat2[n-1][j];
                }
            }
        }

        result->set_mat(res);
        return result;
    }

    void set_time(auto nsecs)
    {
        this->time = std::chrono::duration_cast<std::chrono::microseconds>(nsecs).count();
    }

    void set_time()
    {
        this->time = 0;
    }

    void add_time(auto nsecs)
    {
        this->time += std::chrono::duration_cast<std::chrono::microseconds>(nsecs).count();
    }

    void get_time()
    {
        std::cout << '\n' << this->time << '\n';
    }

    void set_matrixes(matrix *m11, matrix *m22)
    {
        if (this->m1 != m11)
            this->m1 = m11;

        if (this->m2 != m22)
            this->m2 = m22;
    }
};


std::ostream& operator<< (std::ostream &out, matrix *mat)
{
    std::vector<std::vector<int>> to_print = mat->get_mat();
    for (unsigned int i = 0; i < to_print.size(); ++i)
    {
        for (unsigned int j = 0; j < to_print[0].size(); ++j)
        {
            out << to_print[i][j] << "\t";
        }
        out << '\n';
    }
    out << '\n';

    return out;
}

class Itest
{
public:
    virtual void tester() = 0;
};

class test:Itest
{
private:
    int i = 100;
public:
    void tester() override
    {
        test_seq_par_1_thread();
        std::cout << "\n";
        test_par_n_thread();
    }

    void test_seq_par_1_thread()
    {
        auto *mult = new multiplicator();
        for (int i = 100; i < 1001; i += 100)
        {
            auto *m1 = new matrix(i, i);
            auto *m2 = new matrix(i, i);
            mult->set_matrixes(m1, m2);

            test_wino_par(mult);
            test_wino_seq(mult);
            this->i += 100;
        }

        this->i = 101;
        for (int i = 101; i < 1002; i += 100)
        {
            auto *m1 = new matrix(i, i);
            auto *m2 = new matrix(i, i);
            mult->set_matrixes(m1, m2);

            test_wino_par(mult);
            test_wino_seq(mult);
            this->i += 100;
        }
    }

    void test_par_n_thread()
    {
        for (int k = 1; k <= 16; k *= 2)
        {
            auto *mult = new multiplicator();
            for (int i = 100; i < 1001; i += 100)
            {
                auto *m1 = new matrix(i, i);
                auto *m2 = new matrix(i, i);
                mult->set_matrixes(m1, m2);

                test_wino_par(mult, k);
                this->i += 100;
            }

            this->i = 101;
            for (int i = 101; i < 1002; i += 100)
            {
                auto *m1 = new matrix(i, i);
                auto *m2 = new matrix(i, i);
                mult->set_matrixes(m1, m2);

                test_wino_par(mult, k);
                this->i += 100;
            }
        }
    }

    void test_wino_par(auto *mult, int num_thread = 1)
    {
        auto start = std::chrono::high_resolution_clock::now();
        mult->wino_paral(num_thread);
        auto end = std::chrono::high_resolution_clock::now();
        mult->set_time(end-start);
        std::cout << '\n' << num_thread << " num threads; " << this->i << " time of parallel winograd is ";
        mult->get_time();
    }

    void test_based(auto *mult)
    {
        auto start = std::chrono::high_resolution_clock::now();
        mult->based();
        auto end = std::chrono::high_resolution_clock::now();
        mult->set_time(end-start);
        std::cout << '\n' << this->i << " time of based is ";
        mult->get_time();
    }

    void test_wino_seq(auto *mult)
    {
        auto start = std::chrono::high_resolution_clock::now();
        mult->wino_sequence();
        auto end = std::chrono::high_resolution_clock::now();
        mult->set_time(end-start);
        std::cout << '\n' << this->i << " time of sequence winograd is ";
        mult->get_time();
    }
};

int main() {
    auto *test1 = new matrix(4);
    auto *test2 = new matrix(4);
    auto *mult = new multiplicator(test1, test2);
    auto *test3 = mult->wino_paral();
    std::cout << test1 << test2;
    std::cout << test3;
//    auto *test1 = new matrix(3,2);
//    auto *test2 = new matrix(2,3);
//    auto *mult = new multiplicator(test1, test2);

//    auto *test3 =  mult->wino_paral();
//    auto *test4 = mult->wino_sequence();

//    std::cout << test1;
//    std::cout << test2;
//    std::cout << test3 << test4;
//    auto *mytest = new test();
//    mytest->tester();
    return 0;
}
